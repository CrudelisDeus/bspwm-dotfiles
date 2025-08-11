#!/bin/bash

# Скрипт для случайного выбора анимированных обоев
# Автор: Deus
# Версия: 1.0

# Директория с анимированными обоями
WALLPAPER_DIR="$HOME/animated_wallpapers"

# Проверяем, существует ли директория
if [ ! -d "$WALLPAPER_DIR" ]; then
    echo "Ошибка: Директория $WALLPAPER_DIR не существует" >&2
    exit 1
fi

# Ищем все видео файлы в директории
video_files=($(find "$WALLPAPER_DIR" -type f \( -name "*.mp4" -o -name "*.mkv" -o -name "*.avi" -o -name "*.mov" -o -name "*.webm" \)))

# Проверяем, найдены ли файлы
if [ ${#video_files[@]} -eq 0 ]; then
    echo "Ошибка: В директории $WALLPAPER_DIR не найдено видео файлов" >&2
    exit 1
fi

# Выбираем случайный файл
random_index=$((RANDOM % ${#video_files[@]}))
selected_wallpaper="${video_files[$random_index]}"

# Выводим выбранный файл
echo "$selected_wallpaper"
