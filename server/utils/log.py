from django.conf import settings

class Log:
    
    @staticmethod
    def info(object):
        if settings.DEBUG:
            print(f'[INFO]: {object}')
    
    @staticmethod
    def warn(object):
        if settings.DEBUG:
            print(f'[WARNING]: {object}')

    @staticmethod
    def error(object):
        print(f'[ERROR]: {object}')