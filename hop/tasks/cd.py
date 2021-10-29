from config_handler import configs
from helpers.utils import apath
from tasks._task import Task

class CD(Task):
    def stage(self, project_name=None):
        project_configs = configs.project_configs(project_name)
        self.composer.add('task', f'export CURRENT_PROJECT={project_name}')
        self.composer.add('task', f'cd {project_configs.get("path")}')
