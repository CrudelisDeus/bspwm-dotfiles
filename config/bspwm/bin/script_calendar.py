#!/usr/bin/env python3

from pathlib import Path
import re
import subprocess

COLOR_CONF = Path.home() / ".config" / "bspwm" / "conf" / "color.txt"


def load_main_color():
    if not COLOR_CONF.exists():
        return "#329DA4"

    for line in COLOR_CONF.read_text().splitlines():
        line = line.strip()
        if line.startswith("MAIN="):
            color = line.split("=", 1)[1].strip()
            if re.match(r"^#[0-9a-fA-F]{6}$", color):
                return color

    return "#329DA4"


color = load_main_color()

subprocess.Popen([
    "bash",
    "-lc",
    f'kitty --override confirm_os_window_close=0 --config <(echo "color1 {color}"; echo "color9 {color}") calcurse'
])
