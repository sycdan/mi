# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running commands

```bash
scaf call <action>          # run a command
scaf call <action> --help   # show args
```

This repo is the `mi` scaf deck (the working directory must be `~/mi` or a subdirectory for scaf to find it).

## Architecture

This is a [scaf](http://scaf.sycdan.com) deck — a Python CLI framework where each command is a directory package under `~/mi/`.

### Scaf action package convention

Every command lives in its own directory with three files:

| File | Purpose |
|---|---|
| `__init__.py` | Empty (marks it as a Python package) |
| `command.py` | Dataclass defining inputs and `Result` dataclass for output |
| `handler.py` | `handle(command) -> command.Result` — the logic |

Scaf parses fields of the command dataclass into CLI args via argparse. Required fields (no default) become positional args; optional fields become `--flag` args. Use `doc=` on `field()` for help text (Python 3.14+).

Call `values_must_fit(self)` in `__post_init__` when using scaf fitters (see `scaf.rules`).

### Self-executing commands

A command dataclass can define an `execute()` method that defers the handler import to avoid circular imports:

```python
def execute(self) -> "MyCommand.Result":
    from my.command.handler import handle
    return handle(self)
```

This lets callers do `MyCommand().execute()` without importing the handler directly.

### Logging

All handlers use `logger = logging.getLogger(__name__)`. Scaf exposes log output via `-v` / `-vv` / `-vvv` flags on `scaf call`.

### Output

`scaf call` JSON-serializes whatever `handle()` returns (via `scaf.output.print_result`). Handlers that want plain stdout output (not JSON) should `print()` directly and return `None`.

### Current commands

**`project/`**
- `project/workon [name] [--create]` — full dev environment flow: pick repo → find/create WSL distro → activate
  - optional `name` arg: auto-selects if exactly one repo matches, fails if ambiguous
  - `--create`: initialises `~/Projects/<name>` as a new git repo if no match found
  - `project/workon/pick [--query QUERY]` — interactive TUI repo picker (msvcrt + ANSI, no deps); with `--query`, auto-selects single match or raises; returns `Pick.Result(path=...)`

**`wsl/`** — WSL distro management; install dirs live under `C:/wsl/<name>/`, images under `C:/wsl-images/*.tar`
- `wsl/list` — list installed distros; returns `List.Result(distros=[...])`
- `wsl/find <origin>` — find a distro whose `~/projects/*/` has any remote pointing to the given Windows path; returns `Find.Result(distro=...)`
- `wsl/create <name> [--origin WIN_PATH] [--image PATH]` — `wsl --import` then clones the Windows repo into `~/projects/<name>`; raises if distro already exists
- `wsl/activate <name> [--project PROJECT]` — launch interactive shell; if `--project` given, starts in `~/projects/<project>`
- `wsl/nuke <name> [--force]` — unregister distro and remove its install dir; prompts for confirmation unless `--force`

#### WSL notes
- `wsl -l -q` outputs UTF-16 LE without BOM — decode with `utf-16-le`.
- WSL drops extra positional args passed after `bash -c 'script'`, so embed dynamic values directly in the script using `shlex.quote()`.
- MINGW (Git Bash) expands absolute POSIX paths (`/mnt/c/...`) to Windows paths at shell level. To avoid mangling, pass Windows paths (`C:/...`) through Python and convert inside WSL using `wslpath`.
- Always export a full `PATH` in non-interactive bash scripts: `export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin` so that `git` and `wslpath` are found.
- In `wsl/find`, the origin is a Windows path; the bash script calls `wslpath` to get the WSL form, then checks all remotes via `git remote -v | grep -qF`.

## Dotfiles

`dotfiles/install.sh` copies git and tmux configs into `~`. After running it, set the email address in `~/.gitconfig` for company environments.
