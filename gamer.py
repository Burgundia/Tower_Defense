#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Gamer:
    def __init__(self):
        self.money = 200
        self.life = 20

    def get_info(self):
        text1 = '{} lifes'.format(self.life)
        text2 = '{} points'.format(self.money)
        return text1, text2
