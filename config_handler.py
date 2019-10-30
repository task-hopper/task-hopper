from helpers.utils import apath
import os.path as path
import yaml

class ConfigHandler:
    def __init__(self):
        self.configs = {}
        with open(apath('~/.hoprc')) as f:
            self.configs = yaml.load(f, Loader=yaml.FullLoader)

    def project_configs(self, pname):
        project = (
            self.configs
            .get('projects', {})
            .get(pname))

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
                sys.exit(f'path is not configured for project {project}')
        else:
            sys.exit(f'project is not configured')
