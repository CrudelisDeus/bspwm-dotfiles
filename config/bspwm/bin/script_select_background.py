#!/usr/bin/env python

import subprocess
import os
from pathlib import Path

# if WALLPAPER NAMED = "main" == set default

WALLPAPER_WORKDIR = Path.home() / ".config/bspwm/wallpaper/desktop_background"

def get_file_type(path):
    ext = os.path.splitext(path)[1].lower()

    images = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"}
    videos = {".mp4", ".mkv", ".webm"}
    
    if ext in images:
        return "image"
    elif ext in videos:
        return "video"
    else:
        return "other"

def get_background_list():
    return sorted(
        [p for p in WALLPAPER_WORKDIR.iterdir() if p.is_file()],
        key=lambda p: p.name.lower()
    )

def get_default_background(files):
    for file in files:
        if file.stem.lower().startswith("main") and get_file_type(file) == "image":
            return file

    for file in files:
        if get_file_type(file) == "image":
            return file

    return None

def main():
     files = get_background_list()
     choice = get_default_background(files)

     if choice is None:
         print("No supported background found")
         return

     if get_file_type(choice) == "image":
         subprocess.run(["feh", "--bg-fill", str(choice)])
     else:
         print("Not support:", choice)


if __name__ == "__main__":
    main()
