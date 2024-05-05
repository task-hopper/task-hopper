from th import (
    Task,
    composer,
)


class CD(Task):
    def stage(self, project_name=None):
        project_configs = self.carrot.project_configs(project_name)
        project_path = project_configs.get("path")
        composer.add("eval", f"cd {project_path}")
