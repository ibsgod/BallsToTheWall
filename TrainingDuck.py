import math
import random

import pygame

from Egg import Egg
from Info import Info


class TrainingDuck:
    def __init__(self, y, screen):
        self.rot = 0
        self.img = pygame.image.load("duck.png")
        self.size = self.img.get_width()
        self.screen = screen
        self.x = 0
        self.y = y
        self.accel = 2
        self.yvel = 0
        self.speed = 30
        self.cx = self.x + self.size/2
        self.cy = self.y + self.size/2
        self.eggs = []
        self.eggTimer = 0
        self.coll = pygame.Rect(self.x, self.y, self.size, self.size)

    def rot_center(self, image, angle):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect().center)
        return rotated_image, (new_rect[0] + self.x, new_rect[1] + self.y)

    def draw(self):
        if self.rot >= 360:
            self.rot -= 360
        tup = self.rot_center(self.img, self.rot)
        self.screen.blit(tup[0], tup[1])

    def tick(self):
        move = random.randint(-1, 1)
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
        if pygame.time.get_ticks() > self.eggTimer + Info.eggCd:
            self.rot = math.degrees(math.atan((self.cy - Info.ducks[Info.currentDuck].cy) / (Info.ducks[Info.currentDuck].cx - self.cx)))
            self.eggs.append(Egg(self.cx - 7, self.cy - 7, self.rot, self, self.screen))
            self.eggTimer = pygame.time.get_ticks()
        for i in Info.ducks[Info.currentDuck].eggs:
            if i.coll.colliderect(self.coll):
                return True
        return False
