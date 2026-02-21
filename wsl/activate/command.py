from dataclasses import dataclass, field


@dataclass
class Activate:
  """Launch an interactive shell in a WSL distro."""

  name: str = field(doc="Distro name to activate")
  project: str = field(default="", doc="Project name to cd into at ~/projects/<project> on start")

  def execute(self, *wsl_args: str) -> None:
    from wsl.activate.handler import handle

    return handle(self, *wsl_args)
