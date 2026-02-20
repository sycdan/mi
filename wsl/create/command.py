from dataclasses import dataclass, field
from pathlib import Path

from scaf.rules import values_must_fit


@dataclass
class Create:
  """Create a new WSL distro for a project via wsl --import."""

  name: str = field(doc="Distro name (typically the repo/project name)")
  origin: str = field(default="", doc="Git remote URL to clone into ~/projects/<name> after import")
  image: str = field(
    default="",
    doc="Path to the .tar image; auto-detects latest in C:/wsl-images/ if omitted",
  )

  def __post_init__(self):
    values_must_fit(self)

  @dataclass
  class Result:
    distro: str = field(default="", doc="Name of the created distro")

  def execute(self) -> "Create.Result":
    from wsl.create.handler import handle

    return handle(self)
