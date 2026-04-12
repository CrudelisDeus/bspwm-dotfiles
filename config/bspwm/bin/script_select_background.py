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
        if file.stem.lower().startswith("main") and get_file_type(file) in {"image", "video"}:
            return file

    for file in files:
        if get_file_type(file) in {"image", "video"}:
            return file

    return None

def stop_video_wallpaper():
    subprocess.run(
        ["killall", "xwinwrap"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def apply_background(choice):
    if not choice:
        return

    file_type = get_file_type(choice)

    if file_type == "image":
        stop_video_wallpaper()
        subprocess.run(["feh", "--bg-fill", str(choice)])
    elif file_type == "video":
        start_video_wallpaper(choice)
    else:
        print("Not support:", choice)

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def get_screen_geometries():
    result = subprocess.run(
        ["sh", "-c", r"xrandr | grep -Eo '[0-9]+x[0-9]+\+[0-9]+\+[0-9]+'"],
        capture_output=True,
        text=True
    )
    return result.stdout.splitlines()


def get_video_aspect(geometry):
    resolution = geometry.split("+")[0]
    width, height = map(int, resolution.split("x"))

    g = gcd(width, height)
    aspect_width = width // g
    aspect_height = height // g

    aspect = f"{aspect_width}:{aspect_height}"

    if aspect == "8:5":
        return "16:10"
    elif aspect == "4:3":
        return "4:3"
    elif aspect == "16:9":
        return "16:9"
    elif aspect == "21:9":
        return "21:9"

    return aspect

def start_video_wallpaper(path):
    stop_video_wallpaper()

    subprocess.Popen(
        [
            "xwinwrap",
            "-g", "1920x1080+0+0",
            "-un",
            "-fdt",
            "-ni",
            "-b",
            "-nf",
            "--",
            "mpv",
            "--hwdec=auto",
            "-vo", "x11",
            "--no-audio",
            "--no-border",
            "--no-config",
            "--no-window-dragging",
            "--no-input-default-bindings",
            "--no-osd-bar",
            "--no-sub",
            "--loop",
            "--wid=%WID",
            str(path),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

def main():
    files = get_background_list()
    choice = get_default_background(files)

    if choice is None:
        print("No supported background found")
        return

    file_type = get_file_type(choice)

    if file_type == "image":
        stop_video_wallpaper()
        subprocess.run(["feh", "--bg-fill", str(choice)])
    elif file_type == "video":
        start_video_wallpaper(choice)
    else:
        print("Not support:", choice)


if __name__ == "__main__":
    main()
