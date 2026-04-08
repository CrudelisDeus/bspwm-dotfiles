#!/usr/bin/python

import subprocess
import sys
import time


IMG = "/tmp/lock.png"


def run(cmd: list[str]) -> bool:
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"command failed: {cmd}", file=sys.stderr)
        print(e, file=sys.stderr)
        return False


def main() -> None:
    time.sleep(0)

    if not run(["scrot", "-o", IMG]):
        return
    if not run(["magick", IMG, "-blur", "0x8", IMG]):
        return
    if not run(["i3lock", "-i", IMG]):
        return


if __name__ == "__main__":
    main()
