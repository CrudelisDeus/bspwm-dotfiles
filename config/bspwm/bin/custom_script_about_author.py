from pathlib import Path
import subprocess

from script_color import c

AUTHOR_FIRST_NAME = "Dmytro"
AUTHOR_NICKNAME   = "Karakurt"
AUTHOR_GITHUB     = "https://github.com/karakurtDeus"
AUTHOR_LINKEDIN   = "https://www.linkedin.com/in/crudelisdeus"
AUTHOR_EMAIL      = "karakurt.deus@gmail.com"
AUTHOR_YOUTUBE    = "channel"
IMAGE_PATH = Path.home() / ".config" / "bspwm" / "wallpaper" / "other" / "custom_script_author.png"

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

{c("GitHub:")}   {AUTHOR_GITHUB}
{c("LinkedIn:")} {AUTHOR_LINKEDIN}
{c("Email:")}    {AUTHOR_EMAIL}
{c("YouTube:")}  {AUTHOR_YOUTUBE}"""

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
            check=True
        )
    except Exception:
        print("[failed to render image]")

if __name__ == "__main__":
    print_image(IMAGE_PATH)
    print()
    print(message)
    input("\nPress Enter to exit...")
