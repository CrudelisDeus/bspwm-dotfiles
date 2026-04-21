#!/usr/bin/env python3

import time
from pathlib import Path
from app_launcher import open_on_desktop, open_link_in_browser


def load_config():
    conf_file = Path.home() / ".config" / "bspwm" / "conf" / "run_workspaces.txt"

    default = """# TYPE|TARGET|DESKTOP|RULES_COUNT

app|obsidian|4|1
url|https://chatgpt.com/|5|1
app|TelegramDesktop|6|1
url|https://music.youtube.com|6|1
app|discord|6|2
"""

    conf_file.parent.mkdir(parents=True, exist_ok=True)

    if not conf_file.exists():
        conf_file.write_text(default)

    actions = []

    for line in conf_file.read_text().splitlines():
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        parts = [p.strip() for p in line.split("|")]

        if len(parts) < 3:
            continue

        action_type = parts[0]
        target = parts[1]
        desktop = parts[2]
        rules_count = 1

        if len(parts) >= 4 and parts[3]:
            try:
                rules_count = int(parts[3])
            except ValueError:
                rules_count = 1

        actions.append({
            "type": action_type,
            "target": target,
            "desktop": desktop,
            "rules_count": rules_count,
        })

    return actions


def run_actions(actions, delay: float = 1.0):
    for action in actions:
        action_type = action["type"]
        target = action["target"]
        desktop = action["desktop"]
        rules_count = action["rules_count"]

        if action_type == "app":
            open_on_desktop(target, [target], desktop, rules_count=rules_count)

        elif action_type == "url":
            open_link_in_browser(target, desktop)

        time.sleep(delay)


def main():
    actions = load_config()
    run_actions(actions, 2)


if __name__ == "__main__":
    main()
