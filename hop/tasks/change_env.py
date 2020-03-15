from config_handler import configs
from tasks._task import Task

class ChangeEnv(Task):
    def stage(self, project_name=configs.current_project(), env=None, list_envs=False, verbose=False):
        project_configs = configs.project_configs(project_name)
        project_env = project_configs.get('env', {})

        if list_envs:
            available_envs = [e for e in project_env if e not in ['default', 'autoload']]

            if len(available_envs) > 0:
                self.composer.add('message', available_envs)

            else:
                self.composer.add('warning', 'No environments configured for current project')

        elif env is not None:
            environments = ['default']

            if env == 'autoload':
                autoload_env = project_env.get('autoload')

                if autoload_env: environments.append(autoload_env)

            elif env in project_env:
                environments.append(env)

            else:
                self.composer.add('error', f'Environment {env} not configured for project {project_name}')

            exports = [ f'export {var}="{val}"'
                        for e, vars in project_env.items() if e in environments
                        for var, val in vars.items() ]

            if verbose: self.composer.add('message', exports)

            self.composer.add('task', exports)

        else:
            self.composer.add('error', 'No options specified')
