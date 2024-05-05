import os
import yaml


REPO_PATH = os.getenv('HOP_REPO')
REGISTRY_PATH = f"{REPO_PATH}/hop/ext/carrot_registry.yml"


def read_registry():
    with open(REGISTRY_PATH) as f:
        return yaml.safe_load(f)


def registy_data_str(carrot_package_name=None):
    data = read_registry

    return data.keys()
