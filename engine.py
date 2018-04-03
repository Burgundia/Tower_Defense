#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from button import Button
from game_state import buttons

BACKGROUND_COLOR = "#E6E6FA"
CELL_SIZE = 32
WIN_WIDTH = 900
WIN_HEIGHT = 600
game_continues = True


class GameEngine:
    def __init__(self, application):
        pygame.init()
        self.font = 'freesansbold.ttf'
        self.font_color = (0, 0, 0)
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Tower Defense")
        self.buttons = self.create_buttons()
        self.application = application
        self.mouse_coord = None

    def handle_general_events(self):
        if pygame.event.get(pygame.QUIT):
            self.off()

    def handle_private_events(self):
        self.mouse_coord = pygame.mouse.get_pos()
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                for handle in self.application.current_state.handle_mouse:
                    handle(mouse)
                for handle in self.application.current_state.handle_buttons:
                    handle(self.button_handler(mouse))
            if e.type == pygame.KEYDOWN:
                for handle in self.application.current_state.handle_keyboard:
                    handle(e.key)

    def button_handler(self, mouse):
        if self.buttons[0].pressed(mouse):
            return buttons.wave
        elif self.buttons[1].pressed(mouse):
            return buttons.pause
        elif self.buttons[2].pressed(mouse):
            return buttons.laser
        elif self.buttons[3].pressed(mouse):
            return buttons.freeze
        elif self.buttons[4].pressed(mouse):
            return buttons.mine

    @staticmethod
    def print_cost_message():  # class TextComments
        print("you have not enough money")

    def draw(self, data, draw_cursor):
        images, texts, rectangles, circles, lines = data
        self.screen.fill(pygame.Color(BACKGROUND_COLOR))
        for rect in rectangles:
            self.draw_rect(*rect)
        for img in images:
            self.draw_image(*img)
        for text in texts:
            self.draw_text(*text)
        for circle in circles:
            self.draw_circle(*circle)
        for line in lines:
            self.draw_line(*line)
        for button in self.buttons:
            self.draw_image(button.image, button.rect)
        if draw_cursor:
            self.draw_rect(((self.mouse_coord[0] // 32) * 32,
                            (self.mouse_coord[1] // 32) * 32), (255, 0, 0))
        pygame.display.update()

    def draw_text(self, data, x, y, font='freesansbold.ttf', size=16,
                  color=(0, 0, 0)):
        text_to_draw = pygame.font.Font(font, size).render(data, 0, color)
        self.screen.blit(text_to_draw, (x, y))

    def draw_image(self, image, rect):
        py_img = pygame.image.load(image)
        py_rect = pygame.Rect(rect)
        self.screen.blit(py_img, py_rect)

    def draw_circle(self, x, y, size, color=(0, 0, 0), thickness=1):
        pygame.draw.circle(self.screen, color, (x, y), size, thickness)

    def draw_line(self, start, end, color=(0, 0, 0), thickness=2):
        pygame.draw.line(self.screen, color, start, end, thickness)

    def draw_rect(self, rect, color):
        py_rect = pygame.Rect(rect[0], rect[1], CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, color, py_rect)

    def set_font(self, font_file, size, color):
        self.font = pygame.font.Font(font_file, size)
        self.font_color = color

    def off(self):
        pygame.quit()
        self.application.state_continuous = False

    @staticmethod
    def create_buttons():
        buttons = []
        button_wave = Button(820, 0, "images/button_wave.png")
        button_pause = Button(820, 150, "images/button_pause.png")
        laser_button = Button(820, 250, "images/laser.png")
        freeze_button = Button(852, 250, "images/freeze.png")
        mine_button = Button(820, 285, "images/mine.png")
        buttons.append(button_wave)
        buttons.append(button_pause)
        buttons.append(laser_button)
        buttons.append(freeze_button)
        buttons.append(mine_button)
        return buttons
