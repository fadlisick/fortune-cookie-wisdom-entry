"""Fortune Cookie Wisdom for Developers — make.fun entry.

The program writes one original fortune-cookie line for a software
developer to ``entry.txt`` inside the output directory the harness
provides. The line is a single sentence of 89 characters, written
with no trailing newline so the file holds exactly the line itself.
"""

import os
import sys
from pathlib import Path

# The fortune: a developer meets the code they wrote at midnight, and
# neither side remembers the other. One balanced sentence, one breath.
FORTUNE = (
    "You will meet the code you wrote at midnight, "
    "and neither of you will remember the other."
)

MAX_CHARS = 120


def output_dir() -> Path:
    """Where the harness expects the entry text."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return Path(chosen)


def check_fortune(text: str) -> None:
    """Refuse to write anything the gate would reject."""
    stripped = text.strip()
    if not stripped:
        raise ValueError("fortune is empty")
    if len(text) != len(stripped):
        raise ValueError("fortune has leading or trailing whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(f"fortune is {len(text)} chars, over the 120 limit")


def write_fortune(directory: Path) -> Path:
    """Write the line as UTF-8 bytes, no trailing newline."""
    check_fortune(FORTUNE)
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / "entry.txt"
    target.write_bytes(FORTUNE.encode("utf-8"))
    # Post-write guard: what landed on disk must be exactly the line,
    # byte for byte, with no newline or stray whitespace sneaking in.
    on_disk = target.read_bytes()
    if on_disk != FORTUNE.encode("utf-8"):
        raise ValueError("entry.txt does not match the fortune exactly")
    return target


def main() -> int:
    target = write_fortune(output_dir())
    print(f"wrote {target} ({len(FORTUNE)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
