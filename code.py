#!/usr/bin/env python3
# Created By: Atri Sarker
# Date: May 28, 2025
# RST

import ugame
import stage
import constants
import util


def game_scene():
    # Image bank for the game background
    image_bank_background = stage.Bank.from_bmp16("bank1.bmp")
    # Image bank for the player sprite
    image_bank_player = stage.Bank.from_bmp16("bank3.bmp")

    # Set the background to the first image in the image bank
    # WIDTH IS 20 TO ACCOUNT FOR SCROLL
    background = stage.Grid(image_bank_background, width=20)

    # CREATE THE STAGE FOR THE GAME
    game = stage.Stage(ugame.display, constants.FPS)

    # INSTANTIATE THE PLAYER SPRITE
    player = stage.Sprite(image_bank_player, frame=0, x=10, y=10, rotation=0)

    # SET THE LAYERS FOR THE GAME
    # ... > PLAYER > BACKGROUND
    game.layers = [player, background]

    # Function that handles scrolling the background
    def scroll_background(scroll=[-32]):
        background.move(scroll[0], 0)
        scroll[0] += 1
        if scroll[0] == 0:
            scroll[0] = -32

    # CREATE BUTTONS
    left_button = util.Button(ugame.K_LEFT)
    right_button = util.Button(ugame.K_RIGHT)
    up_button = util.Button(ugame.K_UP)
    down_button = util.Button(ugame.K_DOWN)

    # Function that handles the movement of the player
    def handle_player_movement():
        new_x = player.x
        new_y = player.y
        # GET BYTE THAT REPRESENTS THE KEYS PRESSED
        keys_pressed = ugame.buttons.get_pressed()
        # MATCH BUTTONS WITH ACTIONS
        if left_button.get_state(keys_pressed) in ["PRESSED", "STILL_PRESSED"]:
            new_x -= constants.PLAYER_SPEED
            # FLIP PLAYER SPRITE
            player.set_frame(rotation=4)
            # ANIMATION
            player.set_frame(0 if player.frame else 1)
        if right_button.get_state(keys_pressed) in ["PRESSED", "STILL_PRESSED"]:
            new_x += constants.PLAYER_SPEED
            player.set_frame(rotation=0)
            # ANIMATION
            player.set_frame(0 if player.frame else 1)
        if up_button.get_state(keys_pressed) in ["PRESSED", "STILL_PRESSED"]:
            new_y -= constants.PLAYER_SPEED
        if down_button.get_state(keys_pressed) in ["PRESSED", "STILL_PRESSED"]:
            new_y += constants.PLAYER_SPEED

        # ALLIGN WITH BOUNDARIES
        new_x = util.clamp(new_x, 0, constants.SCREEN_WIDTH - constants.SPRITE_SIZE)
        new_y = util.clamp(new_y, 0, constants.SCREEN_HEIGHT - constants.SPRITE_SIZE)

        # SET PLAYER POSITION
        player.move(new_x, new_y)

    def game_loop():
        # Scroll the background
        scroll_background()
        # handle player movement
        handle_player_movement()
        # RENDER
        game.render_block()
        # WAIT FOR NEXT FRAME
        game.tick()

    while True:
        game_loop()


if __name__ == "__main__":
    game_scene()
