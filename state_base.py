#!/usr/bin/env python
# -*- coding: utf-8 -*-


class StateBase:

    def __init__(self, application):
        self.application = application

    def run_loop_once(self):
        pass

    def register_mouse_handlers(self, handlers):
        pass

    def register_button_handlers(self, handlers):
        pass

    def register_keyboard_handlers(self, handlers):
        pass

    def get_mouse_handlers(self):
        pass

    def get_button_handlers(self):
        pass

    def get_button_handlers(self):
        pass
