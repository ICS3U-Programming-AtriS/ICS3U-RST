#!/usr/bin/env python3
# Created By: Atri Sarker
# Date: May 28, 2025
# RST

import ugame 
import stage

# I apologize for the severe lack of comments, I will add them later
def main():
    # Image bank for the background
    image_bank_background = stage.Bank.from_bmp16("bank1.bmp")
    # Image bank for the player
    image_bank_player = stage.Bank.from_bmp16("bank2.bmp")

    # Set the background to the first image in the image bank
    background = stage.Grid(image_bank_background, 20, 8)

    # display the background at 60fps
    game = stage.Stage(ugame.display, 60)

    # Player
    player = stage.Sprite(image_bank_player, 0, 10, 10)
    game.layers = [player, background]

    # Function that scrolls the background
    # [Using a mutable default for handling the scroll]
    def scroll_background(scroll = [-32]):
        background.move(scroll[0], 0)
        scroll[0] += 1
        if scroll[0] == 0:
            scroll[0] = -32
        game.tick()


    # Handle player movement
    # [Using a mutable default for handling gravity]
    def handle_player_movement(y_velocity = [0]):
        # Get user input
        keys = ugame.buttons.get_pressed()
        # Speed in the X direction
        horizontal_speed = 2

        # Match the pressed keys with the desired movement
        if keys & ugame.K_RIGHT:
            player.move(player.x + horizontal_speed, player.y)
        if keys & ugame.K_LEFT:
            player.move(player.x - horizontal_speed, player.y)
        if keys & ugame.K_UP:
            player.move(player.x, player.y)
            if 16*6.8 < player.y <= 16*7:
                y_velocity[0] = -5

        # Check if the player is off the ground
        if player.y < 16*7:
            y_velocity[0] += 0.3
        
        new_y = player.y + y_velocity[0]
        # Prevent player from sinking into the ground
        if new_y >= 16*7:
            new_y = 16*7
            y_velocity[0] = 0

        player.move(player.x, new_y)

        
    def game_loop():
        # Scroll the background
        scroll_background()
        # handle player movement
        handle_player_movement()

    # Hacked up a scrolling background
    scroll = -50
    while True:
        game_loop()
        game.tick()
        game.render_block()


if __name__ == "__main__":
    main()