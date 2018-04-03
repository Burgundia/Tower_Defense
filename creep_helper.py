#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import deque
from creep import Creep
from radius import Radius

CELL_SIZE = 32
COLOR = "#888888"


class CreepHelper(Creep):
    def __init__(self, x, y, way, speed):
        super().__init__(x, y, way, speed)
        self.image = 'images/helper.png'
        self.radius = Radius(x, y, 100)

    def intersects(self, creep):
        size = self.radius.size
        left = self.rect[0] + 16 - self.radius.size
        top = self.rect[1] + 16 - self.radius.size
        creep_rect = creep.rect
        if creep_rect[0] >= left and creep_rect[2] <= left + size * 2:
            if top <= creep_rect[1] and top + size * 2 >= creep_rect[3]:
                return True
        return False
