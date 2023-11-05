import random
import bcrypt

# returns generated 6 digit OTP
def generate():
    OTP = str(random.random())[3:9]
    salt = bcrypt.gensalt(10)
    hashOTP = bcrypt.hashpw(OTP.encode('utf-8'), salt)
    return OTP, hashOTP.decode('utf-8')

# check whether the OTP is valid or not
def compare(OTP, hashOTP):
    if bcrypt.checkpw(OTP.encode('utf-8'), hashOTP.encode('utf-8')):
        return True
    return False