#!/usr/bin/env python3

import subprocess
from custom_script_about_author import print_image
from pathlib import Path
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


def load_main_color() -> str | None:
    conf_file = Path.home() / ".config" / "bspwm" / "conf" / "color.txt"

    if not conf_file.exists():
        return None

    for line in conf_file.read_text().splitlines():
        if "=" not in line:
            continue

        key, value = line.strip().split("=", 1)

        if key.strip() == "MAIN":
            value = value.strip()
            return value if value else None

    return None


def c(text: str, color: str | None) -> str:
    if not color or not color.startswith("#") or len(color) != 7:
        return text

    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)

    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"


def print_info():
    subprocess.run(["fastfetch", "--logo", "none"])


def main() -> None:
    main_color = load_main_color()
    username = getpass.getuser()

    print_image(IMAGE_PATH)
    print_under_image(f"{c('karakurtOS', main_color)}\nWelcome,{username}")
    print_info()

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
