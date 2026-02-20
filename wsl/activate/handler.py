import logging
import shlex
import subprocess

from wsl.activate.command import Activate

logger = logging.getLogger(__name__)


def handle(command: Activate) -> None:
  logger.info(f"Activating distro {command.name!r}" + (f" → ~/projects/{command.project}" if command.project else ""))
  if command.project:
    script = f"cd ~/projects/{shlex.quote(command.project)} && exec bash -i"
    subprocess.run(["wsl", "-d", command.name, "--", "bash", "-c", script])
  else:
    subprocess.run(["wsl", "-d", command.name])
