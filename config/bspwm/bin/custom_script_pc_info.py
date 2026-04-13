#!/usr/bin/python

import subprocess
from custom_script_about_author import print_image
from pathlib import Path
from script_color import c
import getpass
import re

IMAGE_PATH = Path.home() / ".config" / "bspwm" / "wallpaper" / "rofi" / "custom_script_pc_info.png"

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")

def visible_len(text: str) -> int:
    return len(ANSI_RE.sub("", text))

def print_under_image(text: str, image_width=40):
    for line in text.splitlines():
        pad = max((image_width - visible_len(line)) // 2, 0)
        print(" " * pad + line)

def print_info():
    subprocess.run(["fastfetch", "--logo", "none"])

def main() -> None:
    print_image(IMAGE_PATH)
    username = getpass.getuser()

    print_under_image(f"{c('karakurtOS')}\nWelcome,{username}")
    print_info()

    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
