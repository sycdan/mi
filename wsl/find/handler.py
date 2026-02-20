import logging
import shlex
import subprocess

from wsl.find.command import Find
from wsl.list.command import List

logger = logging.getLogger(__name__)


def _distro_has_origin(distro: str, origin: str) -> bool:
  # WSL drops extra positional args, so embed origin directly via shlex.quote
  quoted = shlex.quote(origin)
  script = (
    "shopt -s nullglob; "
    "for d in ~/projects/*/; do "
    f'url=$(git -C "$d" remote get-url origin 2>/dev/null); '
    f"[ \"$url\" = {quoted} ] && echo found && break; "
    "done"
  )
  try:
    result = subprocess.run(
      ["wsl", "-d", distro, "--", "bash", "-c", script],
      capture_output=True,
      text=True,
      timeout=15,
    )
    logger.debug(f"{distro}: stdout={result.stdout.strip()!r} stderr={result.stderr.strip()!r}")
    return result.stdout.strip() == "found"
  except Exception as e:
    logger.debug(f"{distro}: check failed: {e}")
    return False


def handle(command: Find) -> Find.Result:
  logger.debug(f"Searching for origin {command.origin!r}")
  distros = List().execute().distros
  logger.info(f"Checking {len(distros)} distros: {distros}")
  for distro in distros:
    logger.debug(f"Checking {distro}")
    if _distro_has_origin(distro, command.origin):
      logger.info(f"Found match: {distro}")
      return Find.Result(distro=distro)
  logger.info("No matching distro found")
  return Find.Result()
