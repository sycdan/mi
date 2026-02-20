import logging
import msvcrt
import shutil
import subprocess
import sys
from pathlib import Path

from project.workon.pick.command import Pick

logger = logging.getLogger(__name__)

PROJECTS_DIR = Path.home() / "Projects"

CLEAR = "\033[2J\033[H"
RESET = "\033[0m"
REVERSE = "\033[7m"


def _latest_commit_timestamp(repo: Path) -> int:
  try:
    result = subprocess.run(
      ["git", "log", "-1", "--format=%ct"],
      cwd=repo,
      capture_output=True,
      text=True,
      timeout=5,
    )
    ts = result.stdout.strip()
    return int(ts) if ts else 0
  except Exception:
    return 0


def _sorted_repos() -> list[Path]:
  if not PROJECTS_DIR.exists():
    logger.warning(f"Projects directory not found: {PROJECTS_DIR}")
    return []
  repos = [
    (_latest_commit_timestamp(d), d)
    for d in PROJECTS_DIR.iterdir()
    if d.is_dir() and (d / ".git").exists()
  ]
  repos.sort(reverse=True)
  logger.debug(f"Found {len(repos)} repos")
  return [d for _, d in repos]


def _pick(items: list[str]) -> str | None:
  """Run the interactive picker. Returns the chosen item or None."""
  query = ""
  cursor = 0
  offset = 0

  def filtered() -> list[str]:
    if not query:
      return items
    q = query.lower()
    return [item for item in items if q in item.lower()]

  def render():
    nonlocal cursor, offset
    cols, rows = shutil.get_terminal_size()
    results = filtered()
    max_items = rows - 2

    cursor = max(0, min(cursor, len(results) - 1))
    if cursor >= offset + max_items:
      offset = cursor - max_items + 1
    if cursor < offset:
      offset = cursor

    out = [CLEAR]
    out.append(f"> {query}\n")
    for i, item in enumerate(results[offset : offset + max_items]):
      abs_i = offset + i
      if abs_i == cursor:
        line = f"{REVERSE}  {item:<{cols - 3}}{RESET}"
      else:
        line = f"  {item}"
      out.append(line + "\n")
    sys.stdout.write("".join(out))
    sys.stdout.flush()

  render()

  while True:
    ch = msvcrt.getwch()

    if ch in ("\r", "\n"):
      results = filtered()
      sys.stdout.write(CLEAR)
      sys.stdout.flush()
      return results[cursor] if results else None

    elif ch == "\x1b":
      sys.stdout.write(CLEAR)
      sys.stdout.flush()
      return None

    elif ch == "\x03":
      sys.stdout.write(CLEAR)
      sys.stdout.flush()
      raise KeyboardInterrupt

    elif ch == "\x08":
      query = query[:-1]
      cursor = 0
      offset = 0

    elif ch in ("\x00", "\xe0"):
      ch2 = msvcrt.getwch()
      if ch2 == "H":
        cursor = max(0, cursor - 1)
      elif ch2 == "P":
        cursor = min(len(filtered()) - 1, cursor + 1)

    elif ch.isprintable():
      query += ch
      cursor = 0
      offset = 0

    render()


def handle(command: Pick) -> Pick.Result:
  logger.debug(f"Handling {command=}")
  repos = _sorted_repos()
  chosen = _pick([d.name for d in repos])
  if not chosen:
    logger.debug("No repo chosen")
    return Pick.Result()
  path = next(d for d in repos if d.name == chosen)
  logger.info(f"Chose {path.as_posix()!r}")
  return Pick.Result(path=path.as_posix())
