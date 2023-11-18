from .models import Project, ProjectApi
from ..account.services import ProfileService
from common.debug.log import Log
from common.utils import generator
from constants.keys import Keys
from common.platform.security import AES256
from django.conf import settings




class ProjectService:
    '''Project crud service'''

    @staticmethod
    def create_project(user, data: dict):
        project = Project.objects.create(user=user, **data)
        return ProjectService.to_json(project)
    
    @staticmethod
    def update_project(id: str, data: dict):
        project = Project.objects.get(id=id)
        project.name = data.get('name')
        project.description = data.get('description')
        project.envtype = data.get('envtype')
        project.save()
        return ProjectService.to_json(project)
    
    @staticmethod
    def list_project(user):
        projects_query = Project.objects.filter(user=user)
        projects = [ProjectService.to_json(project) for project in projects_query]
        return projects

    @staticmethod
    def delete_project(id: str):
        Project.objects.get(id=id).delete()
    
    @staticmethod
    def to_json(project: Project):
        return {
            'id': project.id,
            'user': ProfileService.to_json(project.user),
            'name': project.name,
            'description': project.description,
            'envtype': project.envtype,
            'createdon': project.created_on
        }




class ProjectApiService:
    '''Project Api Service'''

    @staticmethod
    def create_project_api(user, project_id: str, data: dict):
        project = Project.objects.get(id=project_id, user=user)
        api_key = Keys.GENERATED_API_KEY_PREFIX + generator.generate_password_key(36)
        api_key = AES256(settings.SERVER_ENC_KEY).encrypt(api_key)
        product = data.get('product')
        hosts_list = str(data.get('host')).split(',')
        project_api = ProjectApi.objects.create(
            project=project, 
            api_key=api_key, 
            product=product, 
            host={'urls': hosts_list}
        )
        return ProjectApiService.to_json(project_api)
    
    @staticmethod
    def list_project_apis(user, project_id: str):
        project = Project.objects.get(id=project_id, user=user)
        project_apis_query = ProjectApi.objects.filter(project=project)
        project_apis = [ProjectApiService.to_json(api) for api in project_apis_query]
        return project_apis

    @staticmethod
    def view_project_api(user, project_id, project_api_id):
        project = Project.objects.get(id=project_id, user=user)
        project_api = ProjectApi.objects.get(id=project_api_id, project=project)
        api_key = AES256(settings.SERVER_ENC_KEY).decrypt(project_api.api_key)
        return api_key

    @staticmethod
    def delete_project_api(user, project_id, project_api_id):
        project = Project.objects.get(id=project_id, user=user)
        ProjectApi.objects.get(id=project_api_id, project=project).delete()
    
    @staticmethod
    def to_json(project_api: ProjectApi):
        return {
            'id': project_api.pk,
            'project': ProjectService.to_json(project_api.project),
            'product': project_api.product,
            'apikey': project_api.api_key,
            'createdon': project_api.created_on
        }
    