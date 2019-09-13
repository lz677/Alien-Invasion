# /usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Zhe LIU
# @Email   : 937150058@qq.com
# @File    : bullet.py
# @Time    : 2019/8/28 18:40

import pygame
from pygame.sprite import Sprite
import scipy
import matplotlib.pyplot as plt
import numpy as np
import sklearn
import flask



class Bullet(Sprite):

    def __init__(self, ai_setting, screen, ship):
        super().__init__()
        self.screen = screen

        # creat a rectangle of the bullet at (0, 0) and set the right position
        self.rect = pygame.Rect(0, 0, ai_setting.bullet_width, ai_setting.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.y = float(self.rect.y)

        self.color = ai_setting.bullet_color
        self.speed_factor = ai_setting.bullet_speed_factor

    def update(self):
        self.y -= self.speed_factor
        # update
        self.rect.y = self.y

    def draw_bullet(self):
        # draw the bullet on the screen
        pygame.draw.rect(self.screen, self.color, self.rect)
