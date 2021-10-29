from composer import composer
from helpers.utils import apath, issubdir, mergedicts
from os import getcwd
import os.path as path
import yaml
import jinja2


class ConfigHandler:
    def __init__(self):
        self.configs = {}
        self.configs = self.load_config(apath('~/.hoprc'))

    def load_config(self, yaml_file):
        with open(yaml_file) as f:
            config_map = yaml.safe_load(f)

            env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath='/'))
            template = env.get_template(yaml_file)

            config = yaml.safe_load(template.render(**config_map))
            return config

    def current_project(self):
        current_project = None
        project_paths = {k: apath(v['path']).rstrip('/') for k, v in self.configs.get('projects', {}).items()}
        current_path = getcwd()
        for project, project_path in project_paths.items():
            if issubdir(current_path, project_path):
                current_project = project

        return current_project

    def project_configs(self, project_name=current_project):
        project_global_config = (
            self.configs
            .get('projects', {})
            .get(project_name))

        if project_global_config:
            project_root = project_global_config.get('path')
            if project_root:
                config_path = apath(f'{project_root}/.hop')
                if path.exists(config_path):
                    project_specific_config = self.load_config(config_path)
                    combined = mergedicts(project_global_config, project_specific_config)
                    return combined
                else:
                    return project_global_config
            else:
                composer.add('error', f'path is not configured for project {project_name}')
        else:
            composer.add('error', f'Project is not configured')

    def carrot_configs(self, carrot_name):
        return self.configs.get('carrots', {}).get(carrot_name, {})

configs = ConfigHandler()
