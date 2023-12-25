from ..project.models import Project
from ..apis.models import Api
from common.platform.products import Product




class BillingService:
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
    
    @staticmethod
    def get_billing(user):
        billings = []
        projects = Project.objects.filter(user=user)
        for project in projects:
            project_billing = {
                'id': project.id,
                'name': project.name,
                'priceToPay': project.price_to_pay,
                'nextPricingDate': project.next_pricing_date,
                'createdon': project.created_on,
                'apis': []
            }
            apis = Api.objects.filter(project=project)
            for api in apis:
                project_billing['apis'].append({
                    'id': api.id,
                    'product': api.product,
                    'type': api.type,
                    'hitsCount': api.hits_count,
                    'createdon': api.created_on
                })
            billings.append(project_billing)
        return billings
    
    @staticmethod
    def get_billing_By_project(user, project_id):
        project = Project.objects.get(user=user, id=project_id)
        billing = {
            'id': project.id,
            'name': project.name,
            'priceToPay': project.price_to_pay,
            'nextPricingDate': project.next_pricing_date,
            'createdon': project.created_on,
            'apis': []
        }
        apis = Api.objects.filter(project=project)
        for api in apis:
            billing['apis'].append({
                'id': api.id,
                'product': api.product,
                'type': api.type,
                'hitsCount': api.hits_count,
                'createdon': api.created_on
            })
        return billing