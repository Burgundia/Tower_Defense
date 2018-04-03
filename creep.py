#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import deque

CELL_SIZE = 32
COLOR = "#888888"


class Creep:
    def __init__(self, x, y, way, speed):
        self.x = x
        self.y = y
        self.motion = None
        self.image = 'images/enemy.png'
        self.rect = (x, y, x + CELL_SIZE, y + CELL_SIZE)
        self.health = 100
        self.way = deque(way)
        self.move_to = None
        self.current_pos = [x, y]
        self.speed = speed
        self.need_help = 0
        self.doctored = False

    def is_dead(self):
        return self.health <= 0
