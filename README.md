# Task Hopper
## Description:
A project management CLI that makes it easier to navigate and automate your project workflow.

## Installation
TODO

## Features
- change directories
- configurations at the global and project-specific level
- manage environment variables
- set up custom scripts and commands
- extensible via carrots, which are installable modules (think gems or eggs)
- life cycle hooks

## Core Commands
#### `cd` to project's root directory and set default environment variables if configured
    hop to <project_alias>

#### Set environment variables for a given environment
    hop env <environment>

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
          local:
            ENV_VAR_B: 456
          autoload: local
      two:
        name: Project Two
        path: ~/projects/project-two
  All projects must be configured in the global configuration file and be listed under `projects:`. You must at least specify an alias, name, and path for each project in the global configuration file. Any other configuration, such as commands or environment variables, can be set in either the global config or a .hop file located in the path specified for the project.

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
