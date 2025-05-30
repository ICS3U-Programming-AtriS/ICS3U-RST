#!/usr/bin/env python3
# Created By: Atri Sarker
# Date: May 28, 2025
# RST

import ugame 
import stage


def main():
    # Image bank for the background
    image_bank_background = stage.Bank.from_bmp16("bank1.bmp")

    # Set the background to the first image in the image bank
    background = stage.Grid(image_bank_background, 20, 8)

    # display the background at 60fps
    game = stage.Stage(ugame.display, 60)
    game.layers = [background]
    game.render_block()

    # Hacked up a scrolling background
    scroll = -50
    while True:
        background.move(scroll,0)
        scroll += 1
        if scroll == 0:
            scroll = -32
        game.tick()
        game.render_block()


if __name__ == "__main__":
    main()