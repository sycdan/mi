# My CLI & dev env

## Setup

Clone to `$HOME`:

```bash
cd ~ && git clone https://github.com/sycdan/mi.git
```

Install dotfiles:

```bash
source ~/mi/dotfiles/install.sh
```

<!-- ## Hooks - disabled for now

To register the hooks for all repos:

```bash
git config --global core.hooksPath ~/mi/dotfiles/git/hooks
```

To register them for only one, run the same command just without the `--global` part, from within a repo folder.

Make the scripts executable:

```bash
chmod +x ~/mi/dotfiles/git/hooks/pre-commit
```

## Formatting

Any staged files will be formatted based on their extension:

- `.cs` - [CSharpier](https://csharpier.com/docs/Configuration)
- `.py` - [Ruff](https://pypi.org/project/ruff/#configuration)

Formatting can be disabled for specific file extensions by adding them to an environment variable:

```bash
export GIT__HOOKS__SKIPFORMAT=cs,py
```
-->
