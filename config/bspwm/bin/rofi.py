#!/usr/bin/env python3

import subprocess
import os

def get_theme(img: str):
    powermenu_theme = rf'''
    window {{
        background-color: @bg;
        width: 800px;
        height: 300px;
        padding: 0px;
        margin: 0px;
    }}
    mainbox {{
        orientation: horizontal;
        children: [ "imagebox", "listbox" ];
        spacing: 0px;
        padding: 0px;
        margin: 0px;
    }}
    imagebox {{
        expand: false;
        width: 300px;
        padding: 3px;
        background-color: @bg-alt;
        border: 8px;
        border-color: @main;
        background-image: url("/home/dmytro/.config/bspwm/wallpaper/rofi/{img}", both);
    }}
    listbox {{
        orientation: vertical;
        children: [ "inputbar", "listview" ];
        width: 500px;
        padding: 0px;
        margin: 0px;
        border: 0px;
        background-color: @bg;
    }}
    inputbar {{
        border: 0px;
        margin: 0px;
        padding: 10px;
        spacing: 0px;
        background-color: @bg;
    }}
    prompt {{
        text-color: @main;
    }}
    textbox-prompt-colon {{
        text-color: @main;
    }}
    entry {{
        text-color: @fg;
        cursor-width: 0px;
        background-color: @bg;
    }}
    listview {{
        border: 0px;
        padding: 0px;
        spacing: 0px;
        background-color: @bg;
        scrollbar: false;
    }}
    element-text {{
        text-color: @fg;
    }}
    element normal.normal {{
        background-color: @bg;
        text-color: @fg;
    }}
    element alternate.normal {{
        background-color: @bg;
        text-color: @fg;
    }}
    element selected.normal {{
        background-color: @main;
        text-color: @fg;
    }}
    element selected.active {{
        background-color: @main;
        text-color: @fg;
    }}
    scrollbar {{
        background-color: @bg-alt;
        handle-color: @main;
    }}
    '''
    return powermenu_theme

def rofi_menu(options, theme, menu_name):
    rofi = subprocess.Popen(
        [
            "rofi",
            "-dmenu",
            "-i",
            "-p", menu_name,
            "-theme-str", theme,
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    stdout, _ = rofi.communicate("\n".join(options))
    return stdout.strip()

def rofi_launcher(theme):
    subprocess.Popen(
        [
            "rofi",
            "-show", "drun",
            "-theme-str", theme,
        ]
    )
