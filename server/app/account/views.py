from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from . import serializers
from .services import SignupService, LoginService, UserService, PasswordRecoveryService, ProfileService, UserIdentityService, EmailChangeService
from common.auth.throttling import SignupThrottling, SignupVerificationThrottling, ResentSignupOtpThrottling, LoginThrottling, PasswordRecoveryThrottling, PasswordRecoveryVerificationThrottling, PasswordRecoveryNewPasswordThrottling, ResentPasswordRecoveryOtpThrottling, LogoutThrottling, AuthenticatedUserThrottling, ChangeNamesThrottling
from common.utils.response import Response
from common.debug.log import Log
from common.platform.platform import Platform
from constants.tokens import TokenExpiry, CookieToken
from common.auth.permissions import IsWebIdentitySessionValid



# Signup
class Signup(APIView):
    throttle_classes = [SignupThrottling]

    def post(self, request):
        try:
            serializer = serializers.SignupSerializer(data=request.data)

            if serializer.is_valid():
                content = SignupService.signup(serializer.data)
                
                # sending response
                response = Response.success({ 'message': content['message']})
                response.set_cookie(
                    CookieToken.SIGNUP_OTP_TOKEN, 
                    content['sot'], 
                    expires=TokenExpiry.OTP_EXPIRE_SECONDS, 
                    httponly=True, 
                    samesite='None', 
                    secure=True
                )
                response.set_cookie(
                    CookieToken.SIGNUP_REQUEST_TOKEN, 
                    content['srt'], 
                    expires=TokenExpiry.SIGNUP_EXPIRE_SECONDS, 
                    httponly=True, 
                    samesite='None',
                    secure=True
                )
                return response

            # sending error response
            return Response.errors(serializer.errors)
        except Exception as e:
            Log.error(e)
            return Response.something_went_wrong()





# Signup Verification
class SignupVerification(APIView):
    throttle_classes = [SignupVerificationThrottling]

    def post(self, request):
        try:
            # validating token
            is_verified, id = SignupService.verify_signup_verification_tokens(request, platform=Platform.WEB)

            if is_verified:
                # retriving email from payload and cache data
                data = SignupService.retrieve_signup_cache_data(id)

                # passing all the data for validation
                serializer = serializers.VerificationSerializer(data=request.data, context={'hashed_otp': data['otp']})

                if serializer.is_valid():
                    # removing cache and deleting otp from data dict
                    SignupService.delete_signup_cache_data(id)
                    del data['otp']
                    
                    # creating user
                    user = SignupService.create_user(data)

                    # generating auth tokens
                    content = LoginService.generate_auth_token(user)

                    # sending response
                    response = Response.success({ 
                        'uid': content['uid'], 
                        'at': content['at']
                    })
                    response.set_cookie(
                        CookieToken.REFRESH_TOKEN, 
                        content['rt'], 
                        expires=TokenExpiry.REFRESH_EXPIRE_SECONDS, 
                        httponly=True,
                        samesite='None', 
                        secure=True
                    )
                    response.delete_cookie(CookieToken.SIGNUP_OTP_TOKEN)
                    response.delete_cookie(CookieToken.SIGNUP_REQUEST_TOKEN)
                    return response

                # sending error response
                return Response.errors(serializer.errors)
            
            response = Response.error('Session out! Try again.')
            response.delete_cookie(CookieToken.SIGNUP_OTP_TOKEN)
            response.delete_cookie(CookieToken.SIGNUP_REQUEST_TOKEN)
            return response
        
        except Exception as e:
            Log.error(e)
            response = Response.something_went_wrong()
            response.delete_cookie(CookieToken.SIGNUP_OTP_TOKEN)
            response.delete_cookie(CookieToken.SIGNUP_REQUEST_TOKEN)
            return response





# Signup Resent OTP
class ResentSignupOtp(APIView):
    throttle_classes = [ResentSignupOtpThrottling]

    def post(self, request):
        try:
            is_verified, id = SignupService.verify_resent_otp_tokens(request, platform=Platform.WEB)

            # validating token
            if is_verified:
                content = SignupService.resent_otp(id, request, platform=Platform.WEB)

                # sending response
                response = Response.success({ 'message': content['message']})
                response.set_cookie(
                    CookieToken.SIGNUP_OTP_TOKEN, 
                    content['sot'], 
                    httponly=True, 
                    expires=TokenExpiry.OTP_EXPIRE_SECONDS, 
                    samesite='None', 
                    secure=True
                )
                response.set_cookie(
                    CookieToken.SIGNUP_REQUEST_TOKEN, 
                    content['srt'], 
                    httponly=True, 
                    expires=TokenExpiry.SIGNUP_EXPIRE_SECONDS, 
                    samesite='None', 
                    secure=True
                )
                return response
            
            response = Response.error('Session out! Try again.')
            response.delete_cookie(CookieToken.SIGNUP_OTP_TOKEN)
            response.delete_cookie(CookieToken.SIGNUP_REQUEST_TOKEN)
            return response
        
        except:
            response = Response.something_went_wrong()
            response.delete_cookie(CookieToken.SIGNUP_OTP_TOKEN)
            response.delete_cookie(CookieToken.SIGNUP_REQUEST_TOKEN)
            return response





# Login
class Login(APIView):
    throttle_classes = [LoginThrottling]

    def post(self, request):
        try:
            serializer = serializers.LoginSerializer(data=request.data)

            if serializer.is_valid():
                # authenticating user with valid credentials
                user = LoginService.login(serializer.data)

                if user is not None:
                    # generating auth tokens
                    content = LoginService.generate_auth_token(user)

                    # sending response
                    response = Response.success({ 
                        'uid': content['uid'], 
                        'at': content['at']
                    })
                    response.set_cookie(
                        CookieToken.REFRESH_TOKEN, 
                        content['rt'], 
                        expires=TokenExpiry.REFRESH_EXPIRE_SECONDS, 
                        httponly=True,
                        samesite='None', 
                        secure=True
                    )
                    return response

                # sending invalid credentials error response
                return Response.error('Invalid Credentials.')

            # sending error reponse
            return Response.errors(serializer.errors)
        except Exception as e:
            Log.error(e)
            return Response.something_went_wrong()





# Logout User
class Logout(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [LogoutThrottling]

    def post(self, request):
        try:
            response = LoginService.logout(request.user)

            # sending response and logout current authenticated user
            return Response.success(response)
        except Exception as e:
            Log.error(e)
            return Response.something_went_wrong()





# Password Recovery
class PasswordRecovery(APIView):
    throttle_classes = [PasswordRecoveryThrottling]

    def post(self, request):
        try:
            serializer = serializers.PasswordRecoverySerializer(data=request.data)

            if serializer.is_valid():
                content = PasswordRecoveryService.recover_password(serializer.user, serializer.data)

                # sending response
                response = Response.success({ 'message': content['message']})
                response.set_cookie(
                    CookieToken.PASSWORD_RECOVERY_OTP_TOKEN, 
                    content['prot'], 
                    expires=TokenExpiry.OTP_EXPIRE_SECONDS, 
                    httponly=True, 
                    samesite='None',
                    secure=True
                )
                response.set_cookie(
                    CookieToken.PASSWORD_RECOVERY_REQUEST_TOKEN, 
                    content['prrt'], 
                    expires=TokenExpiry.PASSWORD_RECOVERY_EXPIRE_SECONDS, 
                    httponly=True, 
                    samesite='None',
                    secure=True
                )
                return response

            # sending error response
            return Response.errors(serializer.errors)
        except Exception as e:
            Log.error(e)
            return Response.something_went_wrong()





# Password Recovery Verification
class PasswordRecoveryVerification(APIView):
    throttle_classes = [PasswordRecoveryVerificationThrottling]

    def post(self, request):
        try:
            is_verified, uid = PasswordRecoveryService.verify_recovery_verification_tokens(request, platform=Platform.WEB)

            # validating token
            if is_verified:
                data = PasswordRecoveryService.retrieve_recovery_cache_data(uid)

                # passing all the data to serializer from validations
                serializer = serializers.VerificationSerializer(data=request.data, context={'hashed_otp': data.get('otp')})
                if serializer.is_valid():
                    # deleting cache and otp from data dict
                    PasswordRecoveryService.delete_recovery_cache_data(uid)
                    del data['otp']

                    content = PasswordRecoveryService.generate_new_pass_token(uid)

                    # sending response
                    response = Response.success({ 'message': content['message']})
                    response.delete_cookie(CookieToken.PASSWORD_RECOVERY_OTP_TOKEN)
                    response.delete_cookie(CookieToken.PASSWORD_RECOVERY_REQUEST_TOKEN)
                    response.set_cookie(
                        CookieToken.PASSWORD_RECOVERY_NEW_PASS_TOKEN, 
                        content['prnpt'], 
                        expires=TokenExpiry.PASSWORD_EXPIRE_SECONDS, 
                        httponly=True, 
                        samesite='None',
                        secure=True
                    )
                    return response

                # sending error response
                return Response.errors(serializer.errors)
            
            response = Response.error('Session out! Try again.')
            response.delete_cookie(CookieToken.PASSWORD_RECOVERY_OTP_TOKEN)
            response.delete_cookie(CookieToken.PASSWORD_RECOVERY_REQUEST_TOKEN)
            return response
        except:
            response = Response.something_went_wrong()
            response.delete_cookie(CookieToken.PASSWORD_RECOVERY_OTP_TOKEN)
            response.delete_cookie(CookieToken.PASSWORD_RECOVERY_REQUEST_TOKEN)
            return response





# Password Recovery New Password
class PasswordRecoveryNewPassword(APIView):
    throttle_classes = [PasswordRecoveryNewPasswordThrottling]

    def post(self, request):
        try:
            is_verified, uid = PasswordRecoveryService.verify_new_pass_tokens(request, platform=Platform.WEB)

            # validating token
            if is_verified:
                # fetching user
                user = UserService.get_user(uid)

                # passing all the data for validation
                serializer = serializers.PasswordRecoveryNewPassSerializer(data=request.data)

                if serializer.is_valid():   
                    # setting new password
                    UserService.change_password(user, serializer.validated_data.get('password'))

                    # sending response
                    response = Response.success({'message': 'Password changed successfully.'})
                    response.delete_cookie(CookieToken.PASSWORD_RECOVERY_NEW_PASS_TOKEN)
                    return response

                # sending error response
                return Response.errors(serializer.errors)
            
            response = Response.error('Session out! Try again.') 
            response.delete_cookie(CookieToken.PASSWORD_RECOVERY_NEW_PASS_TOKEN)
            return response
        except:
            response = Response.something_went_wrong()
            response.delete_cookie(CookieToken.PASSWORD_RECOVERY_NEW_PASS_TOKEN)
            return response





# Password Recovery Resent OTP
class ResentPasswordRecoveryOtp(APIView):
    throttle_classes = [ResentPasswordRecoveryOtpThrottling]

    def post(self, request):
        try:
            is_verified, uid = PasswordRecoveryService.verify_resent_otp_tokens(request, platform=Platform.WEB)

            # validating token
            if is_verified:
                content = PasswordRecoveryService.resent_otp(uid, request, platform=Platform.WEB)

                # sending response
                response = Response.success({ 'message': content['message']})
                response.set_cookie(
                    CookieToken.PASSWORD_RECOVERY_OTP_TOKEN, 
                    content['prot'], 
                    expires=TokenExpiry.OTP_EXPIRE_SECONDS, 
                    httponly=True, 
                    samesite='None',
                    secure=True
                )
                response.set_cookie(
                    CookieToken.PASSWORD_RECOVERY_REQUEST_TOKEN, 
                    content['prrt'], 
                    expires=TokenExpiry.PASSWORD_RECOVERY_EXPIRE_SECONDS, 
                    httponly=True, 
                    samesite='None',
                    secure=True
                )
                return response
            
            response = Response.error('Session out! Try again.')
            response.delete_cookie(CookieToken.PASSWORD_RECOVERY_OTP_TOKEN)
            response.delete_cookie(CookieToken.PASSWORD_RECOVERY_REQUEST_TOKEN)
            return response
        except:
            response = Response.something_went_wrong()
            response.delete_cookie(CookieToken.PASSWORD_RECOVERY_OTP_TOKEN)
            response.delete_cookie(CookieToken.PASSWORD_RECOVERY_REQUEST_TOKEN)
            return response




# User Identity
class UserIdentity(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AuthenticatedUserThrottling]

    def post(self, request):
        try:
            content = UserIdentityService.initiate(request.user)

            # sending response
            response = Response.success({'message': content['message']})
            response.set_cookie(
                CookieToken.IDENTITY_OTP_TOKEN, 
                content['idot'], 
                expires=TokenExpiry.OTP_EXPIRE_SECONDS, 
                httponly=True, 
                samesite='None',
                secure=True
            )
            return response
        except Exception as e:
            Log.error(e)
            return Response.something_went_wrong()





# User Identity Verification
class UserIdentityVerification(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AuthenticatedUserThrottling]

    def post(self, request):
        try:
            is_verified, uid = UserIdentityService.verify_identity_otp_token(request, platform=Platform.WEB)
            if is_verified:
                data = UserIdentityService.retrieve_identity_cache_data(uid)

                # passing all the data to serializer from validations
                serializer = serializers.VerificationSerializer(data=request.data, context={'hashed_otp': data.get('otp')})
                if serializer.is_valid():
                    UserIdentityService.delete_identity_cache_data(uid)

                    content = UserIdentityService.generate_identity_token(request.user)

                    # sending response
                    response = Response.success({'message': 'Identity Token'})
                    response.set_cookie(
                        CookieToken.IDENTITY_TOKEN, 
                        content['idt'], 
                        expires=TokenExpiry.IDENTITY_EXPIRE_SECONDS, 
                        httponly=True, 
                        samesite='None',
                        secure=True
                    )
                    response.delete_cookie(CookieToken.IDENTITY_OTP_TOKEN)
                    return response
            
                # sending error response
                response = Response.errors(serializer.errors)
                response.delete_cookie(CookieToken.IDENTITY_OTP_TOKEN)
                return response
            
            # sending error response
            response = Response.error('Session out! Try again.')
            response.delete_cookie(CookieToken.IDENTITY_OTP_TOKEN)
            return response
            
        except Exception as e:
            Log.error(e)
            return Response.something_went_wrong()





# Change Email
class ChangeEmail(APIView):
    permission_classes = [IsAuthenticated, IsWebIdentitySessionValid]
    throttle_classes = [AuthenticatedUserThrottling]

    def post(self, request):
        try:
            serializer = serializers.EmailChangeSerializer(data=request.data)
            if serializer.is_valid():
                content = EmailChangeService.generate_email_change_token(request.user, serializer.validated_data.get('email'))

                # sending response
                response = Response.success({ 'message': content['message']})
                response.set_cookie(
                    CookieToken.EMAIL_CHANGE_OTP_TOKEN,
                    content['ecot'],
                    expires=TokenExpiry.OTP_EXPIRE_SECONDS,
                    httponly=True,
                    samesite='None',
                    secure=True
                )
                return response
            
            # sending error response
            return Response.errors(serializer.errors)
        
        except Exception as e:
            Log.error(e)
            return Response.something_went_wrong()





# Change Email
class ChangeEmailVerification(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AuthenticatedUserThrottling]

    def post(self, request):
        try:
            is_verified, uid = EmailChangeService.verify_email_otp_token(request, platform=Platform.WEB)
            if is_verified:
                data = EmailChangeService.retrieve_email_change_cache_data(uid)

                # passing all the data to serializer from validations
                serializer = serializers.VerificationSerializer(data=request.data, context={'hashed_otp': data.get('otp')})
                if serializer.is_valid():
                    UserService.update_email(request.user, data.get('email'))

                    EmailChangeService.delete_email_change_cache_data(uid)

                    response = Response.success({'message': 'Email Changed Successfully'})
                    response.delete_cookie(CookieToken.EMAIL_CHANGE_OTP_TOKEN)
                    return response
                
                return Response.errors(serializer.errors)
            
            response = Response.error('Session Out! Try again.')
            response.delete_cookie(CookieToken.EMAIL_CHANGE_OTP_TOKEN)
            return response
                
        except Exception as e:
            Log.error(e)
            response = Response.something_went_wrong()
            response.delete_cookie(CookieToken.EMAIL_CHANGE_OTP_TOKEN)
            return response





# Change Password
class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AuthenticatedUserThrottling]

    def post(self, request):
        try:
            serializer = serializers.ChangePasswordSerializer(data=request.data, context={'user': request.user})

            # validating current password
            if serializer.is_valid():

                # saving new password
                UserService.change_password(request.user, serializer.validated_data.get('new_password'))

                return Response.success({
                    'message': 'Password changed successfully.'
                })

            return Response.errors(serializer.errors)
        except:
            return Response.something_went_wrong()





# Change User Names
class ChangeUserName(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [ChangeNamesThrottling]

    def post(self, request):
        try:
            serializer = serializers.ChangeUserNameSerializer(data=request.data, context={'user': request.user})

            if serializer.is_valid():
                UserService.change_name(
                    user=request.user,
                    first_name=request.data.get('first_name'),
                    last_name=request.data.get('last_name'),
                    username=request.data.get('username'),
                )

                return Response.success({
                    'message': 'Names changed',
                })

            return Response.errors(serializer.errors)
        except Exception as e:
            Log.error(e)
            return Response.something_went_wrong()






# User FCM Token
class UserFCMessagingToken(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AuthenticatedUserThrottling]

    def post(self, request):
        try:
            serializer = serializers.UserFCMessagingTokenSerializer(data=request.data)

            # validating fcm token
            if serializer.is_valid():

                # updating fcm token
                UserService.update_fcm_token(user=request.user, token=serializer.validated_data.get('msg_token'))

                return Response.success({
                    'message': 'FCM Token updated.'
                })

            return Response.errors(serializer.errors)
        except:
            return Response.something_went_wrong()





# Login check
class RefreshToken(APIView):
    throttle_classes = [AuthenticatedUserThrottling]

    def get(self, request):
        try:
            content = LoginService.refresh_auth_token(request.COOKIES.get(CookieToken.REFRESH_TOKEN))

            # sending response
            response = Response.success({ 
                'uid': content['uid'], 
                'at': content['at']
            })
            response.set_cookie(
                CookieToken.REFRESH_TOKEN, 
                content['rt'], 
                expires=TokenExpiry.REFRESH_EXPIRE_SECONDS, 
                httponly=True,
                samesite='None', 
                secure=True
            )
            return response
        except Exception as e:
            Log.error(e)
            return Response.something_went_wrong()





# Get User Profile
class UserProfile(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AuthenticatedUserThrottling]

    def get(self, request, uid):
        try:
            response = ProfileService.generate_user_profile(uid)

            # sending profile in response
            return Response.success(response)
        except:
            return Response.something_went_wrong()
        
    def put(self, request, uid):
        try:
            if request.user.uid == uid:
                serializer = serializers.ProfileUpdateSerializer(data=request.data)

                if serializer.is_valid():
                    # updating profile
                    response = ProfileService.update_profile(request.user, serializer.validated_data)

                    # sending response
                    return Response.success(response)

                # sending error response
                return Response.errors(serializer.errors)
            
            # sending error response
            return Response.permission_denied()
        except Exception as e:
            Log.error(e)
            return Response.something_went_wrong()





# Change Profile Photo
class ProfilePhotoUpdate(APIView):
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAuthenticated]
    throttle_classes = [AuthenticatedUserThrottling]

    def put(self, request, uid):
        try:
            if request.user.uid != uid:
                return Response.permission_denied()

            serializer = serializers.ProfilePhotoUpdateSerializer(data=request.data)

            if serializer.is_valid():
                # updating profile photo
                response = ProfileService.update_profile_photo(request.user, serializer.validated_data)

                # sending response
                return Response.success(response)

            # sending error response
            return Response.errors(serializer.errors)
        except Exception as e:
            Log.error(e)
            return Response.something_went_wrong()
