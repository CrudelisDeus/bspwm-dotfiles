#!/bin/bash

options="Screen lock\nCheck system\nLogout\nShutdown\nReboot"

chosen=$(echo -e "$options" | rofi -dmenu -i -p "Power")

case "$chosen" in
"Check system")
  kitty -e python ~/.config/bspwm/bin/checks.py
  ;;
"Screen lock")
  python ~/.config/bspwm/bin/lockscreen.py
  ;;
"Logout")
  loginctl terminate-session "$XDG_SESSION_ID"
  ;;
"Shutdown")
  systemctl poweroff
  ;;
"Reboot")
  systemctl reboot
  ;;
esac
