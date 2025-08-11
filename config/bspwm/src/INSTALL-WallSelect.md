# Установка обновленного WallSelect

## Что изменилось

Обновленный `WallSelect` теперь поддерживает:
- ✅ Статические обои из текущей темы
- ✅ Анимированные обои из `~/animated_wallpapers/`
- ✅ Превью для видео файлов
- ✅ Индикаторы для анимированных обоев

## Быстрая установка

### 1. Установите зависимости

```bash
# Arch Linux
sudo pacman -S feh imagemagick mpv ffmpeg
paru -S xwinwrap-0.9-bin xxhash

# Ubuntu/Debian
sudo apt install feh imagemagick mpv ffmpeg xxhash
```

### 2. Скопируйте обновленные файлы

```bash
# Скопируйте обновленный WallSelect
cp config/bspwm/src/WallSelect ~/.config/bspwm/src/

# Скопируйте обновленную Rofi тему
cp config/bspwm/src/rofi-themes/WallSelect.rasi ~/.config/bspwm/src/rofi-themes/

# Сделайте скрипт исполняемым
chmod +x ~/.config/bspwm/src/WallSelect
```

### 3. Создайте директорию для анимированных обоев

```bash
mkdir -p ~/animated_wallpapers
```

### 4. Добавьте анимированные обои

Поместите ваши `.mp4`, `.mkv` или `.gif` файлы в `~/animated_wallpapers/`

### 5. Перезагрузите sxhkd

Нажмите **Super + Escape** или выполните:

```bash
pkill -USR1 -x sxhkd
```

## Использование

- **Super + Alt + W** - открыть селектор обоев
- Статические обои отображаются как обычно
- Анимированные обои помечены как `[ANIMATED]`
- При выборе анимированного обоя автоматически запускается `AnimatedWall`

## Проверка работы

1. Нажмите **Super + Alt + W**
2. Убедитесь, что видны как статические, так и анимированные обои
3. Выберите анимированный обой и проверьте, что он воспроизводится

## Устранение проблем

Если анимированные обои не отображаются:
- Проверьте, что `ffmpeg` установлен
- Убедитесь, что директория `~/animated_wallpapers/` существует
- Проверьте права доступа к файлам

Если превью не создаются:
- Установите `ffmpeg`
- Проверьте, что видео файлы не повреждены
