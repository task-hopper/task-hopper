import os
import types
from copy import deepcopy

from th import (
    Carrot,
    Command,
    composer,
    load_custom_configs,
)

from th.utils.os_tools import (
    apath,
    issubdir,
)

from th.utils.casing import snake_case


class ProjectManager(Carrot):
    def __load__(self):
        current_project = self.current_project()
        if current_project:
            project_commands = self.configs.get(f"projects.{current_project}.commands", {})
        else:
            project_commands = {}

        converted_commands = {}
        for alias, cmd in project_commands.items():
            help_msg = (cmd[:35] + "...") if len(cmd) > 35 else cmd
            command = Command(alias=alias, help=help_msg)

            def new_process_command(self, _, c=cmd):
                cmd_args = " ".join(self.additional_args)
                composer.add("eval", f"{c} {cmd_args}")

            command.process_command = types.MethodType(new_process_command, command)

            command._bootstrap(subparsers=self.subparsers)
            converted_commands[alias] = command


        self.loader.push_commands(converted_commands)

    def current_project(self):
        current_project = None
        project_paths = {
            project_name: apath(project_configs.get("path")).rstrip("/")
            for project_name, project_configs
            in self.configs.get("projects", {}).items()
        }
        current_path = os.getcwd()
        for project, project_path in project_paths.items():
            if issubdir(current_path, project_path):
                current_project = project

        return current_project

    def current_env(self):
        project = self.current_project()
        if project:
            formatted_project_name = snake_case(project).upper()
            env_var = f"HOP_ENV_{formatted_project_name}"
            return os.getenv(env_var, None)

        return None

    def project_configs(self, project_name=None):
        pname = project_name or self.current_project()
        global_project_configs = self.configs.get(f"projects.{pname}", {})

        if global_project_configs:
            project_root = global_project_configs.get("path")
            if project_root:
                config_path = apath(f"{project_root}/.hop")
                if os.path.exists(config_path):
                    #  local_project_config = self.load_config(config_path)
                    local_project_configs = load_custom_configs(config_path=config_path)
                    updated_configs = deepcopy(global_project_configs)
                    updated_configs.update(deepcopy(local_project_configs.data))
                    return load_custom_configs(preloaded_data=updated_configs)
                else:
                    return load_custom_configs(preloaded_data=global_project_configs)
            else:
                composer.add("error", f"path is not configured for project {pname}")
        else:
            composer.add("error", f"Project is not configured")


