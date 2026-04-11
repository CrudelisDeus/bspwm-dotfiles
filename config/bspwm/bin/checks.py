import subprocess
import os

process_list = [
    'bspwm',
    'sxhkd',
    'dunst',
    'picom',
    'polybar',
    'greenclip',
    'pipewire',
    'pipewire-pulse',
    'wireplumber'
]

env_list = [
    {
        "name": "dbus",
        "var": "DBUS_SESSION_BUS_ADDRESS"
    }
]

def check_process(process: str) -> bool:
    result = subprocess.run(
        ['pgrep', '-x', process],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return result.returncode == 0

def check_env(var: str) -> bool:
    return bool(os.environ.get(var))

def check_process_list() -> None:
    for p in process_list:
        status = f"OK" if check_process(p) else f"FAIL"
        print(f'process {status}: {p}')

def check_env_list() -> None:
    for e in env_list:
        status = "OK" if check_env(e["var"]) else "FAIL"
        print(f'env {status}: {e["name"]}')

def main() -> None:
    check_process_list()
    check_env_list()

    input("\nPress Enter to exit...")

if __name__ == '__main__':
    main()
