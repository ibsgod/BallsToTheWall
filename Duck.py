import math

import pygame

from Egg import Egg
from Info import Info


class Duck:
    def __init__(self, y, screen):
        self.rot = 0
        self.img = pygame.image.load("duck.png")
        self.size = self.img.get_width()
        self.screen = screen
        self.x = 0
        self.y = y
        self.speed = 20
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

    def tick(self, up, down, mousePos, mouseClick):
        if up:
            self.y = max(self.y - self.speed, 0)
        elif down:
            self.y = min(self.y + self.speed, self.screen.get_height() - self.size)
        self.cx = self.x + self.size / 2
        self.cy = self.y + self.size / 2
        self.coll = pygame.Rect(self.x, self.y, self.size, self.size)
        if mousePos[0] > self.cx:
            self.rot = math.degrees(math.atan((self.cy - mousePos[1]) / (mousePos[0] - self.cx)))
        elif self.cy > mousePos[1]:
                self.rot = 90
        else:
            self.rot = -90
        if mouseClick and pygame.time.get_ticks() > self.eggTimer + Info.eggCd:
            self.eggs.append(Egg(self.cx - 7, self.cy - 7, self.rot, self, self.screen))
            self.eggTimer = pygame.time.get_ticks()
        for i in Info.ducks[Info.currentDuck].eggs:
            if i.coll.colliderect(self.coll):
                return True
        return False
