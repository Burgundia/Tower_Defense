#!/usr/bin/env python
# -*- coding: utf-8 -*-
from stateBase import StateBase


class MainMenuState(StateBase):

    def __init__(self, application):
        super(application)

    def run_loop_once(self):
        self.application.pygameEngine.draw()
        self.spplication.pygameEngine.handleEvents()

    def register_press(self):
        pass
