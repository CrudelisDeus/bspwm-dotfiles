#!/usr/bin/python

#   / _ \
# \_\(_)/_/  github: CrudelisDeus
#  _//o\\_   email: karakurt.deus@gmail.com
#   /   \
#
# script info: global change color

from pathlib import Path
import re
import subprocess

MAIN = '#329DA4'
#MAIN = '#4c394e'
RESET = "\033[0m"

def hex_to_ansi(hex_color: str) -> str:
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f"\033[38;2;{r};{g};{b}m"

def c(text: str) -> str:
    return f"{hex_to_ansi(MAIN)}{text}{RESET}"

def reload_bspwm():
    subprocess.run(["bspc", "wm", "-r"])

def reload_dunst():
    subprocess.run(["killall", "dunst"], stderr=subprocess.DEVNULL)
    subprocess.Popen(["dunst"])

def change_dunst() -> bool:
    # change frame color
    try:
        path = Path.home() / ".config/dunst/dunstrc"
        text = path.read_text()

        pattern = r'(frame_color\s*=\s*")(.+?)(")'

        if re.search(pattern, text):
            text = re.sub(pattern, rf'\1{MAIN}\3', text)
        else:
            text += f'\nframe_color = "{MAIN}"\n'

        path.write_text(text)
        return True

    except:
        return False

def change_rofi() -> bool:
    # change main color 
    try:
        path = Path.home() / ".config/rofi/config.rasi"
        text = path.read_text()

        pattern = r'(main:\s*)(#[0-9a-fA-F]{6})'
        if re.search(pattern, text):
            text = re.sub(pattern, rf'\1{MAIN}', text)
        else:
            text = '* {\n    main: ' + MAIN + ';\n}\n\n' + text

        path.write_text(text)
        return True
    except:
        return False

def change_polybar() -> bool:
    # change primary color
    try:
        path = Path.home() / ".config/polybar/config.ini"
        text = path.read_text()

        pattern = r'(primary\s*=\s*)(.+)'

        if re.search(pattern, text):
            text = re.sub(pattern, rf'\1{MAIN}', text)
        else:
            text += f'\nprimary = {MAIN}\n'

        path.write_text(text)
        return True
    except:
        return False

def change_bspwmrc() -> bool:
    # change select color
    try: 
        path = Path.home() / ".config/bspwm/bspwmrc"
        text = path.read_text()

        pattern = r'(bspc config focused_border_color\s+")(.+?)(")'

        if re.search(pattern, text):
            text = re.sub(pattern, rf'\1{MAIN}\3', text)
        else:
            text += f'\nbspc config focused_border_color "{MAIN}"\n'

        path.write_text(text)
        return True
    except:
        return False

# start program
def main():
    if change_bspwmrc():
        print("OK: bspwmrc select color")
    else:
        print("FAILED: bspwmrc select color")

    if change_polybar():
        print("OK: polybar primary")
    else:
        print("FAILED: polybar primary")

    if change_rofi():
        print("OK: rofi main color")
    else:
        print("FAILED: rofi main color")

    if change_dunst():
        print("OK: dunst frame_color")
    else:
        print("FAILED: dunst frame_color")

    reload_dunst()
    reload_bspwm()

if __name__ == '__main__':
    main()
