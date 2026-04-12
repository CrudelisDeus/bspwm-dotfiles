#!/usr/bin/python

import subprocess

def print_info():
    subprocess.run(['fastfetch', '--logo', 'none'])

def main() -> None:
    print_info()

    input("\nPress Enter to exit...")

if __name__ == '__main__':
    main()
