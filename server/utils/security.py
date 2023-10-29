from AesEverywhere import aes256

class AES256:
    def __init__(self, key):
        self.key = key

    def encrypt(self, raw):
        cipher = aes256.encrypt(raw, self.key)
        return cipher.decode('utf-8')

    def decrypt(self, cipher):
        raw = aes256.decrypt(cipher.encode('utf-8'), self.key)
        return raw.decode('utf-8')