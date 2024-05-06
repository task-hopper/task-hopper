# Task Hopper
## Description:
An extensible CLI designed to improve customized workflows.

## Installation
### 1. Clone Repo
```
git clone git@github.com:task-hopper/task-hopper.git ~/.hop/repo
```

### 2. Install TaskHopper
Add the following to your `~/.bashrc`
```
source $HOME/.hop/repo/bin/hop.bash
```

### 3. Initialize TaskHopper
Now that TaskHopper is installed, it is time to initialize the CLI. (this is a one-time command)
```
hop init
```

What does `init` do?
-  Sets up required directories (located at `~/.hop`)
-  Checks that python3 is installed and creates a virtual environment for dependencies
-  Installs python dependencies into the virtual environment

_\* You can rerun `init` to clear the existing init by passing the `-f` flag_


## Carrots
### What are carrots?
Carrots are plugins that enchance the TaskHopper CLI. They are written in python and come in two varieties:
1. __Official__ - These are plugins that have been accepted and included as part of the official TaskHopper repository.
1. __Unofficial__ - These are plugins developed by a 3rd party or yourself. ___Please use caution when using 3rd party carrots as the TaskHopper CLI has direct shell session access. Reviewing the code or using debug mode to audit the composer is highly advised.___

### How do you install a carrot?
To view the carrot registry:
```
hop carrot available
```

To install run:
```
hop carrot install <carrot_name>
```

### Official Carrots
- __Project Manager__ - This carrot is a tool for easy project navigation and interaction. _(see documentation)_
  - Features:
      - project-specific configuration and commands
      - changing to project directory via a configured project alias
      - manage environment variables

### Developer Guide
The carrot architecture was built to be as simple as simple as possible to develop on. While it is very flexible, there some strict conventions that must be followed.

#### Project Structure:
```
└── my_carrot
    ├── bin
    │   ├── python_script.py
    │   └── shell_script.sh
    ├── commands
    │   ├── __init__.py
    │   └── custom_command.py
    ├── tasks
    │   ├── __init__.py
    │   └── custom_task.py
    └── __init__.py
```
- `bin/` - This is where custom scripts used for callbacks will reside. These can be python scripts or bash scripts.
- `commands/` - Custom commands go here. You must have an `__init__.py` to ensure the module is picked up by the loader. If you define commands in subfiles, please ensure you import them in the init.
- `tasks/` - Custom tasks go here. You must have an `__init__.py` to ensure the module is picked up by the loader. If you define tasks in subfiles, please ensure you import them in the init.
- `__init__.py` (top-level) - This is where the primary Carrot class resides.
- `.carrotmeta` - This is a yaml file that holds metadata about the carrot such as the authors, version, and homepage.


#### Command
##### Class Reference
```
A class that adds a subcommand to "hop".

Attributes
----------
alias : str, required
  the subcommand to be added to hop
help : str
  the details that will be printed when using the "-h" or "--help" flags.
  default - ""
---
These attributes are bound via the loader and should not be altered or passed in.
carrot : Carrot
  the instantiated Carrot class that the command belongs to (if added via a Carrot)
parser : Parser
  the argparse parser for the command. The name is defaulted to the Command's alias.

Methods
-------
process_command(parsed_args):
  This is where the logic goes for what happens after the command is called.
  Arguments:
    parsed_args: the parsed arguments via argparse
  This will raise a NotImplementedError if not included in the class that inherits Command
setup_command():
  This is where you can use the Command's parser and customize the argparse behavior off of it.
push_task(task, *args, **kwargs):
  Arguments:
    task : str - the string representation of the task class.
  This will push a task to the composer for processing / composition.
```

Commands are what is used to add subcommands to `hop`. The Command class is built around the argparse library. Each Command child class is bootstrapped with a subparser and convenience methods to build out your own CLI command.

At minimum, you need the class to have an `__init__` method that sets an `alias` attribute (what you will type on the command line), and a `help` attribute (the displayed description when using a `-h` or `--help` command).

The class will also need to define a `process_command` method that accepts a `parsed_args` argument. This is the method that should hold the logic for what happens when the command executes. `parsed_args` is the parsed arguments that comes from the argparse library.

A minimal class could look like this:
```python
from th import Command, composer

class MyCommand(Command):
  def __init__(self):
    self.alias = "sayit"
    self.help = "It says the thing!"

  def process_command(self, parsed_args):
    composer.add("info", "Hello, World!")
```
In action:
```
> hop sayit
Hello, World!
```

If you want to further customize the commands by adding more subparsers or things such as arguments or argument groups (see argparse documentation for how to do this), you can make use of the `setup_command` method. The parser for your command is bound to an attribute via `self.parser`. If we wanted to take in a flag to replace the word "World" in the output of the minimal class example, it would look something like this:

```python
from th import Command, composer

class MyCommand(Command):
  def __init__(self):
    self.alias = "sayit"
    self.help = "It says the thing!"

  def setup_command(self):
    self.parser.add_argument("word", help="the word to say")

  def process_command(self, parsed_args):
    word = parsed_args.word
    composer.add("info", f"Hello, {word}!")
```
In action:
```
> hop sayit Friend
Hello, Friend!
```

#### Task
##### Class Reference
```
TODO

Attributes
----------
alias : str, required
  the subcommand to be added to hop
help : str
  the details that will be printed when using the "-h" or "--help" flags.
  default - ""
---
These attributes are bound via the loader and should not be altered or passed in.
carrot : Carrot
  the instantiated Carrot class that the command belongs to (if added via a Carrot)
parser : Parser
  the argparse parser for the command. The name is defaulted to the Command's alias.

Methods
-------
process_command(parsed_args):
  This is where the logic goes for what happens after the command is called.
  Arguments:
    parsed_args: the parsed arguments via argparse
  This will raise a NotImplementedError if not included in the class that inherits Command
setup_command():
  This is where you can use the Command's parser and customize the argparse behavior off of it.
push_task(task, *args, **kwargs):
  Arguments:
    task : str - the string representation of the task class.
  This will push a task to the composer for processing / composition.
```
Tasks are classes that hold repeatable logic and often add directives to the composer.



## Core Commands
### TODO
---
---
---
OLD DOCS
---
---
---

## Core Commands
#### `cd` to project's root directory and set default environment variables if configured
    hop to <project_alias>

#### Set environment variables for a given environment
    hop env <environment>
      -l: list environments configured for current project
      -v: verbosely change environment settings

#### Create default configuration for a new project
    hop init
      -d: specify directory (default: current directory)
      -n: specify project name
      -a: specify project alias, used with commands like `hop edit` and `hop to`

#### Edit configuration for an existing project
    hop edit <project_alias>
      -g: edit global configuration (~/.hoprc)

#### List configured projects
    hop list
      --no-color: print the list without color

#### Print current project details
    hop current  # with no options, this prints the project alias
      -n: print current project name
      -p: print current project path

#### Manage Carrots
    hop carrot <sub_command>
      install <repo> (installs carrot)
      update <repo> (updates specified carrot)
      ls (lists installed carrots)

## Configuration
  Configuration is done through YAML files with jinja2 templating. By default, the global configuration file is located at ~/.hoprc. Project-specific configuration can be done by creating a .hop file in the root directory of the project (specified as the path in the global config).

#### Example configuration files
##### Example ~/.hoprc
    some_variable: 123
    some_other_variable: some string value

    projects:
      one:  # this is the alias
        name: Project One
        path: ~/projects/project-one
        commands:
          run: yarn start
          number_please: echo {{some_variable}}
        env:
          default:
            ENV_VAR_A: '{{some_other_variable}}'  # need quotes because YAML will think you're trying to create a dictionary if you try to use { as the first character of a string
          local:  # this is the name that will be used with `hop env` as in `hop env local`
            ENV_VAR_B: 456
          autoload: local
      two:
        name: Project Two
        path: ~/projects/project-two
  All projects must be configured in the global configuration file and be listed under `projects:`. You must at least specify an alias, name, and path for each project in the global configuration file. Any other configuration, such as custom commands or environment settings, can be set in either the global config or a .hop file located in the path specified for the project.

##### Example .hop file
    commands:
      run: rails s -p 1234
      example-command: echo {{env.dev.VAR}}
    env:
      autoload: dev
      dev:
        VAR: var in dev environment
      prod:
        VAR: var in prod environment
  Note that in project-level .hop files, you do not need to specify the name and path.
