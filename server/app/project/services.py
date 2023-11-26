from .models import Project
from ..account.services import ProfileService
from common.debug.log import Log




class ProjectService:
    '''Project crud service'''

    @staticmethod
    def create_project(user, data: dict):
        hosts_list = str(data.get('host')).split(',')
        project = Project.objects.create(
            user=user, 
            name=data.get('name'),
            description=data.get('description'),
            envtype=data.get('envtype'),
            host={'urls': hosts_list}
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
    def get_project(id):
        project = Project.objects.get(id=id)
        return ProjectService.to_json(project)

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
            'updatedon': project.updated_on,
            'createdon': project.created_on
        }
