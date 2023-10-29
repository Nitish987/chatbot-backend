from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class SignupThrottling(AnonRateThrottle):
    scope = 'signup'

class SignupVerificationThrottling(AnonRateThrottle):
    scope = 'signup_verification'
    
class ResentSignupOtpThrottling(AnonRateThrottle):
    scope = 'resent_signup_otp'

class LoginThrottling(AnonRateThrottle):
    scope = 'login'

class PasswordRecoveryThrottling(AnonRateThrottle):
    scope = 'password_recovery'

class PasswordRecoveryVerificationThrottling(AnonRateThrottle):
    scope = 'password_recovery_verification'

class PasswordRecoveryNewPasswordThrottling(AnonRateThrottle):
    scope = 'password_recovery_new_password'

class ResentPasswordRecoveryOtpThrottling(AnonRateThrottle):
    scope = 'resent_password_recovery_otp'

class AuthenticatedUserThrottling(UserRateThrottle):
    scope = 'authenticated_user'

class ChangeNamesThrottling(UserRateThrottle):
    scope = 'change_names'

class LogoutThrottling(UserRateThrottle):
    scope = 'logout'