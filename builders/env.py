from config_handler import configs
from builders._builder import Builder

class Env(Builder):
    @classmethod
    def build(cls, project_name=None):
        project_configs = (configs or ConfigHandler()).project_configs(project_name)
        project_env = project_configs.get('env', {})
        autoload_type = project_env.get('autoload', False)
        if autoload_type:
            return [f'export {var}={val}' 
                    for (env, vars) in project_env.items() if env in ['default', autoload_type] 
                    for var, val in vars.items()]
        else:
            return []
