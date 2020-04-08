# -*- coding: utf-8 -*-
'''
EASY    9х9   = 81  -> 10 бомб -> 12.3%
MEDIUM  16х16 = 256 -> 40 бомб -> 15.6%
HARD    30х16 = 480 -> 99 бомб -> 20.6%
NIGHTMARE - таймер идёт на убыль
'''
import os
from model.field import Field
from view.game_window import GameWindow


class Game(object):
    def __init__(self):
        self._game_over = False
        self._active_bombs = 0
        self._defused_bombs = 0

    @property
    def defused_bombs(self):
        return self._defused_bombs

    @defused_bombs.setter
    def defused_bombs(self, value):
        self._defused_boms = value
        # if self._defused_bombs == 

    def start(self, complexity):
        minesweeper = GameWindow(complexity, self)
        minesweeper.ShowDialog()

    def is_game_over(self):
        pass

    def new_easy_game(self, sender, args):
        form = sender.OwnerItem.OwnerItem.Owner.Parent
        form.Hide()
        self.start(Field(Field.EASY))
        form.Close()

    def new_normal_game(self, sender, args):
        form = sender.OwnerItem.OwnerItem.Owner.Parent
        form.Hide()
        self.start(Field(Field.NORMAL))
        form.Close()

    def new_hard_game(self, sender, args):
        form = sender.OwnerItem.OwnerItem.Owner.Parent
        form.Hide()
        self.start(Field(Field.HARD))
        form.Close()

    @staticmethod
    def close(sender, args):
        os._exit(0)
