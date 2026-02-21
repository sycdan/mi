import logging
import shlex
import subprocess
from pathlib import Path

from wsl.create.command import Create
from wsl.list.command import List

logger = logging.getLogger(__name__)

IMAGES_DIR = Path("C:/wsl-images")
INSTALL_ROOT = Path("C:/wsl")


def _latest_image() -> Path:
  tars = sorted(IMAGES_DIR.glob("*.tar"), key=lambda p: p.stat().st_mtime, reverse=True)
  if not tars:
    raise FileNotFoundError(f"No .tar images found in {IMAGES_DIR}")
  return tars[0]


def handle(command: Create) -> Create.Result:
  existing = List().execute().distros
  if command.name in existing:
    raise ValueError(
      f"WSL distro {command.name!r} already exists — use wsl/nuke to remove it first"
    )

  image = Path(command.image) if command.image else _latest_image()
  install_dir = INSTALL_ROOT / command.name
  logger.info(f"Importing {image.name} → distro={command.name!r} at {install_dir}")
  install_dir.mkdir(parents=True, exist_ok=True)

  subprocess.run(
    ["wsl", "--import", command.name, str(install_dir), str(image)],
    check=True,
    capture_output=True,
    timeout=120,
  )
  logger.info(f"Created distro {command.name!r}")

  if command.origin:
    from wsl.path.get.query import Get

    wsl_path = Get(win_path=command.origin).execute().wsl_path
    clone_script = (
      f"mkdir -p $HOME/projects && "
      f"git clone {shlex.quote(wsl_path)} $HOME/projects/{shlex.quote(command.name)}"
    )
    logger.info(f"Cloning {command.origin!r} ({wsl_path}) into distro")
    subprocess.run(
      ["wsl", "-d", command.name, "--", "bash", "-c", clone_script],
      check=True,
      capture_output=True,
      timeout=120,
    )
    logger.info("Clone complete")

  return Create.Result(distro=command.name)
