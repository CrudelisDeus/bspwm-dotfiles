#!/usr/bin/env python3

import subprocess
import os
from rofi import rofi_buffer, get_theme

img = "buffer.png"

def main():
    choice = rofi_buffer(get_theme(img))

if __name__ == "__main__":
    main()
