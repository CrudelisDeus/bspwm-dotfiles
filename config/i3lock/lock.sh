#!/bin/sh

IMG="/tmp/lock.png"

sleep 1
scrot -o "$IMG" &&
  magick "$IMG" -blur 0x8 "$IMG" &&
  i3lock -i "$IMG"
