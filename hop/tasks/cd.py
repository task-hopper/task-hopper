from config_handler import configs
from helpers.utils import apath
from tasks._task import Task

class CD(Task):
    def stage(self, project_name=None):
        project_configs = configs.project_configs(project_name)
        project_path = apath(project_configs.get("path"))
        self.composer.add('task', f'cd {project_configs.get("path")}')
