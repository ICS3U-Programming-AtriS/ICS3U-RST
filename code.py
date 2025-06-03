#!/usr/bin/env python3
# Created By: Atri Sarker
# Date: May 28, 2025
# RST

import ugame 
import stage


def loading_screen():
    # black background
    bank = stage.Bank.from_bmp16("bank2.bmp")
    
def main():
    # Image bank for the background
    image_bank_background = stage.Bank.from_bmp16("bank1.bmp")
    # Image bank for the player
    image_bank_player = stage.Bank.from_bmp16("bank3.bmp")

    # Set the background to the first image in the image bank
    background = stage.Grid(image_bank_background, 20)

    # display the background at 60fps
    game = stage.Stage(ugame.display, 60)

    # Player
    player = stage.Sprite(image_bank_player, 0, 10, 10, rotation=0)
    game.layers = [player, background]
    
    game.render_block()

    # Peak code
    def scroll_background(scroll = [-32]):
        background.move(scroll[0], 0)
        scroll[0] += 1
        if scroll[0] == 0:
            scroll[0] = -32
        game.tick()


    # Handle player movement
    def handle_player_movement(y_velocity = [0]):
        # Get user input
        keys = ugame.buttons.get_pressed()
        horizontal_speed = 2

        x_velocity = 0

        if keys & ugame.K_RIGHT:
            x_velocity = horizontal_speed
            player.set_frame(rotation = 0)
            player.set_frame(0 if player.frame else 1)
        if keys & ugame.K_LEFT:
            x_velocity = -horizontal_speed
            player.set_frame(rotation = 4)
            player.set_frame(0 if player.frame else 1)
        if keys & ugame.K_DOWN:
            player.set_frame(2)
        if keys & ugame.K_UP:
            player.move(player.x, player.y)
            if 16*6.8 < player.y <= 16*7:
                y_velocity[0] = -5

        if player.y < 16*7:
            y_velocity[0] += 0.4
        
        new_x = player.x + x_velocity

        new_y = player.y + y_velocity[0]
        if new_y >= 16*7:
            new_y = 16*7
            y_velocity[0] = 0

        player.move(new_x, new_y)

        
    def game_loop():
        # Scroll the background
        scroll_background()
        # handle player movement
        handle_player_movement()

    # Hacked up a scrolling background
    while True:
        game.render_block()
        game_loop()
        game.tick()


if __name__ == "__main__":
    main()