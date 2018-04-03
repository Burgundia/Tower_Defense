#!/usr/bin/env python
# -*- coding: utf-8 -*-
from creep import Creep
from timer import Timer
from unity import Unity
from creep_helper import CreepHelper

CELL_SIZE = 32


class World:
    def __init__(self, map_name):
        self.access_cells = None
        self.tower_places = None
        self.ways = None
        self.speed = 1
        self.towers = []
        self.creeps = []
        self.mines = []
        self.put_mine = False
        self.boom_mine = None
        self.start_creep = None
        self.start = None
        self.finish = None
        self.branch_start = None
        self.branch_end = None
        self.is_branched = False
        self.wave = 1
        self.made_creeps = 0
        self.current_tower_type = "laser"
        self.upgrade_cost = 40
        self.buy_cost = 60
        self.start_wave = False
        self.time = 10
        self.seconds_timer = Timer(self.count_seconds)
        self.create_creep_timer = Timer(self.create_more_creeps)
        self.map = self.read_from_file(map_name)
        self.initialize_map(self.map)
        self.make_way()

    @staticmethod
    def read_from_file(file_calling):
        with open(file_calling) as file:
            return file.readlines()

    def initialize_map(self, labyrinth):
        self.access_cells, self.tower_places, self.start, self.finish,\
         self.branch_start, self.branch_end = Unity.identifier(labyrinth)
        if self.branch_start is not None and self.branch_end is not None:
            self.is_branched = True
        elif self.branch_start is not None and self.branch_end is None or \
                self.branch_start is None and self.branch_end is not None:
            raise ValueError("Check map branch")

    def count_seconds(self):
        if self.time > 0:
            self.time -= 1
            if self.start_wave:
                self.time = 0
            if self.time == 0:
                self.start_wave = True

    def create_more_creeps(self):
        branches_count = len(self.ways)
        i = self.made_creeps % branches_count
        if self.wave > 1 and self.made_creeps % 4 == 0:
            self.creeps.append(CreepHelper(self.start[0], self.start[1],
                                           self.ways[i], self.speed))
        else:
            self.creeps.append(Creep(self.start[0], self.start[1],
                                     self.ways[i], self.speed))
        self.made_creeps += 1

    def make_way(self):
        self.ways = Unity.build_way(self.access_cells, self.start, self.finish,
                                    self.branch_start, self.branch_end)
        self.start_creep = Creep(self.start[0], self.start[1], self.ways[0],
                                 self.speed)
        self.creeps.append(self.start_creep)
        self.made_creeps += 1

    def update(self):
        self.wave += 1
        if self.wave == 2:
            self.speed += 1
        self.made_creeps = 0
        self.creeps.append(Creep(self.start[0], self.start[1], self.ways[0],
                                 self.speed))
        self.made_creeps += 1
        self.start_wave = False
        self.time = 10
