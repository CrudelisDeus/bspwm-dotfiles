#!/usr/bin/env python3

import subprocess
import os
from rofi import rofi_menu, get_theme

img = "custom_script.png"

options = [
    "Check system",
    "Update system",
]

def main():
    choice = rofi_menu(options, get_theme(img), "Custom script")

    if choice == "Check system":
        subprocess.Popen(["kitty", "-e", "python", os.path.expanduser("~/.config/bspwm/bin/custom_script_checks.py")])
    elif choice == "Update system":
        subprocess.Popen(["kitty", "-e", "python", os.path.expanduser("~/.config/bspwm/bin/custom_script_update.py")])

if __name__ == "__main__":
    main()
