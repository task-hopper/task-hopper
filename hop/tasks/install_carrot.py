import os
import shutil
from hop import apath, Task
from helpers.carrot_utils import read_registry


REPO_PATH = os.getenv('HOP_REPO')


class InstallCarrot(Task):
    def stage(self, carrot_package_name, version, repo):
        registry_data = read_registry()
        carrot = registry_data.get(carrot_package_name)

        if not carrot:
            self.composer.add("warn", "Unofficial carrots are not yet supported")
            self.composer.add("error", f"{carrot_package_name} could not be found.")

        if carrot.get("type") == "official":
            self._install_official(carrot_package_name)
        else:
            self.composer.add("warn", "Unofficial carrots are not yet supported")
            self.composer.compose()


    def _install_official(self, carrot_package_name, carrot_data=None):
        self.composer.add("info", f"Installing {carrot_package_name}...")
        carrot_location = f"{REPO_PATH}/carrots/{carrot_package_name}"
        install_location = apath(f"~/.hop/carrots/{carrot_package_name}")

        os.makedirs(install_location, exist_ok=True)
        shutil.copytree(carrot_location, install_location, dirs_exist_ok=True)
        self.composer.add("info", "...installation complete.")

