# -*- coding: utf-8 -*-
import clr
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import Button


class Cell(Button):
    def __init__(self, y, x):
        self._y = y
        self._x = x
        self._active = False
        self._hidden_value = None

    @property
    def y(self):
        return self._y

    @property
    def x(self):
        return self._x

    @property
    def is_active(self):
        return self._active

    @is_active.setter
    def is_active(self, value):
        self._active = value
