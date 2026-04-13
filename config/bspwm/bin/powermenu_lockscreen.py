#!/usr/bin/python

import subprocess
import sys
import time

from script_color import *

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
    if not run(
        [
            "i3lock",
            "-i",
            IMG,
            f"--ring-color={hex_to_i3lock(MAIN)}",
            f"--inside-color={hex_to_i3lock(COLOR_BACKGROUND)}",
            f"--ringver-color={hex_to_i3lock(COLOR_SECONDARY_TEXT)}",
            f"--insidever-color={hex_to_i3lock(COLOR_BACKGROUND)}",
            f"--verif-color={hex_to_i3lock(COLOR_FOREGROUND)}",
            f"--ringwrong-color={hex_to_i3lock(MAIN)}",
            f"--insidewrong-color={hex_to_i3lock(COLOR_BACKGROUND)}",
            f"--wrong-color={hex_to_i3lock(MAIN)}",

            f"--keyhl-color={hex_to_i3lock(COLOR_SECONDARY_TEXT)}",
            f"--bshl-color={hex_to_i3lock(COLOR_SECONDARY_TEXT)}",
        ]
    ):
        return


if __name__ == "__main__":
    main()
