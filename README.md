# My CLI & dev env

## Setup

On host machine, install [scaf](http://scaf.sycdan.com) in user pacakges (it has no deps, just needs Python 3.14).

```bash
pip install git+https://github.com/sycdan/scaf
```

Clone this repo to `$HOME`:

```bash
cd ~ && git clone https://github.com/sycdan/mi.git
```

Ensure a scaf deck exists:

```bash
cd ~ && scaf init
```

### Local dev environments

Add an alias in your `~/.scaf/aliases`:

```bash
alias mi.project.workon="scaf -vv call $DECK/mi/project/workon"
```

Load a new terminal, then start working on a project:

```bash
mi.project.workon myproject
```

### Work dev environments

Install dotfiles:

```bash
source ~/mi/dotfiles/install.sh
```
