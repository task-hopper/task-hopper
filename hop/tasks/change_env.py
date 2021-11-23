from config_handler import configs
from tasks._task import Task
from helpers.utils import snake_case

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

            # unset the previous environment's env vars before continuing
            current_env = configs.current_env()
            if current_env:
                unsets = [ f'unset {var}' for var in project_env.get(current_env).keys() ]
                self.composer.add('task', unsets)

            # autoload environment if specified and set the current environment env var.
            if env == 'autoload':
                autoload_env = project_env.get('autoload')

                formatted_project_name = snake_case(project_name).upper()
                self.composer.add('task', f'export HOP_ENV_{formatted_project_name}="{autoload_env}"')

                if autoload_env: environments.append(autoload_env)

            elif env in project_env:
                formatted_project_name = snake_case(project_name).upper()
                self.composer.add('task', f'export HOP_ENV_{formatted_project_name}="{env}"')
                environments.append(env)
            else:
                self.composer.add('error', f'Environment {env} not configured for project {project_name}')

            # export env vars
            exports = [ f'export {var}="{val}"'
                        for e, vars in project_env.items() if e in environments
                        for var, val in vars.items() ]

            if verbose: self.composer.add('message', exports)

            self.composer.add('task', exports)

        else:
            self.composer.add('error', 'No options specified')
