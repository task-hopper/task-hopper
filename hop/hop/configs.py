import os
import json
import yaml
import jinja2
from copy import deepcopy
from functools import reduce

from helpers.utils import apath, dig


class Configs:
    def __init__(self, scope=None, preloaded_data={}):
        self._scope = scope
        self._data = preloaded_data or self._load_config()

    def get(self, key_str, default=None):
        return dig(self._data, *key_str.split("."), default=default)

    def clip_scope(self, key_str):
        keypath = key_str.split(".")
        data = deepcopy(dig(self._data, *keypath, default={}))

        return Configs(scope=key_str, preloaded_data=data)

    def print(self):
        print(json.dumps(self._data, indent=4))

    def reload(self):
        self._data = self._load_config()
        self.configs = Config(self._data)

    def _load_config(self):
        fpath = apath("~/.hoprc")
        if os.path.exists(fpath):
            with open(fpath) as f:
                config_map = yaml.safe_load(f) or {}

                #  return if hoprc has no contents
                if not config_map:
                    return {}

                env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="/"))
                template = env.get_template(fpath)

                config = yaml.safe_load(template.render(**config_map))

                return self._unpack_configs(config)
        else:
            return {}

    def _unpack_configs(self, configs, unpacked_configs={}, keypath=[]):
        for key, val in configs.items():
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
