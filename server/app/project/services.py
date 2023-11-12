from .models import Project
from ..account.services import ProfileService
from common.debug.log import Log




class ProjectService:
    '''Project crud service'''

    @staticmethod
    def create_project(user, data: dict):
        project = Project.objects.create(user=user, **data)
        return ProjectService.to_json(project)
    
    @staticmethod
    def update_project(id: str, data: dict):
        project = Project.objects.get(id=id)
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
    