# #!/bin/sh

# # keyboard
# setxkbmap -option grp:alt_shift_toggle us,ru

# # auto start
# kitty &
# sxhkd &              
# $HOME/.config/polybar/launch.sh &   
# picom -b &           

# # Запуск оконного менеджера
# exec bspwm

# Настройка раскладки клавиатуры:
setxkbmap -option grp:alt_shift_toggle us,ru

# Запуск демона горячих клавиш (sxhkd)
sxhkd &

# Запуск композитора (Picom) в фоновом режиме
picom -f &

# Установка нормального вида курсора
xsetroot -cursor_name left_ptr &

# Запуск оконного менеджера BSPWM (выполняется в последнюю очередь)
exec bspwm