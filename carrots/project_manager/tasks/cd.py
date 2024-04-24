from hop import (
    Task,
    configs,
)


class CD(Task):
    def stage(self, project_name=None):
        project_configs = configs.project_configs(project_name)
        self.composer.add('eval', f'cd {project_configs.get("path")}')
