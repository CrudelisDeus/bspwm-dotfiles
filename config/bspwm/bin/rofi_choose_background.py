#!/usr/bin/env python3

import subprocess
import os
from rofi import rofi_background_img, get_theme
from script_select_background import get_file_type

img = "choose_background.png"

def main():
    choice = rofi_background_img(get_theme(img))

    if not choice:
        return

    file_type = get_file_type(choice)

    if file_type == "image":
        subprocess.run(["feh", "--bg-fill", choice])
    else:
        print("Not support:", choice)

if __name__ == "__main__":
    main()
