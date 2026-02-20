from dataclasses import dataclass, field


@dataclass
class Workon:
  """Start a dev environment for a project."""

  create: bool = field(default=False, doc="Create a new repo in ~/Projects/<name> if no match is found")
