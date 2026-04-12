#!/usr/bin/env python3

import subprocess
import os
from pathlib import Path

WALLPAPER_WORKDIR = Path.home() / ".config/bspwm/wallpaper/desktop_background"


def get_file_type(path):
    ext = os.path.splitext(str(path))[1].lower()

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


def get_connected_monitors():
    result = subprocess.run(
        ["xrandr", "--query"],
        capture_output=True,
        text=True
    )

    monitors = []

    for line in result.stdout.splitlines():
        if " connected" not in line:
            continue

        parts = line.split()
        name = parts[0]

        geometry = None
        for part in parts:
            if "x" in part and "+" in part:
                # пример: 1920x1080+1200+0
                geometry = part
                break

        if geometry is None:
            continue

        resolution = geometry.split("+")[0]
        width, height = map(int, resolution.split("x"))

        rest = geometry[len(resolution):]  # +1200+0
        offsets = rest.split("+")
        x = int(offsets[1])
        y = int(offsets[2])

        monitors.append({
            "name": name,
            "geometry": geometry,
            "width": width,
            "height": height,
            "x": x,
            "y": y,
        })

    return monitors


def set_image_wallpaper(path):
    monitors = get_connected_monitors()

    if not monitors:
        subprocess.run(["feh", "--bg-fill", str(path)])
        return

    files = [str(path)] * len(monitors)

    subprocess.run(
        ["feh", "--no-fehbg", "--bg-fill", *files],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def start_video_wallpaper(path):
    stop_video_wallpaper()

    monitors = get_connected_monitors()

    if not monitors:
        return

    for monitor in monitors:
        subprocess.Popen(
            [
                "xwinwrap",
                "-g", monitor["geometry"],
                "-un",
                "-fdt",
                "-ni",
                "-b",
                "-nf",
                "--",
                "mpv",
                "--hwdec=auto",
                "--vo=x11",
                "--no-audio",
                "--no-border",
                "--no-config",
                "--no-window-dragging",
                "--no-input-default-bindings",
                "--no-osd-bar",
                "--no-sub",
                "--loop",
                "--panscan=1.0",
                "--wid=%WID",
                str(path),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


def apply_background(choice):
    if not choice:
        return

    file_type = get_file_type(choice)

    if file_type == "image":
        stop_video_wallpaper()
        set_image_wallpaper(choice)
    elif file_type == "video":
        start_video_wallpaper(choice)
    else:
        print("Not support:", choice)


def main():
    files = get_background_list()
    choice = get_default_background(files)

    if choice is None:
        print("No supported background found")
        return

    apply_background(choice)


if __name__ == "__main__":
    main()
