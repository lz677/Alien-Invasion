# /usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Zhe LIU
# @Email   : 937150058@qq.com
# @File    : button.py
# @Time    : 2019/8/30 21:00

import pygame.sysfont


class Button:
    def __init__(self, ai_setting, screen, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # set the button's size and other attributes
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.sysfont.SysFont(None, 48)

        # create button's rectangle and put it in the middle
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # create button's only once
        self.prep_meg(msg)

    def prep_meg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
