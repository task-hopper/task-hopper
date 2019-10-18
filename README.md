# Task Hopper
## Description
A project management CLI that makes it easier to navigate and automate your project workflow.

## Features:
- change directories
- configurations at the global and project-specific level
- manage environment variables
- set up custom scripts and commands
- extensible via carrots, which are installable modules (think gems or eggs)
- life cycle hooks

## Core Commands:
- Go to project directory and execute lifecycle hooks

  `hop to <project_name>`
- Swap environment variables between configured environments

  `hop env <environment>`
- Project startup

  `hop start`(optional `-p <project_name`)
- New/Edit config

  `hop config` (optional `-p <project_name` for project specific configs)
- Add directory as a project and creates default config

  `hop init` (optional `-d <directory>` to specify directory)
- Manage Carrots

  `hop carrot <sub_command>`

  subcommands:
    - `install <repo>`(installs carrot)
    - `update <repo>` (updates specified carrot)
    - `ls` (lists installed carrots)
