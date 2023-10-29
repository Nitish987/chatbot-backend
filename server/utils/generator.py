import random
import array
import uuid
import secrets
import time

# returns unique uuid
def generate_uuid():
    choice = random.choice(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
    uid = str(uuid.uuid4()).replace('-', choice)
    return uid

# returns unique identifier
def generate_identity():
    return str(uuid.uuid4())

# returns generated username
def generate_username(first_name, last_name):
    if first_name != '' and last_name != '':
        return first_name.lower() + '_' + last_name.lower() + '_' + str(random.randint(1000, 9999))
    return first_name.lower() + '_' + str(random.randint(1000, 9999))

# returns generated random token
def generate_token():
    return str(secrets.token_hex())

# returns generated char sequence of n char
def generate_string(prefix= 'string', n = 10):
    s = prefix + '_'
    for i in range(n):
        s = s + random.choice(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
    return s

# returns generated time epoc string
def generate_milli_string():
    curr_time = round(time.time()*1000)
    return str(curr_time)

# random password key generator
def generate_password_key(n = 16):
    MAX_LEN = n
    DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>', '*', '(', ')', '<']

    COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS

    rand_digit = random.choice(DIGITS)
    rand_upper = random.choice(UPCASE_CHARACTERS)
    rand_lower = random.choice(LOCASE_CHARACTERS)
    rand_symbol = random.choice(SYMBOLS)

    temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol

    for x in range(MAX_LEN - 4):
        temp_pass = temp_pass + random.choice(COMBINED_LIST)
        temp_pass_list = array.array('u', temp_pass)
        random.shuffle(temp_pass_list)

    password = ""
    for x in temp_pass_list:
        password = password + x
    
    return password
