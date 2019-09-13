# /usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Zhe LIU
# @Email   : 937150058@qq.com
# @File    : aline_invasion.py
# @Time    : 2019/8/28 16:18

# import sys
import pygame

from setting import Setting
from ship import Ship
from button import Button
from scoreboard import Scoreboard
from pygame.sprite import Group
from game_stats import GameStats
import game_function as gf


def run_game():
    # Initialize the game and Create a screen object
    pygame.init()
    pygame.display.set_caption("Alien Invasion")
    # create a setting
    ai_setting = Setting()

    # create a screen
    screen = pygame.display.set_mode((ai_setting.screen_width, ai_setting.screen_height))

    # create a stats for storing the information
    stats = GameStats(ai_setting)

    # create a scoreboard 
    scoreboard = Scoreboard(ai_setting, screen, stats)
    # create a ship
    ship = Ship(ai_setting, screen)

    # create a bullet
    bullets = Group()

    # create the alien
    # alien = Alien(ai_setting, screen)
    aliens = Group()

    # create a play button
    play_button = Button(ai_setting, screen, "Play")

    gf.create_fleet(ai_setting, screen, ship, aliens)

    # Main Loop of game's beginning
    while True:
        # update the ship
        gf.check_events(ai_setting, screen, stats, scoreboard, play_button, ship,
                        aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullet(ai_setting, screen, stats, scoreboard, ship, aliens, bullets)
            gf.update_aliens(ai_setting, screen, stats, scoreboard, ship, aliens, bullets)
        # show the update screen
        gf.update_screen(ai_setting, screen, stats, scoreboard, ship,
                         aliens, bullets, play_button)


run_game()
