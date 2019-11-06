from composer import composer
from config_handler import configs
from tasks._task import Task

class ChangeEnv(Task):
    @classmethod
    def stage(cls, project_name=configs.current_project(), env=None):
        project_configs = configs.project_configs(project_name)
        project_env = project_configs.get('env', {})
        if env == 'autoload':
            autoload_type = project_env.get('autoload')
            environments = list(filter(None, ['default', autoload_type]))
        elif env:
            environments = env if isinstance(env, list) else [env]
        
        exports = [ f'export {var}={val}'
                    for env, vars in project_env.items() if env in environments
                    for var, val in vars.items() ]

        composer.add('task', exports) 
