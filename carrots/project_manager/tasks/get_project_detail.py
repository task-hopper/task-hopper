from th import (
    Task,
    composer,
)


class GetProjectDetail(Task):
    def stage(self, detail_type='alias', project_name=None):
        pname = project_name or self.carrot.current_project()
        detail = {
            'alias': pname,
            'name': self.carrot.project_configs(project_name).get('name', project_name),
            'path': self.carrot.project_configs(project_name).get('path', '')
        }.get(detail_type, '')

        composer.add('info', detail)
