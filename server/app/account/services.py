from django.conf import settings
from django.core.cache import cache
from common.utils import otp, generator
from common.platform.platform import Platform
from common.utils.messenger import Mailer
from common.debug.log import Log
from common.exception.exceptions import UserNotFoundError, NoCacheDataError, NoSessionError
from common.auth.jwt_token import Jwt
from common.platform.security import AES256
from .models import User, LoginState
from django.contrib.auth import authenticate
from constants.tokens import TokenExpiry, TokenType, CookieToken, HeaderToken




class UserService:
    '''User Service for user model crud operations'''

    @staticmethod
    def create_user(data: dict) -> User:
        return User.objects.create_user_with_profile(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            gender=data.get('gender'),
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
        aes = AES256(settings.SERVER_ENC_KEY)
        enc_key = aes.decrypt(user.enc_key)
        return enc_key

    @staticmethod
    def check_username_availability(username: str) -> bool:
        return not User.objects.filter(username=username).exists()
    
    @staticmethod
    def change_name(user: User, first_name: str, last_name: str, username: str):
        if UserService.check_username_availability(username=username):
            user.username = username
        
        user.first_name = first_name.lower()
        user.last_name = last_name.lower()
        user.save()
    
    @staticmethod
    def update_email(user: User, email: str):
        if User.objects.filter(email=email).exists():
            raise Exception('Email already in use')
        user.email = email
        user.save()






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
        aes = AES256(settings.SERVER_ENC_KEY)
        data['password'] = aes.encrypt(password)
        data['otp'] = hashed_otp

        # putting data into cache for validation
        cache.set(f'{id}:signup', data, timeout=TokenExpiry.SIGNUP_EXPIRE_SECONDS)

        # generating signup otp token
        signup_otp_token = Jwt.generate(type=TokenType.SIGNUP_OTP, sub=id, seconds=TokenExpiry.OTP_EXPIRE_SECONDS)
        signup_request_token = Jwt.generate(type=TokenType.SIGNUP_REQUEST, sub=id, seconds=TokenExpiry.SIGNUP_EXPIRE_SECONDS)

        # sending otp mail to user
        Mailer.sendEmail(email, f'''Your Verification OTP is {actual_otp}. Please don't share this OTP to anyone else, valid for {TokenExpiry.OTP_EXPIRE_SECONDS} seconds.''')

        return { 
            'message': f'Enter the otp sent to email {email}',
            'sot': signup_otp_token,
            'srt': signup_request_token
        }
    
    @staticmethod
    def verify_signup_verification_tokens(request, platform: str):
        # retriving headers data
        if platform == Platform.MOBILE:
            _sot = request.META.get(HeaderToken.SIGNUP_OTP_TOKEN)
            _srt = request.META.get(HeaderToken.SIGNUP_REQUEST_TOKEN)
        else:
            _sot = request.COOKIES.get(CookieToken.SIGNUP_OTP_TOKEN)
            _srt = request.COOKIES.get(CookieToken.SIGNUP_REQUEST_TOKEN)
            
        success_o, payload_o = Jwt.validate(_sot)
        success_r, payload_r = Jwt.validate(_srt)
            
        # validating token
        is_verified = success_o and payload_o.get('type') == TokenType.SIGNUP_OTP and success_r and payload_r.get('type') == TokenType.SIGNUP_REQUEST and payload_o['sub'] == payload_r['sub']
        id = payload_o['sub'] if is_verified else None
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
        aes = AES256(settings.SERVER_ENC_KEY)
        data['password'] = aes.decrypt(data['password'])

        # creating user with user profile
        user = UserService.create_user(data)
        return user
    
    @staticmethod
    def verify_resent_otp_tokens(request, platform: str):
        # retriving headers data
        if platform == Platform.MOBILE:
            _srt = request.META.get(HeaderToken.SIGNUP_REQUEST_TOKEN)
        else:
            _srt = request.COOKIES.get(CookieToken.SIGNUP_REQUEST_TOKEN)

        success, payload = Jwt.validate(_srt)

        # validating token
        is_verified = success and payload.get('type') == TokenType.SIGNUP_REQUEST
        id = payload['sub'] if is_verified else None

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
        cache.set(f'{id}:signup', data, timeout=TokenExpiry.SIGNUP_EXPIRE_SECONDS)

        # creating new signup otp token
        signup_otp_token = Jwt.generate(type=TokenType.SIGNUP_OTP, sub=id, seconds=TokenExpiry.OTP_EXPIRE_SECONDS)
        if platform == Platform.MOBILE:
            signup_request_token = request.META.get(HeaderToken.SIGNUP_REQUEST_TOKEN)
        else:
            signup_request_token = request.COOKIES.get(CookieToken.SIGNUP_REQUEST_TOKEN)

        # sending otp email to user
        Mailer.sendEmail(email, f'''Your Verification OTP is {actual_otp}. Please don't share this OTP to anyone else, valid for {TokenExpiry.OTP_EXPIRE_SECONDS} seconds.''')

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
    def generate_auth_token(user: User) -> dict:
        # generating access token
        access_token = Jwt.generate(
            type=TokenType.LOGIN,
            sub=user.uid,
            category=Jwt.ACCESS, 
            seconds=TokenExpiry.ACCESS_EXPIRE_SECONDS
        )

        # generating refresh token if no session found for the user
        login_state = LoginState.objects.filter(user=user)
        if login_state.exists() and Jwt.validate(login_state[0].refresh_token, category=Jwt.REFRESH)[0]:
            refresh_token = login_state[0].refresh_token
        else:
            session_id = generator.generate_identity()
            refresh_token = Jwt.generate(
                type=TokenType.LOGIN,
                sub=session_id,
                category=Jwt.REFRESH,
                seconds=TokenExpiry.REFRESH_EXPIRE_SECONDS
            )
            LoginState.objects.create(user=user, session_id=session_id, refresh_token=refresh_token)

        # getting user encryption key
        enc_key = UserService.get_user_enc_key(user)

        return { 
            'uid': user.uid,
            'at': access_token,
            'rt': refresh_token,
            'enc_key': enc_key
        }
    
    @staticmethod
    def refresh_auth_token(refresh_token: str) -> dict:
        is_valid, payload = Jwt.validate(refresh_token, category=Jwt.REFRESH)
        if is_valid:
            user = LoginState.objects.get(session_id=payload['sub']).user

            # refreshing access token
            access_token = Jwt.generate(
                type=TokenType.LOGIN,
                sub=user.uid,
                category=Jwt.ACCESS, 
                seconds=TokenExpiry.ACCESS_EXPIRE_SECONDS
            )

            # getting user encryption key
            enc_key = UserService.get_user_enc_key(user)
            
            return { 
                'uid': user.uid,
                'at': access_token,
                'rt': refresh_token,
                'enc_key': enc_key
            }
        raise NoSessionError('Unauthenticated! No Session Found.')
        

    @staticmethod
    def logout(user) -> dict:
        # removing msg_token from user
        UserService.update_fcm_token(user=user)

        return { 'message': 'Account Logged out Successfully. See you soon.' }





class PasswordRecoveryService:
    '''Password Recovery Service used when user forgets account password'''
    @staticmethod
    def recover_password(user: User, data) -> dict:
        email = data.get('email')

        # generating otp and hashed otp
        actual_otp, hashed_otp = otp.generate()
        data['otp'] = hashed_otp

        # creating password recovery session
        cache.set(f'{user.uid}:pr', data, timeout=TokenExpiry.PASSWORD_RECOVERY_EXPIRE_SECONDS)

        # creating password recovery token
        password_recovery_otp_token = Jwt.generate(type=TokenType.PASSWORD_RECOVERY_OTP, sub=user.uid, seconds=TokenExpiry.OTP_EXPIRE_SECONDS)
        password_recovery_request_token = Jwt.generate(type=TokenType.PASSWORD_RECOVERY_REQUEST, sub=user.uid, seconds=TokenExpiry.PASSWORD_RECOVERY_EXPIRE_SECONDS)

        # sending otp email
        Mailer.sendEmail(email, f'''Your Verification OTP is {actual_otp}. Please don't share this OTP to anyone else, valid for {TokenExpiry.OTP_EXPIRE_SECONDS} seconds.''')

        return { 
            'message': f'Enter the otp sent to email {email}',
            'prot': password_recovery_otp_token,
            'prrt': password_recovery_request_token
        }
    
    @staticmethod
    def verify_recovery_verification_tokens(request, platform: str):
        # retriving headers data 
        if platform == Platform.MOBILE:
            _prot = request.META.get(HeaderToken.PASSWORD_RECOVERY_OTP_TOKEN)
            _prrt = request.META.get(HeaderToken.PASSWORD_RECOVERY_REQUEST_TOKEN)
        else:
            _prot = request.COOKIES.get(CookieToken.PASSWORD_RECOVERY_OTP_TOKEN)
            _prrt = request.COOKIES.get(CookieToken.PASSWORD_RECOVERY_REQUEST_TOKEN)
            
        success_o, payload_o = Jwt.validate(_prot)
        success_r, payload_r = Jwt.validate(_prrt)
            
        # validating token
        is_verified = success_o and payload_o.get('type') == TokenType.PASSWORD_RECOVERY_OTP and success_r and payload_r.get('type') == TokenType.PASSWORD_RECOVERY_REQUEST and payload_o['sub'] == payload_r['sub']
        uid = payload_o['sub'] if is_verified else None
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
        password_recovery_new_pass_token = Jwt.generate(type=TokenType.PASSWORD_RECOVERY_NEW_PASS, sub=uid, seconds=TokenExpiry.PASSWORD_EXPIRE_SECONDS)

        # sending response
        return {
            'message': 'Create your new password.',
            'prnpt': password_recovery_new_pass_token
        }
    
    @staticmethod
    def verify_new_pass_tokens(request, platform: str):
        # retriving headers data
        if platform == Platform.MOBILE:
            _prnpt = request.META.get(HeaderToken.PASSWORD_RECOVERY_NEW_PASS_TOKEN)
        else:
            _prnpt = request.COOKIES.get(CookieToken.PASSWORD_RECOVERY_NEW_PASS_TOKEN)
        success, payload = Jwt.validate(_prnpt)
            
        # validating token
        is_verified = success and payload.get('type') == TokenType.PASSWORD_RECOVERY_NEW_PASS
        uid = payload['sub'] if is_verified else None
        return is_verified, uid
    
    @staticmethod
    def verify_resent_otp_tokens(request, platform: str):
        # retriving headers data
        if platform == Platform.MOBILE:
            _prrt = request.META.get(HeaderToken.PASSWORD_RECOVERY_REQUEST_TOKEN)
        else:
            _prrt = request.COOKIES.get(CookieToken.PASSWORD_RECOVERY_REQUEST_TOKEN)
            
        success, payload = Jwt.validate(_prrt)

        # validating token
        is_verified = success and payload.get('type') == TokenType.PASSWORD_RECOVERY_REQUEST
        uid = payload['sub'] if is_verified else None

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
        cache.set(f'{uid}:pr', data, timeout=TokenExpiry.PASSWORD_RECOVERY_EXPIRE_SECONDS)

        # generating new password recovery token
        password_recovery_otp_token = Jwt.generate(type=TokenType.PASSWORD_RECOVERY_OTP, sub=uid, seconds=TokenExpiry.OTP_EXPIRE_SECONDS)
        if platform == Platform.MOBILE:
            password_recovery_request_token = request.META.get(HeaderToken.PASSWORD_RECOVERY_REQUEST_TOKEN)
        else:
            password_recovery_request_token = request.COOKIES.get(CookieToken.PASSWORD_RECOVERY_REQUEST_TOKEN)

        # sending otp email to user
        Mailer.sendEmail(email, f'''Your Verification OTP is {actual_otp}. Please don't share this OTP to anyone else, valid for {TokenExpiry.OTP_EXPIRE_SECONDS} seconds.''')

        # sending response
        return { 
            'message': f'Enter the otp sent to email {email}',
            'prot': password_recovery_otp_token,
            'prrt': password_recovery_request_token
        }




class UserIdentityService:
    '''User Identity Service for verifing user identity'''

    @staticmethod
    def initiate(user: User):
        actual_otp, hashed_otp = otp.generate()
        cache.set(f'{user.uid}:identity', {'otp': hashed_otp})

        identity_otp_token = Jwt.generate(type=TokenType.IDENTITY_OTP, sub=user.uid, seconds=TokenExpiry.OTP_EXPIRE_SECONDS)
        
        Mailer.sendEmail(user.email, f'''Your verification OTP is {actual_otp}. Please don't share this OTP to anyone else, valid for {TokenExpiry.OTP_EXPIRE_SECONDS} seconds.''')

        return {
            'message': f'Enter the otp sent to email {user.email}',
            'idot': identity_otp_token,
        }

    @staticmethod
    def verify_identity_otp_token(request, platform: str):
        if platform == Platform.MOBILE:
            _idot = request.META.get(HeaderToken.IDENTITY_OTP_TOKEN)
        else:
            _idot = request.COOKIES.get(CookieToken.IDENTITY_OTP_TOKEN)
        success, payload = Jwt.validate(_idot)

        is_verified = success and payload.get('type') == TokenType.IDENTITY_OTP and payload['sub'] == request.user.uid
        uid = payload['sub'] if is_verified else None

        return is_verified, uid

    @staticmethod
    def retrieve_identity_cache_data(uid):
        data = cache.get(f'{uid}:identity')
        if not data:
            raise NoCacheDataError()
        return data
    
    @staticmethod
    def delete_identity_cache_data(uid):
        cache.delete(f'{uid}:identity')
    
    @staticmethod
    def generate_identity_token(user: User):
        identity_token = Jwt.generate(type=TokenType.IDENTITY, sub=user.uid, seconds=TokenExpiry.IDENTITY_EXPIRE_SECONDS)
        return {
            'idt': identity_token
        }



class EmailChangeService:
    '''Email Change Service for user'''

    @staticmethod
    def generate_email_change_token(user: User, email: str):
        actual_otp, hashed_otp = otp.generate()
        cache.set(f'{user.uid}:emailchange', {'email': email, 'otp': hashed_otp})

        email_change_token = Jwt.generate(type=TokenType.EMAIL_CHANGE_OTP, sub=user.uid, seconds=TokenExpiry.OTP_EXPIRE_SECONDS)
        
        Mailer.sendEmail(email, f'''Your verification OTP is {actual_otp}. Please don't share this OTP to anyone else, valid for {TokenExpiry.OTP_EXPIRE_SECONDS} seconds.''')

        return {
            'message': f'Enter the otp sent to email {email}',
            'ecot': email_change_token
        }
    
    @staticmethod
    def verify_email_otp_token(request, platform: str):
        if platform == Platform.MOBILE:
            _ecot = request.META.get(HeaderToken.EMAIL_CHANGE_OTP_TOKEN)
        else:
            _ecot = request.COOKIES.get(CookieToken.EMAIL_CHANGE_OTP_TOKEN)
        success, payload = Jwt.validate(_ecot)

        is_verified = success and payload.get('type') == TokenType.EMAIL_CHANGE_OTP and payload['sub'] == request.user.uid
        uid = payload['sub'] if is_verified else None

        return is_verified, uid

    @staticmethod
    def retrieve_email_change_cache_data(uid):
        data = cache.get(f'{uid}:emailchange')
        if not data:
            raise NoCacheDataError()
        return data
    
    @staticmethod
    def delete_email_change_cache_data(uid):
        cache.delete(f'{uid}:emailchange')




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