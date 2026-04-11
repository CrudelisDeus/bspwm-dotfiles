#!/usr/bin/env python3

import subprocess
import os
from rofi import rofi_launcher, get_theme

img = "app.png"


def main():
    choice = rofi_launcher(get_theme(img))

if __name__ == "__main__":
    main()
