# -*- coding: utf-8 -*-
import clr
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import Button


class Cell(Button):
    def __init__(self, y, x):
        self._y = y
        self._x = x
        self._checked = False

    @property
    def y(self):
        return self._y

    @property
    def x(self):
        return self._x

    @property
    def is_checked(self):
        return self._checked

    @is_checked.setter
    def is_checked(self, value):
        self._checked = value

    def OnGotFocus(self, *args):
        self.NotifyDefault(False)
