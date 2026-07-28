# Task Hopper v1 — Reference for Rewrite

This document captures how v1 works so a new session can rewrite it from scratch without needing to read all the source files.

---

## What It Is

Task Hopper (`hop`) is a CLI tool for navigating multi-project development workflows. Its core value is `hop to <project>` — instantly cd to a project, load its env vars, and run setup commands. Everything else is supporting infrastructure.

---

## The Fundamental Constraint

Python cannot `cd` or `export` into the user's current shell — those are shell builtins. To get around this, hop uses a **deferred execution / directive model**:

1. The Python process prints structured output to stdout.
2. A shell wrapper function (`hop()` in `hop.sh`) reads that output line by line, interprets directive markers, and `eval`s the actual shell commands in the current shell context.

This means **Python never executes shell commands directly** — it only composes text that the shell will execute.

---

## Directive Protocol

Python outputs a stream of directives and payloads:

```
__hop_message__
some text to echo
__hop_task__
cd ~/projects/myproject
__hop_task__
export FOO=bar
__hop_warning__
something went wrong but continuing
__hop_error__
fatal: project not found
```

Rules:
- A directive line matches `^__hop_[A-Za-z]*__$`
- The line immediately after a directive is its payload
- `__hop_task__` → shell `eval`s the payload (enables cd/export)
- `__hop_message__` → `echo` the payload
- `__hop_warning__` → `echo` in yellow
- `__hop_error__` → `echo` in red, then exit (composer calls `sys.exit()` immediately on error)
- Multiple payloads for a single directive are emitted as separate directive+payload pairs

---

## Architecture

```
CLI args
  └─> __main__.py (argparse)
        └─> Command.process_command()
              └─> Task.stage()  [one or more]
                    └─> Composer.add()
                          └─> Composer.compose() → stdout
                                └─> hop.sh eval loop
```

### Key Singletons

- `composer` — instantiated once in `composer.py`, imported everywhere
- `configs` — instantiated once in `config_handler.py`, imported everywhere

---

## Configuration

### Files

- **`~/.hoprc`** — global config, always loaded
- **`<project_path>/.hop`** — project-specific config, loaded and deep-merged over global when a project is active

### Format

YAML with Jinja2 templating. The config is loaded, then re-rendered as a Jinja2 template with itself as context, then re-parsed as YAML. This lets you do:

```yaml
db_host: localhost
projects:
  myproject:
    env:
      dev:
        DATABASE_URL: "postgres://{{db_host}}/mydb"
```

### Schema

```yaml
# ~/.hoprc
some_variable: 123

commands:             # global custom commands (alias: shell command)
  deploy: ./deploy.sh

projects:
  <alias>:
    name: Project One
    path: ~/projects/project-one
    autorun:          # shell commands run after cd on `hop to`
      - git pull
      - nvm use
    commands:         # project-specific custom commands
      run: yarn start
      build: yarn build
    env:
      default:        # always-loaded env vars for this project
        NODE_ENV: development
      local:          # named environment, loaded via `hop env local`
        DATABASE_URL: postgres://localhost/mydb
      autoload: local # environment to auto-load on `hop to`
```

### Merge Behavior

`mergedicts()` does a deep recursive merge. Project `.hop` config overrides global config at all nesting levels. Project-level `.hop` files don't need `name` or `path`.

### How the Current Project Is Detected

`ConfigHandler.current_project()` compares `os.getcwd()` against each project's configured `path` (checking if cwd is a subdirectory). Returns the matching alias or `None`.

### How the Current Environment Is Tracked

When an env is loaded, hop exports `HOP_ENV_<PROJECT_ALIAS_UPPER>` (e.g. `HOP_ENV_MYPROJECT=dev`). `ConfigHandler.current_env()` reads this env var to know what's currently loaded.

---

## Commands

### `hop to <alias>` [-v] [-d]

1. If currently in a project, unset its env vars (`ChangeEnv action=unset`)
2. CD to destination (`CD`)
3. Load destination's autoload env (`ChangeEnv action=set env=autoload`)
4. Run autorun commands unless `-d` flag (`AutoRun`)

### `hop env <environment>` [-l] [-u] [-v]

- `-l`: list available environments for current project
- `-u`: unset current environment's vars
- default: unset current env, then set the specified env

### `hop list` [--no-color]

Prints all configured projects.

### `hop current` [-n] [-p]

Prints current project alias (default), name (`-n`), or path (`-p`).

### `hop init` [-d dir] [-n name] [-a alias] [-c]

Appends a new project entry to `~/.hoprc`. `-c` also creates a `.hop` file in the project dir.

### `hop edit [alias]` [-g]

Opens the project's `.hop` file (or global `~/.hoprc` with `-g`) in `$EDITOR`.

### Custom commands

Any `commands:` entries in `~/.hoprc` or a project's `.hop` are surfaced as top-level `hop` subcommands. They accept arbitrary extra args which are appended to the shell command string.

---

## Core Classes

### `Composer` (`hop/composer.py`)

Singleton. Collects (directive, payload) pairs and flushes them to stdout when `compose()` is called (or immediately on error).

```python
composer.add('task', 'cd ~/projects/foo')     # single payload
composer.add('task', ['export A=1', 'export B=2'])  # list of payloads
composer.add('message', 'Hopped to foo')
composer.add('warning', 'No autoload env set')
composer.add('error', 'Project not found')    # also calls compose() + sys.exit()
```

### `ConfigHandler` (`hop/config_handler.py`)

Singleton. Loads and merges YAML configs. Key methods:
- `current_project()` → alias string or None
- `current_env()` → env name string or None
- `project_configs(project_name)` → merged config dict for that project

### `HopCommand` (`hop/commands/_hop_command.py`)

Base class for all commands. Subclasses implement:
- `setup_command(subparsers)` — register argparse subparser
- `process_command(parsed_args)` — call `self.push_task(...)` to stage work

`push_task(TaskName, **kwargs)` calls `task_ref[TaskName].stage(**kwargs)`.

### `Task` (`hop/tasks/_task.py`)

Base class for all tasks. Subclasses implement `stage(**kwargs)`. Tasks hold a reference to `composer` and call `composer.add(...)` to queue directives. Tasks can be monkey-patched by carrots via `Task.patch(func)`.

---

## Task Implementations

### `CD`

Calls `composer.add('task', f'cd {path}')`. Resolves project path from config. Errors if project not found or path doesn't exist.

### `ChangeEnv`

Handles set/unset/list for environment variables.

- `action='set'`: exports `default` vars + named env vars + sets `HOP_ENV_<PROJECT>` tracking var
- `action='unset'`: unsets currently-loaded env's vars + default vars + `HOP_ENV_<PROJECT>`
- `action='list'`: messages the list of available env names (excluding `default` and `autoload` keys)
- `env='autoload'`: reads `autoload:` key from config to determine which env to load

### `AutoRun`

Iterates `project_configs.get('autorun', [])` and stages each as a `task`. With `verbose=True`, also stages a `message` for each command.

### `ListProjects`

Reads all projects from config, outputs formatted colored list via `message` directives.

### `GetProjectDetail`

Outputs current project's alias, name, or path based on `detail_type` arg.

### `InitConfig`

Appends YAML to `~/.hoprc` for a new project. Optionally creates a `.hop` file.

### `EditConfig`

Stages `$EDITOR <config_path>` as a `task` directive.

---

## Loader / Initialization (`hop/helpers/loaders.py`)

`initialize_hop(composer)` wires everything together:

1. `load_carrots(composer)` — discovers carrot packages under `~/.hop/lib/carrots/`
2. `load_tasks(composer)` — discovers all `Task` subclasses in `hop/tasks/`
3. `load_commands(composer, tasks)` — discovers all `HopCommand` subclasses in `hop/commands/`, binds composer + task_ref
4. Applies carrot task patches and adds carrot commands
5. `load_configured_commands(composer)` — reads `commands:` from config, builds dynamic `HopCommand` instances
6. Returns merged commands dict keyed by alias

Discovery uses `pkgutil.iter_modules` + `inspect.getmembers` — no explicit registration needed.

---

## Carrots (Plugin System)

Carrots live under `~/.hop/lib/carrots/<name>/`. Each carrot:
- Has a top-level class that subclasses `Carrot`
- Can contain `Task` subclasses and `HopCommand` subclasses
- Implements `patch_tasks()` returning `{TaskName: new_stage_func}` to monkey-patch core tasks

The loader discovers carrots by package structure (no manifest file in v1).

---

## Shell Integration (`hop/ext/hop.sh.example`)

The `hop()` shell function:
- Runs the Python process: `python /path/to/task-hopper/hop $@`
- Reads stdout line by line
- Recognizes directive lines by regex `^__hop_[A-Za-z]*__$`
- Dispatches: `eval` for tasks, `echo` for messages, colored `echo` for warnings/errors

Also provides:
- `hopd()` — debug mode wrapper: shows raw output first, then replays through the eval loop
- `_hop()` — bash completion function: tab-completes subcommands, project aliases for `to`, env names for `env`

---

## Known Gaps in v1

- No tests
- No package metadata (`pyproject.toml` / `setup.py`)
- `sys.path.append` hacks instead of proper packaging
- Carrots have no manifest — discovery is purely by Python package structure
- No type hints
- `hop carrot` command exists (install/update/ls subcommands) but implementation is a stub
- `hop.sh.example` has hardcoded absolute paths to the Python binary and repo — requires manual editing per install
- Shell wrapper reads one payload line per directive — multi-line payloads would break
