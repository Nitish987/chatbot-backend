from ..project.models import Project
from ..project.services import ProjectService
from ..apis.models import Api
from ..apis.services import ApiService
from common.platform.security import AES256
from django.conf import settings



class ExternalExportService:
    '''External Export service for transfer data to external servers.'''

    @staticmethod
    def get_project(project_id) -> dict:
        project = ProjectService.get_project(project_id)
        return {
            'id': project.get('id'),
            'host': project.get('host')
        }