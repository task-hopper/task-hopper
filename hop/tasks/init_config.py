from config_handler import configs
from helpers.utils import apath
from tasks._task import Task
from os import getcwd
import os.path as path
import shutil
import sys


class InitConfig(Task):
    def stage(self, directory=None, name=None, alias=None, create_hop_file=False):
        if directory is None:
            directory = getcwd()

        directory = path.abspath(directory)

        if not path.exists(directory):
            self.composer.add('error', f'Directory {directory} does not exist')

        if name is None:
            name = path.basename(directory).title()

        if alias is None:
            alias = name.lower()

        if create_hop_file is None:
            create_hop_file = False

        all_projects = configs.configs.get('projects')
        project_directories = {apath(config.get('path')): name for name, config in all_projects.items()}

        if directory in project_directories:
            project_name = project_directories[directory]
            self.composer.add('warning', f'Project {project_name} already configured for directory {directory}')

        else:
            basic_config = f"""
  {alias}:
    name: {name}
    path: {directory}"""

            self.composer.add('message', f'\033[0;32mAdding new project {name} to ~/.hoprc\033[0;32m')
            with open(apath('~/.hoprc'), 'a+') as f:
                f.write(basic_config)

        if create_hop_file:
            hop_file_destination = path.join(directory, '.hop')

            if path.exists(hop_file_destination):
                self.composer.add('warning', f'.hop file already exists in {directory}')

            else:
                self.composer.add('message', f'\033[0;32mCreating .hop file in {directory}')

                example_hop_file = path.join(sys.argv[0], 'ext/.hop.example')
                shutil.copy(example_hop_file, hop_file_destination)
