#!/bin/sh

# keyboard
setxkbmap -option grp:alt_shift_toggle us,ru

# auto start
sxhkd &              
$HOME/.config/polybar/launch.sh &   
picom -b &           

# Запуск оконного менеджера
exec bspwm
