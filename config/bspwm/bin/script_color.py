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

# COLORS
# <==============================
MAIN = '#329DA4'
#MAIN = '#4c394e'

RESET = "\033[0m"
# <==============================


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def hex_to_fastfetch(hex_color: str) -> str:
    r, g, b = hex_to_rgb(hex_color)
    return f"38;2;{r};{g};{b}"

def change_fastfetch() -> bool:
    try:
        path = Path.home() / ".config/fastfetch/config.jsonc"
        text = path.read_text()

        ansi = hex_to_fastfetch(MAIN)

        text = re.sub(r'("keys"\s*:\s*")([^"]+)(")', rf'\g<1>{ansi}\g<3>', text)
        text = re.sub(r'("title"\s*:\s*")([^"]+)(")', rf'\g<1>{ansi}\g<3>', text)

        path.write_text(text)
        return True

    except Exception as e:
        print(f"fastfetch error: {e}")
        return False

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

    # MAIN COLOR
    if change_bspwmrc():
        print("OK: MAIN bspwmrc select color")
    else:
        print("FAILED: MAIN bspwmrc select color")

    if change_polybar():
        print("OK: MAIN polybar primary")
    else:
        print("FAILED: MAIN polybar primary")

    if change_rofi():
        print("OK: MAIN rofi color")
    else:
        print("FAILED: MAIN rofi color")

    if change_dunst():
        print("OK: MAIN dunst frame_color")
    else:
        print("FAILED: MAIN dunst frame_color")

    if change_fastfetch():
        print("OK: MAIN fastfetch colors")
    else:
        print("FAILED: MAIN fastfetch colors")

    reload_dunst()
    reload_bspwm()

if __name__ == '__main__':
    main()
