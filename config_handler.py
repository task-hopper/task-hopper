from composer import composer
from helpers.utils import apath, issubdir
from os import getcwd
import os.path as path
import yaml

class ConfigHandler:
    def __init__(self):
        self.configs = {}
        with open(apath('~/.hoprc')) as f:
            self.configs = yaml.load(f, Loader=yaml.FullLoader)

    def current_project(self):
        current_project = None
        project_paths = { k: apath(v['path']) for k,v in self.configs.get('projects', {}).items() } 
        current_path = getcwd()
        for project, project_path in project_paths.items():
            if issubdir(current_path, project_path):
                current_project = project

        return current_project

    def project_configs(self, project_name=current_project):
        project = (
            self.configs
            .get('projects', {})
            .get(project_name))

        if project:
            project_root = project.get('path')
            if project_root:
                config_path = apath(f'{project_root}/.hop')
                if path.exists(config_path):
                    project_override = { 'path': project_root }
                    with open(config_path) as f:
                       return {**project_override, **yaml.load(f, Loader=yaml.FullLoader)}
                else:
                    return project
            else:
                composer.add('error', f'path is not configured for project {project}')
        else:
            parent_config = self.configs.get('project_parents')
            if parent_config:
                parents = [apath(i) for i in self.configs.get('project_parents')]
                for p in parents:
                    if path.exists(p):
                        project_root = f'{p}/{project_name}'
                        if path.exists(project_root):
                            config_path = f'{project_root}/.hop'
                            if path.exists(config_path):
                                project_override = { 'path': project_root }
                                with open(config_path) as f:
                                    return {**project_override, **yaml.load(f, Loader=yaml.FullLoader)}
                            else:
                                # composer.add('warn', f'No .hop file found in project {project_name}')
                                return {
                                    'name': project_name,
                                    'path': project_root
                                }
            composer.add('error', f'Project is not configured')

configs = ConfigHandler()
