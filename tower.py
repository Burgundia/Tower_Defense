#!/usr/bin/env python
# -*- coding: utf-8 -*-
from radius import Radius

CELL_SIZE = 32
RED = "#FF0000"


class Tower:
    def __init__(self, x, y, tower_type):
        self.x = x
        self.y = y
        self.rect = (x, y, x + CELL_SIZE, y + CELL_SIZE)
        self.type = tower_type
        self.image = None
        self.choose_image_name()
        self.level = 1
        self.damage = 1
        self.radius = Radius(x, y, 48)
        self.is_blast = False
        self.attacked_creep = None

    def choose_image_name(self):
        if self.type == "laser":
            self.image = "images/tower_laser.png"
        elif self.type == "freeze":
            self.image = "images/tower_freeze.png"
        else:
            raise NotImplementedError

    def pressed(self, mouse):
        if mouse[0] > self.rect[0]:
            if mouse[1] > self.rect[1]:
                if mouse[0] < self.rect[2]:
                    if mouse[1] < self.rect[3]:
                        return True
            return False

    def can_be_upgraded(self):
        return self.level < 2

    def upgrade(self):
        if self.can_be_upgraded():
            self.level += 1
            self.damage += 1
            self.radius.size += 32

    def stop_blast(self):
        self.is_blast = False
        self.attacked_creep = None
