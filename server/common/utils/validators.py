from django.core.validators import validate_email, URLValidator

# check whether the email is valid or not
def is_email(email):
    try:
        validate_email(str(email))
        return True
    except:
        return False

# check whether the text is aleast of given length
def atleast_length(text, length):
    if len(str(text)) >= length:
        return True
    return False

# check whether the text is atmost of given length
def atmost_length(text, length):
    if len(str(text)) <= length:
        return True
    return False

# check whether the text length is equal to given length
def is_equal_length(text, length):
    if len(str(text)) == length:
        return True
    return False

# check whether the text is aleast of given length
def is_empty(text):
    if text == None or len(str(text)) == 0:
        return True
    return False

# check whether the text contains a script or not
def contains_script(text):
    text = str(text)
    if '<' in text or '</' in text or '>' in text or '=' in text or 'fetch' in text:
        return True
    return False

# check whether the password contains number and characters both
def is_password(password):
    containsNum, containsAlpha = False, False
    for i in str(password):
        ascii = ord(i)
        if not containsAlpha and ((ascii >= 65 and ascii <= 90) or (ascii >= 97 and ascii <= 122)):
            containsAlpha = True
        if not containsNum and (ascii >= 48 and ascii <= 57):
            containsNum = True
        if containsNum and containsAlpha:
            return True
    return False

# check whether the url is valid or not
def is_url(url):
    validate_url = URLValidator()
    try:
        validate_url(url)
        return True
    except:
        return False