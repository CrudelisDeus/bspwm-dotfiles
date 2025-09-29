#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: screenshot_editor.py <screenshot_path>", file=sys.stderr)
        return 2

    path = sys.argv[1]

    # If user has a preferred GUI editor, open it (no python deps)
    editor = os.environ.get("IMAGE_EDITOR")
    if editor and shutil.which(editor):
        os.execvp(editor, [editor, path])
        return 0

    # Fallback: Re-select an area over the screen and overwrite the file using maim
    # This provides a fast, dependency-light crop flow (selection first, save later)
    maim = shutil.which("maim")
    if not maim:
        print("maim is required for selection. Please install maim.", file=sys.stderr)
        return 1

    # -s: interactive selection overlay; -u: ignore compositor; -d 0: no delay
    # Overwrite the provided screenshot path with the selected area
    cmd = [maim, "-s", "-u", "-d", "0", path]
    try:
        res = subprocess.run(cmd)
    except Exception as e:
        print(f"Failed to run maim: {e}", file=sys.stderr)
        return 1

    return res.returncode


if __name__ == "__main__":
    raise SystemExit(main())


