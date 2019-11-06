from composer import composer
from config_handler import configs
from tasks._task import Task

class GetProjectDetail(Task):
    @classmethod
    def stage(cls, detail_type='alias', project_name=configs.current_project()):
        detail = {
            'alias': project_name,
            'name': configs.project_configs(project_name).get('name', project_name),
            'path': configs.project_configs(project_name).get('path', '')
        }.get(detail_type, '')

        composer.add('message', detail)
