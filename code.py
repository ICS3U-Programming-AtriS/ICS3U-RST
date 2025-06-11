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
    # 0.5 SECONDS
    time.sleep(0.5)


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
    game_over = False
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
    image_bank_enemy = stage.Bank.from_bmp16("bank2.bmp")

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
            game_area.tile(x=counter_x, y=counter_y, tile=4)
        # BRICKS
        for counter_y in range(
            constants.GAME_AREA_HEIGHT_IN_SPRITES,
            constants.GAME_AREA_HEIGHT_IN_SPRITES + 2
        ):
            game_area.tile(x=counter_x, y=counter_y, tile=5)
    game_area.move(x=0, y=constants.GAME_BOUND_TOP + 16)

    # BUTTONS
    button_right_ui = stage.Sprite(image_bank_background, frame=6, x=42, y=106, rotation=0)
    button_left_ui = stage.Sprite(image_bank_background, frame=6, x=22, y=106, rotation=2)
    button_up_ui = stage.Sprite(image_bank_background, frame=6, x=32, y=100, rotation=1)
    button_down_ui = stage.Sprite(image_bank_background, frame=6, x=32, y=112, rotation=3)
    button_a_ui = stage.Sprite(image_bank_background, frame=6, x=140, y=102, rotation=1)
    button_uis = [button_a_ui, button_down_ui, button_left_ui, button_right_ui, button_up_ui]
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
                if stage.collide(top_corner_x, top_corner_y , bottom_corner_x, bottom_corner_y, enemy.x, enemy.y, enemy.x + 16, enemy.y + 16):
                    enemy.hp -= 1
                    enemy.set_frame(6)
                    if enemy.hp <= 0:
                        enemy.move(x=constants.OFFSCREEN_X, y=constants.OFFSCREEN_Y)
                        score += 10
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


    def shoot_towards_player(enemy):
        pass

    def get_active_enemies():
        return [enemy for enemy in enemies if enemy.y >= 0]
    def get_inactive_enemies():
        return [enemy for enemy in enemies if enemy.y < 0]
        
    def handle_enemies():
        active_enemies = get_active_enemies()
        for enemy in active_enemies:
            new_x = enemy.x 
            new_y = enemy.y
            if enemy.x <= 3:
                new_x += 5
            elif enemy.x >= constants.SCREEN_WIDTH - 21:
                new_x -= 5
            
            if enemy.enemy_id == 1:
                if enemy.x < player.x:
                    new_x += random.randint(0, enemy.movement_speed)
                else:
                    new_x -= random.randint(0, enemy.movement_speed)
                if enemy.y < player.y:
                    new_y += random.randint(0, enemy.movement_speed)
                else:
                    new_y -= random.randint(0, enemy.movement_speed)
            elif enemy.enemy_id == 2:
                if enemy.x < player.x:
                    new_x += random.randint(1-(enemy.movement_speed), enemy.movement_speed)
                else:
                    new_x -= random.randint(1-(enemy.movement_speed), enemy.movement_speed)
                if enemy.y < player.y:
                    new_y += random.randint(1-(enemy.movement_speed), enemy.movement_speed)
                else:
                    new_y -= random.randint(1-(enemy.movement_speed), enemy.movement_speed)
            elif enemy.enemy_id == 3:
                if enemy.x < player.x:
                    new_x += random.randint(2-(enemy.movement_speed), enemy.movement_speed)
                else:
                    new_x -= random.randint(2-(enemy.movement_speed), enemy.movement_speed)
                if enemy.y < player.y:
                    new_y += random.randint(2-(enemy.movement_speed), enemy.movement_speed)
                else:
                    new_y -= random.randint(2-(enemy.movement_speed), enemy.movement_speed)
            
            if enemy.frame == 6:
                if enemy.enemy_id == 1:
                    enemy.set_frame(frame=0)
                elif enemy.enemy_id == 2:
                    enemy.set_frame(frame=5)
                elif enemy.enemy_id == 3:
                    enemy.set_frame(frame=7)

            enemy.move(new_x, new_y)

    def spawn_enemy(enemy_id, enemy_power):
        inactive_enemies = get_inactive_enemies()
        if inactive_enemies == []:
            return
        new_enemy = inactive_enemies[0]
        start_pos_x = [-16, constants.SCREEN_WIDTH][random.randint(0,1)]
        start_pos_y = random.randint(constants.GAME_BOUND_TOP + 6, constants.GAME_BOUND_BOTTOM - constants.SPRITE_SIZE)
        new_enemy.hp = 2 + (enemy_power // 4)
        if enemy_id == 1:
            new_enemy.set_frame(frame=0)
            new_enemy.movement_speed = 1
        elif enemy_id == 2:
            new_enemy.set_frame(frame=5)
            new_enemy.movement_speed = 2
        elif enemy_id == 3:
            new_enemy.set_frame(frame=7)
            new_enemy.movement_speed = 2
        new_enemy.enemy_id = enemy_id
        new_enemy.move(x=start_pos_x, y=start_pos_y)
    
    wave_num = 0
    def handle_waves():
        enemy_count = len(get_active_enemies())
        if enemy_count == 0:
            wave_num += 1
            for counter in range(min(random.randint(1 + wave_num//2, wave_num), constants.ENEMY_LIMIT)):
                battle_power = random.randint(1, wave_num)
                enemy_id = random.randint(1, 3) if wave_num >= 3 else 1
                spawn_enemy(enemy_id, battle_power)
            
            

        

    # SET THE LAYERS FOR THE GAME
    # ... > PLAYER > GAME_AREA > BACKGROUND
    game.layers = [score_text] + enemies + player_projectiles + button_uis + [player, game_area, background]

    # Function that handles scrolling the background
    def scroll_background():
        background.x += 1
        if background.x >= 0:
            background.x = -16
        background.move(background.x, background.y)

    # CREATE BUTTONS
    left_button = util.Button(ugame.K_LEFT)
    right_button = util.Button(ugame.K_RIGHT)
    up_button = util.Button(ugame.K_UP)
    down_button = util.Button(ugame.K_DOWN)
    button_A = util.Button(ugame.K_O)

    # CREATE SOUNDS
    attack_sound = util.Sound("click")

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
            button_left_ui.set_frame(frame=7)
            new_x -= constants.PLAYER_SPEED
            # FLIP PLAYER SPRITE
            player.set_frame(rotation=4)
            player_moving = not player_moving
        else:
            button_left_ui.set_frame(frame=6)
        if right_button.get_state(keys_pressed) in ["PRESSED", "STILL_PRESSED"]:
            button_right_ui.set_frame(frame=7)
            new_x += constants.PLAYER_SPEED
            player.set_frame(rotation=0)
            player_moving = not player_moving
        else:
            button_right_ui.set_frame(frame=6)
        if up_button.get_state(keys_pressed) in ["PRESSED", "STILL_PRESSED"]:
            button_up_ui.set_frame(frame=7)
            new_y -= constants.PLAYER_SPEED
            player_moving = True
        else:
            button_up_ui.set_frame(frame=6)
        if down_button.get_state(keys_pressed) in ["PRESSED", "STILL_PRESSED"]:
            button_down_ui.set_frame(frame=7)
            new_y += constants.PLAYER_SPEED
            player_moving = True
        else:
            button_down_ui.set_frame(frame=6)
            

        # IF THE PLAYER PRESSES THE A BUTTON, PLAY THE SOUND
        # CHECK IF THE BUTTON WAS JUST PRESSED
        if button_A.get_state(keys_pressed) in ["PRESSED", "STILL_PRESSED"]:
            button_a_ui.set_frame(frame=7)
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
                    attack_sound.play()
                    # DEBOUNCE
                    attack_debounce = 7
                    break
        else:
            button_a_ui.set_frame(frame=6)

        # DECREMENT DEBOUNCE
        attack_debounce = max(attack_debounce - 1, 0)
        # HANDLE ANIMATION
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
        new_y = util.clamp(new_y, constants.GAME_BOUND_TOP + 6, constants.GAME_BOUND_BOTTOM - constants.SPRITE_SIZE)

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
            if stage.collide(plr_hitbox_top_x, plr_hitbox_top_y, plr_hitbox_bottom_x, plr_hitbox_bottom_y, enemy.x, enemy.y, enemy.x + 16, enemy.y + 16):
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

def game_over(final_score:int):
    # Image bank for the game over background
    image_bank_background = stage.Bank.from_bmp16("bank2.bmp")

    # Add text objects
    text_objects = []

    title_text = stage.Text(
        width=32, height=16, font=None, palette=constants.TEXT_PALETTE, buffer=None
    )
    title_text.move((constants.SCREEN_WIDTH / 2) - title_text.width, 20)
    title_text.text(f"FINAL SCORE: {final_score}")
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

def main():
    while True:
        splash_scene()
        menu_scene()
        final_score = game_scene()
        game_over(final_score)


if __name__ == "__main__":
    main()