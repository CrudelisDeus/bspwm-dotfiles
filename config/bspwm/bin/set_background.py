#!/usr/bin/env python3

#   / _ \
# \_\(_)/_/  github: CrudelisDeus
#  _//o\\_   email: karakurt.deus@gmail.com
#   /   \
#
# script info: set background img

from pathlib import Path
import subprocess

def get_desktop_background() -> list: 
    """get background list"""
    path = Path.home() / ".config/bspwm/wallpaper/desktop_background"
    bkg_list = list(path.iterdir())
    return bkg_list

def set_background(bkg: list) -> None:
    """set background list"""
    subprocess.run(["feh", "--bg-fill", bkg[0]])

# start program 
def main():
    bkg_list = get_desktop_background()
    set_background(bkg_list)

if __name__ == '__main__':
    main()
