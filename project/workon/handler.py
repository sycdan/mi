import logging
import subprocess
from pathlib import Path

from project.workon.command import Workon
from project.workon.pick.command import Pick
from wsl.create.command import Create
from wsl.find.command import Find

logger = logging.getLogger(__name__)


def _get_origin(repo: Path) -> str | None:
  result = subprocess.run(
    ["git", "remote", "get-url", "origin"],
    cwd=repo,
    capture_output=True,
    text=True,
  )
  origin = result.stdout.strip() or None
  logger.debug(f"Origin for {repo.name!r}: {origin!r}")
  return origin


def handle(command: Workon) -> None:
  logger.debug(f"Handling {command=}")

  pick_result = Pick().execute()
  if not pick_result.path:
    logger.debug("No repo selected")
    return

  repo = Path(pick_result.path)
  origin = _get_origin(repo)
  if not origin:
    logger.error(f"No git remote origin found for {repo}")
    return

  logger.info(f"Finding WSL distro for {origin!r}")
  distro = Find(origin=origin).execute().distro
  if not distro:
    logger.info(f"No existing distro found, creating {repo.name!r}")
    distro = Create(name=repo.name).execute().distro

  print(distro)
