#!/usr/bin/env python3

from pathlib import Path
import subprocess

AUTHOR_FIRST_NAME = "Dmytro"
AUTHOR_NICKNAME   = "Karakurt"
AUTHOR_GITHUB     = "https://github.com/karakurtDeus"
AUTHOR_LINKEDIN   = "https://www.linkedin.com/in/crudelisdeus"
AUTHOR_EMAIL      = "karakurt.deus@gmail.com"
AUTHOR_YOUTUBE    = "https://www.youtube.com/@karakurtDeus"

IMAGE_PATH = Path.home() / ".config" / "bspwm" / "wallpaper" / "other" / "custom_script_author.png"


def load_main_color() -> str | None:
    conf_file = Path.home() / ".config" / "bspwm" / "conf" / "color.txt"

    if not conf_file.exists():
        return None

    for line in conf_file.read_text().splitlines():
        if "=" not in line:
            continue

        key, value = line.strip().split("=", 1)

        if key.strip() == "MAIN":
            value = value.strip()
            return value if value else None

    return None


def c(text: str, color: str | None) -> str:
    if not color or not color.startswith("#") or len(color) != 7:
        return text

    try:
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
    except ValueError:
        return text

    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"


def print_image(path: Path) -> None:
    if not path.exists():
        print(f"[image not found: {path}]")
        return

    try:
        subprocess.run(
            [
                "chafa",
                str(path),
                "--size=40x20",
            ],
            check=True,
        )
    except Exception:
        print("[failed to render image]")


def main() -> None:
    main_color = load_main_color()

    message = f"""Yo! What's up?

My name is {AUTHOR_FIRST_NAME}, also known as {AUTHOR_NICKNAME}.
This is a console-like system built on top of bspwm.

The main idea is simplicity and speed:
no heavy UI layers (like eww), everything is controlled through
keybindings and minimal interfaces.

I have been working as a SecDevOps / SRE engineer for 6+ years,
and I needed a system optimized for daily work and learning.

System management is implemented in Python — clean, readable,
and easier to maintain (for me) than shell scripts.

Core structure:
  scripts:    bspwm/bin
  assets:     bspwm/wallpaper

This system is actively used by me, so it evolves constantly.
If something breaks — it gets fixed.

I’m open to ideas, improvements, and feedback.

I also plan to create YouTube content about:
  - How the system works
  - Installation
  - Linux workflows and real usage

{c("GitHub:", main_color)}   {AUTHOR_GITHUB}
{c("LinkedIn:", main_color)} {AUTHOR_LINKEDIN}
{c("Email:", main_color)}    {AUTHOR_EMAIL}
{c("YouTube:", main_color)}  {AUTHOR_YOUTUBE}"""

    print_image(IMAGE_PATH)
    print()
    print(message)
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
