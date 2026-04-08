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

def reload_bspwm():
    subprocess.run(["bspc", "wm", "-r"])

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

    reload_bspwm()

if __name__ == '__main__':
    main()
