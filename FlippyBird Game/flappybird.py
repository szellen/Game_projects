import pygame
import gamebox
import random
camera = gamebox.Camera(400,400)

bird = gamebox.from_color(camera.x, camera.y,"yellow",15,15)
end_text = gamebox.from_text(camera.x,camera.y,"Game over","Arial",50,"black",bold = True)

pillars_up = [
    gamebox.from_color(100, 0, "red", 20, 170),
    gamebox.from_color(300, 0, "red", 20, 412),]

pillars_down = [
    gamebox.from_color(100, 400, "red", 20, 80),
    gamebox.from_color(300, 400, "red", 20, 160)]

end_game = False
ticks = 0
def tick(keys):
    global end_game
    global ticks
    ticks += 1

    camera.clear("white")

    x = random.randrange(100, 400)
    y = random.randrange(100, 400)
    if 400-x/2 - y/2 < 60:
        x = random.randrange(50, 300)
        y = random.randrange(50, 300)

    for pillar in pillars_up:
        pillar.x -= 7
        if bird.touches(pillar):
            end_game = True
        if pillar.x < camera.left:
            pillar.x += 400
            pillar.size = [20, x]
        camera.draw(pillar)

    for pillar in pillars_down:
        pillar.x -= 7
        if bird.touches(pillar):
            end_game = True
        if pillar.x < camera.left:
            pillar.x += 400
            pillar.size = [20, y]
        camera.draw(pillar)

    if pygame.K_SPACE in keys:
        bird.y -= 12
    bird.y += 6
    bird.move_speed()

    if bird.y < 0:
        end_game = True
    if bird.y > 400:
        end_game = True

    camera.draw(bird)

    for pillar in pillars_up:
        camera.draw(pillar)
    for pillar in pillars_down:
        camera.draw(pillar)

    score = gamebox.from_text(camera.x, 250, "scores:" + str(ticks // 30),"Arial", 30, "black", bold=True)

    if end_game:
        gamebox.pause()
        camera.draw(end_text)
        camera.draw(score)

    camera.display()

gamebox.timer_loop(30, tick)