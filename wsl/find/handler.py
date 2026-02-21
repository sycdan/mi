import logging
import subprocess

from wsl.find.command import Find
from wsl.list.command import List

logger = logging.getLogger(__name__)


def _wsl(distro: str, *cmd: str, timeout: int = 10) -> subprocess.CompletedProcess:
  return subprocess.run(
    ["wsl", "-d", distro, "--", *cmd],
    capture_output=True,
    text=True,
    timeout=timeout,
  )


def _distro_has_origin(distro: str, wsl_path: str) -> bool:
  try:
    home = _wsl(distro, "bash", "-c", "echo $HOME").stdout.strip()
    if not home:
      return False
    dirs = _wsl(
      distro,
      "find",
      f"{home}/projects",
      "-maxdepth",
      "1",
      "-mindepth",
      "1",
      "-type",
      "d",
    ).stdout.splitlines()
    for d in dirs:
      remotes = _wsl(distro, "git", "-C", d, "remote", "-v").stdout
      if wsl_path in remotes:
        return True
  except Exception as e:
    logger.debug(f"{distro}: check failed: {e}")
  return False


def handle(command: Find) -> Find.Result:
  logger.debug(f"Searching for origin {command.origin!r}")
  from wsl.path.get.query import Get

  wsl_path = Get(win_path=command.origin).execute().wsl_path
  if not wsl_path:
    logger.warning(f"Could not convert {command.origin!r} to a WSL path")
    return Find.Result()
  logger.debug(f"WSL path: {wsl_path!r}")

  distros = List().execute().distros
  logger.info(f"Checking {len(distros)} distros: {distros}")
  for distro in distros:
    logger.debug(f"Checking {distro}")
    if _distro_has_origin(distro, wsl_path):
      logger.info(f"Found match: {distro}")
      return Find.Result(distro=distro)
  logger.info("No matching distro found")
  return Find.Result()
