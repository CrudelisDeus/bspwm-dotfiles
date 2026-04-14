#!/usr/bin/env python

from main import logo, ask_yes_no, run_step, setup_user_files
import os

def main():
    os.system("clear")
    logo()
    if not ask_yes_no("\nDo you want to paste config? (y/n): "):
        return

    run_step("Setup user files", setup_user_files)
    input("\nPress Enter...")

if __name__ == '__main__':
    main()
