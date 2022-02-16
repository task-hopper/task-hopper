from config_handler import configs
from tasks._task import Task

class AutoRun(Task):
    def stage(self, project_name=configs.current_project(), verbose=False):
        project_configs = configs.project_configs(project_name)
        project_autorun = project_configs.get('autorun', {})

        for command in project_autorun:
            if verbose: self.composer.add('message', f'> {command}')
            self.composer.add('task', command)
