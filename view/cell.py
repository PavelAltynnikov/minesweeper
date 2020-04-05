# -*- coding: utf-8 -*-
import clr
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import Button


class Cell(Button):
    def __init__(self, location):
        self._active = False
        self._location = location
        self._hidden_value = None

    @property
    def is_active(self):
        return self._active

    @is_active.setter
    def is_active(self, value):
        self._active = value

    @property
    def location(self):
        '''надо переименовать чтобы не было путаницы с Location
        '''
        return self._location

    @property
    def hidden_value(self):
        return self._hidden_value

    @hidden_value.setter
    def hidden_value(self, value):
        self._hidden_value = value
