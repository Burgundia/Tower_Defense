#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Button:
    def __init__(self, x, y, img):
        self.image = img
        self.rect = (x, y, x + 48, y + 48)

    def pressed(self, mouse):
        if mouse[0] > self.rect[0]:
            if mouse[1] > self.rect[1]:
                if mouse[0] < self.rect[2]:
                    if mouse[1] < self.rect[3]:
                        return True
        return False
