import os
import random
import sys

import pygame

from CPUDuck import CPUDuck
from Duck import Duck
from Info import Info
from TrainingDuck import TrainingDuck

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
width = 1300
height = 650
screen = pygame.display.set_mode((width, height))
screen.fill((255, 255, 255))
print("Moving and shooting coefs for initial ducks")
for i in range(Info.initpop):
    Info.ducks.append(CPUDuck(500, screen))
cpu = Info.ducks[0]
Info.currentDuck = 0
# p = Duck(100, screen)
p = TrainingDuck(100, screen)
Info.playerDuck = p
up = False
down = False
playing = False
pauseTime = 0
pauseStart = 0
gen = 1
fps = 60
genLbl = pygame.font.SysFont("Microsoft Yahei UI Light", 40).render("Gen " + str(gen) + " Duck " + str(Info.currentDuck+1), True, (0, 0, 0))
pauseLbl = pygame.font.SysFont("Microsoft Yahei UI Light", 40).render("Press space to pause/unpause, up/down to change fps", True, (0, 0, 0))
modeLbl = pygame.font.SysFont("Microsoft Yahei UI Light", 40).render("Press p to switch mode", True, (0, 0, 0))
while True:
    screen.fill((255, 255, 255))
    screen.blit(genLbl, (int((screen.get_width() - genLbl.get_width())/2), 0))
    screen.blit(pauseLbl, (int((screen.get_width() - pauseLbl.get_width())/2), genLbl.get_height() + 10))
    screen.blit(modeLbl, (int((screen.get_width() - pauseLbl.get_width())/2), genLbl.get_height() + pauseLbl.get_height() + 10))
    events = pygame.event.get()
    mousePos = pygame.mouse.get_pos()
    mouseClick = False

    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                up = True
            if event.key == pygame.K_s:
                down = True
            if event.key == pygame.K_SPACE:
                playing = not playing
                if not playing:
                    pauseStart = pygame.time.get_ticks()
                else:
                    pauseTime += pygame.time.get_ticks() - pauseStart
            if event.key == pygame.K_UP:
                fps += 10
            if event.key == pygame.K_DOWN:
                fps -= 10
            if event.key == pygame.K_p:
                if isinstance(p, Duck):
                    p = TrainingDuck(100, screen)
                else:
                    p = Duck(100, screen)
                Info.playerDuck = p
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                up = False
            if event.key == pygame.K_s:
                down = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseClick = True
    Info.totalTime = pygame.time.get_ticks() - pauseTime
    if cpu.startTime == 0:
        cpu.startTime = Info.totalTime
    if playing:
        if cpu.process([screen.get_width(), screen.get_height(), cpu.cy, p.cy, p.eggs[0].x if len(p.eggs) > 0 else screen.get_width() / 2,
                     p.eggs[0].y if len(p.eggs) > 0 else screen.get_height() / 2, p.eggs[0].angle if len(p.eggs) > 0 else 0]) or Info.totalTime - cpu.startTime >= 10000:
            playing = False
            cpu.fitness = 1999 - cpu.mindist + (Info.totalTime - cpu.startTime)/1000
        if isinstance(p, Duck) and p.tick(up, down, mousePos, mouseClick):
            playing = False
            cpu.fitness = 9999 - (Info.totalTime - cpu.startTime)/1000
        if isinstance(p, TrainingDuck) and p.tick():
            playing = False
            cpu.fitness = 9999 - (Info.totalTime - cpu.startTime)/1000
        if not playing:
            pauseStart = pygame.time.get_ticks()
            if Info.currentDuck == len(Info.ducks)-1:
                gen += 1
                sums = [0] * len(Info.ducks)
                newducks = []
                sums[0] = int(Info.ducks[0].fitness)
                for i in range(1, len(Info.ducks)):
                    sums[i] = sums[i - 1] + int(Info.ducks[i].fitness)
                for i in range(Info.repnum):
                    rand = random.randint(0, sums[len(sums) - 1])
                    j = 0
                    while j < len(sums):
                        if rand < sums[j]:
                            newducks.append(Info.ducks[j])
                            childmoves = []
                            childshoots = []
                            for k in range(7):
                                childmoves.append(Info.ducks[j].movevals[k] + random.randint(-100, 100) / 1000)
                                if k < 5:
                                    childshoots.append(Info.ducks[j].shootvals[k] + random.randint(-50, 50) / 1000)
                            print("Moving and shooting coefs for child ducks")
                            newducks.append(CPUDuck(500, Info.ducks[j].screen, Info.ducks[j], childmoves, childshoots))
                            break
                        j += 1
                Info.ducks = newducks
                Info.currentDuck = 0
                cpu = Info.ducks[Info.currentDuck]
                cpu.rot = 180
                cpu.y = 500
                cpu.eggs.clear()
                cpu.mindist = 9999
                cpu.startTime = Info.totalTime
            else:
                Info.currentDuck += 1
                cpu = Info.ducks[Info.currentDuck]
                cpu.rot = 180
                cpu.y = 500
                cpu.eggs.clear()
                cpu.mindist = 9999
                cpu.startTime = Info.totalTime
            genLbl = pygame.font.SysFont("Microsoft Yahei UI Light", 40).render(
                "Gen " + str(gen) + " Duck " + str(Info.currentDuck + 1), True, (0, 0, 0))
            p = Duck(100, screen) if isinstance(p, Duck) else TrainingDuck(100, screen)
            Info.playerDuck = p
            playing = True

        for i in p.eggs:
            i.tick()
        for i in cpu.eggs:
            i.tick()
            if pow(pow(i.x - p.cx, 2) + pow(i.y - p.cy, 2), 0.5) < cpu.mindist:
                cpu.mindist = pow(pow(i.x - p.cx, 2) + pow(i.y - p.cy, 2), 0.5)
    p.draw()
    cpu.draw()
    for i in p.eggs:
        i.draw()
    for i in cpu.eggs:
        i.draw()
    pygame.display.update()
    pygame.time.Clock().tick(fps)
