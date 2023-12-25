from ..project.models import Project
from ..apis.models import Api
from ..chatbot.models import Chatbot
from ..chatbot.services import ChatbotService
from ..emforms.models import Emform
from ..emforms.services import EmformService
from common.platform.security import AES256
from common.platform.products import Product
from django.conf import settings



class ExternalExportService:
    '''External Export service for transfer data to external servers.'''

    @staticmethod
    def get_project(project_id) -> dict:
        project = Project.objects.get(id=project_id)
        if not project.can_make_request:
            raise Exception('Permission Denied')

        return {
            'id': project.id,
            'host': project.host
        }
    
    @staticmethod
    def get_product(project_id, api_id):
        project = Project.objects.get(id=project_id)
        api = Api.objects.get(id=api_id, project=project)
        api_key = AES256(settings.SERVER_ENC_KEY).decrypt(api.api_key)
        if api.product == Product.chatbot.name:
            product = Chatbot.objects.get(api=api)
            return {
                'apikey': api_key,
                'product': ChatbotService.to_json(product)
            }
        elif api.product == Product.emforms.name:
            product = Emform.objects.get(api=api)
            return {
                'apikey': api_key,
                'product': EmformService.to_json(product)
            }
        raise Exception('No Product Found.')
    
    @staticmethod
    def update_billing(project_id, api_id):
        project = Project.objects.get(id=project_id)
        api = Api.objects.get(id=api_id, project=project)
        if api.product == Product.chatbot.name or api.product == Product.emforms.name:
            api.hits_count = api.hits_count + 1
            api.save()
        apis = Api.objects.filter(project=project)
        for a in apis:
            price = Product.chatbot.price if a.product == Product.chatbot.name else Product.emforms.price
            project.price_to_pay = project.price_to_pay + (a.hits_count * price)
        project.save()
        return project.price_to_pay
            
            