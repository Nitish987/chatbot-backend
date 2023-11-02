from django.conf import settings
from django.core.mail import EmailMessage
from .log import Log

class Mailer:
    @staticmethod
    def sendEmail(email, data):
        '''sends email'''

        if settings.DEBUG:
            # printing data only for Development
            Log.info(data)
        else:
            try:
                email = EmailMessage(
                    subject=f'{settings.APP_NAME} app', 
                    body=str(data), 
                    from_email=str(settings.EMAIL_HOST_USER), 
                    to=[email,], 
                    reply_to=['support@example.com']
                )
                email.send(fail_silently=False)
            except Exception as e:
                Log.error(e)
            