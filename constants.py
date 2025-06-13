#!/usr/bin/env python3
# Created By: Atri Sarker
# Date: June 2, 2025
# This module contains constants


# 10x16 = 160, THE WIDTH OF THE SCREEN IS 160 PIXELS
SCREEN_WIDTH = 160
# 8x16 = 128, THE HEIGHT OF THE SCREEN IS 128 PIXELS
SCREEN_HEIGHT = 128


# ALL SPRITES HAVE 16x16 PIXEL DIMENSIONS
SPRITE_SIZE = 16


# FPS
FPS = 60
# PLAYER SPEED
PLAYER_SPEED = 4
# ATTACK COOLDOWN [IN FRAMES]
ATTACK_COOLDOWN = 7
# PLAYER PROJECTILE SPEED
PLAYER_PROJECTILE_SPEED = 6

# Position values for offscreen sprites
OFFSCREEN_X = -100
OFFSCREEN_Y = -100


# BOUNDS FOR PROJECTILES DISAPPEARING OFFSCREEN
OUT_RIGHT_BOUND = SCREEN_WIDTH + SPRITE_SIZE
OUT_LEFT_BOUND = -1 * SPRITE_SIZE
MAX_PLAYER_PROJECTILE_COUNT = 8

GAME_AREA_WIDTH_IN_SPRITES = 10
GAME_AREA_HEIGHT_IN_SPRITES = 4
# GAME AREA BOUNDS [Y]
GAME_BOUND_BOTTOM = SCREEN_HEIGHT - 36
GAME_BOUND_TOP = 16


ENEMY_LIMIT = 5
# first 2 pieces: background, next 2 pieces: stroke color
# next 2 pieces: text fill color
# every other piece: idk
TEXT_PALETTE = (
    b"\xf8\x1f\x07\xe0\xcey\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff"
    b"\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff"
)
DAMAGED_PALETTE = (
    b"\xf8\x00\xf8\x00\xcey\xf8\x00\xf8\x00\xf8\x00\x00\x00\x00\x00"
    b"\xf8\x00\xf8\x00\xf8\x00\xf8\x00\x00\x00\x00\x00\x00\x00\x00\x00"
)

DEFAULT_PALETTE = (
    b"\xf8\x1f\x00\x00\xcey\xff\xff\xf8\x1f\x00\x19\xfc\xe0\xfd\xe0"
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
)

# PALETTES FOR CHARACTER SELECTION
PLAYER_PALLETTES = [
    DEFAULT_PALETTE,
    (
        b"\xf8\x00\xf8\x00\xcey\xf8\x00\xf8\x00\xf8\x00\xfc\xe0\xfd\xe0"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    ),
]
