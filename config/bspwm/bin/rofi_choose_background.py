#!/usr/bin/env python3

from rofi import rofi_background_img, get_theme
from script_select_background import apply_background

img = "choose_background.png"

def main():
    choice = rofi_background_img(get_theme(img))
    apply_background(choice)

if __name__ == "__main__":
    main()
