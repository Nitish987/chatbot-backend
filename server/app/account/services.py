import user_agents
from django.conf import settings
from django.core.cache import cache
from utils import otp, generator, security
from utils.platform import Platform
from utils.messenger import Mailer
from .jwt_token import Jwt
from .models import User, LoginState
from .exceptions import UserNotFoundError, NoCacheDataError
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta




class UserService:
    '''User Service for user model crud operations'''

    @staticmethod
    def create_user(data: dict) -> User:
        return User.objects.create_user_with_profile(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            gender=data.get('gender'),
            date_of_birth=data.get('date_of_birth'),
            msg_token=data.get('msg_token'),
            email=data.get('email'),
            password=data.get('password'),
        )
    
    @staticmethod
    def get_user(uid: str) -> User:
        if User.objects.filter(uid=uid).exists():
            return User.objects.get(uid=uid)
        raise UserNotFoundError()
    
    @staticmethod
    def get_user_by_username(username: str) -> User:
        if User.objects.filter(username=username).exists():
            return User.objects.get(username=username)
        raise UserNotFoundError()
    
    
    @staticmethod
    def delete_user(uid: str):
        if User.objects.filter(uid=uid).exists():
            User.objects.get(uid=uid).delete()
        raise UserNotFoundError()


    @staticmethod
    def update_fcm_token(user: User, token=''):
        user.msg_token = token
        user.save()
    
    @staticmethod
    def change_password(user: User, password: str):
        user.set_password(password)
        user.save()
    
    @staticmethod
    def get_user_enc_key(user: User) -> str:
        aes = security.AES256(settings.SERVER_ENC_KEY)
        enc_key = aes.decrypt(user.enc_key)
        return enc_key

    @staticmethod
    def check_username_availability(username: str) -> bool:
        return not User.objects.filter(username=username).exists()
    
    @staticmethod
    def change_names(user: User, first_name: str, last_name: str, username: str):
        if UserService.check_username_availability(username=username):
            user.username = username
        
        user.first_name = first_name.lower()
        user.last_name = last_name.lower()
        user.save()





class LoginStateTokenService:
    '''Web Login State Token Service for creating, fetching and deleting login token and it's state'''
    @staticmethod
    def create(user: User, user_agent_header, timeout) -> LoginState:
        user_agent = user_agents.parse(user_agent_header)
        login_token = generator.generate_token()

        login_states = LoginState.objects.filter(user=user).order_by('-created_on')
        if len(login_states) == 5:
            login_states[0].delete()
        
        created_on = timezone.now()
        active_until = created_on + timedelta(seconds=timeout)
            
        login_state = LoginState.objects.create(
            user=user,
            token=login_token,
            device=user_agent.device.family,
            os=user_agent.os.family,
            browser=user_agent.browser.family,
            created_on=created_on,
            active_until=active_until,
        )

        return login_state
    
    @staticmethod
    def get(user: User, token: str) -> LoginState:
        return LoginState.objects.get(user=user, token=token)

    @staticmethod
    def delete(user: User, token: str):
        LoginStateTokenService.get(user=user, token=token).delete()





class SignupService:
    '''Signup Service for signing up user'''
    @staticmethod
    def signup(data: dict) -> dict:
        # retrieving data
        email = data.get('email')
        password = data.get('password')

        # generating otp, hashed otp and id
        actual_otp, hashed_otp = otp.generate()
        id = generator.generate_identity()

        # adding encrypted password an hasted otp to data dict
        aes = security.AES256(settings.SERVER_ENC_KEY)
        data['password'] = aes.encrypt(password)
        data['otp'] = hashed_otp

        # putting data into cache for validation
        cache.set(f'{id}:signup', data, timeout=settings.SIGNUP_EXPIRE_SECONDS)

        # generating signup otp token
        signup_otp_token = Jwt.generate(type='SO', data={'id': id}, seconds=settings.OTP_EXPIRE_SECONDS)
        signup_request_token = Jwt.generate(type='SR', data={'id': id}, seconds=settings.SIGNUP_EXPIRE_SECONDS)

        # sending otp mail to user
        Mailer.sendEmail(email, f'''Your Verification OTP is {actual_otp}. Please don't share this OTP to anyone else, valid for {settings.OTP_EXPIRE_SECONDS} seconds.''')

        return { 
            'message': f'Enter the otp sent to email {email}',
            'sot': signup_otp_token,
            'srt': signup_request_token
        }
    
    @staticmethod
    def verify_signup_verification_tokens(request, platform: str):
        # retriving headers data
        if platform == Platform.MOBILE:
            _sot = request.META.get('HTTP_SOT')
            _srt = request.META.get('HTTP_SRT')
            success_o, payload_o = Jwt.validate(_sot)
            success_r, payload_r = Jwt.validate(_srt)
        else:
            _sot = request.COOKIES.get('sot')
            _srt = request.COOKIES.get('srt')
            success_o, payload_o = Jwt.validate(_sot)
            success_r, payload_r = Jwt.validate(_srt)
            
        # validating token
        is_verified = success_o and payload_o.get('type') == 'SO' and success_r and payload_r.get('type') == 'SR' and payload_o['data']['id'] == payload_r['data']['id']
        id = payload_o['data']['id'] if is_verified else None
        return is_verified, id
    
    @staticmethod
    def retrieve_signup_cache_data(id):
        data = cache.get(f'{id}:signup')
        if not data:
            raise NoCacheDataError()
        return data
    
    @staticmethod
    def delete_signup_cache_data(id):
        cache.delete(f'{id}:signup')

    @staticmethod
    def create_user(data: dict) -> User:
        # retriving hashed otp and decrypting password and changing the data dict password key value
        aes = security.AES256(settings.SERVER_ENC_KEY)
        data['password'] = aes.decrypt(data['password'])

        # creating user with user profile
        user = UserService.create_user(data)
        return user
    
    @staticmethod
    def verify_resent_otp_tokens(request, platform: str):
        # retriving headers data
        if platform == Platform.MOBILE:
            _srt = request.META.get('HTTP_SRT')
        else:
            _srt = request.COOKIES.get('srt')
        success, payload = Jwt.validate(_srt)

        # validating token
        is_verified = success and payload.get('type') == 'SR'
        id = payload['data']['id'] if is_verified else None

        return is_verified, id
    
    @staticmethod
    def resent_otp(id, request, platform: str) -> dict:
        # retriving data
        data = SignupService.retrieve_signup_cache_data(id)
        email = data.get('email')

        # generating new otp and changing otp value in data
        actual_otp, hashed_otp = otp.generate()
        data['otp'] = hashed_otp

        # putting data into cache for validation
        cache.set(f'{id}:signup', data, timeout=settings.SIGNUP_EXPIRE_SECONDS)

        # creating new signup otp token
        signup_otp_token = Jwt.generate(type='SO', data={'id': id}, seconds=settings.OTP_EXPIRE_SECONDS)
        if platform == Platform.MOBILE:
            signup_request_token = request.META.get('HTTP_SRT')
        else:
            signup_request_token = request.COOKIES.get('srt')

        # sending otp email to user
        Mailer.sendEmail(email, f'''Your Verification OTP is {actual_otp}. Please don't share this OTP to anyone else, valid for {settings.OTP_EXPIRE_SECONDS} seconds.''')

        # sending response
        return { 
            'message': f'Enter the otp sent to email {email}',
            'sot': signup_otp_token,
            'srt': signup_request_token
        }




class LoginService:
    '''Login Service for login user'''

    @staticmethod
    def __login_authentication(data):
        return authenticate(email=data.get('email'), password=data.get('password'))
        

    @staticmethod
    def login(data):
        user = LoginService.__login_authentication(data)
        if user is not None:
            # updating messaging token
            UserService.update_fcm_token(user, data.get('msg_token'))
        
        return user
    
    @staticmethod
    def generate_auth_token(user: User, request) -> dict:
        # creating login state
        login_state = LoginStateTokenService.create(
            user=user,
            user_agent_header=request.META['HTTP_USER_AGENT'],
            timeout=settings.AUTH_EXPIRE_SECONDS
        )
        login_token = login_state.token

        # creating logged in authenticatin token
        auth_token = Jwt.generate(type='LI', data={'uid': user.uid}, seconds=settings.AUTH_EXPIRE_SECONDS)

        # getting user encryption key
        enc_key = UserService.get_user_enc_key(user)

        return { 
            'uid': user.uid,
            'at': auth_token,
            'lst': login_token,
            'enc_key': enc_key,
        }

    @staticmethod
    def logout(user, platform_lst_token=None) -> dict:
        # deleting login state
        LoginStateTokenService.delete(user=user, token=platform_lst_token)
            
        # removing msg_token from user
        UserService.update_fcm_token(user=user)

        return { 'message': 'Account Logged out Successfully. See you soon.' }





class PasswordRecoveryService:
    '''Password Recovery Service used when user forgets account password'''
    @staticmethod
    def recover_password(user, data) -> dict:
        email = data.get('email')

        # generating otp and hashed otp
        actual_otp, hashed_otp = otp.generate()
        data['otp'] = hashed_otp

        # creating password recovery session
        cache.set(f'{user.uid}:pr', data, timeout=settings.PASSWORD_RECOVERY_EXPIRE_SECONDS)

        # creating password recovery token
        password_recovery_otp_token = Jwt.generate(type='PRO', data={'uid': user.uid}, seconds=settings.OTP_EXPIRE_SECONDS)
        password_recovery_request_token = Jwt.generate(type='PRR', data={'uid': user.uid}, seconds=settings.PASSWORD_RECOVERY_EXPIRE_SECONDS)

        # sending otp email
        Mailer.sendEmail(email, f'''Your Verification OTP is {actual_otp}. Please don't share this OTP to anyone else, valid for {settings.OTP_EXPIRE_SECONDS} seconds.''')

        return { 
            'message': f'Enter the otp sent to email {email}',
            'prot': password_recovery_otp_token,
            'prrt': password_recovery_request_token
        }
    
    @staticmethod
    def verify_recovery_verification_tokens(request, platform: str):
        # retriving headers data 
        if platform == Platform.MOBILE:
            _prot = request.META.get('HTTP_PROT')
            _prrt = request.META.get('HTTP_PRRT')
        else:
            _prot = request.COOKIES.get('prot')
            _prrt = request.COOKIES.get('prrt')
        success_o, payload_o = Jwt.validate(_prot)
        success_r, payload_r = Jwt.validate(_prrt)
            
        # validating token
        is_verified = success_o and payload_o.get('type') == 'PRO' and success_r and payload_r.get('type') == 'PRR' and payload_o['data']['uid'] == payload_r['data']['uid']
        uid = payload_o['data']['uid'] if is_verified else None
        return is_verified, uid
    
    @staticmethod
    def retrieve_recovery_cache_data(uid):
        data = cache.get(f'{uid}:pr')
        if not data:
            raise NoCacheDataError()
        return data
    
    @staticmethod
    def delete_recovery_cache_data(uid):
        cache.delete(f'{uid}:pr')

    @staticmethod
    def generate_new_pass_token(uid) -> dict:
        # creating password recovery verification token
        password_recovery_new_pass_token = Jwt.generate(type='PRNP', data={'uid': uid}, seconds=settings.PASSWORD_EXPIRE_SECONDS)

        # sending response
        return {
            'message': 'Create your new password.',
            'prnpt': password_recovery_new_pass_token
        }
    
    @staticmethod
    def verify_new_pass_tokens(request, platform: str):
        # retriving headers data
        if platform == Platform.MOBILE:
            _prnpt = request.META.get('HTTP_PRNPT')
        else:
            _prnpt = request.COOKIES.get('prnpt')
        success, payload = Jwt.validate(_prnpt)
            
        # validating token
        is_verified = success and payload.get('type') == 'PRNP'
        uid = payload['data']['uid'] if is_verified else None
        return is_verified, uid
    
    @staticmethod
    def verify_resent_otp_tokens(request, platform: str):
        # retriving headers data
        if platform == Platform.MOBILE:
            _prrt = request.META.get('HTTP_PRRT')
        else:
            _prrt = request.COOKIES.get('prrt')
        success, payload = Jwt.validate(_prrt)

        # validating token
        is_verified = success and payload.get('type') == 'PRR'
        uid = payload['data']['uid'] if is_verified else None

        return is_verified, uid
    
    @staticmethod
    def resent_otp(uid, request, platform: str) -> dict:
        # retriving email from payload and cache data
        data = PasswordRecoveryService.retrieve_recovery_cache_data(uid)

        # retriving data
        email = data.get('email')

        # generating otp and hashed otp
        actual_otp, hashed_otp = otp.generate()
        data['otp'] = hashed_otp

        # assiging new data to password recovery session
        cache.set(f'{uid}:pr', data, timeout=settings.PASSWORD_RECOVERY_EXPIRE_SECONDS)

        # generating new password recovery token
        password_recovery_otp_token = Jwt.generate(type='PRO', data={'uid': uid}, seconds=settings.OTP_EXPIRE_SECONDS)
        if platform == Platform.MOBILE:
            password_recovery_request_token = request.META.get('HTTP_PRRT')
        else:
            password_recovery_request_token = request.COOKIES.get('prrt')

        # sending otp email to user
        Mailer.sendEmail(email, f'''Your Verification OTP is {actual_otp}. Please don't share this OTP to anyone else, valid for {settings.OTP_EXPIRE_SECONDS} seconds.''')

        # sending response
        return { 
            'message': f'Enter the otp sent to email {email}',
            'prot': password_recovery_otp_token,
            'prrt': password_recovery_request_token
        }




class ProfileService:
    '''User Profile Service for crud operation to user profile section.'''
    
    @staticmethod
    def generate_user_profile(uid) -> dict:
        '''user - logged in user, uid - user uid who's profile is to be generated.'''

        user = UserService.get_user(uid)

        # profile json response
        response = {
            'type': user.acc_type,
            'profile': {
                'uid': user.uid,
                'name': user.full_name,
                'username': user.username,
                'photo': user.photo.url,
                'gender': user.gender
            },
        }

        return response

    @staticmethod
    def update_profile(user: User, data) -> dict:
        user.message = data.get('message')
        user.location = data.get('location').lower()
        user.interest = data.get('interest')
        user.bio = data.get('bio')
        user.website = data.get('website')

        # saving profile
        user.save()

        return {
            'type': user.acc_type,
            'profile': {
                'uid': user.uid,
                'name': user.full_name,
                'username': user.username,
                'photo': user.photo.url,
                'gender': user.gender
            },
        }
    
    @staticmethod
    def update_profile_photo(user: User, data) -> dict:
        user.photo = data.get('photo')
        user.save()
        return { 'photo': user.photo.url }