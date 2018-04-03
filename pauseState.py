#!/usr/bin/env python
# -*- coding: utf-8 -*-
from stateBase import StateBase


class PauseState(StateBase):
    def __init__(self, application):
        super().__init__(application)
        self.handle_keyboard = []
        self.handle_mouse = []
        self.handle_buttons = []

    def pack_data(self):
        texts = []
        texts.append(('pause', 400, 250, 'freesansbold.ttf', 50, (33, 100, 100)))
        return [[], texts, [], [], []]

    def handle_keyboard_events(self, mouse):
        pass

    def get_mouse_handlers(self):
        return []

    def get_button_handlers(self):
        return []

    def get_keyboard_handlers(self):
        return [self.handle_keyboard_events]

    def handle_keyboard_events(self, key):
        self.application.process_stack.pop()
        self.application.current_state = self.application.process_stack[len(self.application.process_stack) - 1]

    def register_mouse_handlers(self, handlers):
        for handle in handlers:
            self.handle_mouse.append(handle)

    def register_button_handlers(self, handlers):
        for handle in handlers:
            self.handle_buttons.append(handle)

    def register_keyboard_handlers(self, handlers):
        for handle in handlers:
            self.handle_keyboard.append(handle)

    def run_loop_once(self):
        self.application.game_engine.handle_private_events()
        self.application.game_engine.draw(self.pack_data())
