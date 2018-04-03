#!/usr/bin/env python
# -*- coding: utf-8 -*-
from game_state import GameState
from engine import GameEngine
from pause_state import PauseState


class Application:

    def __init__(self):
        self.process_stack = []
        self.game_engine = GameEngine(self)
        self.state_continuous = True
        self.current_state = None
        self.ending_message = ''

    def run(self):
        game_state = GameState(self)
        self.current_state = game_state
        self.add_new_state(game_state)
        while len(self.process_stack) != 0:
            self.game_engine.handle_general_events()
            if not self.state_continuous:
                break
            self.current_state = self.process_stack[-1]
            self.current_state.run_loop_once()
        print(self.ending_message)

    def add_new_state(self, state):
        self.process_stack.append(state)
        self.current_state = state
        self.current_state.register_mouse_handlers(state.get_mouse_handlers())
        self.current_state.register_button_handlers(state.get_button_handlers())
        self.current_state.register_keyboard_handlers(state.get_keyboard_handlers())
        # for keyboard

    def get_game_engine(self):
        return self.game_engine
