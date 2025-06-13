#!/usr/bin/env python3
# Created By: Atri Sarker
# Date: May 28, 2025
# RST


import ugame
import stage
import constants
import util
import random
import time


def splash_scene():
    # Image bank for the Immaculata crest
    crest_bank = stage.Bank.from_bmp16("crest.bmp")

    title_text = stage.Text(
        width=30, height=16, font=None, palette=constants.TEXT_PALETTE, buffer=None
    )
    title_text.move(20, 20)
    title_text.text("IMH GAME STUDIO")

    # Make the crest
    crest = stage.Grid(crest_bank, width=4, height=4)
    for frame_num in range(16):
        tile_pos_x = frame_num // 4
        tile_pos_y = frame_num % 4
        crest.tile(x=tile_pos_x, y=tile_pos_y, tile=frame_num)
    # MOVE CREST TO CENTER
    crest.move(x=48, y=48)
    # CREATE THE STAGE FOR THE GAME
    game = stage.Stage(ugame.display, constants.FPS)
    # APPLY THE LAYERS
    game.layers = [title_text] + [crest]
    # RENDER
    game.render_block()
    # 2 SECONDS
    time.sleep(2.0)


def menu_scene():
    # Image bank for the menu background
    image_bank_background = stage.Bank.from_bmp16("background_bank.bmp")

    # Add text objects
    text_objects = []

    title_text = stage.Text(
        width=32, height=16, font=None, palette=constants.TEXT_PALETTE, buffer=None
    )
    title_text.move(10, 20)
    title_text.text("ULTIMATE SURVIVOR")
    text_objects.append(title_text)

    prompt_text = stage.Text(
        width=32, height=16, font=None, palette=constants.TEXT_PALETTE, buffer=None
    )
    prompt_text.move(5, 100)
    prompt_text.text("START - PLAY GAME")
    text_objects.append(prompt_text)
    prompt_text2 = stage.Text(
        width=32, height=16, font=None, palette=constants.TEXT_PALETTE, buffer=None
    )
    prompt_text2.move(5, 120)
    prompt_text2.text("SELECT-INSTRUCTIONS")
    text_objects.append(prompt_text2)

    # GRASS
    grass = stage.Grid(image_bank_background, width=11, height=5)
    grass.move(x=0, y=56)
    # SET EVERY TILE TO GRASS
    for counter_x in range(grass.width):
        for counter_y in range(grass.height):
            grass.tile(x=counter_x, y=counter_y, tile=4)

    # Function that handles scrolling the grass
    def scroll_grass():
        # HORIZONTAL SCROLL
        grass.x -= 4
        if grass.x <= -16:
            grass.x = 0
        grass.move(grass.x, grass.y)

    # Image bank for the player sprite
    image_bank_player = stage.Bank.from_bmp16("player_sprite_bank.bmp")
    # PLAYER SPRITE
    player_sprite = stage.Sprite(image_bank_player, frame=1, x=24, y=72, rotation=0)

    # CREATE THE STAGE FOR THE GAME
    game = stage.Stage(ugame.display, constants.FPS)
    # APPLY THE LAYERS
    game.layers = text_objects + [player_sprite] + [grass]

    button_START = util.Button(ugame.K_START)
    button_SELECT = util.Button(ugame.K_SELECT)
    while True:
        scroll_grass()
        # ANIMATE PLAYER SPRITE
        if 1 <= player_sprite.frame <= 7:
            player_sprite.set_frame(player_sprite.frame + 1)
        if player_sprite.frame >= 8:
            player_sprite.set_frame(1)
        game.tick()
        # RENDER
        game.render_block()
        keys_pressed = ugame.buttons.get_pressed()
        if button_START.get_state(keys_pressed) == "RELEASED":
            break
        if button_SELECT.get_state(keys_pressed) == "RELEASED":
            instructions_scene()


def instructions_scene():
    # Add text objects
    text_objects = []

    text1 = stage.Text(
        width=32, height=16, font=None, palette=constants.TEXT_PALETTE, buffer=None
    )
    text1.move(20, 20)
    text1.text("A - ATTACK")
    text_objects.append(text1)
    text2 = stage.Text(
        width=32, height=16, font=None, palette=constants.TEXT_PALETTE, buffer=None
    )
    text2.move(0, 40)
    text2.text("B - RUN")
    text_objects.append(text2)
    text2a = stage.Text(
        width=32, height=16, font=None, palette=constants.TEXT_PALETTE, buffer=None
    )
    text2a.move(10, 48)
    text2a.text("[DISABLES ATTACK]")
    text_objects.append(text2a)
    text3 = stage.Text(
        width=32, height=16, font=None, palette=constants.TEXT_PALETTE, buffer=None
    )
    text3.move(0, 70)
    text3.text("LEFT SIDE - MOVEMENT")
    text_objects.append(text3)
    text4 = stage.Text(
        width=32, height=16, font=None, palette=constants.TEXT_PALETTE, buffer=None
    )
    text4.move(0, 90)
    text4.text("SELECT-BACK TO MENU")
    text_objects.append(text4)

    # CREATE THE STAGE FOR THE GAME
    game = stage.Stage(ugame.display, constants.FPS)
    # APPLY THE LAYERS
    game.layers = text_objects

    button_SELECT = util.Button(ugame.K_SELECT)
    while True:
        game.tick()
        # RENDER
        game.render_block()
        keys_pressed = ugame.buttons.get_pressed()
        if button_SELECT.get_state(keys_pressed) == "RELEASED":
            break


# GAME SCENE
def game_scene():
    # SCORE
    score = 0
    # SCORE TEXT
    score_text = stage.Text(
        width=32, height=16, font=None, palette=constants.TEXT_PALETTE, buffer=None
    )
    score_text.move(50, 100)
    score_text.text(f"Score: {score}")
    # Image bank for the game background
    image_bank_background = stage.Bank.from_bmp16("background_bank.bmp")
    # Image bank for the player sprite
    image_bank_player = stage.Bank.from_bmp16("player_sprite_bank.bmp")
    # Image bank for the enemy sprites
    image_bank_enemy = stage.Bank.from_bmp16("enemy_bank.bmp")

    # Set the background to the first image in the image bank
    # WIDTH IS 14 TO ACCOUNT FOR SCROLL
    background = stage.Grid(image_bank_background, width=14)

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
            game_area.tile(x=counter_x, y=counter_y, tile=4)
        # BRICKS
        for counter_y in range(
            constants.GAME_AREA_HEIGHT_IN_SPRITES,
            constants.GAME_AREA_HEIGHT_IN_SPRITES + 2,
        ):
            game_area.tile(x=counter_x, y=counter_y, tile=5)
    game_area.move(x=0, y=constants.GAME_BOUND_TOP + 16)

    # BUTTONS
    button_right_ui = stage.Sprite(
        image_bank_background, frame=6, x=42, y=106, rotation=0
    )
    button_left_ui = stage.Sprite(
        image_bank_background, frame=6, x=22, y=106, rotation=2
    )
    button_up_ui = stage.Sprite(image_bank_background, frame=6, x=32, y=100, rotation=1)
    button_down_ui = stage.Sprite(
        image_bank_background, frame=6, x=32, y=112, rotation=3
    )
    button_a_ui = stage.Sprite(image_bank_background, frame=6, x=140, y=102, rotation=1)
    button_b_ui = stage.Sprite(image_bank_background, frame=6, x=120, y=108, rotation=1)
    button_uis = [
        button_b_ui,
        button_a_ui,
        button_down_ui,
        button_left_ui,
        button_right_ui,
        button_up_ui,
    ]
    # CREATE THE STAGE FOR THE GAME
    game = stage.Stage(ugame.display, constants.FPS)

    # INSTANTIATE THE PLAYER SPRITE
    player = stage.Sprite(image_bank_player, frame=1, x=50, y=50, rotation=0)

    # CREATE LIST FOR PLAYER PROJECTILES
    player_projectiles = []

    def move_projectiles():
        # GET LIST OF ENEMIES
        active_enemies = get_active_enemies()
        # MOVE ALL PROJECTILES
        for slash in player_projectiles:
            if not (constants.OUT_LEFT_BOUND < slash.x < constants.OUT_RIGHT_BOUND):
                continue
            if slash.rotation == 0:
                slash.move(slash.x + constants.PLAYER_PROJECTILE_SPEED, slash.y)
            else:
                slash.move(slash.x - constants.PLAYER_PROJECTILE_SPEED, slash.y)

            top_corner_x = slash.x + 2
            top_corner_y = slash.y + 2
            bottom_corner_x = slash.x + 10
            bottom_corner_y = slash.y + 10
            for enemy in active_enemies:
                if stage.collide(
                    top_corner_x,
                    top_corner_y,
                    bottom_corner_x,
                    bottom_corner_y,
                    enemy.x,
                    enemy.y,
                    enemy.x + 16,
                    enemy.y + 16,
                ):
                    enemy.hp -= 1
                    enemy.set_frame(enemy.frame + 1)
                    if enemy.hp <= 0:
                        enemy.move(x=constants.OFFSCREEN_X, y=constants.OFFSCREEN_Y)
                        score += 5
                        score_text.clear()
                        score_text.cursor(0, 0)
                        score_text.text(f"Score: {score}")
                    slash.move(x=constants.OFFSCREEN_X, y=constants.OFFSCREEN_Y)

    # CREATE PROJECTILES
    for counter in range(constants.MAX_PLAYER_PROJECTILE_COUNT):
        player_slash = stage.Sprite(
            image_bank_player,
            frame=0,
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
            image_bank_enemy,
            frame=0,
            x=constants.OFFSCREEN_X,
            y=constants.OFFSCREEN_Y,
            rotation=0,
        )
        enemies.append(new_enemy)

    # FUNCTION THAT RETURNS A LIST OF ALL ACTIVE ENEMIES
    def get_active_enemies() -> list:
        # RETURN A LIST OF ALL ENEMIES THAT AREN'T OFFSCREEN
        return [enemy for enemy in enemies if enemy.y >= 0]

    # FUNCTION THAT RETURNS A LIST OF ALL ACTIVE ENEMIES
    def get_inactive_enemies() -> list:
        # RETURN A LIST OF ALL ENEMIES THAT ARE OFFSCREEN
        return [enemy for enemy in enemies if enemy.y < 0]

    # FUNCTION THAT HANDLES ENEMY BEHAVIOUR
    def handle_enemies():
        # GET LIST OF ACTIVE ENEMIES
        active_enemies = get_active_enemies()
        # LOOP THROUGH EVERY ENEMY
        for enemy in active_enemies:
            # FUTURE POSITION VARIABLES
            new_x = enemy.x
            new_y = enemy.y
            # GENTLY SHIFT AND CLAMP ENEMIES ONTO THE SCREEN
            if enemy.x <= 0:
                new_x += 5
            elif enemy.x >= constants.SCREEN_WIDTH - constants.SPRITE_SIZE:
                new_x -= 5

            # MATCH ENEMY ID WITH ENEMY BEHAVIOUR
            if enemy.enemy_id == 1:
                # BASIC ENEMY 1
                # THIS GUY JUSTS MOVES TOWARDS THE PLAYER
                if enemy.x < player.x:
                    new_x += random.randint(0, enemy.movement_speed)
                    enemy.set_frame(rotation=0)
                else:
                    new_x -= random.randint(0, enemy.movement_speed)
                    enemy.set_frame(rotation=4)
                if enemy.y < player.y:
                    new_y += random.randint(0, enemy.movement_speed)
                else:
                    new_y -= random.randint(0, enemy.movement_speed)
            elif enemy.enemy_id == 2:
                # BASIC ENEMY 2
                # THIS GUY ALSO JUSTS MOVES TOWARDS THE PLAYER
                # JUST A BIT MORE SPORADICALLY
                if enemy.x < player.x:
                    new_x += random.randint(
                        -(enemy.movement_speed), enemy.movement_speed * 2
                    )
                    enemy.set_frame(rotation=0)
                else:
                    new_x -= random.randint(
                        -(enemy.movement_speed), enemy.movement_speed * 2
                    )
                    enemy.set_frame(rotation=4)
                if enemy.y < player.y:
                    new_y += random.randint(
                        -(enemy.movement_speed), enemy.movement_speed * 2
                    )
                else:
                    new_y -= random.randint(
                        -(enemy.movement_speed), enemy.movement_speed * 2
                    )
            elif enemy.enemy_id == 3:
                # DVD SCREENSAVER ENEMY
                # MOVEMENT BEHAVES LIKE THE MOVEMENT OF A TV SCREENSAVER
                if enemy.x <= 0:
                    enemy.set_frame(rotation=(0 if enemy.rotation == 2 else 4))
                if enemy.x >= constants.SCREEN_WIDTH - constants.SPRITE_SIZE:
                    enemy.set_frame(rotation=(2 if enemy.rotation == 0 else 6))
                if enemy.y <= constants.GAME_BOUND_TOP + 16:
                    enemy.set_frame(rotation=(4 if enemy.rotation == 0 else 6))
                if enemy.y >= constants.GAME_BOUND_BOTTOM - constants.SPRITE_SIZE:
                    enemy.set_frame(rotation=(0 if enemy.rotation == 4 else 2))
                if enemy.rotation == 0:
                    new_x += enemy.movement_speed
                    new_y -= enemy.movement_speed
                elif enemy.rotation == 2:
                    new_x -= enemy.movement_speed
                    new_y -= enemy.movement_speed
                elif enemy.rotation == 4:
                    new_x += enemy.movement_speed
                    new_y += enemy.movement_speed
                elif enemy.rotation == 6:
                    new_x -= enemy.movement_speed
                    new_y += enemy.movement_speed
            elif enemy.enemy_id == 4:
                # BOWSER VIKING DUDE
                # HE SETS HIS EYES UPON THE PLAYER
                # AND THEN HE RUSHES TOWARDS THEM
                if enemy.x <= constants.SPRITE_SIZE + 3:
                    enemy.set_frame(rotation=1)
                    if enemy.y < player.y - 5:
                        new_y += random.randint(0, enemy.movement_speed)
                    elif enemy.y > player.y + 5:
                        new_y -= random.randint(0, enemy.movement_speed)
                    else:
                        enemy.set_frame(rotation=0)
                        new_x += 3
                elif enemy.x >= constants.SCREEN_WIDTH - constants.SPRITE_SIZE - 4:
                    enemy.set_frame(rotation=5)
                    if enemy.y < player.y - 5:
                        new_y += random.randint(0, enemy.movement_speed)
                    elif enemy.y > player.y + 5:
                        new_y -= random.randint(0, enemy.movement_speed)
                    else:
                        enemy.set_frame(rotation=4)
                        new_x -= 3
                if enemy.rotation == 0:
                    new_x += enemy.movement_speed * 2
                elif enemy.rotation == 4:
                    new_x -= enemy.movement_speed * 2
            elif enemy.enemy_id == 5:
                # THE BRICK
                # IT JUMPS TO THE SKY AND GETS ABOVE THE PLAYER
                # AND THEN DIVES ONTO THE GROUND
                if enemy.rotation == 0 and enemy.y >= 14:
                    new_y -= enemy.movement_speed
                if enemy.y < 14 and enemy.rotation == 0:
                    enemy.set_frame(rotation=2)
                if enemy.rotation == 2 and enemy.x < player.x + 7:
                    new_x += random.randint(0, enemy.movement_speed * 3)
                elif enemy.rotation == 2 and enemy.x > player.x - 7:
                    new_x -= random.randint(0, enemy.movement_speed * 3)
                if enemy.rotation == 2 and player.x - 7 < enemy.x < player.x + 7:
                    new_y += 2 * enemy.movement_speed
                    enemy.set_frame(rotation=4)
                if enemy.rotation == 4:
                    new_y += 2 * enemy.movement_speed
                if enemy.y >= constants.GAME_BOUND_BOTTOM - constants.SPRITE_SIZE - 5:
                    enemy.set_frame(rotation=0)

            if enemy.frame % 2 == 1:
                enemy.set_frame(frame=enemy.frame - 1)

            enemy.move(new_x, new_y)

    def spawn_enemy(enemy_id, enemy_power):
        inactive_enemies = get_inactive_enemies()
        if inactive_enemies == []:
            return
        new_enemy = inactive_enemies[0]
        start_pos_x = [-16, constants.SCREEN_WIDTH][random.randint(0, 1)]
        start_pos_y = random.randint(
            constants.GAME_BOUND_TOP + 6,
            constants.GAME_BOUND_BOTTOM - constants.SPRITE_SIZE,
        )
        new_enemy.hp = 2 + (enemy_power // 4)
        new_enemy.set_frame(frame=(2 * (enemy_id - 1)), rotation=0)
        new_enemy.enemy_id = enemy_id
        new_enemy.movement_speed = min(1 + (enemy_power // 5), 4)
        new_enemy.move(x=start_pos_x, y=start_pos_y)

    wave_num = 0

    def handle_waves():
        enemy_count = len(get_active_enemies())
        if enemy_count == 0:
            wave_num += 1
            for counter in range(
                min(random.randint(1 + wave_num // 2, wave_num), constants.ENEMY_LIMIT)
            ):
                battle_power = random.randint(1, wave_num)
                enemy_id = random.randint(1, 5) if wave_num >= 3 else 1
                spawn_enemy(enemy_id, battle_power)

    # SET THE LAYERS FOR THE GAME
    # ... > PLAYER > GAME_AREA > BACKGROUND
    game.layers = (
        [score_text]
        + enemies
        + player_projectiles
        + button_uis
        + [player, game_area, background]
    )

    # Function that handles scrolling the background
    def scroll_background():
        # HORIZONTAL SCROLL
        background.x += 2
        if background.x >= 0:
            background.x = -16
        # VERTICAL SCROLL
        background.y -= 1
        if background.y <= -16:
            background.y = 0
        background.move(background.x, background.y)

    # CREATE BUTTONS
    left_button = util.Button(ugame.K_LEFT)
    right_button = util.Button(ugame.K_RIGHT)
    up_button = util.Button(ugame.K_UP)
    down_button = util.Button(ugame.K_DOWN)
    button_A = util.Button(ugame.K_O)
    button_B = util.Button(ugame.K_X)

    # CREATE SOUNDS
    attack_sound = util.Sound("click")

    # Function that handles the actions of the player
    attack_debounce = constants.ATTACK_COOLDOWN

    def handle_player_action():
        new_x = player.x
        new_y = player.y
        player_moving_horizontally = False
        player_moving_vertically = False
        # GET BYTE THAT REPRESENTS THE KEYS PRESSED
        keys_pressed = ugame.buttons.get_pressed()
        # MATCH BUTTONS WITH ACTIONS
        if left_button.get_state(keys_pressed) in ["PRESSED", "STILL_PRESSED"]:
            button_left_ui.set_frame(frame=7)
            new_x -= constants.PLAYER_SPEED
            # FLIP PLAYER SPRITE
            player.set_frame(rotation=4)
            player_moving_horizontally = not player_moving_horizontally
        else:
            button_left_ui.set_frame(frame=6)
        if right_button.get_state(keys_pressed) in ["PRESSED", "STILL_PRESSED"]:
            button_right_ui.set_frame(frame=7)
            new_x += constants.PLAYER_SPEED
            player.set_frame(rotation=0)
            player_moving_horizontally = not player_moving_horizontally
        else:
            button_right_ui.set_frame(frame=6)
        if up_button.get_state(keys_pressed) in ["PRESSED", "STILL_PRESSED"]:
            button_up_ui.set_frame(frame=7)
            new_y -= constants.PLAYER_SPEED
            player_moving_vertically = not player_moving_vertically
        else:
            button_up_ui.set_frame(frame=6)
        if down_button.get_state(keys_pressed) in ["PRESSED", "STILL_PRESSED"]:
            button_down_ui.set_frame(frame=7)
            new_y += constants.PLAYER_SPEED
            player_moving_vertically = not player_moving_vertically
        else:
            button_down_ui.set_frame(frame=6)

        # BOOST BUTTON [ DOUBLES MOVEMENT ]
        # BUT IN EXCHANGE, ATTACKING IS DISABLED
        if button_B.get_state(keys_pressed) in ["PRESSED", "STILL_PRESSED"]:
            button_b_ui.set_frame(frame=7)
            new_x += new_x - player.x
            new_y += new_y - player.y
        else:
            button_b_ui.set_frame(frame=6)

        # ATTACK BUTTON
        # CHECK IF THE BUTTON WAS JUST PRESSED
        if button_A.get_state(keys_pressed) in ["PRESSED", "STILL_PRESSED"]:
            button_a_ui.set_frame(frame=7)
            # SHOOT A PROJECTILE
            for slash in player_projectiles:
                # ATTACKING IS DISABLED IF BUTTON B IS BEING PRESSED
                if button_B.state in ["PRESSED", "STILL_PRESSED"]:
                    break
                if attack_debounce >= 1:
                    break
                if not (constants.OUT_LEFT_BOUND < slash.x < constants.OUT_RIGHT_BOUND):
                    slash.move(player.x, player.y)
                    slash.set_frame(rotation=player.rotation)
                    # HANDLE ANIMATION
                    player.set_frame(frame=10)
                    # PLAY THE SOUND
                    attack_sound.play()
                    # DEBOUNCE
                    attack_debounce = 7
                    break
        else:
            button_a_ui.set_frame(frame=6)

        # DECREMENT DEBOUNCE
        attack_debounce = max(attack_debounce - 1, 0)
        # HANDLE ANIMATION
        player_moving = player_moving_horizontally or player_moving_vertically
        # [WALKING]
        if player_moving and 1 <= player.frame <= 7:
            player.set_frame(player.frame + 1)
        elif 1 <= player.frame <= 8:
            player.set_frame(1)
        # [ATTACK]
        elif 9 <= player.frame <= 14:
            player.set_frame(player.frame + 1)
        elif player.frame >= 15:
            player.set_frame(1)

        # ALIGN WITH BOUNDARIES
        new_x = util.clamp(new_x, 0, constants.SCREEN_WIDTH - constants.SPRITE_SIZE)
        new_y = util.clamp(
            new_y,
            constants.GAME_BOUND_TOP + 6,
            constants.GAME_BOUND_BOTTOM - constants.SPRITE_SIZE,
        )

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
        # handle enemies
        handle_enemies()
        # handle waves
        handle_waves()
        # move projectiles
        move_projectiles()
        # RENDER
        game.render_block()
        # WAIT FOR NEXT FRAME
        game.tick()

    while True:
        game_loop()
        # GAME OVER CHECK
        active_enemies = get_active_enemies()
        plr_hitbox_top_x = player.x + 5
        plr_hitbox_top_y = player.y + 5
        plr_hitbox_bottom_x = player.x + 12
        plr_hitbox_bottom_y = player.y + 12
        game_over = False
        for enemy in active_enemies:
            if stage.collide(
                plr_hitbox_top_x,
                plr_hitbox_top_y,
                plr_hitbox_bottom_x,
                plr_hitbox_bottom_y,
                enemy.x,
                enemy.y,
                enemy.x + 16,
                enemy.y + 16,
            ):
                game_over = True
                break
        if game_over:
            # 2 SECONDS
            for counter in range(10):
                attack_sound.play()
                time.sleep(0.2)
            break

    # RETURN THE FINAL SCORE
    return score


def game_over(final_score: int):
    # Image bank for the game over background
    image_bank_background = stage.Bank.from_bmp16("background_bank.bmp")

    # Add text objects
    text_objects = []

    title_text = stage.Text(
        width=32, height=16, font=None, palette=constants.TEXT_PALETTE, buffer=None
    )
    title_text.move(0, 20)
    title_text.text(f"FINAL SCORE: {final_score}")
    text_objects.append(title_text)

    prompt_text = stage.Text(
        width=32, height=16, font=None, palette=constants.TEXT_PALETTE, buffer=None
    )
    prompt_text.move(0, 100)
    prompt_text.text("START-REPLAY GAME")
    text_objects.append(prompt_text)

    # Make the background
    background = stage.Grid(
        image_bank_background, width=10, palette=constants.DAMAGED_PALETTE
    )

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
        if button_START.get_state(keys_pressed) == "RELEASED":
            break


def main():
    while True:
        splash_scene()
        menu_scene()
        final_score = game_scene()
        game_over(final_score)


if __name__ == "__main__":
    main()
