import logging
import subprocess

from wsl.list.command import List

logger = logging.getLogger(__name__)


def handle(command: List) -> List.Result:
  result = subprocess.run(["wsl", "-l", "-q"], capture_output=True, timeout=10)
  # WSL outputs UTF-16 LE without BOM
  try:
    text = result.stdout.decode("utf-16-le")
  except UnicodeDecodeError:
    text = result.stdout.decode("utf-8", errors="replace")

  distros = [line.strip() for line in text.splitlines() if line.strip()]
  logger.debug(f"Found distros: {distros}")
  return List.Result(distros=distros)
