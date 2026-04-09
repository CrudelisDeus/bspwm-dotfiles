#!/usr/bin/env python3

import subprocess
import os

options = [
    "Screen lock",
    "Check system",
    "Logout",
    "Shutdown",
    "Reboot"
]

def rofi_menu(options):
    rofi = subprocess.Popen(
        ["rofi", "-dmenu", "-i", "-p", "Power"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    stdout, _ = rofi.communicate("\n".join(options))
    return stdout.strip()

def main():
    choice = rofi_menu(options)

    if choice == "Check system":
        subprocess.Popen(["kitty", "-e", "python", os.path.expanduser("~/.config/bspwm/bin/checks.py")])

    elif choice == "Screen lock":
        subprocess.Popen(["python", os.path.expanduser("~/.config/bspwm/bin/lockscreen.py")])

    elif choice == "Logout":
        subprocess.run(["loginctl", "terminate-session", os.environ.get("XDG_SESSION_ID", "")])

    elif choice == "Shutdown":
        subprocess.run(["systemctl", "poweroff"])

    elif choice == "Reboot":
        subprocess.run(["systemctl", "reboot"])


if __name__ == "__main__":
    main()
