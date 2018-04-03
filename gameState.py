#!/usr/bin/env python
# -*- coding: utf-8 -*-
from stateBase import StateBase
from world import World
from gamer import Gamer
from tower import Tower
from unity import Unity
from enum import Enum
from pauseState import PauseState
from mine import Mine
from creep_helper import CreepHelper

CELL_SIZE = 32
buttons = Enum('Buttons', 'laser freeze wave pause mine')


class GameState(StateBase):
    def __init__(self, application):
        super().__init__(application)
        self.world = World('level1.txt')
        self.gamer = Gamer()
        self.handle_keyboard = []
        self.handle_mouse = []
        self.handle_buttons = []
        self.change_map = True

    def register_mouse_handlers(self, handlers):
        for handle in handlers:
            self.handle_mouse.append(handle)

    def register_button_handlers(self, handlers):
        for handle in handlers:
            self.handle_buttons.append(handle)

    def register_keyboard_handlers(self, handlers):
        for handle in handlers:
            self.handle_keyboard.append(handle)

    def play_logic(self, world, gamer):
        self.check_creeps(world, gamer)
        self.activate_timer()
        if self.world.wave == 5 and len(self.world.creeps) == 0:
            self.kill_game()
        if self.world.start_wave:
            self.stop_timer()
            self.move_creeps(world.creeps)
            self.activate_many_creeps()
            self.stop_creating_creeps()
        self.update_level(world)
        if self.world.wave == 3 and self.change_map:
            self.world = World('level2.txt')
            self.world.wave = 3
            self.world.speed = 2
            self.change_map = False
        if self.gamer.life <= 0:
            self.kill_game()

    def kill_game(self):
        self.application.state_continuous = False
        if self.gamer.life <= 0:
            self.application.ending_message = 'You lose'
        else:
            self.application.ending_message = 'Congratulations! Your scores: ' + str(self.gamer.money)

    def activate_timer(self):
        if not self.world.seconds_timer.active and not self.world.start_wave:
            self.world.seconds_timer.start()

    def stop_timer(self):
        if self.world.seconds_timer.active:
                self.world.seconds_timer.stop()

    def activate_many_creeps(self):
        if len(self.world.creeps) == 1 and self.world.creeps[0].current_pos == self.world.ways[0][1]:
            self.world.create_creep_timer.start()

    def stop_creating_creeps(self):
        if self.world.made_creeps > 7 + self.world.wave * 2:
            self.world.create_creep_timer.stop()

    def update_level(self, world):
        if self.wave_is_over(world) and self.world.made_creeps > 7 + self.world.wave * 2:
            world.update()

    def check_creeps(self, world, gamer):
        for creep in world.creeps[:]:
            if self.creep_go_to_the_final(creep, world):
                self.gamer.life -= 1
                self.world.creeps.remove(creep)
                self.stop_blast(world.towers, creep)
                continue
            if self.need_next_cell(creep):
                self.make_direction(creep, creep.speed)
            self.blast_and_kill(creep, world, gamer)
            self.help_creeps(creep)

    def help_creeps(self, creep):
        if isinstance(creep, CreepHelper):
            for sec_creep in self.world.creeps:
                if creep.intersects(sec_creep) and sec_creep.health < 100:
                    if sec_creep.need_help % 13 == 0:
                        if sec_creep.health + 10 < 100:
                            sec_creep.health += 10
                            sec_creep.doctored = True
                        else:
                            sec_creep.health = 100
                            sec_creep.doctored = True
                sec_creep.need_help += 1
        for creeper in self.world.creeps:
            if creeper.need_help % 8 == 0 and creeper.doctored:
                creeper.doctored = False

    @staticmethod
    def wave_is_over(world):
        return len(world.creeps) == 0

    @staticmethod
    def creep_go_to_the_final(creep, world):
        return [creep.rect[0], creep.rect[1]] == world.finish

    def blast_and_kill(self, creep, world, gamer):
        for mine in world.mines:
            if mine.intersects(creep):
                self.world.mines.remove(mine)
                self.world.creeps.remove(creep)
                self.world.boom_mine = mine
                self.gamer.money += 20
        for tower in world.towers:
            if not tower.is_blast or tower.attacked_creep == creep:
                if self.intersects(tower, creep):
                    self.blast(tower, creep)
                    if creep.is_dead():
                        self.world.creeps.remove(creep)
                        self.stop_blast(self.world.towers, creep)
                        self.get_reward(self.gamer)
                        tower.attacked_creep = None
                        break
                    if creep not in self.world.creeps:
                        tower.attacked_creep = None
                        tower.is_blast = False
                else:
                    if tower.attacked_creep is not None:
                        tower.attacked_creep.speed = world.speed
                        tower.is_blast = False
                    tower.attacked_creep = None

    @staticmethod
    def blast(tower, creep):
        creep.health -= tower.damage
        tower.is_blast = True
        tower.attacked_creep = creep
        if tower.type == "freeze":
            creep.speed = 1

    @staticmethod
    def stop_blast(towers, creep):
        for tower in towers:
            if tower.attacked_creep == creep:
                tower.stop_blast()

    @staticmethod
    def get_reward(gamer):
        gamer.money += 20

    @staticmethod
    def move_creeps(creeps):
        for creep in creeps:
            creep.rect = Unity.take_new_coordinates(creep)
            creep.current_pos[0] += creep.motion[0]
            creep.current_pos[1] += creep.motion[1]

    @staticmethod
    def need_next_cell(creep):
        current_pos = creep.current_pos
        next_pos = creep.move_to
        if next_pos is None:
            return True
        return current_pos == next_pos

    @staticmethod
    def make_direction(creep, speed):
        creep.motion, creep.move_to = Unity.make_direction(creep, creep.speed)

    @staticmethod
    def intersects(tower, creep):
        size = 0
        left = tower.radius.x - tower.radius.size
        top = tower.radius.y - tower.radius.size
        if tower.level == 1:
            size = 32 * 3
        elif tower.level == 2:
            size = 32 * 5
        creep_rect = creep.rect
        if creep_rect[0] >= left and creep_rect[2] <= left + size:
            if top <= creep_rect[1] and top + size >= creep_rect[3]:
                return True
        return False

    def pack_creeps(self):
        images = []
        texts = []
        circles = []
        for creep in self.world.creeps:
            images.append((creep.image, creep.rect))
            texts.append((str(creep.health), creep.rect[0] + 5, creep.rect[1] - 5, 'freesansbold.ttf', 12))
            if isinstance(creep, CreepHelper):
                x = creep.rect[0] + 16
                y = creep.rect[1] + 16
                circles.append((x, y, creep.radius.size, (255, 0, 0)))
            if creep.doctored:
                texts.append(('+10', creep.rect[0] + 5, creep.rect[1] - 12, 'freesansbold.ttf', 12, (0, 255, 0)))
        return images, texts, circles

    def pack_mines(self):
        images = []
        for mine in self.world.mines:
            images.append((mine.image, mine.rect))
        if self.world.boom_mine is not None:
            images.append(('images/boom.png',self.world.boom_mine.rect))
            self.world.boom_mine = None
        return images

    def pack_way(self):
        rectangles = []
        rectangles.append((self.world.start, (105, 105, 105)))
        rectangles.append((self.world.finish, (105, 105, 105)))
        if self.world.is_branched:
            rectangles.append((self.world.branch_start, (105, 105, 105)))
            rectangles.append((self.world.branch_end, (105, 105, 105)))
        for cell in self.world.access_cells:
            rectangles.append((cell, (105, 105, 105)))
        return rectangles

    def pack_tower_places(self):
        images = []
        for tower_place in self.world.tower_places:
            images.append((tower_place.image, tower_place.rect))
        return images

    def pack_towers_and_features(self):
        images = []
        circles = []
        lines = []
        for tower in self.world.towers:
            images.append((tower.image, tower.rect))
            circles.append((tower.radius.x, tower.radius.y, tower.radius.size, tower.radius.color))
            if tower.attacked_creep is not None:
                start = (tower.x + 16, tower.y + 16)
                creep = tower.attacked_creep
                end = (creep.rect[0] + 16, creep.rect[1] + 16)
                if tower.type == 'laser':
                    color = (255, 0, 0)
                elif tower.type == 'freeze':
                    color = (100, 149, 237)
                else:
                    raise NotImplementedError
                lines.append((start, end, color))
        return images, circles, lines

    def pack_texts(self):
        texts = list()
        texts.append(('level: ' + str(self.world.wave), 815, 420))
        texts.append((str(self.world.time) + ' sec', 820, 70))
        texts.append((self.gamer.get_info()[0], 820, 100, 'freesansbold.ttf', 18, (0, 155, 0)))
        texts.append((self.gamer.get_info()[1], 820, 120, 'freesansbold.ttf', 15, (100, 100, 250)))
        texts.append(('tower type:', 815, 350, 'freesansbold.ttf', 15, (0, 1, 99)))
        if self.world.current_tower_type == 'laser':
            color = (255, 0, 0)
        else:
            color = (0, 0, 255)
        texts.append((self.world.current_tower_type, 820, 370, 'freesansbold.ttf', 15, color))
        if self.world.put_mine:
            texts.append(("put mine!", 820, 420))
        return texts

    def pack_data(self):
        images, circles, lines = self.pack_towers_and_features()
        img, texts, circl = self.pack_creeps()
        images += img
        circles += circl
        images += self.pack_tower_places()
        rectangles = self.pack_way()
        texts += self.pack_texts()
        images += self.pack_mines()
        return [images, texts, rectangles, circles, lines]

    @staticmethod
    def is_enough_money(cost, gamer):
        return gamer.money - cost >= 0

    def handle_button_events(self, button):
        if button == buttons.wave:
            self.world.start_wave = True
        elif button == buttons.laser:
            self.world.current_tower_type = "laser"
        elif button == buttons.freeze:
            self.world.current_tower_type = "freeze"
        elif button == buttons.pause:
            '''
            state_pause = PauseState
            self.application.add_new_state(state_pause)
            '''
            pass
        elif button == buttons.mine:
            self.world.put_mine = not self.world.put_mine

    def handle_mouse_events(self, mouse):
        for tower in self.world.towers:
            if tower.pressed(mouse) and self.world.current_tower_type == tower.type and not self.world.put_mine:
                if self.is_enough_money(self.world.upgrade_cost, self.gamer) and tower.can_be_upgraded():
                    self.gamer.money -= self.world.upgrade_cost
                    tower.upgrade()
                else:
                    pass
                    #printCostMessage()
        for cell in self.world.tower_places:
            if cell.pressed(mouse) and not self.world.put_mine:
                if self.is_enough_money(self.world.buy_cost, self.gamer):
                    self.gamer.money -= self.world.buy_cost
                    self.world.tower_places.remove(cell)
                    self.world.towers.append(Tower(cell.x, cell.y, self.world.current_tower_type))
                else:
                    pass
                    #printCostMessage()
        if self.world.put_mine:
            inter = False
            mine = Mine((mouse[0] // 32) * 32, (mouse[1] // 32) * 32)
            for tower in self.world.towers:
                if mine.intersects(tower):
                    inter = True
            for creep in self.world.creeps:
                if mine.intersects(creep):
                    inter = True
            for tow_pl in self.world.tower_places:
                if mine.intersects(tow_pl):
                    inter = True
            if not inter:
                if self.is_enough_money(20, self.gamer):
                    self.world.mines.append(mine)
                    self.gamer.money -= 20
                self.world.put_mine = False


    def handle_timer_events(self):
        if self.world.time > 0:
            self.world.time -= 1
            if self.world.time == 0:
                self.world.start_wave = True

    def get_mouse_handlers(self):
        return [self.handle_mouse_events]

    def get_button_handlers(self):
        return [self.handle_button_events]

    def get_keyboard_handlers(self):
        return []

    def run_loop_once(self):
        self.application.game_engine.handle_private_events()
        self.play_logic(self.world, self.gamer)
        self.application.game_engine.draw(self.pack_data(), self.world.put_mine)