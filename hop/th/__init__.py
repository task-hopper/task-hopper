# th module is for public interface / carrot development
from core.carrot import Carrot
from core.command import Command
from core.task import Task
from core.loader import (
    composer,
    configs,
)

def load_custom_configs(config_path=None, preloaded_data=None):
    from core.configs import Configs

    return Configs(config_path=config_path, preloaded_data=preloaded_data or {})
