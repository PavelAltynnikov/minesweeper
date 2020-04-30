# -*- coding: utf-8 -*-
import clr
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import Button, FlatStyle
clr.AddReference('System.Drawing')
from System.Drawing import Color


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

    def set_value(self, value):
        self.Text = value

    def _change_view(self, value, is_bomb):
        if is_bomb:
            self.BackColor = Color.FromArgb(250, 0, 0)
        else:
            self.BackColor = Color.FromArgb(192, 192, 192)
        self.Enabled = False
        self.is_checked = True
        self.Text = value
        self.FlatAppearance.BorderSize = 1
        self.FlatAppearance.BorderColor = Color.FromArgb(128, 128, 128)
        self.FlatStyle = FlatStyle.Flat

    def __str__(self):
        return 'y: {}, x: {}'.format(self._y, self._x)
