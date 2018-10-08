# Jiajia Liang
# jl9pg
import pygame
import gamebox
import random

camera = gamebox.Camera(480, 600)
box = gamebox.from_color(camera.x, camera.y, "Yellow", 60, 60)
enemy = gamebox.from_color(random.randrange(0,480),random.randrange(-300,-100), "white", 65, 20)
background = gamebox.from_image(camera.x, camera.y, "Background_Clouds.png")
collection = gamebox.from_image(random.randrange(0, 480), random.randrange(-200, -100), "hud_keyYellow.png")
collection.scale_by(0.6)

shot = gamebox.from_image(500, 650, "ButtonRound_BlackDark.png")
shot.scale_by(0.25)
shot_time = 0

platforms_list = []
platform1 = [
    gamebox.from_image(camera.x, camera.bottom, "ButtonExtraWide_BeigheDrak.png"),
    gamebox.from_image(random.randrange(0, 480), random.randrange(0, 100), "ButtonExtraWide_BeigheDrak.png"),
    gamebox.from_image(random.randrange(0, 480), random.randrange(50, 200), "ButtonExtraWide_BeigheDrak.png"),
    gamebox.from_image(random.randrange(0, 480), random.randrange(200, 300), "ButtonExtraWide_BeigheDrak.png"),
    gamebox.from_image(random.randrange(0, 480), random.randrange(100, 200), "ButtonExtraWide_BeigheDrak.png"),
    gamebox.from_image(random.randrange(0, 480), random.randrange(200, 300), "ButtonExtraWide_BeigheDrak.png"),
    gamebox.from_image(random.randrange(0, 480), random.randrange(300, 350), "ButtonExtraWide_BeigheDrak.png"),
    gamebox.from_image(random.randrange(0, 480), random.randrange(400, 550), "ButtonExtraWide_BeigheDrak.png")
]

platform2 = [
             gamebox.from_image(random.randrange(0, 480), random.randrange(0, 600),"ButtonExtraWide_GreenDark.png")
]

platform3 = [gamebox.from_image(random.randrange(0, 480), random.randrange(0, 600), "ButtonExtraWide_Black.png"),
]
platform4 = [gamebox.from_image(random.randrange(0, 480), random.randrange(0, 600), "ButtonExtraWide_Black.png"),
]
platform5 = [gamebox.from_image(random.randrange(0, 480), random.randrange(0, 600), "ButtonExtraWide_Black.png"),
]
platform6 = [gamebox.from_image(random.randrange(0, 480), random.randrange(0, 600), "ButtonExtraWide_Black.png"),
]
platforms_list.append(platform1)
platforms_list.append(platform2)
platforms_list.append(platform3)
platforms_list.append(platform4)
platforms_list.append(platform5)
platforms_list.append(platform6)

for platform_list in platforms_list:
    for platform in platform_list:
        platform.scale_by(0.3)

enemy_sheet = gamebox.load_sprite_sheet("enemy_spritesheet.png",2,1)
sheet = gamebox.load_sprite_sheet("p3_spritesheet.png", 3, 7)
background_music = gamebox.load_sound(
        "https://upload.wikimedia.org/wikipedia/commons/0/09/Clementi_Sonatina_Opus_36_Number_5_Movement_III_Rondo.oga")
background_music.play()
time = 0
jump_time = 0
end_game = False
score = 0
show_splash = True
ticks = 0
jumping = False
add_score = False
add_score_time = 0
disappear = False
moving_right1 = True
moving_right2 = False
distance1 = 0
distance2 = 0
moving_up1 = True
moving_up2 = False
height1 = 0
height2 = 0
# splash screen
def splash(keys):
    global show_splash
    camera.clear('black')

    text = gamebox.from_text(camera.x, camera.y, "Dummy Jump", "Arial", 40, 'white', bold=True)
    camera.draw(text)

    name1 = gamebox.from_text(camera.x, camera.y, "Jiajia Liang - jl9pg", "Arial", 20, 'white')
    name1.bottom = text.top
    camera.draw(name1)

    Instruction1 = gamebox.from_text(camera.x, camera.y, "Press LEFT/RIGHT to move", "Arial", 20, 'white')
    Instruction1.top = text.bottom
    camera.draw(Instruction1)

    Instruction2 = gamebox.from_text(camera.x, camera.y, "Press UP to jump", "Arial", 20, 'white')
    Instruction2.top = Instruction1.bottom
    camera.draw(Instruction2)

    Instruction3 = gamebox.from_text(camera.x, camera.y, "Press SPACE to shot", "Arial", 20, 'white')
    Instruction3.top = Instruction2.bottom
    camera.draw(Instruction3)

    directions = gamebox.from_text(camera.x, 420, "Now, press SPACE to start!", "Arial", 20, 'white')
    camera.draw(directions)

    if pygame.K_SPACE in keys:
        show_splash = False
    camera.display()


def tick(keys):
    global jump_time, end_game, score, ticks, jumping, time, add_score, add_score_time, shot_time, disappear
    global moving_right1,moving_right2, distance1,distance2
    global moving_up1,moving_up2,height1,height2
    ticks += 1

    if show_splash:
        splash(keys)
        return
    camera.clear('paleturquoise')

    # moving left and right
    box.image = sheet[0]
    if pygame.K_RIGHT in keys:
        box.image = sheet[(ticks // 3) % 6]
        box.speedx = 5

    if pygame.K_LEFT in keys:
        box.image = sheet[(ticks // 3) % 5 + 7]
        box.speedx = -5

    if box.x <= 0:
        box.x += 480
    if box.x >= 480:
        box.x -= 480

    # drag
    box.speedx *= 0.90
    box.move_speed()

    for platform_list in platforms_list:
        for platform in platform_list:
            if box.bottom_touches(platform):
                box.speedx = 0

    # jumping behaviour
    on_ground = False
    for platform_list in platforms_list:
        for platform in platform_list:
            if box.bottom_touches(platform):
                box.move_to_stop_overlapping(platform)
    for platform_list in platforms_list:
        for platform in platform_list:
           if box.bottom_touches(platform):
                on_ground = True

    box.speedy += 1
    box.speedy *= 0.95
    if pygame.K_UP in keys:
        jumping = True

    if pygame.K_UP in keys and on_ground and jump_time > 20:
        box.speedy = -25
        jump_sound = gamebox.load_sound("Jump.wav")
        jump_sound.play()
        jump_time = 0
    jump_time += 1

    if jumping:
        time += 1
        box.image = sheet[13]
        if time > 30:
            box.image = sheet[0]
            time = 0
            jumping = False
    # green platform
    for platform in platform2:
        if box.bottom_touches(platform):
            disappear = True
        if disappear:
            for platform in platform2:
                platform.speedy += 0.5
                platform.move_speed()
                if platform.top > 600:
                    disappear = False


    # black platform
    for platform in platform3:
        if moving_right1:
            platform.x += 1.5
            distance1 += 2
        else:
            platform.x -= 1.5
            distance1 -= 2
        if distance1 >= 100:
            moving_right1 = False
        if distance1 <= -100:
            moving_right1 = True

    for platform in platform4:
        if moving_right2:
            platform.x += 1
            distance2 += 1
        else:
            platform.x -= 1
            distance2 -= 1
        if distance2 >= 60:
            moving_right2 = False
        if distance2 <= -60:
            moving_right2 = True

    for platform in platform5:
        if moving_up1:
            platform.y -= 1
            height1 -= 1
        else:
            platform.y += 1
            height1 += 1
        if height1 >= 60:
            moving_up1 = True
        if height1 <= -60:
            moving_up1 = False

    for platform in platform6:
        if moving_up2:
            platform.y -= 1
            height2 -= 1
        else:
            platform.y += 1
            height2 += 1
        if height2 >= 60:
            moving_up2 = True
        if height2 <= -60:
            moving_up2 = False

    # rolling the screen
    if box.y < 300 and end_game is not True:
        box.y += max(abs(box.speedy), 2)
        score += 1

        collection.y += max(abs(box.speedy), 2)
        enemy.y += max(abs(box.speedy), 2)
        for platform_list in platforms_list:
            for platform in platform_list:
                platform.y += max(abs(box.speedy), 2)
        for platform_list in platforms_list:
            for platform in platform_list:
                if platform.top > 600:
                    platform_list.remove(platform)


    while len(platform1) < 10:
        platform = gamebox.from_image(random.randrange(0, 480),
                                      random.randrange(-150, -30),
                                      "ButtonExtraWide_BeigheDrak.png")
        platform.scale_by(0.3)
        platform1.append(platform)

    while len(platform2) < 1:
        platform = gamebox.from_image(random.randrange(0, 480),
                                      random.randrange(-300, -100),
                                      "ButtonExtraWide_GreenDark.png")
        platform.scale_by(0.3)
        platform2.append(platform)

    while len(platform3) < 1:
        platform = gamebox.from_image(random.randrange(0, 480),
                                      random.randrange(-300, -10),
                                      "ButtonExtraWide_Black.png")
        platform.scale_by(0.3)
        platform3.append(platform)

    while len(platform4) < 1:
        platform = gamebox.from_image(random.randrange(0, 480),
                                      random.randrange(-300, -10),
                                      "ButtonExtraWide_Black.png")
        platform.scale_by(0.3)
        platform4.append(platform)

    while len(platform5) < 1:
        platform = gamebox.from_image(random.randrange(0, 480),
                                      random.randrange(-300, -10),
                                      "ButtonExtraWide_Black.png")
        platform.scale_by(0.3)
        platform5.append(platform)

    while len(platform6) < 1:
        platform = gamebox.from_image(random.randrange(0, 480),
                                      random.randrange(-300, -10),
                                      "ButtonExtraWide_Black.png")
        platform.scale_by(0.3)
        platform6.append(platform)

    # when to die
    if box.bottom > 600:
            end_game = True
    if 660 > box.bottom > 600:
        die_sound = gamebox.load_sound("die.wav")
        die_sound.play()
    camera.draw(background)

    # collection
    if collection.bottom > 600:
        collection.y = random.randrange(-200, -100)
        collection.x = random.randrange(0, 480)
    if box.touches(collection):
        collect_coins = gamebox.load_sound("Coin.wav")
        collect_coins.play()
        add_score = True
        collection.y = random.randrange(-200, -100)
        collection.x = random.randrange(0, 480)

# enermy
    enemy.image = enemy_sheet[(ticks % 2)]
    enemy.speedx = -1
    if enemy.x <= 0:
        enemy.x += 500
    enemy.move_speed()

    if enemy.bottom > 600:
        enemy.y = random.randrange(-400, -100)
        enemy.x = random.randrange(0, 480)
    if box.touches(enemy):
        enemy_sound = gamebox.load_sound(
            "https://upload.wikimedia.org/wikipedia/commons/4/48/Krusty_laugh_impression.ogg")
        enemy_sound.play()
        end_game = True

     # move the shot
    if pygame.K_SPACE in keys and shot_time > 30:
        shot.center = box.center
        shot.speedy = -10
        shot_time = 0
        shot_sound = gamebox.load_sound("Laser_Shoot.wav")
        shot_sound.play()
    shot.move_speed()
    shot_time += 1

    if shot.touches(enemy):
        enemy.y = random.randrange(-400, -100)
        enemy.x = random.randrange(0, 480)

# draw text
    if end_game:
        for platform_list in platforms_list:
            for platform in platform_list:
                platform.y -= max(box.speedy, 10)
        collection.y -= max(box.speedy, 10)
        enemy.y -= max(box.speedy, 10)
        end_text = gamebox.from_text(camera.x, camera.y, "Game End", "Arial", 50, "Black", bold=True)
        camera.draw(end_text)
        background_music.stop()
    score_text = gamebox.from_text(camera.x, 20, str(score), "arial", 30, "black")

    if add_score:
        add_score_time += 1
        collection_text = gamebox.from_text(camera.x, 20, " +100", "Arial", 30, 'red')
        collection_text.left = score_text.right
        camera.draw(collection_text)
        if add_score_time >= 50:
            add_score = False
            add_score_time = 0
            score += 100
    # draw platforms
    for platform_list in platforms_list:
        for platform in platform_list:
            camera.draw(platform)
    camera.draw(collection)
    camera.draw(box)
    camera.draw(score_text)
    camera.draw(enemy)
    camera.draw(shot)
    camera.display()


gamebox.timer_loop(60, tick)