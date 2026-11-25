"""make.fun entry: Dear Human, the AI Breakup Line.

Reads entry.txt next to this file and copies it byte-identical to
$MAKEFUN_OUTPUT_DIR/entry.txt with mode 0644. No temp file.
"""

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.txt"


def main() -> int:
    """Copy entry.txt byte-identical to the output dir. Returns 0 on success."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    try:
        data = SRC.read_bytes()
    except OSError as exc:
        print(f"cannot read {SRC}: {exc}", file=sys.stderr)
        return 1
    if not data.strip():
        print("entry.txt is empty or whitespace-only", file=sys.stderr)
        return 1
    if len(data.decode("utf-8", errors="strict").rstrip("\n")) > 200:
        print("entry.txt exceeds 200 characters", file=sys.stderr)
        return 1
    dest = Path(out_dir) / "entry.txt"
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        with open(dest, "wb") as f:
            f.write(data)
        os.chmod(dest, 0o644)
    except OSError as exc:
        print(f"cannot write {dest}: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
