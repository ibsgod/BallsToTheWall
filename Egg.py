import math

import pygame

class Egg:
    def __init__(self, x, y, angle, player, screen):
        self.x = x
        self.y = y
        self.angle = angle
        self.rotate = 0
        self.speed = 20
        self.size = 15
        self.player = player
        self.img = pygame.image.load('egg.png')
        self.coll = pygame.Rect(self.x, self.y, self.size, self.size)
        self.screen = screen

    def rot_center(self, image, angle):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect().center)
        return rotated_image, (new_rect[0] + self.x, new_rect[1] + self.y)

    def draw(self):
        tup = self.rot_center(self.img, self.rotate)
        self.screen.blit(tup[0], tup[1])

    def tick(self):
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y -= math.sin(math.radians(self.angle)) * self.speed
        self.rotate += 10
        self.coll = pygame.Rect(self.x, self.y, self.size, self.size)
        if self.x < 0 or self.y < 0 or self.x - 15 > self.screen.get_width() or self.y - 15 > self.screen.get_height():
            self.player.eggs.remove(self)


