from helpers.utils import apath
from config_handler import configs
from builders._builder import Builder

class CD(Builder):
    @classmethod
    def build(cls, project_name=None, directory=None):
        if project_name:
            project_configs = configs.project_configs(project_name)
            project_path = apath(project_configs.get("path"))
            return f'cd {project_configs.get("path")}'
        else:
            abs_directory = apath(directory)
            return f'cd {abs_directory}'
