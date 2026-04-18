#!/usr/bin/python

from pathlib import Path
import re
import subprocess

# COLORS
# <==============================
MAIN = '#329DA4'
#MAIN = '#4c394e'

# POLYBAR title 
COLOR_SECONDARY_TEXT = "#C5C8C6"
#COLOR_SECONDARY_TEXT = "#6B1112"

# color (TEXT)
#COLOR_FOREGROUND = "#6B1112"
COLOR_FOREGROUND = "#ffffff"

# background rofi
COLOR_BACKGROUND = "#000000"

RESET = "\033[0m"
# <==============================

def ensure_color_file() -> Path:
    conf_dir = Path.home() / ".config" / "bspwm" / "conf"
    conf_dir.mkdir(parents=True, exist_ok=True)

    color_file = conf_dir / "color.txt"

    if not color_file.exists():
        color_file.write_text(f"{MAIN}\n")

    return color_file

def get_main_color() -> str:
    try:
        path = Path.home() / ".config/bspwm/conf/color.txt"
        if path.exists():
            value = path.read_text().strip()
            if value:
                return value
    except:
        pass

    return MAIN

def hex_to_i3lock(hex_color: str) -> str:
    return hex_color.lstrip("#") + "FF"

def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def hex_to_fastfetch(hex_color: str) -> str:
    r, g, b = hex_to_rgb(hex_color)
    return f"38;2;{r};{g};{b}"

def change_fastfetch() -> bool:
    try:
        path = Path.home() / ".config/fastfetch/config.jsonc"
        text = path.read_text()

        ansi_main = hex_to_fastfetch(MAIN)
        ansi_font = hex_to_fastfetch(COLOR_FOREGROUND)

        text = re.sub(r'("keys"\s*:\s*")([^"]+)(")', rf'\g<1>{ansi_main}\g<3>', text)
        text = re.sub(r'("title"\s*:\s*")([^"]+)(")', rf'\g<1>{ansi_main}\g<3>', text)

        text = re.sub(r'("output"\s*:\s*")([^"]+)(")', rf'\g<1>{ansi_font}\g<3>', text)

        text = re.sub(r'("green"\s*:\s*")([^"]+)(")', rf'\g<1>{ansi_font}\g<3>', text)
        text = re.sub(r'("yellow"\s*:\s*")([^"]+)(")', rf'\g<1>{ansi_font}\g<3>', text)
        text = re.sub(r'("red"\s*:\s*")([^"]+)(")', rf'\g<1>{ansi_font}\g<3>', text)

        text = re.sub(r'("output"\s*:\s*")([^"]+)(")', rf'\g<1>{ansi_font}\g<3>', text)

        path.write_text(text)
        return True

    except Exception as e:
        print(f"fastfetch error: {e}")
        return False

def hex_to_ansi(hex_color: str) -> str:
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f"\033[38;2;{r};{g};{b}m"

def c(text: str) -> str:
    return f"{hex_to_ansi(MAIN)}{text}{RESET}"

def reload_bspwm():
    subprocess.run(["bspc", "wm", "-r"])

def reload_dunst():
    subprocess.run(["killall", "dunst"], stderr=subprocess.DEVNULL)
    subprocess.Popen(["dunst"])

def change_dunst() -> bool:
    # change frame color
    try:
        path = Path.home() / ".config/dunst/dunstrc"
        text = path.read_text()

        pattern = r'(frame_color\s*=\s*")(.+?)(")'

        if re.search(pattern, text):
            text = re.sub(pattern, rf'\1{MAIN}\3', text)
        else:
            text += f'\nframe_color = "{MAIN}"\n'

        path.write_text(text)
        return True

    except:
        return False

def change_rofi() -> bool:
    try:
        path = Path.home() / ".config/rofi/config.rasi"
        text = path.read_text()

        match = re.search(r'(?ms)(^\*\s*\{.*?^\})', text)
        if not match:
            return False

        block = match.group(1)

        block = re.sub(r'(?m)^(    main:\s*)(#[0-9a-fA-F]{6})(;?)$',
                       rf'\1{MAIN}\3',
                       block)

        block = re.sub(r'(?m)^(    bg:\s*)(#[0-9a-fA-F]{6})(;?)$',
                       rf'\1{COLOR_BACKGROUND}\3',
                       block)

        block = re.sub(r'(?m)^(    bg-alt:\s*)(#[0-9a-fA-F]{6})(;?)$',
                       rf'\1{COLOR_BACKGROUND}\3',
                       block)

        block = re.sub(r'(?m)^(    fg:\s*)(#[0-9a-fA-F]{6})(;?)$',
                       rf'\1{COLOR_FOREGROUND}\3',
                       block)

        block = re.sub(r'(?m)^(    secondary-text:\s*)(#[0-9a-fA-F]{6})(;?)$',
                       rf'\1{COLOR_SECONDARY_TEXT}\3',
                       block)

        text = text[:match.start(1)] + block + text[match.end(1):]

        path.write_text(text)
        return True
    except:
        return False

def change_polybar() -> bool:
    try:
        path = Path.home() / ".config/polybar/config.ini"
        text = path.read_text()

        match = re.search(r'(?ms)(^\[colors\]\n.*?)(?=^\[|\Z)', text)
        if not match:
            return False

        colors_block = match.group(1)

        colors_block = re.sub(r'(?m)^(primary\s*=\s*).*$',
                              rf'\1{MAIN}',
                              colors_block)

        colors_block = re.sub(r'(?m)^(foreground\s*=\s*).*$',
                              rf'\1{COLOR_SECONDARY_TEXT}',
                              colors_block)

        text = text[:match.start(1)] + colors_block + text[match.end(1):]

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
    ensure_color_file()

    global MAIN
    MAIN = get_main_color()
    # MAIN COLOR
    if change_bspwmrc():
        print("OK: MAIN bspwmrc select color")
    else:
        print("FAILED: MAIN bspwmrc select color")

    if change_polybar():
        print("OK: MAIN and FOREGROUND polybar primary")
    else:
        print("FAILED: MAIN and FOREGROUND polybar primary")

    if change_rofi():
        print("OK: MAIN rofi color")
    else:
        print("FAILED: MAIN rofi color")

    if change_dunst():
        print("OK: MAIN dunst frame_color")
    else:
        print("FAILED: MAIN dunst frame_color")

    if change_fastfetch():
        print("OK: MAIN and FOREGROUND fastfetch colors")
    else:
        print("FAILED: MAIN and FOREGROUND fastfetch colors")

    reload_dunst()
    reload_bspwm()

if __name__ == '__main__':
    main()
