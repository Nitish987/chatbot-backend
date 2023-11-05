from django.urls import path
from . import views

urlpatterns = [
    path('v1/signup/', views.Signup.as_view(), name='signup'),
    path('v1/signup-verify/', views.SignupVerification.as_view(), name='signup-verification'),
    path('v1/signup-resent-otp/', views.ResentSignupOtp.as_view(), name='signup-resent-otp'),
    path('v1/login/', views.Login.as_view(), name='login'),
    path('v1/logout/', views.Logout.as_view(), name='logout'),
    path('v1/recovery-password/', views.PasswordRecovery.as_view(), name='account-recovery'),
    path('v1/recovery-password-verify/', views.PasswordRecoveryVerification.as_view(), name='account-recovery-verification'),
    path('v1/recovery-password-new/', views.PasswordRecoveryNewPassword.as_view(), name='account-recovery-new-password'),
    path('v1/recovery-password-resent-otp/', views.ResentPasswordRecoveryOtp.as_view(), name='password-recovery-resent-otp'),
    path('v1/user-identity/', views.UserIdentity.as_view(), name='user-identity'),
    path('v1/user-identity-verify/', views.UserIdentityVerification.as_view(), name='user-identity-verify'),
    path('v1/account-email-change/', views.ChangeEmail.as_view(), name='email-change'),
    path('v1/account-email-change-verify/', views.ChangeEmailVerification.as_view(), name='email-change-verify'),
    path('v1/account-password-change/', views.ChangePassword.as_view(), name='password-change'),
    path('v1/account-name-change/', views.ChangeUserName.as_view(), name='name-change'),
    path('v1/fcm-token/', views.UserFCMessagingToken.as_view(), name='fcm-token'),
    path('v1/refresh-token/', views.RefreshToken.as_view(), name='refresh-token'),
    path('v1/profile/<str:uid>/', views.UserProfile.as_view(), name='profile'),
    path('v1/profile/<str:uid>/photo-update/', views.ProfilePhotoUpdate.as_view(), name='profile-photo-update'),
]