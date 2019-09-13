# /usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Zhe LIU
# @Email   : 937150058@qq.com
# @File    : aliens.py
# @Time    : 2019/8/29 22:10

import pygame
from pygame.sprite import Sprite


class Alien(Sprite):

    def __init__(self, ai_setting, screen):
        super().__init__()

        self.screen = screen
        self.ai_setting = ai_setting

        # load the aline image and set the rectangle's attributes
        self.image = pygame.image.load('image/alien.bmp')
        self.rect = self.image.get_rect()

        # every alien at the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store alien's position
        self.x = float(self.rect.x)

    def draw_alien(self):
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        # move the aliens to the right side
        self.x += (self.ai_setting.alien_speed_factor * self.ai_setting.fleet_direction)
        self.rect.x = self.x
