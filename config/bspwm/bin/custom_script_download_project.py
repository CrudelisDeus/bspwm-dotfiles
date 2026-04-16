#!/usr/bin/env python3

from pathlib import Path
import subprocess

PROJECTS_DIR = "projects"
IMAGE_PATH = Path.home() / ".config" / "bspwm" / "wallpaper" / "rofi" / "custom_script_download_project.png"

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


def git_clone() -> str:
    home = Path.home()
    projects_path = home / PROJECTS_DIR

    projects_path.mkdir(exist_ok=True)

    url = input("\nEnter Git repository URL: ").strip()
    if not url:
        print("Empty URL, skip.")
        return ""

    branch = input("Enter branch (leave empty for default): ").strip()

    cmd = ["git", "clone"]

    if branch:
        cmd += ["-b", branch]

    cmd.append(url)

    try:
        subprocess.run(cmd, cwd=projects_path, check=True)
        print("Clone: OK")
        return url
    except subprocess.CalledProcessError as e:
        print("Clone failed:", e)
        return ""

def main():
    print_image(IMAGE_PATH)
    git_clone()
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
