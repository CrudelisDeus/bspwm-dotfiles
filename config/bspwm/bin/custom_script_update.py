#!/usr/bin/env python3

from pathlib import Path
import subprocess
import shutil

IMAGE_PATH = Path.home() / ".config" / "bspwm" / "wallpaper" / "rofi" / "custom_script_update.png"


def print_image(path: Path) -> None:
    if not path.exists():
        print(f"[image not found: {path}]")
        return

    if shutil.which("chafa") is None:
        print("[chafa not installed]")
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
    except subprocess.CalledProcessError:
        print("[failed to render image]")


def run(cmd) -> int:
    return subprocess.call(cmd)


def ask(q: str) -> bool:
    return input(f"{q} [y/N]: ").strip().lower() in ("y", "yes")


def has(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def update_mirrors() -> None:
    if not has("reflector"):
        print("reflector not installed (skip)")
        return

    print("\nUpdating mirrors...\n")

    run([
        "sudo", "reflector",
        "--latest", "10",
        "--sort", "rate",
        "--save", "/etc/pacman.d/mirrorlist",
    ])


def check_repo_updates() -> list[str]:
    if not has("checkupdates"):
        print("Install pacman-contrib")
        return []

    result = subprocess.run(
        ["checkupdates"],
        capture_output=True,
        text=True,
    )

    return [line for line in result.stdout.splitlines() if line.strip()]


def check_aur_updates() -> list[str]:
    if not has("yay"):
        print("yay not installed (skip AUR check)")
        return []

    result = subprocess.run(
        ["yay", "-Qua"],
        capture_output=True,
        text=True,
    )

    return [line for line in result.stdout.splitlines() if line.strip()]


def upgrade_repo() -> None:
    print("\nUpgrading repo packages...\n")
    run(["sudo", "pacman", "-Syu"])


def upgrade_aur() -> None:
    if not has("yay"):
        print("yay not installed (skip AUR upgrade)")
        return

    print("\nUpgrading AUR packages...\n")
    run(["yay", "-Sua"])


def main() -> None:
    print_image(IMAGE_PATH)

    if ask("Update mirrors?"):
        update_mirrors()

    repo_updates = check_repo_updates()
    repo_count = len(repo_updates)

    print(f"\nFound {repo_count} repo updates\n")
    if repo_count > 0:
        for update in repo_updates:
            print(update)

    if repo_count > 0 and ask("\nUpgrade repo packages?"):
        upgrade_repo()

    aur_updates = check_aur_updates()
    aur_count = len(aur_updates)

    print(f"\nFound {aur_count} AUR updates\n")
    if aur_count > 0:
        for update in aur_updates:
            print(update)

    if aur_count > 0 and ask("\nUpgrade AUR packages?"):
        upgrade_aur()
    else:
        print("\nDone.")

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
