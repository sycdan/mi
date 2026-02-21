from dataclasses import dataclass, field

from scaf.rules import values_must_fit


@dataclass
class Nuke:
  """Unregister a WSL distro and remove its install directory."""

  name: str = field(doc="Distro name to delete")
  force: bool = field(default=False, doc="Skip confirmation prompt")

  def __post_init__(self):
    values_must_fit(self)

  @dataclass
  class Result:
    distro: str = field(default="", doc="Name of the deleted distro, or empty if cancelled")

  def execute(self) -> "Nuke.Result":
    from wsl.nuke.handler import handle

    return handle(self)
