#!/usr/bin/env python3

import time
from app_launcher import open_on_desktop, open_link_in_browser


def main(actions, delay: float = 1.0):
    for action in actions:
        action()
        time.sleep(delay)


if __name__ == '__main__':
    actions = [
        lambda: open_on_desktop("obsidian", ["obsidian"], "4"),
        lambda: open_link_in_browser("https://chatgpt.com/", "5"),
        lambda: open_on_desktop("TelegramDesktop", ["Telegram"], "6"),
        lambda: open_link_in_browser("https://music.youtube.com", "6"),
        lambda: open_on_desktop("discord", ["discord"], "6", rules_count=2),
    ]

    main(actions, 2)
