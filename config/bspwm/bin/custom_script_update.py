#!/usr/bin/env python3

import subprocess
import shutil


def run(cmd):
    return subprocess.call(cmd)


def ask(q):
    return input(f"{q} [y/N]: ").strip().lower() in ("y", "yes")


def has(cmd):
    return shutil.which(cmd) is not None


def update_mirrors():
    if not has("reflector"):
        print("reflector not installed (skip)")
        return

    print("\nUpdating mirrors...\n")

    run([
        "sudo", "reflector",
        "--latest", "10",
        "--sort", "rate",
        "--save", "/etc/pacman.d/mirrorlist"
    ])


# --- CHECK UPDATES ---
def check_updates():
    if not has("checkupdates"):
        print("Install pacman-contrib")
        return []

    result = subprocess.run(
        ["checkupdates"],
        capture_output=True,
        text=True
    )

    return [l for l in result.stdout.splitlines() if l.strip()]


# --- UPGRADE ---
def upgrade():
    print("\nUpgrading system...\n")
    run(["sudo", "pacman", "-Syu"])


# --- MAIN FLOW ---
def main():
    # 1. mirrors
    if ask("Update mirrors?"):
        update_mirrors()

    # 2. check
    updates = check_updates()
    count = len(updates)

    print(f"\nFound {count} updates\n")

    if count > 0:
        for u in updates:
            print(u)

    # 3. upgrade
    if count > 0 and ask("\nUpgrade system?"):
        upgrade()
    else:
        print("\nDone.")


    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
