from hop import (
    Task,
)


class CD(Task):
    def stage(self, project_name=None):
        #  project_configs = cself.onfigs.project_configs(project_name)
        #  self.composer.add('eval', f'cd {project_configs.get("path")}')
        self.composer.add("info", "...changing directory")
