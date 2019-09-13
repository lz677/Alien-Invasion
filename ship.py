# /usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Zhe LIU
# @Email   : 937150058@qq.com
# @File    : ship.py
# @Time    : 2019/8/28 17:15

import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_setting, screen):
        super().__init__()
        # init the ship and its position
        self.ai_setting = ai_setting
        self.screen = screen

        # loading the ship image and get its bounding rectangle
        self.image = pygame.image.load('image/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # put every new ship on the bottom center of screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # store float
        self.center = float(self.rect.centerx)

        # moving flag
        self.moving_right = False
        self.moving_left = False

    # 建议可以中间在两个边缘，所以可以多扩宽1/2个图像
    def update(self):
        right_bounding = self.screen_rect.right + int((self.rect.right - self.rect.left) / 2) - 3
        left_bounding = 0 - int((self.rect.right - self.rect.left) / 2) + 3
        if self.moving_right and self.rect.right < right_bounding:
            self.center += self.ai_setting.ship_speed_factor
        if self.moving_left and self.rect.left > left_bounding:
            self.center -= self.ai_setting.ship_speed_factor

        # update the changed value
        self.rect.centerx = self.center

    def drawme(self):
        # draw the ship
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.center = self.screen_rect.centerx
