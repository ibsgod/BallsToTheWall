import random

import pygame

from Egg import Egg
from Info import Info


class CPUDuck:
    def __init__(self, y, screen, parent=None, moves=None, shoots=None):
        self.rot = 180
        self.speed = 2
        self.img = pygame.image.load("duck.png")
        self.size = self.img.get_width()
        self.screen = screen
        self.x = screen.get_width() - self.size
        self.y = y
        self.cx = self.x + self.size/2
        self.cy = self.y + self.size/2
        self.accel = 2
        self.yvel = 0
        self.speed = 30
        self.eggs = []
        # 1300 + 650 + 620 + 620 + 1293 + 643 + 90
        self.eggTimer = 0
        self.startTime = 0
        self.fitness = 0
        self.mindist = 9999
        self.parent = parent
        self.coll = pygame.Rect(self.x, self.y, self.size, self.size)
        # each list contains coefs. for width, height, paddle location, enemy paddle location, egg x and y, egg angle
        if self.parent is None:
            self.movevals = []
            self.shootvals = []
            for i in range(7):
                self.movevals.append(random.randrange(-100, 100) / 100)
                if i < 5:
                    self.shootvals.append(random.randrange(-100, 100) / 100)
        else:
            self.movevals = moves
            self.shootvals = shoots
        print(self.movevals)
        print(self.shootvals)


    def rot_center(self, image, angle):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect().center)
        return rotated_image, (new_rect[0] + self.x, new_rect[1] + self.y)

    def draw(self):
        if self.rot >= 360:
            self.rot -= 360
        tup = self.rot_center(pygame.transform.flip(self.img, False, True), self.rot)
        self.screen.blit(tup[0], tup[1])

    def tick(self, move, shoot):
        if move < 0:
            self.yvel = min(0, max(-self.speed, self.yvel - self.accel))
        elif move > 0:
            self.yvel = min(self.speed, max(0, self.yvel + self.accel))
        else:
            self.yvel += 1 if self.yvel < 0 else -1 if self.yvel > 0 else 0
        self.y = max(min(self.y + self.yvel, self.screen.get_height() - self.size), 0)
        self.coll = pygame.Rect(self.x, self.y, self.size, self.size)
        self.cx = self.x + self.size / 2
        self.cy = self.y + self.size / 2
        if shoot is not None:
            self.rot = min(225, max(135, 180 + shoot/23))
            if pygame.time.get_ticks() > self.eggTimer + Info.eggCd:
                self.eggs.append(Egg(self.cx - 7, self.cy - 7, self.rot, self, self.screen))
                self.eggTimer = pygame.time.get_ticks()
        for i in Info.playerDuck.eggs:
            if i.coll.colliderect(self.coll):
                return True
        return False

    def process(self, info):
        move = 0
        shoot = 0
        for i in range(7):
            move += info[i] * self.movevals[i]
            if i < 5:
                shoot += info[i] * self.shootvals[i]
        return self.tick(move, shoot)








