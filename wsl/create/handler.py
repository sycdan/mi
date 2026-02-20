import logging
import subprocess
from pathlib import Path

from wsl.create.command import Create

logger = logging.getLogger(__name__)

IMAGES_DIR = Path("C:/wsl-images")
INSTALL_ROOT = Path("C:/wsl")


def _latest_image() -> Path:
  tars = sorted(IMAGES_DIR.glob("*.tar"), key=lambda p: p.stat().st_mtime, reverse=True)
  if not tars:
    raise FileNotFoundError(f"No .tar images found in {IMAGES_DIR}")
  return tars[0]


def handle(command: Create) -> Create.Result:
  image = Path(command.image) if command.image else _latest_image()
  install_dir = INSTALL_ROOT / command.name
  logger.info(f"Importing {image.name} → distro={command.name!r} at {install_dir}")
  install_dir.mkdir(parents=True, exist_ok=True)

  subprocess.run(
    ["wsl", "--import", command.name, str(install_dir), str(image)],
    check=True,
    timeout=120,
  )
  logger.info(f"Created distro {command.name!r}")
  return Create.Result(distro=command.name)
