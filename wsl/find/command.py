from dataclasses import dataclass, field


@dataclass
class Find:
  """Find a WSL distro that has a git repo with the given origin URL."""

  origin: str = field(doc="Git remote origin URL to search for")

  @dataclass
  class Result:
    distro: str = field(default="", doc="Matching distro name, or empty if none found")

  def execute(self) -> "Find.Result":
    from wsl.find.handler import handle

    return handle(self)
