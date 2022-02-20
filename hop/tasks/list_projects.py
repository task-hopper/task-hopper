from config_handler import configs
from tasks._task import Task


class ListProjects(Task):
    def stage(self, no_color=False):
        all_projects = configs.configs.get('projects', {})
        current_project = configs.current_project()

        project_list = [name for name, config in all_projects.items()]
        sorted_list = sorted(project_list)

        use_color = not no_color
        begin_color = '\033[0;32m'
        end_color = '\033[0m'

        colored_list = [f'{"=>" if item == current_project else "  "} {begin_color if use_color else ""}{item}{end_color if use_color else ""}' for item in sorted_list]

        message = colored_list
        message.append('')
        message.append('# => - current')

        self.composer.add('message', message)
