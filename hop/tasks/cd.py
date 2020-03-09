from composer import composer
from config_handler import configs
from helpers.utils import apath
from tasks._task import Task

class CD(Task):
    @classmethod
    def stage(cls, project_name=None, directory=None):
        if project_name:
            project_configs = configs.project_configs(project_name)
            project_path = apath(project_configs.get("path"))
            composer.add('task', f'cd {project_configs.get("path")}')
        else:
            abs_directory = apath(directory)
            composer.add('task', f'cd {abs_directory}')
