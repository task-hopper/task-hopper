import inspect
import pkgutil
import sys
import types
from hop import Carrot, Command, Task, configs
from helpers.utils import apath
from composer import Composer


CARROT_PATH = apath("~/.hop/carrots")
sys.path.append(CARROT_PATH)


def _issubclass(cls_member, parent_cls):
    return (
        issubclass(cls_member[1], parent_cls)
        and
        cls_member[1] is not parent_cls
    )


class Loader:
    def __init__(self, subparsers):
        self.subparsers = subparsers
        self.composer = Composer()
        self.bunch = {}
        self.tasks = {}
        self.commands = {}
        self._load_task_hopper()


    def _load_task_hopper(self):
        self._load_tasks()
        self._load_core_commands()
        self._load_configured_commands()
        self._load_carrots()

        for _, meta in self.bunch.items():
            self._push_tasks(meta.get("tasks", {}), source_name=meta.get("name"))
            for _, cmd in meta.get("commands", {}).items():
                cmd._bind_tasks(self.tasks)
            self._push_commands(meta.get("commands", {}), source_name=meta.get("name"))

        for _, cmd in self.commands.items():
            cmd.setup_command()

    def _push_tasks(self, tasks={}, source_name="?"):
        for task_name, task in tasks.items():
            if task_name in self.tasks:
                self.composer.add(
                    "error",
                    (
                        f"[{source_name}] {task_name} already exists. "
                        "To overwrite, use patch interface."
                    )
                )
            else:
                self.tasks[task_name] = task

    def _push_commands(self, commands={}, source_name="?"):
        for command_name, command in commands.items():
            if command_name in self.commands:
                self.composer.add(
                    "error",
                    (
                        f"[{source_name}]Command '{command_name}' already exists. "
                        "To overwrite, use patch interface."
                    )
                )
            else:
                self.commands[command_name] = command

    def _load_carrots(self):
        '''
        '''
        # Iterate through each carrot plugin in the "carrots" folder
        for _1, carrot_package_name, is_pkg1 in pkgutil.iter_modules([CARROT_PATH]):
            if is_pkg1:
                carrot_package = __import__(carrot_package_name, fromlist=["devnull"])
                carrot_members = [
                    m
                    for m
                    in inspect.getmembers(carrot_package, inspect.isclass)
                    if _issubclass(m, Carrot)
                ]
                # Make sure there is only 1 Carrot subclass defined for the carrot plugin
                if len(carrot_members) > 1:
                    self.composer.add("error", f"Carrot Error: {carrot_package_name} module has multiple members of Carrot class when one is required.")
                if not len(carrot_members):
                    self.composer.add("error", f"Carrot Error: {carrot_package_name} module missing Carrot class member.")

                # Start carrot metadata dict
                carrot_spec = None
                _, carrot_cls = carrot_members[0]
                carrot = carrot_cls()
                carrot_name = carrot_cls.__name__
                carrot._bootstrap(
                    configs=configs.clip_scope(f"carrot.{carrot_name}"),
                )
                carrot_spec = {
                    "name": carrot_name,
                    "klass": carrot,
                    "tasks": {},
                    "commands": {}
                }

                # Iterate through carrot submodules
                for _2, carrot_submodule_name, is_pkg2 in pkgutil.iter_modules(carrot_package.__path__, carrot_package.__name__ + "."):
                    # Allow tasks and commands submodules only
                    allowed_submodules = [ f"{carrot_package_name}.{asm}" for asm in ["tasks", "commands"] ]
                    if is_pkg2 and carrot_submodule_name in allowed_submodules:
                        carrot_submodule = __import__(carrot_submodule_name, fromlist=["devnull"]) 
                        carrot_submodule_members = [
                            m
                            for m
                            in inspect.getmembers(carrot_submodule, inspect.isclass)
                            if _issubclass(m, Command) or _issubclass(m, Task)
                        ]

                        for (_, c) in carrot_submodule_members:
                            base_modules = [i.__name__ for i in c.__bases__]
                            if "Task" in base_modules:
                                task = c()
                                task._bootstrap(
                                    composer=self.composer,
                                    carrot=carrot
                                )
                                carrot_spec["tasks"][c.__name__] = task
                            if "Command" in base_modules:
                                command = c()
                                command._bootstrap(
                                    carrot=carrot,
                                    composer=self.composer,
                                    subparsers=self.subparsers,
                                )
                                carrot_spec["commands"][command.alias] = command
                self.bunch[carrot_name] = carrot_spec

    def _load_tasks(self):
        imported_package = __import__("tasks", fromlist=["devnull"])

        for _, task_name, is_pkg \
        in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + "."):
            if not is_pkg:
                task_module = __import__(task_name, fromlist=["devnull"])
                cls_members = inspect.getmembers(task_module, inspect.isclass)
                for cls in cls_members:
                    if _issubclass(cls, Task):
                        (_, c) = cls
                        task = c()
                        task._bootstrap(composer=self.composer)
                        self.tasks[c.__name__] = task

    def _load_core_commands(self):
        '''
        load core Task Hopper commands
        '''
        imported_package = __import__("commands", fromlist=["devnull"])

        for _, command_name, is_pkg \
        in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + "."):
            if not is_pkg:
                command_module = __import__(command_name, fromlist=["devnull"])
                cls_members = inspect.getmembers(command_module, inspect.isclass)
                for cls in cls_members:
                    if _issubclass(cls, Command):
                        (_, c) = cls
                        command = c()
                        command._bootstrap(
                            composer=self.composer,
                            tasks=self.tasks,
                            subparsers=self.subparsers
                        )
                        self.commands[command.alias] = command

    def _load_configured_commands(self):
        '''
        TODO
        '''
        # get configuration
        configured_commands = configs.get("commands", {})
        #  current_project = configs.current_project()
        #  project_commands = {}
        #  if current_project:
            #  project_commands = configs.project_configs(current_project).get("commands", {})
        #  config_commands = mergedicts(global_commands, project_commands)
        #  config_commands = global_commands

        # build commands
        for alias, cmd in configured_commands.items():
            help_msg = (cmd[:35] + "...") if len(cmd) > 35 else cmd
            command = Command(alias=alias, help=help_msg)

            def new_process_command(self, _, c=cmd):
                cmd_args = " ".join(self.additional_args)
                self.composer.add("eval", f"{c} {cmd_args}")

            command.process_command = types.MethodType(new_process_command, command)

            command._bootstrap(composer=self.composer, subparsers=self.subparsers)
            self.commands[alias] = command
