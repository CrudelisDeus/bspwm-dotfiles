#!/usr/bin/env python3

# Wallpaper manager for bspwm (image + video support)
# Automatically selects default background (main* or first available)
# Applies images via feh and videos via xwinwrap + mpv (multi-monitor aware)

import subprocess
import os
import time
import random
from pathlib import Path


def load_config():
    conf_file = Path.home() / ".config/bspwm/conf/wallpaper.txt"

    default = """# AUTO_WALLPAPER:
# true  - enable auto change loop
# false - set wallpaper once
AUTO_WALLPAPER=false

# USE_ONLY_VIDEOS:
# true  - only videos
USE_ONLY_VIDEOS=false

# USE_ONLY_IMAGES:
# true  - only images
USE_ONLY_IMAGES=true

# WALLPAPER_INTERVAL_MINUTES:
# interval in minutes
WALLPAPER_INTERVAL_MINUTES=10

# WALLPAPER_RANDOM:
# true  - random loop
# false - queue loop
WALLPAPER_RANDOM=false
"""

    conf_file.parent.mkdir(parents=True, exist_ok=True)
    if not conf_file.exists():
        conf_file.write_text(default)

    AUTO_WALLPAPER = False
    USE_ONLY_VIDEOS = False
    USE_ONLY_IMAGES = True
    WALLPAPER_INTERVAL_MINUTES = 10
    WALLPAPER_RANDOM = False

    for line in conf_file.read_text().splitlines():
        if "=" not in line:
            continue

        k, v = line.strip().split("=", 1)
        v = v.strip().lower()

        if k == "AUTO_WALLPAPER":
            AUTO_WALLPAPER = v in ("true", "1", "yes")
        elif k == "USE_ONLY_VIDEOS":
            USE_ONLY_VIDEOS = v in ("true", "1", "yes")
        elif k == "USE_ONLY_IMAGES":
            USE_ONLY_IMAGES = v in ("true", "1", "yes")
        elif k == "WALLPAPER_INTERVAL_MINUTES":
            try:
                WALLPAPER_INTERVAL_MINUTES = max(1, int(v))
            except:
                pass
        elif k == "WALLPAPER_RANDOM":
            WALLPAPER_RANDOM = v in ("true", "1", "yes")

    if USE_ONLY_VIDEOS and USE_ONLY_IMAGES:
        USE_ONLY_VIDEOS = False
        USE_ONLY_IMAGES = False

    return (
        AUTO_WALLPAPER,
        USE_ONLY_VIDEOS,
        USE_ONLY_IMAGES,
        WALLPAPER_INTERVAL_MINUTES,
        WALLPAPER_RANDOM,
    )


WALLPAPER_WORKDIR = Path.home() / ".config/bspwm/wallpaper/desktop_background"


def get_file_type(path):
    ext = os.path.splitext(str(path))[1].lower()

    images = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"}
    videos = {".mp4", ".mkv", ".webm"}

    if ext in images:
        return "image"
    elif ext in videos:
        return "video"
    return "other"


def get_background_list():
    if not WALLPAPER_WORKDIR.exists():
        return []

    return sorted(
        [p for p in WALLPAPER_WORKDIR.iterdir() if p.is_file()],
        key=lambda p: p.name.lower()
    )


def get_filtered_backgrounds(files, use_only_videos, use_only_images):
    result = []

    for file in files:
        t = get_file_type(file)

        if use_only_videos and t != "video":
            continue
        if use_only_images and t != "image":
            continue

        if t in {"image", "video"}:
            result.append(file)

    return result


def get_default_background(files):
    for f in files:
        if f.stem.lower().startswith("main") and get_file_type(f) in {"image", "video"}:
            return f

    for f in files:
        if get_file_type(f) in {"image", "video"}:
            return f

    return None


def stop_video_wallpaper():
    subprocess.run(["killall", "xwinwrap"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["killall", "mpv"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def get_connected_monitors():
    result = subprocess.run(["xrandr", "--query"], capture_output=True, text=True)

    monitors = []

    for line in result.stdout.splitlines():
        if " connected" not in line:
            continue

        parts = line.split()
        name = parts[0]

        geometry = next((p for p in parts if "x" in p and "+" in p), None)
        if not geometry:
            continue

        resolution = geometry.split("+")[0]
        w, h = map(int, resolution.split("x"))

        rest = geometry[len(resolution):]
        off = rest.split("+")
        x = int(off[1])
        y = int(off[2])

        monitors.append({
            "name": name,
            "geometry": geometry,
            "width": w,
            "height": h,
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

    for m in get_connected_monitors():
        subprocess.Popen([
            "xwinwrap", "-g", m["geometry"], "-un", "-fdt", "-ni", "-b", "-nf", "--",
            "mpv",
            "--hwdec=auto",
            "--vo=x11",
            "--no-audio",
            "--loop",
            "--wid=%WID",
            str(path)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def apply_background(choice):
    if not choice:
        return

    if get_file_type(choice) == "image":
        stop_video_wallpaper()
        set_image_wallpaper(choice)
    elif get_file_type(choice) == "video":
        start_video_wallpaper(choice)


def main():
    AUTO_WALLPAPER, USE_ONLY_VIDEOS, USE_ONLY_IMAGES, INTERVAL, RANDOM_MODE = load_config()

    files = get_filtered_backgrounds(
        get_background_list(),
        USE_ONLY_VIDEOS,
        USE_ONLY_IMAGES
    )

    if not files:
        print("No wallpapers")
        return

    # --- one ---
    if not AUTO_WALLPAPER:
        apply_background(get_default_background(files))
        return

    # --- auto ---
    if RANDOM_MODE:
        last = None

        while True:
            available = [f for f in files if f != last] or files
            choice = random.choice(available)
            apply_background(choice)
            last = choice
            time.sleep(INTERVAL * 60)

    else:
        pool = files[:]
        random.shuffle(pool)

        while True:
            if not pool:
                pool = files[:]
                random.shuffle(pool)

            choice = pool.pop(0)
            apply_background(choice)
            time.sleep(INTERVAL * 60)


if __name__ == "__main__":
    main()
