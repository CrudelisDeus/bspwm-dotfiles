#!/usr/bin/env python3

import subprocess
import os
from rofi import rofi_menu, get_theme

img = "custom_script.png"

options = [
    "Run workspace",
    "Check system",
    "Update system",
    "Toggle theme",
]

def main():
    choice = rofi_menu(options, get_theme(img), "Custom script")

    if choice == "Check system":
        subprocess.Popen(["kitty", "-e", "python", os.path.expanduser("~/.config/bspwm/bin/custom_script_checks.py")])
    elif choice == "Update system":
        subprocess.Popen(["kitty", "-e", "python", os.path.expanduser("~/.config/bspwm/bin/custom_script_update.py")])
    elif choice == "Toggle theme":
        subprocess.Popen(["python", os.path.expanduser("~/.config/bspwm/bin/custom_script_change_theme_dark_or_light.py")])
    elif choice == "Run workspace":
        subprocess.Popen(["python", os.path.expanduser("/home/dmytro/.config/bspwm/bin/app_launcher_autorun.py")])


if __name__ == "__main__":
    main()
