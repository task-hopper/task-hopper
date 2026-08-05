# Task Hopper v2 — Current Status & Todo List

## Repos

- **Core**: `task-hopper` (branch: `v2-start`)
- **Warren carrot**: `task-hopper-warren` (local, at `/home/jtcrank/Repos/personal/task-hopper-warren`)

---

## What's Built

### Core (`task-hopper`)

- `hop/core/directives.py` — TASK, MESSAGE, WARNING, ERROR constants
- `hop/core/composer.py` + `hop/composer.py` — singleton, atexit flush
- `hop/core/config.py` + `hop/config.py` — `configs.get()` (deep-merged `~/.hoprc` + `.hop`), `configs.carrot_configs(name)`
- `hop/core/render.py` — Rich markup → ANSI string helper
- `hop/core/prompt.py` — questionary wrappers via `/dev/tty` (`ask`, `confirm`, `select`, `path`)
- `hop/core/commands.py` — `register_command(app, name, shell_cmd, panel=None)` helper
- `hop/core/logo.py` — ASCII rabbit logo
- `hop/sdk.py` — public carrot SDK: `composer`, `directives`, `render`, `register_command`, `ask`, `confirm`, `select`, `path`
- `hop/carrot/manifest.py` — Pydantic `CarrotManifest` / `CarrotMeta`
- `hop/carrot/registry.py` — command collision guard singleton
- `hop/carrot/loader.py` — discovers carrots, adds to `sys.path`, calls `module.register(app)` via `importlib.import_module`
- `hop/carrot/resolver.py` — parses LOCAL / GITHUB / URL / OFFICIAL carrot sources
- `hop/carrot/manager.py` — install / remove / list carrot management
- `hop/commands/carrot/scaffold.py` — interactive wizard (`hop carrot scaffold`)
- `hop/commands/carrot/__init__.py` — `hop carrot` sub-app
- `hop/commands/init.py` — `hop init` stub
- `hop/__main__.py` — load order: globals first (`_load_configured_commands`), then carrots (`load_carrots`) — carrots win on collision; implicit order by position in `carrots:` list in hoprc
- `hop/ext/hop.sh.example` — shell wrapper; output captured then fed via here-string so `cd` works in current shell; Typer native bash completion wired up

### Warren carrot (`task-hopper-warren`)

- `warren/config.py` — `get_projects()`, `project_configs()`, `current_project()`, `current_env()`
- `warren/env_manager.py` — `load_env(alias, env_name)`, `unload_env(alias)`; values single-quoted in export directives
- `commands/to.py` — `hop to <alias> [-d]`; unloads current env, cds, autoloads env, runs autorun
- `commands/env.py` — `hop env [name] [-u] [-a] [-l]`; validates env name; tab-completes per-project envs
- `commands/projects/__init__.py` — `hop projects` Typer sub-app
- `commands/projects/list.py` — `hop projects list`; Rich table with active marker and env column
- `commands/projects/current.py` — `hop projects current`
- `commands/project_commands.py` — registers current project's `commands:` onto the app under a `"<Project Name> Commands"` rich_help_panel
- `carrot.toml` — commands: `to`, `env`, `projects`, `project-commands`

### `~/.hoprc` schema (warren-owned keys)

```yaml
carrots:
  - path:/absolute/path/to/carrot   # local carrot
  # future: user/repo (github), https://... (url), name (official)

warren:
  projects:
    <alias>:
      name: Human Name
      path: ~/path/to/project
      autorun:
        - git pull
      commands:
        serve: uv run pserve app_dev.ini --reload
      env:
        default:
          KEY: value           # loaded with every env
        <env-name>:
          KEY: value           # loaded for this env only
        autoload: <env-name>   # auto-loaded on `hop to`

commands:
  <alias>: shell command       # global command shortcuts
```

---

## Key Design Decisions

- **Directive protocol**: single-line `__hop_task__:cmd`, `__hop_message__:text` etc. — Python outputs, shell evals
- **Shell wrapper**: captures output first, feeds via here-string so `cd`/`export` run in current shell context (not subshell)
- **Carrot imports**: use `importlib.import_module(module_path)` — works for files and packages once `carrot_dir` is on `sys.path`; no `spec_from_file_location` needed
- **SDK convention**: carrot devs import from `hop.sdk` only; directives accessed as `directives.MESSAGE` etc.
- **Load order**: globals first, carrots last — carrots win on collision; order within carrots implicit by `carrots:` list position
- **Project commands panel**: shown under `"<Project Name> Commands"` section in `hop -h` via `rich_help_panel`
- **HOP_WARREN_ENV**: single env var tracks current warren environment (not per-project)
- **`project-commands` in carrot.toml**: registers behavior without being a direct user command — worth revisiting (possible `[hooks]` or `[modules]` section in future)
- **No `hop update`**: `uv tool upgrade task-hopper` is the upgrade path; document it rather than wrapping it

---

## Todo List

### 1. Installer ✓
- `install.sh` — isolated venv at `~/.hop/venv`, absolute-path shim at `~/.local/bin/hop`, idempotent rc injection, `--dev` flag for editable installs
- Shell wrapper (`~/.hop/hop.sh`) generated with hardcoded `HOP_BIN` to avoid `command -v hop` resolving to the shell function
- `add_completion=False` on Typer app — completion handled by wrapper
- Startup guard with branching messages for 3 broken scenarios (no shell wrapper / wrong venv / both)
- `hop doctor` — grouped checks for install health, config health, and per-carrot health
- Published to PyPI as `task-hopper 2.0.0`; `curl | bash` install path verified end to end

### 2. Plugin management

**Design decisions:**
- No official index — carrots are installed via config, vimplug-style
- Two config forms: `org/repo` (GitHub) or `path:` (local); version pinning via `org/repo@vX.Y.Z`
- No `hop carrot add` / `hop carrot remove` — installing is editing `~/.hoprc` then running `hop carrot install`
- Warren will live at `task-hopper/warren` (rename from `task-hopper-warren`)
- Recommended carrots documented in README/docs, no central registry

**Commands to implement:**
- `hop carrot install` — clone/pull all carrots in config that aren't already installed
- `hop carrot update` — update all non-pinned carrots; pinned only updates if not already at pinned version
- `hop carrot update <name>` — update a single carrot by repo name (e.g. `hop carrot update warren`); if multiple installed carrots share the name, prompt user to specify `org/repo`
- `hop carrot list` — list installed carrots; `-v` / `--verbose` for version and other details
- `hop carrot scaffold` — already exists, no changes needed

**Deferred:**
- `hop carrot check` — not enough signal it's needed yet
- Command aliasing / conflict resolution — revisit if conflicts become a real problem
- Developer carrot health check — defer, scaffold covers the immediate need

**To do before next release:**
- Rename `task-hopper-warren` repo to `task-hopper/warren`
- Update warren references in README and docs

### 3. Carrot protocol cleanup
- Revisit `project-commands` entry in `carrot.toml` — modules that register behavior without being direct commands may warrant a separate `[hooks]` or `[modules]` section
- Decide Jinja2 templating scope in config — should any top-level key be referenceable as a template variable, or should there be a dedicated `variables:` section?
- Carrot config lives as a flat top-level key matching the carrot name (e.g. `warren:`) — revisit if this causes confusion as more carrots are added

### 4. Documentation
- Core `README.md` — installation instructions, quick start
- `docs/` folder for GitHub navigation (markdown files per topic)
- SDK reference for carrot developers
- Consider VitePress for a proper docs site (not immediate)

### 5. Debug tooling
- `hopd debug command-loading` — show what commands registered, what overrode what, from which carrot/config
- `hopd debug config-loading` — show merged config and where each key came from
- Enabled via `HOP_DEBUG=1` env var set by `hopd`

### 6. Deferred warren commands
- `hop init` — append new project entry to `~/.hoprc`
- `hop edit [alias]` — open project `.hop` or global `~/.hoprc` in `$EDITOR`
- `hop projects current -n` / `-p` flags (name and path)

### 7. CLI testing strategy
- Deferred until architecture is stable; design separately
