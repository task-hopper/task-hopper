# Task Hopper

Task Hopper is a shell-native, plugin-based CLI for working smarter in your terminal. Out of the box it works as a configurable command shortcut tool — and is extended into something more powerful through plugins called carrots. It runs commands in your current shell session — so things like `cd`, environment variables, and shell state actually take effect.

## Installation

```bash
curl -fsSL https://raw.githubusercontent.com/task-hopper/task-hopper/main/install.sh | bash
```

Then reload your shell:

```bash
source ~/.bashrc  # or ~/.zshrc
```

The installer creates an isolated venv at `~/.hop/venv`, writes a shim to `~/.local/bin/hop`, and automatically sources the shell integration into your `~/.bashrc` or `~/.zshrc`. Running the installer again is safe — it won't duplicate anything.

**Security note:** hop sources its shell integration directly into your session, and carrots can emit directives that are evaluated in your shell. Only install carrots from sources you trust.

## Usage & Configuration

After installing, run `hop -h` to see available commands. On a bare install, hop comes with a handful of built-in commands — the rest comes from carrots and your own config.

Define command shortcuts in `~/.hoprc` under `commands:`:

```yaml
# ~/.hoprc
commands:
  serve: uv run pserve app.ini --reload
  logs: tail -f /var/log/myapp.log
```

Then run them:

```bash
hop serve
hop logs
```

Values support Jinja2 templating, so you can reference other keys in your config:

```yaml
my_port: 3000

commands:
  serve: uv run pserve app.ini --port {{ my_port }}
```

## Carrots

Carrots are plugins that extend hop with new commands and functionality. A bare install of hop has no domain-specific commands — everything comes from carrots.

Carrots can be official (maintained by the task-hopper project), third-party (from GitHub or a URL), or local (a directory on your machine).

Install a carrot by adding it to your `~/.hoprc`:

```yaml
carrots:
  - path:/absolute/path/to/carrot   # local
  - github:user/repo                 # third-party
  - warren                           # official
```

Then run `hop carrot install` to clone any GitHub carrots that aren't already installed. Local (`path:`) carrots are loaded directly from disk and don't need this step.

**Official carrots:**
- [warren](https://github.com/task-hopper/task-hopper-warren) — manage development projects, navigate directories, and handle environment variables

## Building a carrot

Run `hop carrot scaffold` to generate a new carrot interactively.

A carrot is a directory with two things:

- `carrot.toml` — declares the carrot's metadata and maps command names to Python modules
- One or more Python modules, each with a `register(app)` function that adds commands to the hop CLI

Install your carrot locally by adding it to `~/.hoprc`:

```yaml
carrots:
  - path:/absolute/path/to/your-carrot
```

## Commands

### `hop init`

Create a starter `~/.hoprc` config file. Safe to run on a fresh install — does nothing if the file already exists.

```bash
hop init
```

### `hop doctor`

Diagnose your hop installation. Checks install health, config validity, and the status of each installed carrot.

```bash
hop doctor
```

### `hop carrot install`

Clone all GitHub carrots declared in `~/.hoprc` that aren't already installed.

```bash
hop carrot install
```

### `hop carrot update [name]`

Update all installed carrots. Pass a carrot name to update only that one. Pinned carrots won't update if they're already at the pinned version.

```bash
hop carrot update          # update all
hop carrot update warren   # update warren only
```

### `hop carrot list`

List installed carrots. Use `-v` / `--verbose` for version and source details.

```bash
hop carrot list
hop carrot list -v
```

### `hop carrot scaffold`

Interactively generate a new carrot. Prompts for name, description, author, location, and first command — then writes the directory structure and optionally adds it to `~/.hoprc`.

```bash
hop carrot scaffold
```

## License

MIT — see [LICENSE](LICENSE)
