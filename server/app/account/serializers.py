from rest_framework import serializers
from .models import User
from utils import validators, otp
from django.core.cache import cache


# Signup
class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    date_of_birth = serializers.CharField(max_length=10)
    gender = serializers.CharField(max_length=1)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'date_of_birth', 'email', 'password', 'msg_token']

    def validate(self, attrs):
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')
        gender = attrs.get('gender')
        date_of_birth = attrs.get('date_of_birth')
        email = attrs.get('email')
        password = attrs.get('password')
        msg_token = attrs.get('msg_token')

        # validations checks
        if validators.is_empty(first_name) or not validators.atleast_length(first_name, 3) or validators.contains_script(first_name):
            raise serializers.ValidationError({'first_name': 'First name must contains atleast 3 characters.'})

        if validators.is_empty(last_name) or not validators.atleast_length(last_name, 2) or validators.contains_script(last_name):
            raise serializers.ValidationError({'last_name': 'Last name must contains atleast 2 characters.'})

        if validators.is_empty(gender) or not validators.atleast_length(gender, 1):
            raise serializers.ValidationError({'gender': 'Gender Must be specified.'})

        if validators.is_empty(date_of_birth) or not validators.is_equal_length(date_of_birth, 10):
            raise serializers.ValidationError({'date_of_birth': 'Invalid Date of Birth.'})

        if not validators.is_email(email):
            raise serializers.ValidationError({'email': 'Invalid Email'})

        if not validators.atleast_length(password, 8) or not validators.atmost_length(password, 32) or not validators.is_password(password):
            raise serializers.ValidationError({'password': 'Password must be of 8 to 32 character, contains atleast one number and one character.'})
        
        if type(msg_token) is not str:
            raise serializers.ValidationError({'token': 'Invalid message token.'})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'account': f'Account already exists with this email {email}. Try with another email.'})

        if cache.get(email):
            raise serializers.ValidationError({'email': 'Please, Try signup again after 10 minutes.'})
        
        return attrs


# Signup Verification
class SignupVerificationSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(max_length=6)

    class Meta:
        model = User
        fields = ['otp']

    def validate(self, attrs):
        entered_otp = attrs.get('otp')
        hashed_otp = self.context.get('hashed_otp')

        # validations checks
        if validators.is_empty(entered_otp) or not validators.is_equal_length(entered_otp, 6):
            raise serializers.ValidationError({'otp': 'OTP must be of 6 digit number.'})
        
        if not otp.compare(entered_otp, hashed_otp):
            raise serializers.ValidationError({'otp': 'Invalid OTP.'})

        return attrs


# Login
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password', 'msg_token']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        msg_token = attrs.get('msg_token')

        # validations checks
        if not validators.is_email(email):
            raise serializers.ValidationError({'email': 'Invalid Email'})

        if not validators.atleast_length(password, 8) or not validators.atmost_length(password, 32) or not validators.is_password(password):
            raise serializers.ValidationError({'password': 'Password must be of 8 to 32 character, contains atleast one number and one character.'})

        if type(msg_token) is not str:
            raise serializers.ValidationError({'token': 'Invalid message token.'})

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'account': 'No account found.'})

        user = User.objects.get(email=email)
        if not user.is_signed:
            raise serializers.ValidationError({'account': 'Something went wrong!'})

        if not user.is_active:
            raise serializers.ValidationError({'account', 'Your account has been deactivated.'})
        
        return attrs


# Password Recovery
class PasswordRecoverySerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')

        # validations checks
        if not validators.is_email(email):
            raise serializers.ValidationError({'email': 'Invalid Email'})

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'account': 'No account found.'})

        self.user = User.objects.get(email=email)
        if not self.user.is_signed:
            raise serializers.ValidationError({'account': 'Something went wrong!'})

        if not self.user.is_active:
            raise serializers.ValidationError({'account', 'Your account has been deactivated.'})

        return attrs


# Password Recovery Verification
class PasswordRecoveryVerificationSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(max_length=6)

    class Meta:
        model = User
        fields = ['otp']

    def validate(self, attrs):
        entered_otp = attrs.get('otp')
        hashed_otp = self.context.get('hashed_otp')

        # validations checks
        if validators.is_empty(entered_otp) or not validators.is_equal_length(entered_otp, 6):
            raise serializers.ValidationError({'otp': 'OTP must be equal to 6 digit number.'})
        
        if not otp.compare(entered_otp, hashed_otp):
            raise serializers.ValidationError({'otp': 'Invalid OTP.'})

        return attrs


# Password Recovery New Password
class PasswordRecoveryNewPassSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']

    def validate(self, attrs):
        password = attrs.get('password')

        # validations checks
        if not validators.atleast_length(password, 8) or not validators.atmost_length(password, 32) or not validators.is_password(password):
            raise serializers.ValidationError({'password': 'Password must be of 8 to 32 character, contains atleast one number and one character.'})
        
        return attrs


# Change Password
class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField()

    class Meta:
        model = User
        fields = ['password', 'new_password']

    def validate(self, attrs):
        password = attrs.get('password')
        new_password = attrs.get('new_password')

        # validations checks
        if not validators.atleast_length(password, 8) or not validators.atmost_length(password, 32) or not validators.is_password(password):
            raise serializers.ValidationError({'password': 'Password must be of 8 to 32 character, contains atleast one number and one character.'})
        
        if not validators.atleast_length(new_password, 8) or not validators.atmost_length(new_password, 32) or not validators.is_password(new_password):
            raise serializers.ValidationError({'password': 'Password must be of 8 to 32 character, contains atleast one number and one character.'})
        
        if not self.context.get('user').check_password(password):
            raise serializers.ValidationError({'password': 'Current password is Invalid.'})
        
        return attrs


# Change Username
class ChangeUserNamesSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']

    def validate(self, attrs):
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')
        username = attrs.get('username')
        password = attrs.get('password')

        # validations checks
        if validators.is_empty(first_name) or not validators.atleast_length(first_name, 3) or validators.contains_script(first_name):
            raise serializers.ValidationError({'first_name': 'First name must contains atleast 3 characters.'})

        if validators.is_empty(last_name) or not validators.atleast_length(last_name, 2) or validators.contains_script(last_name):
            raise serializers.ValidationError({'last_name': 'Last name must contains atleast 2 characters.'})
        
        if validators.is_empty(username) or ':' in username or '@' in username or validators.contains_script(username):
            raise serializers.ValidationError({'username': 'Username must not contains ":" or "@".'})
        
        if self.context.get('user').username != username:
            if User.objects.filter(username=username).exists():
                raise serializers.ValidationError({'username': f'Username {username} already taken.'})

        if not validators.atleast_length(password, 8) or not validators.atmost_length(password, 32) or not validators.is_password(password):
            raise serializers.ValidationError({'password': 'Password must be of 8 to 32 character, contains atleast one number and one character.'})
        
        if not self.context.get('user').check_password(password):
            raise serializers.ValidationError({'password': 'Invalid Password.'})
        
        return attrs


# User FCM Serializer
class UserFCMessagingTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['msg_token']

    def validate(self, attrs):
        msg_token = attrs.get('msg_token')

        if validators.is_empty(msg_token):
            raise serializers.ValidationError({'token': 'Invalid Messaging Token.'})

        return attrs



# User Update Profile Photo
class  ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['message', 'location', 'interest', 'bio', 'website']

    def validate(self, attrs):
        message = attrs.get('message')
        location = attrs.get('location')
        interest = attrs.get('interest')
        bio = attrs.get('bio')
        website = attrs.get('website')
        
        if validators.contains_script(message) or not validators.atmost_length(message, 100):
            raise serializers.ValidationError({'message': 'Invalid Message'})

        if validators.contains_script(location):
            raise serializers.ValidationError({'location': 'Invalid Location'})

        if validators.contains_script(interest):
            raise serializers.ValidationError({'interest': 'Invalid Interest'})
        
        if validators.contains_script(bio) or not validators.atmost_length(bio, 2000):
            raise serializers.ValidationError({'bio': 'Invalid Bio'})

        if validators.contains_script(website) or (website != '' and not validators.is_url(website)):
            raise serializers.ValidationError({'bio': 'Invalid website'})

        return attrs



# User Update Profile Photo
class ProfilePhotoUpdateSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField()

    class Meta:
        model = User
        fields = ['photo']

    def validate(self, attrs):
        photo = attrs.get('photo')
        
        if photo is None:
            raise serializers.ValidationError({'user': 'Invalid Profile Pic.'})

        return attrs
