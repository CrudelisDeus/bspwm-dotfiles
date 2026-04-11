#!/usr/bin/env python3

import subprocess
import os
from rofi import rofi_menu, get_theme

img = "powermenu.png"

options = [
    "Screen lock",
    "Logout",
    "Shutdown",
    "Reboot"
]

def main():
    choice = rofi_menu(options, get_theme(img), "Power")

    if choice == "Screen lock":
        subprocess.Popen(["python", os.path.expanduser("~/.config/bspwm/bin/powermenu_lockscreen.py")])

    elif choice == "Logout":
        subprocess.run(["loginctl", "terminate-session", os.environ.get("XDG_SESSION_ID", "")])

    elif choice == "Shutdown":
        subprocess.run(["systemctl", "poweroff"])

    elif choice == "Reboot":
        subprocess.run(["systemctl", "reboot"])


if __name__ == "__main__":
    main()
