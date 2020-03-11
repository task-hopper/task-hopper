from config_handler import configs
from tasks._task import Task


class ListProjects(Task):
    def stage(self):
        all_projects = configs.configs['projects']
        current_project = configs.current_project()

        project_list = [name for name, config in all_projects.items()]
        sorted_list = sorted(project_list)
        colored_list = [f'{"=>" if item == current_project else "  "} \e[32m{item}\e[0m' for item in sorted_list]

        message = colored_list
        message.append('')
        message.append('# => - current')

        self.composer.add('message', message)
