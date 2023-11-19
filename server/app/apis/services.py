from .models import ProjectApi
from common.debug.log import Log
from common.utils import generator
from constants.keys import Keys
from common.platform.security import AES256
from django.conf import settings
from ..project.models import Project
from ..project.services import ProjectService





class ProjectApiService:
    '''Project Api Service'''

    @staticmethod
    def create_project_api(user, project_id: str, data: dict):
        project = Project.objects.get(id=project_id, user=user)
        api_key = Keys.GENERATED_API_KEY_PREFIX + generator.generate_password_key(Keys.GENERATED_API_KEY_SIZE)
        api_key = AES256(settings.SERVER_ENC_KEY).encrypt(api_key)
        hosts_list = str(data.get('host')).split(',')
        project_api = ProjectApi.objects.create(
            project=project, 
            api_key=api_key, 
            product=data.get('product'), 
            type=data.get('type'),
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
            'type': project_api.type,
            'apikey': project_api.api_key,
            'createdon': project_api.created_on
        }