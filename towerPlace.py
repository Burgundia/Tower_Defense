#!/usr/bin/env python
# -*- coding: utf-8 -*-

CELL_SIZE = 32
COLOR = "#FFDAB9"


class TowerPlace:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = 'images/tower_place.png'
        self.rect = (x, y, x + CELL_SIZE, y + CELL_SIZE)

    def pressed(self, mouse):
        if mouse[0] > self.rect[0]:
            if mouse[1] > self.rect[1]:
                if mouse[0] < self.rect[2]:
                    if mouse[1] < self.rect[3]:
                        return True
            return False
