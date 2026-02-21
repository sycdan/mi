import logging
import shlex
import subprocess

from wsl.activate.command import Activate

logger = logging.getLogger(__name__)


def handle(command: Activate, *wsl_args: str) -> None:
  logger.info(
    f"Activating distro {command.name!r}"
    + (f" → ~/projects/{command.project}" if command.project else "")
    + (f" — running {wsl_args}" if wsl_args else "")
  )
  if wsl_args:
    if command.project:
      script = f"cd ~/projects/{shlex.quote(command.project)} && {shlex.join(wsl_args)}"
      subprocess.run(["wsl", "-d", command.name, "--", "bash", "-c", script])
    else:
      subprocess.run(["wsl", "-d", command.name, "--", *wsl_args])
  elif command.project:
    script = f"cd ~/projects/{shlex.quote(command.project)} && exec bash -i"
    subprocess.run(["wsl", "-d", command.name, "--", "bash", "-c", script])
  else:
    subprocess.run(["wsl", "-d", command.name])
