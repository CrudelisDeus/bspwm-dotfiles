#!/usr/bin/env python

import subprocess
import os
from rofi import rofi_menu, get_theme

def current_theme():
    out = subprocess.check_output(
        ["~/.config/bspwm/bin/polybar_current_theme.py"],
        text=True,
        shell=True
    ).strip()
    return out

img = "custom_script.png"

def main():
    #theme_symb = current_theme()

    options = [
    "Run workspace",
    "Download project",
    "Check system",
    "Update system",
    f"Toggle theme",
    "System info",
    "About Author",
    ]

    choice = rofi_menu(options, get_theme(img), "Custom script")

    if choice == "Check system":
        subprocess.Popen(["kitty", "-e", "python", os.path.expanduser("~/.config/bspwm/bin/custom_script_checks.py")])
    elif choice == "Update system":
        subprocess.Popen(["kitty", "-e", "python", os.path.expanduser("~/.config/bspwm/bin/custom_script_update.py")])
    elif choice == f"Toggle theme":
        subprocess.Popen(["python", os.path.expanduser("~/.config/bspwm/bin/custom_script_change_theme_dark_or_light.py")])
    elif choice == "Run workspace":
        subprocess.Popen(["python", os.path.expanduser("/home/dmytro/.config/bspwm/bin/app_launcher_autorun.py")])
    elif choice == "System info":
        subprocess.Popen([
            "kitty", "-e", "python",
            os.path.expanduser("~/.config/bspwm/bin/custom_script_pc_info.py")
        ])
    elif choice == "About Author":
        subprocess.Popen([
            "kitty", "-e", "python",
            os.path.expanduser("~/.config/bspwm/bin/custom_script_about_author.py")
        ])
    elif choice == "Download project":
        subprocess.Popen([
            "kitty", "-e", "python",
            os.path.expanduser("~/.config/bspwm/bin/custom_script_download_project.py")
        ])





if __name__ == "__main__":
    main()
