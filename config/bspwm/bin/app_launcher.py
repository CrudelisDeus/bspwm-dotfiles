#!/usr/bin/env python3

import subprocess
import os

# bspc rule -a firefox desktop='^6' follow=off -o && firefox "https://google.com" &

import subprocess

def open_link_in_browser(link: str, desktop: str) -> None:
    subprocess.run(
        [
            "bspc",
            "rule",
            "-a",
            "firefox",
            f"desktop=^{desktop}",
            "follow=off",
            "-o",
        ],
        check=True,
    )

    subprocess.Popen(
        ["firefox", "--new-window", link],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def open_on_desktop(app_class: str, command: list[str], desktop: str, rules_count: int = 1) -> None:
    for _ in range(rules_count):
        subprocess.run(
            [
                "bspc",
                "rule",
                "-a",
                app_class,
                f"desktop=^{desktop}",
                "follow=off",
                "-o",
            ],
            check=True,
        )

    subprocess.Popen(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

if __name__ == '__main__':
    open_on_desktop("obsidian", ["obsidian"], "4")
    open_link_in_browser('https://chatgpt.com/', "5")
    open_on_desktop("TelegramDesktop", ["Telegram"], "6")
    open_link_in_browser('https://music.youtube.com', "6")
    open_on_desktop("discord", ["discord"], "6", rules_count=2)
