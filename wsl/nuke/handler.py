import logging
import shutil
import subprocess
from pathlib import Path

from wsl.nuke.command import Nuke

logger = logging.getLogger(__name__)

INSTALL_ROOT = Path("C:/wsl")


def handle(command: Nuke) -> Nuke.Result:
  logger.debug(f"Handling {command=}")

  if not command.force:
    answer = input(f"Delete WSL distro {command.name!r}? [y/N] ").strip().lower()
    if answer != "y":
      logger.info("Cancelled")
      return Nuke.Result()

  logger.info(f"Unregistering distro {command.name!r}")
  subprocess.run(["wsl", "--unregister", command.name], check=True, timeout=30)

  install_dir = INSTALL_ROOT / command.name
  if install_dir.exists():
    logger.info(f"Removing {install_dir}")
    shutil.rmtree(install_dir)

  return Nuke.Result(distro=command.name)
