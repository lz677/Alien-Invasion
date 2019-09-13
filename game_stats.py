# /usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Zhe LIU
# @Email   : 937150058@qq.com
# @File    : game_stats.py
# @Time    : 2019/8/30 14:47


class GameStats:
    # fallow the game's statistical information
    def __init__(self, ai_setting):
        self.ai_setting = ai_setting
        self.reset_stats()
        self.game_active = False
        self.high_score = 0

    def reset_stats(self):
        # initialize the changeable information when gaming
        self.ships_left = self.ai_setting.ship_limit
        self.score = 0
        self.level = 1

