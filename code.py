#!/usr/bin/env python3
# Created By: Atri Sarker
# Date: May 28, 2025
# RST


import ugame
import stage
import constants
import util


def splash_scene():
    # Image bank for the splash scene background
    image_bank_background = stage.Bank.from_bmp16("bank1.bmp")

    # Add text objects
    text_objects = []

    title_text = stage.Text(
        width=30, height=16, font=None, palette=constants.TEXT_PALETTE, buffer=None
    )
    title_text.move((constants.SCREEN_WIDTH / 2) - title_text.width, 20)
    title_text.text("GRASS")
    text_objects.append(title_text)

    prompt_text = stage.Text(
        width=32, height=16, font=None, palette=constants.TEXT_PALETTE, buffer=None
    )
    prompt_text.move((constants.SCREEN_WIDTH / 2) - prompt_text.width, 100)
    prompt_text.text("SPLASH SCREEN")
    text_objects.append(prompt_text)

    # Make the background
    background = stage.Grid(image_bank_background, width=10)

    # CREATE THE STAGE FOR THE GAME
    game = stage.Stage(ugame.display, constants.FPS)
    # APPLY THE LAYERS
    game.layers = text_objects + [background]
    # RENDER
    game.render_block()

    for i in range(1 * constants.FPS):
        game.render_block()
        game.tick()


def menu_scene():
    # Image bank for the menu background
    image_bank_background = stage.Bank.from_bmp16("bank2.bmp")

    # Add text objects
    text_objects = []

    title_text = stage.Text(
        width=32, height=16, font=None, palette=constants.TEXT_PALETTE, buffer=None
    )
    title_text.move((constants.SCREEN_WIDTH / 2) - title_text.width, 20)
    title_text.text("A GAME?!??")
    text_objects.append(title_text)

    prompt_text = stage.Text(
        width=32, height=16, font=None, palette=constants.TEXT_PALETTE, buffer=None
    )
    prompt_text.move((constants.SCREEN_WIDTH / 2) - prompt_text.width, 100)
    prompt_text.text("PRESS START")
    text_objects.append(prompt_text)

    # Make the background
    background = stage.Grid(image_bank_background, width=10)

    # CREATE THE STAGE FOR THE GAME
    game = stage.Stage(ugame.display, constants.FPS)
    # APPLY THE LAYERS
    game.layers = text_objects + [background]
    # RENDER
    game.render_block()

    #
    button_START = util.Button(ugame.K_START)
    while True:
        keys_pressed = ugame.buttons.get_pressed()
        if button_START.get_state(keys_pressed) == "PRESSED":
            break


def game_scene():
    # Image bank for the game background
    image_bank_background = stage.Bank.from_bmp16("bank1.bmp")
    # Image bank for the player sprite
    image_bank_player = stage.Bank.from_bmp16("bank3.bmp")

    # Set the background to the first image in the image bank
    # WIDTH IS 20 TO ACCOUNT FOR SCROLL
    background = stage.Grid(image_bank_background, width=20)

    # CREATE GAME AREA UPON WHICH THE PLAYER AND ENEMIES STAND
    game_area = stage.Grid(
        image_bank_background,
        width=constants.GAME_AREA_WIDTH_IN_SPRITES,
        height=constants.GAME_AREA_HEIGHT_IN_SPRITES
        + 2,  # to account for the bricks at the bottom
    )
    # SET EVERY TILE
    for counter_x in range(constants.GAME_AREA_WIDTH_IN_SPRITES):
        # GRASS
        for counter_y in range(constants.GAME_AREA_HEIGHT_IN_SPRITES):
            game.tile(x=counter_x, y=counter_y, tile=3)
        # BRICKS
        for counter_y in range(
            constants.GAME_AREA_HEIGHT_IN_SPRITES,
            constants.GAME_AREA_HEIGHT_IN_SPRITES + 2,
        ):
            game.tile(x=counter_x, y=counter_y, tile=4)
    game_area.move(x=0, y=constants.GAME_BOUND_TOP)

    # CREATE THE STAGE FOR THE GAME
    game = stage.Stage(ugame.display, constants.FPS)

    coin_sound = open(".\Sounds\coin.wav", "rb")
    sound = ugame.audio
    sound.stop()
    sound.mute(False)

    # INSTANTIATE THE PLAYER SPRITE
    player = stage.Sprite(image_bank_player, frame=1, x=10, y=10, rotation=0)

    # CREATE LIST FOR PLAYER PROJECTILES
    player_projectiles = []

    def move_projectiles():
        # MOVE ALL PROJECTILES
        for slash in player_projectiles:
            if not (constants.OUT_LEFT_BOUND < slash.x < constants.OUT_RIGHT_BOUND):
                continue
            if slash.rotation == 0:
                slash.move(slash.x + 3, slash.y)
            else:
                slash.move(slash.x - 3, slash.y)

    # CREATE PROJECTILES
    for counter in range(constants.MAX_PLAYER_PROJECTILE_COUNT):
        player_slash = stage.Sprite(
            image_bank_background,
            frame=14,
            x=constants.OFFSCREEN_X,
            y=constants.OFFSCREEN_Y,
            rotation=0,
        )
        player_projectiles.append(player_slash)

    # ENEMIES
    enemies = []
    # CREATE ENEMIES
    for counter in range(constants.ENEMY_LIMIT):
        new_enemy = stage.Sprite(
            image_bank_background,
            frame=9,
            x=constants.OFFSCREEN_X,
            y=constants.OFFSCREEN_Y,
            rotation=0,
        )
        enemies.append(new_enemy)

    def spawn_enemy(enemy_id, pos_x, pos_y):
        for enemy in enemies:
            if not (constants.OUT_LEFT_BOUND < enemy.x < constants.OUT_RIGHT_BOUND):
                match enemy_id:
                    case 1:
                        enemy.hp = 10
                        enemy.set_frame()
                        enemy.id = enemy_id
                        enemy.action_counter = 60

    def shoot_towards_player(enemy_id, start_pos_x, end_pos_x):
        pass

    def move_enemies():
        # MOVE ALL ENEMIES
        for enemy in enemies:
            if not (constants.OUT_LEFT_BOUND < enemy.x < constants.OUT_RIGHT_BOUND):
                continue
            if enemy.rotation == 0:
                enemy.move(enemy.x + 3, enemy.y)
            else:
                enemy.move(enemy.x - 3, enemy.y)

    # SET THE LAYERS FOR THE GAME
    # ... > PLAYER > GAME_AREA > BACKGROUND
    game.layers = enemies + player_projectiles + [player, background]

    # Function that handles scrolling the background
    def scroll_background():
        background.x += 1
        if background.x == 0:
            background.x = -16
        background.move(background.x, background.y)

    # CREATE BUTTONS
    left_button = util.Button(ugame.K_LEFT)
    right_button = util.Button(ugame.K_RIGHT)
    up_button = util.Button(ugame.K_UP)
    down_button = util.Button(ugame.K_DOWN)
    button_A = util.Button(ugame.K_O)

    # CREATE SOUNDS
    attack_sound = util.Sound("coin")

    # Function that handles the actions of the player
    attack_debounce = constants.ATTACK_COOLDOWN

    def handle_player_action():
        new_x = player.x
        new_y = player.y
        player_moving = False
        # GET BYTE THAT REPRESENTS THE KEYS PRESSED
        keys_pressed = ugame.buttons.get_pressed()
        # MATCH BUTTONS WITH ACTIONS
        if left_button.get_state(keys_pressed) in ["PRESSED", "STILL_PRESSED"]:
            new_x -= constants.PLAYER_SPEED
            # FLIP PLAYER SPRITE
            player.set_frame(rotation=4)
            player_moving = not player_moving
        if right_button.get_state(keys_pressed) in ["PRESSED", "STILL_PRESSED"]:
            new_x += constants.PLAYER_SPEED
            player.set_frame(rotation=0)
            player_moving = not player_moving
        if up_button.get_state(keys_pressed) in ["PRESSED", "STILL_PRESSED"]:
            new_y -= constants.PLAYER_SPEED
        if down_button.get_state(keys_pressed) in ["PRESSED", "STILL_PRESSED"]:
            new_y += constants.PLAYER_SPEED

        # IF THE PLAYER PRESSES THE A BUTTON, PLAY THE SOUND
        # CHECK IF THE BUTTON WAS JUST PRESSED
        if button_A.get_state(keys_pressed) == "PRESSED":
            # SHOOT A PROJECTILE
            for slash in player_projectiles:
                if attack_debounce >= 1:
                    break
                if not (constants.OUT_LEFT_BOUND < slash.x < constants.OUT_RIGHT_BOUND):
                    slash.move(player.x, player.y)
                    slash.set_frame(rotation=player.rotation)
                    # HANDLE ANIMATION
                    player.set_frame(frame=10)
                    # PLAY THE SOUND
                    # attack_sound.play()
                    # DEBOUNCE
                    attack_debounce = 7
                    break

        # DECREMENT DEBOUNCE
        attack_debounce = max(attack_debounce - 1, 0)
        # HANDLE ANIMATION
        # [WALKING]
        if player_moving and 1 <= player.frame <= 7:
            player.set_frame(player.frame + 1)
        elif 1 <= player.frame <= 8:
            player.set_frame(1)
        # [ATTACK]
        elif 9 <= player.frame:
            player.set_frame(player.frame + 1)
        elif player.frame == 15:
            player.set_frame(1)

        # ALIGN WITH BOUNDARIES
        new_x = util.clamp(new_x, 0, constants.SCREEN_WIDTH - constants.SPRITE_SIZE)
        new_y = util.clamp(new_y, 0, constants.SCREEN_HEIGHT - constants.SPRITE_SIZE)

        # SET PLAYER POSITION
        player.move(new_x, new_y)

    def game_loop():
        # RESET SOUNDS
        # ugame.audio.stop()
        # ugame.audio.mute(False)
        # Scroll the background
        scroll_background()
        # handle player actions
        handle_player_action()
        # move projectiles
        move_projectiles()
        # RENDER
        game.render_block()
        # WAIT FOR NEXT FRAME
        game.tick()

    while True:
        game_loop()


def main():
    splash_scene()
    menu_scene()
    game_scene()


if __name__ == "__main__":
    main()
