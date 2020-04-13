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
        self._field = None
        self.is_game_over = False
        self.closed_cells = 0
        self.flags_count = 0

    def start(self, field):
        self._field = field
        self.closed_cells = field.size - field.bombs
        self.flags_count = field.bombs
        minesweeper = GameWindow(self._field.rows, self._field.columns, self)
        minesweeper.ShowDialog()

    def new_easy_game(self, sender, args):
        form = sender.OwnerItem.OwnerItem.Owner.Parent
        form.Hide()
        form.Close()
        self.start(Field(Field.EASY))

    def new_normal_game(self, sender, args):
        form = sender.OwnerItem.OwnerItem.Owner.Parent
        form.Hide()
        form.Close()
        self.start(Field(Field.NORMAL))

    def new_hard_game(self, sender, args):
        form = sender.OwnerItem.OwnerItem.Owner.Parent
        form.Hide()
        form.Close()
        self.start(Field(Field.HARD))

    def game_over(self, game_window):
        self.is_game_over = True
        if not self.closed_cells:
            game_window.final_alert('You Win!')
            self.enabled_cells(game_window)
        else:
            game_window.final_alert('You Loose')
            self.show_and_activated_all_bombs(game_window)

    def show_and_activated_all_bombs(self, game_window):
        for row in game_window._cells:
            for cell in row:
                if self.is_bomb(cell.y, cell.x):
                    if not cell.is_checked:
                        game_window._change_view(cell, is_bomb=True)
                cell.Enabled = False

    def enabled_cells(self, game_window):
        for row in game_window._cells:
            for cell in row:
                if cell.Enabled:
                    cell.Enabled = False

    def is_bomb(self, y, x):
        if self._field._bombs[y][x]:
            return True
        else:
            return False

    def close(self, sender, args):
        os._exit(0)
