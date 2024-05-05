from th import (
    Task,
    composer,
)

from th.utils.casing import snake_case


class ChangeEnv(Task):
    def stage(self, project_name=None, env=None, action='set', verbose=False):
        project_name = project_name or self.carrot.current_project()
        project_configs = self.carrot.project_configs(project_name)
        project_env = project_configs.get('env', {})
        formatted_project_name = snake_case(project_name).upper()

        if action == 'list':
            available_envs = [e for e in project_env if e not in ['default', 'autoload']]

            if len(available_envs) > 0:
                composer.add('message', available_envs)

            else:
                composer.add('warn', 'No environments configured for current project')

        if action == 'unset':
            current_env = self.carrot.current_env()
            if current_env:
                current_env_unsets = [ f'unset {var}' for var in project_env.get(current_env, {}).keys() ]
                default_env_unsets = [ f'unset {var}' for var in project_env.get('default', {}).keys() ]
                unsets = [ *current_env_unsets, *default_env_unsets ]

                if verbose: composer.add('message', unsets)

                composer.add('eval', unsets)
                composer.add('eval', f'unset HOP_ENV_{formatted_project_name}')

        if action == 'set':
            if env is None: composer.add('error', 'No environment specified')

            environments = ['default']

            # autoload environment if specified and set the current environment env var.
            if env == 'autoload':
                autoload_env = project_env.get('autoload')

                composer.add('eval', f'export HOP_ENV_{formatted_project_name}="{autoload_env}"')

                if autoload_env: environments.append(autoload_env)

            elif env in project_env:
                formatted_project_name = snake_case(project_name).upper()
                composer.add('eval', f'export HOP_ENV_{formatted_project_name}="{env}"')
                environments.append(env)
            else:
                composer.add('error', f'Environment {env} not configured for project {project_name}')

            # export env vars
            exports = [ f'export {var}="{val}"'
                        for e, vars in project_env.items() if e in environments
                        for var, val in vars.items() ]

            if verbose: composer.add('info', exports)

            composer.add('eval', exports)
