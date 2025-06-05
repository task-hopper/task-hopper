# Getting Started

## Installation
### 1. Clone the repo
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


## Validate Installation
```
> hop -h
```
Should produce the following output:

```
usage: hop [-h]  ...

positional arguments:

    carrot    perform carrot action

options:
  -h, --help  show this help message and exit
```

## What does `init` do?
-  Sets up required directories (located at `~/.hop`)
-  Checks that python3 is installed and creates a virtual environment for dependencies
-  Installs python dependencies into the virtual environment

_\* You can rerun `init` to clear the existing init by passing the `-f` flag_

---

## Sample `.hoprc`
This sample config will add an alias `test` for the command `echo 'It Works!'`
```
# ~/.hoprc
commands:
  test: echo 'It works!'
```

### Test it out

View the help:

```
> hop -h
usage: hop [-h]  ...

positional arguments:

    carrot    perform carrot action
    test      echo 'It works!'

options:
  -h, --help  show this help message and exit
```

Run the command:
```
> hop test
It works!
```

---

## Install a Carrot
### View available carrots
```
> hop carrot available
Available Carrots
-----------------

project_manager
```

### Install the Project Manager Carrot
```
> hop carrot install project_manager
```

Check for the new commands:
```
> hop -h
usage: hop [-h]  ...

positional arguments:
    carrot    perform carrot action
    test      echo 'It works!'
    current   show current project details
    list      list configured projects
    to        cd to project directory

options:
  -h, --help  show this help message and exit

```

---

__Thats it! You are ready to go! Explore the documentation to learn how to use Task Hopper to its fullest extent.__
