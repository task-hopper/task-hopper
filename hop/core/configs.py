import os
import json
import yaml
import jinja2
from copy import deepcopy
from functools import reduce

from utils.os_tools import apath
from utils.dict_tools import dig


class Configs:
    def __init__(self, config_path=None, preloaded_data={}):
        self.data = preloaded_data or self._load_config(config_path or apath("~/.hoprc"))

    def get(self, key_str, default=None):
        return dig(self.data, *key_str.split("."), default=default)

    def clip_scope(self, key_str):
        keypath = key_str.split(".")
        data = deepcopy(dig(self.data, *keypath, default={}))

        return Configs(preloaded_data=data)

    def print(self):
        print(json.dumps(self.data, indent=4))

    def _load_config(self, config_path):
        if os.path.exists(config_path):
            with open(config_path) as f:
                config_map = yaml.safe_load(f) or {}

                #  return if hoprc has no contents
                if not config_map:
                    return {}

                env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="/"))
                template = env.get_template(config_path)

                config = yaml.safe_load(template.render(**config_map))

                self.initial_data = config
                return self._unpack_configs(config, unpacked_configs={}, keypath=[])
        else:
            return {}

    def _unpack_configs(self, config, unpacked_configs, keypath):
        for key, val in config.items():
            if "." in key or keypath:
                nested_keys = [*keypath, *key.split(".")]
                nesetd_val = reduce(
                    lambda d, k: d.setdefault(k, {}),
                    nested_keys[:-1],
                    unpacked_configs
                )
                if isinstance(val, dict):
                    self._unpack_configs(val, unpacked_configs, nested_keys)
                else:
                    nesetd_val[nested_keys[-1]] = val
            else:
                if isinstance(val, dict):
                    self._unpack_configs(val, unpacked_configs, [*keypath, key])
                else:
                    unpacked_configs[key] = val

        return unpacked_configs


configs = Configs()
