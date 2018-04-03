#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from unity import Unity
from collections import deque
from creep import Creep
from game_state import GameState
from tower import Tower
import application
from mine import Mine
from mock import patch
from world import World
from creep_helper import CreepHelper


class Test(unittest.TestCase):
    labyrinth = ["S.....   ........F  ",
                 "TT   .....TTT      "]

    def test_amount_of_tower_places(self):
        access_cells, tower_places, start, finish, branch_start, branch_end = Unity.identifier(self.labyrinth)
        self.assertEqual(len(tower_places), 5)

    def test_correct_way(self):
        access_cells, tower_places, start, finish, branch_start, branch_end = Unity.identifier(self.labyrinth)
        ways = Unity.build_way(access_cells, start, finish, branch_start, branch_end)
        self.assertEqual(ways[0], deque([[32, 0], [64, 0], [96, 0], [128, 0], [160, 0], [160, 32], [192, 32], [224, 32],
                               [256, 32], [288, 32], [288, 0], [320, 0], [352, 0], [384, 0], [416, 0], [448, 0],
                               [480, 0], [512, 0], [544, 0]]))

    def test_amount_access_cells(self):
        access_cells, tower_places, start, finish, branch_start, branch_end = Unity.identifier(self.labyrinth)
        self.assertEqual(len(access_cells), 18)

    def test_access_cells_content(self):
        access_cells, tower_places, start, finish, branch_start, branch_end = Unity.identifier(self.labyrinth)
        self.assertEqual(access_cells, [[32, 0], [64, 0], [96, 0], [128, 0], [160, 0], [288, 0], [320, 0], [352, 0],
                                        [384, 0], [416, 0], [448, 0], [480, 0], [512, 0], [160, 32], [192, 32],
                                        [224, 32], [256, 32], [288, 32]])

    def test_creep_move_to(self):
        cells = Unity.identifier(self.labyrinth)[0]
        way = deque(cells)
        pos = way.popleft()
        creep = Creep(pos[0], pos[1], way, 1)
        creep.current_pos = [0, 0]
        creep.motion, creep.move_to = Unity.make_direction(creep, creep.speed)
        creep.rect = Unity.take_new_coordinates(creep)

        self.assertEqual(creep.move_to, [64, 0])

    def test_creep_motion(self):
        cells = Unity.identifier(self.labyrinth)[0]
        way = deque(cells)
        pos = way.popleft()
        creep = Creep(pos[0], pos[1], way, 1)
        creep.current_pos = [0, 0]
        creep.motion, creep.move_to = Unity.make_direction(creep, creep.speed)
        creep.rect = Unity.take_new_coordinates(creep)
        self.assertEqual(creep.motion, [1, 0])

    def test_creep_rect(self):
        cells = Unity.identifier(self.labyrinth)[0]
        way = deque(cells)
        pos = way.popleft()
        creep = Creep(pos[0], pos[1], way, 1)
        creep.current_pos = [0, 0]
        creep.motion, creep.move_to = Unity.make_direction(creep, creep.speed)
        creep.rect = Unity.take_new_coordinates(creep)
        self.assertEqual(creep.rect, (33, 0, 65, 32))

    def test_correct_deleting(self):
        with patch('application.Application') as perm_mock:
            perm_mock.game_engine = None
        cells = Unity.identifier(self.labyrinth)[0]
        way = deque(cells)
        pos = way[3]
        pos2 = way[2]
        game_state = GameState(perm_mock)
        creep2 = Creep(pos2[0], pos2[1], way, 1)
        creep = Creep(pos[0], pos[1], way, 1)
        game_state.world.creeps.append(creep)
        game_state.world.creeps.append(creep2)
        i = 0
        while i < 4:
            creep.way.popleft()
            if i < 3:
                creep2.way.popleft()
            i += 1
        game_state.world.creeps[0].health = 0
        tower = Tower(0, 32, 'laser')
        tower.is_blast = True
        tower.level = 2
        tower.attacked_creep = game_state.world.creeps[0]
        game_state.world.towers.append(tower)
        game_state.check_creeps(game_state.world, game_state.gamer)
        self.assertEqual(len(game_state.world.creeps), 2)

    def test_correct_motion(self):
        with patch('application.Application') as perm_mock:
            perm_mock.game_engine = None
        cells = Unity.identifier(self.labyrinth)[0]
        way = deque(cells)
        pos = way[3]
        pos2 = way[2]
        game_state = GameState(perm_mock)
        creep2 = Creep(pos2[0], pos2[1], way, 1)
        creep = Creep(pos[0], pos[1], way, 1)
        game_state.world.creeps.append(creep)
        game_state.world.creeps.append(creep2)
        i = 0
        while i < 4:
            creep.way.popleft()
            if i < 3:
                creep2.way.popleft()
            i += 1
        game_state.world.creeps[0].health = 0
        tower = Tower(0, 32, 'laser')
        tower.is_blast = True
        tower.level = 2
        tower.attacked_creep = game_state.world.creeps[0]
        game_state.world.towers.append(tower)
        game_state.check_creeps(game_state.world, game_state.gamer)
        self.assertEqual(creep.move_to, way[4])

    def test_go_to_the_final(self):
        with patch('application.Application') as perm_mock:
            perm_mock.game_engine = None
        access_cells, tower_places, start, finish, branch_start, branch_end = Unity.identifier(self.labyrinth)
        ways = Unity.build_way(access_cells, start, finish, branch_start, branch_end)
        pos = finish
        game_state = GameState(perm_mock)
        game_state.world.finish = finish
        creep = Creep(pos[0], pos[1], ways[0], 1)
        game_state.world.creeps.append(creep)
        self.assertEqual(game_state.creep_go_to_the_final(creep, game_state.world), True)

    def test_mines(self):
        with patch('application.Application') as perm_mock:
            perm_mock.game_engine = None
        cells = Unity.identifier(self.labyrinth)[0]
        way = deque(cells)
        pos = way[3]
        game_state = GameState(perm_mock)
        creep = Creep(pos[0], pos[1], way, 1)
        mine = Mine(pos[0], pos[1])
        game_state.world.mines.append(mine)
        game_state.world.creeps.append(creep)
        game_state.blast_and_kill(creep, game_state.world, game_state.gamer)
        self.assertEqual(len(game_state.world.mines), 0)

    def test_creeps_after_mines(self):
        with patch('application.Application') as perm_mock:
            perm_mock.game_engine = None
        cells = Unity.identifier(self.labyrinth)[0]
        way = deque(cells)
        pos = way[3]
        game_state = GameState(perm_mock)
        creep = Creep(pos[0], pos[1], way, 1)
        mine = Mine(pos[0], pos[1])
        game_state.world.mines.append(mine)
        game_state.world.creeps.append(creep)
        game_state.blast_and_kill(creep, game_state.world, game_state.gamer)
        self.assertEqual(len(game_state.world.creeps), 1)

    def test_count_seconds(self):
        world = World('level1.txt')
        world.time = 1
        world.count_seconds()
        self.assertEqual(world.start_wave, True)

    def test_create_more_creeps(self):
        world = World('level1.txt')
        world.create_more_creeps()
        self.assertEqual(world.made_creeps, 2)
        self.assertEqual(len(world.creeps), 2)

    def test_initialize_map(self):
        world = World('level1.txt')
        world.initialize_map(self.labyrinth)
        self.assertEqual(world.is_branched, False)

    def test_make_way(self):
        world = World('level1.txt')
        self.assertEqual(len(world.creeps), 1)
        self.assertEqual(world.made_creeps, 1)
        world.make_way()
        self.assertEqual(len(world.creeps), 2)
        self.assertEqual(world.made_creeps, 2)

    def test_update(self):
        world = World('level1.txt')
        world.wave = 1
        world.update()
        self.assertEqual(world.wave, 2)
        self.assertEqual(world.speed, 2)
        self.assertEqual(world.start_wave, False)
        self.assertEqual(world.time, 10)
        self.assertEqual(world.made_creeps, 1)

    def test_blast(self):
        with patch('application.Application') as perm_mock:
            perm_mock.game_engine = None
        game_state = GameState(perm_mock)
        creep = Creep(50, 62, game_state.world.ways[0], 1)
        tower = Tower(50, 62, 'laser')
        game_state.blast(tower, creep)
        self.assertEqual(creep.health, 99)

    def test_blast_and_kill(self):
        with patch('application.Application') as perm_mock:
            perm_mock.game_engine = None
        game_state = GameState(perm_mock)
        creep = Creep(50, 62, game_state.world.ways[0], 1)
        tower = Tower(50, 62, 'laser')
        game_state.world.towers.append(tower)
        game_state.blast_and_kill(creep, game_state.world, game_state.gamer)
        self.assertEqual(creep.health, 99)

    def test_stop_blast(self):
        with patch('application.Application') as perm_mock:
            perm_mock.game_engine = None
        game_state = GameState(perm_mock)
        tower = Tower(50, 62, 'laser')
        creep = Creep(50, 62, game_state.world.ways[0], 1)
        tower.attacked_creep = creep
        game_state.world.towers.append(tower)
        game_state.stop_blast(game_state.world.towers, creep)
        self.assertEqual(game_state.world.towers[0].is_blast, False)
        self.assertEqual(game_state.world.towers[0].attacked_creep, None)

    def test_creep_go_to_the_final(self):
        with patch('application.Application') as perm_mock:
            perm_mock.game_engine = None
        game_state = GameState(perm_mock)
        game_state.world.finish = [90, 88]
        game_state.world.creeps[0].rect = (90, 88, 150, 150)
        self.assertEqual(game_state.creep_go_to_the_final(game_state.world.creeps[0], game_state.world), True)
        game_state.world.creeps[0].rect = (100, 99, 121, 121)
        self.assertNotEqual(game_state.creep_go_to_the_final(game_state.world.creeps[0], game_state.world), True)

    def test_get_reward(self):
        with patch('application.Application') as perm_mock:
            perm_mock.game_engine = None
        game_state = GameState(perm_mock)
        game_state.gamer.money = 100
        game_state.get_reward(game_state.gamer)
        self.assertEqual(game_state.gamer.money, 120)

    def test_check_creeps(self):
        with patch('application.Application') as perm_mock:
            perm_mock.game_engine = None
        game_state = GameState(perm_mock)
        game_state.world.finish = [120, 150]
        creep = Creep(120, 150, game_state.world.ways[0], 2)
        tower = Tower(90, 90, 'laser')
        tower2 = Tower(50, 70, 'laser')
        tower2.attacked_creep = game_state.world.creeps[0]
        tower.attacked_creep = creep
        game_state.world.towers.append(tower)
        game_state.world.towers.append(tower2)
        game_state.world.creeps.append(creep)
        game_state.gamer.life = 10
        game_state.check_creeps(game_state.world, game_state.gamer)
        self.assertEqual(game_state.gamer.life, 9)
        self.assertEqual(len(game_state.world.creeps), 1)
        self.assertEqual(game_state.world.towers[0].attacked_creep, None)
        self.assertNotEqual(game_state.world.towers[1].attacked_creep, None)

    def test_help_creeps(self):
        with patch('application.Application') as perm_mock:
            perm_mock.game_engine = None
        game_state = GameState(perm_mock)
        creep_helper = CreepHelper(100, 150, game_state.world.ways[0], 1)
        creep = Creep(132, 150, game_state.world.ways[0], 1)
        creep.health = 80
        creep.need_help = 26
        game_state.world.creeps.append(creep)
        game_state.world.creeps.append(creep_helper)
        game_state.help_creeps(game_state.world.creeps[2])
        self.assertEqual(game_state.world.creeps[1].health, 90)
        self.assertEqual(game_state.world.creeps[1].doctored, True)
        game_state.world.creeps[1].health = 93
        game_state.world.creeps[1].need_help = 26
        game_state.help_creeps(game_state.world.creeps[2])
        self.assertEqual(game_state.world.creeps[1].health, 100)

    def test_is_enough_money(self):
        with patch('application.Application') as perm_mock:
            perm_mock.game_engine = None
        game_state = GameState(perm_mock)
        game_state.gamer.money = 100
        cost = 60
        self.assertEqual(game_state.is_enough_money(cost, game_state.gamer), True)
        cost = 120
        self.assertEqual(game_state.is_enough_money(cost, game_state.gamer), False)

    def test_wave_is_over(self):
        with patch('application.Application') as perm_mock:
            perm_mock.game_engine = None
        game_state = GameState(perm_mock)
        game_state.world.creeps[0].rect = (20, 20, 50, 100)
        game_state.world.finish = [20, 20]
        game_state.check_creeps(game_state.world, game_state.gamer)
        self.assertEqual(game_state.wave_is_over(game_state.world), True)
        creep = Creep(20, 50, game_state.world.ways[0], 2)
        tower = Tower(30, 50, 'laser')
        tower.level = 2
        creep.health = 0
        game_state.world.creeps.append(creep)
        game_state.world.towers.append(tower)
        game_state.blast_and_kill(game_state.world.creeps[0], game_state.world, game_state.gamer)
        self.assertEqual(game_state.wave_is_over(game_state.world), True)

    def test_kill_game(self):
        with patch('application.Application') as perm_mock:
            perm_mock.game_engine = None
        game_state = GameState(perm_mock)
        game_state.gamer.life = 0
        game_state.kill_game()
        self.assertEqual(game_state.application.state_continuous, False)
        self.assertEqual(game_state.application.ending_message, 'You lose')

    def test_intersects(self):
        with patch('application.Application') as perm_mock:
            perm_mock.game_engine = None
        game_state = GameState(perm_mock)
        creep = Creep(20, 50, game_state.world.ways[0], 2)
        tower = Tower(40, 50, 'laser')
        tower.level = 2
        self.assertEqual(game_state.intersects(tower, creep), True)
        tower = Tower(150, 300, 'freeze')
        self.assertEqual(game_state.intersects(tower, creep), False)

    def test_stop_blast(self):
        tower = Tower(10, 20, 'laser')
        tower.attacked_creep = Creep(10, 20, [0, 0], 1)
        tower.is_blast = True
        tower.stop_blast()
        self.assertEqual(tower.is_blast, False)
        self.assertEqual(tower.attacked_creep, None)

    def test_is_dead(self):
        creep = Creep(10, 20, [50, 50], 2)
        creep.health = 0
        self.assertEqual(creep.is_dead(), True)
        creep.health = 90
        self.assertEqual(creep.is_dead(), False)

    def test_can_be_upgraded(self):
        tower = Tower(10, 20, 'laser')
        self.assertEqual(tower.can_be_upgraded(), True)
        tower.upgrade()
        self.assertEqual(tower.can_be_upgraded(), False)

    def test_upgrade(self):
        tower = Tower(10, 20, 'freeze')
        self.assertEqual(tower.level, 1)
        self.assertEqual(tower.radius.size, 48)
        self.assertEqual(tower.damage, 1)
        tower.upgrade()
        self.assertEqual(tower.level, 2)
        self.assertEqual(tower.radius.size, 80)
        self.assertEqual(tower.damage, 2)

    def test_need_next_cell(self):
        with patch('application.Application') as perm_mock:
            perm_mock.game_engine = None
        game_state = GameState(perm_mock)
        game_state.world.creeps[0].current_pos = [20, 20]
        game_state.world.creeps[0].move_to = [20, 20]
        self.assertEqual(game_state.need_next_cell(game_state.world.creeps[0]), True)


if __name__ == "__main__":
    unittest.main(exit=False)
