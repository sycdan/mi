from dataclasses import dataclass, field


@dataclass
class List:
  """List installed WSL distros."""

  @dataclass
  class Result:
    distros: list[str] = field(default_factory=list, doc="Names of installed WSL distros")

  def execute(self) -> "List.Result":
    from wsl.list.handler import handle

    return handle(self)
