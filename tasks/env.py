from composer import composer
from config_handler import configs
from tasks._task import Task

class Env(Task):
    @classmethod
    def stage(cls, project_name=None):
        project_configs = (configs or ConfigHandler()).project_configs(project_name)
        project_env = project_configs.get('env', {})
        autoload_type = project_env.get('autoload', False)
        if autoload_type:
            exports =  [f'export {var}={val}' 
                        for (env, vars) in project_env.items() if env in ['default', autoload_type] 
                        for var, val in vars.items()]
            composer.add('task', exports)
