from config_handler import configs
from helpers.utils import apath
from tasks._task import Task
import os.path as path

# TODO
#  from helpers.colors import bash_colors

class EditConfig(Task):
    def stage(self, project_name=None, edit_global=False):
        config_file = None

        if edit_global:
            config_file = '~/.hoprc'

        elif project_name is not None:
            config = configs.project_configs(project_name)

            hop_file = path.join(config.get('path'), '.hop')

            if path.exists(apath(hop_file)):
                config_file = hop_file

            else:
                self.composer.add('message', [
                    f'No .hop file is present in project {project_name}. Your options are:',
                    '\033[0;32m',
                    f'  hop to {project_name}',
                    f'  hop init --create-hop-file',
                    '\033[0m',
                    'or you can edit the global config file with:',
                    '\033[0;32m',
                    '  hop edit -g',
                    '\033[0m'
                ])
                return

        else:
            self.composer.add('error', 'No options specified')

        self.composer.add('task', f'$EDITOR {config_file} </dev/tty')
