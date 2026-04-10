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

POWERMENU_THEME = r'''
window {
    background-color: @bg;
    width: 800px;
    height: 300px;
    padding: 0px;
    margin: 0px;
}

mainbox {
    orientation: horizontal;
    children: [ "imagebox", "listbox" ];
    spacing: 0px;
    padding: 0px;
    margin: 0px;
}

imagebox {
    expand: false;
    width: 300px;

    padding: 3px;
    background-color: @bg-alt;

    border: 8px;
    border-color: @main;

    background-image: url("/home/dmytro/.config/bspwm/wallpaper/rofi/powermenu.png", both);
}

listbox {
    orientation: vertical;
    children: [ "inputbar", "listview" ];
    width: 500px;
    padding: 0px;
    margin: 0px;
    border: 0px;
    background-color: @bg;
}

inputbar {
    border: 0px;
    margin: 0px;
    padding: 10px;
    spacing: 0px;
    background-color: @bg;
}

prompt {
    text-color: @main;
}

textbox-prompt-colon {
    text-color: @main;
}

entry {
    text-color: @fg;
    cursor-width: 0px;
    background-color: @bg;
}

listview {
    border: 0px;
    padding: 0px;
    spacing: 0px;
    background-color: @bg;
    scrollbar: false;
}

element-text {
    text-color: @fg;
}

element normal.normal {
    background-color: @bg;
    text-color: @fg;
}

element alternate.normal {
    background-color: @bg;
    text-color: @fg;
}

element selected.normal {
    background-color: @main;
    text-color: @fg;
}

element selected.active {
    background-color: @main;
    text-color: @fg;
}

scrollbar {
    background-color: @bg-alt;
    handle-color: @main;
}
'''

def eww_menu():
    subprocess.run(["eww", "update", "powermenu_choice="])
    subprocess.Popen(["eww", "open", "powermenu"])

    while True:
        result = subprocess.check_output(
            ["eww", "get", "powermenu_choice"],
            text=True
        ).strip()

        if result:
            subprocess.run(["eww", "close", "powermenu"])
            return result

def rofi_menu(options):
    rofi = subprocess.Popen(
        [
            "rofi",
            "-dmenu",
            "-i",
            "-p", "Power",
            "-theme-str", POWERMENU_THEME,
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    stdout, _ = rofi.communicate("\n".join(options))
    return stdout.strip()

def main():
    choice = rofi_menu(options)
    # choice = eww_menu()

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
