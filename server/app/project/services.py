from .models import Project, _next_pricing_date
from ..account.services import ProfileService
from common.debug.log import Log




class ProjectService:
    '''Project crud service'''

    @staticmethod
    def can_create_project(user):
        return Project.objects.filter(user=user).count() < 3

    @staticmethod
    def create_project(user, data: dict):
        hosts_list = str(data.get('host')).split(',')
        project = Project.objects.create(
            user=user, 
            name=data.get('name'),
            description=data.get('description'),
            envtype=data.get('envtype'),
            host={'urls': hosts_list},
            next_pricing_date=_next_pricing_date()
        )
        return ProjectService.to_json(project)
    
    @staticmethod
    def update_project(user, id: str, data: dict):
        hosts_list = str(data.get('host')).split(',')
        project = Project.objects.get(user=user, id=id)
        project.name = data.get('name')
        project.description = data.get('description')
        project.envtype = data.get('envtype')
        project.host = {'urls': hosts_list}
        project.save()
        return ProjectService.to_json(project)
    
    @staticmethod
    def list_project(user):
        projects_query = Project.objects.filter(user=user)
        projects = [ProjectService.to_json(project) for project in projects_query]
        return projects

    @staticmethod
    def delete_project(user, id: str):
        Project.objects.get(user=user, id=id).delete()
    
    @staticmethod
    def to_json(project: Project):
        return {
            'id': project.id,
            'user': ProfileService.to_json(project.user),
            'name': project.name,
            'description': project.description,
            'envtype': project.envtype,
            'host': project.host,
            'priceToPay': project.price_to_pay,
            'nextPricingDate': project.next_pricing_date,
            'updatedon': project.updated_on,
            'createdon': project.created_on
        }
