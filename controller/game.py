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
from model.timer import Timer


class Game(object):
    TEST = {
        'rows': 3,
        'columns': 4,
        'bombs': 1,
        'timer': 5
    }

    EASY = {
        'rows': 9,
        'columns': 9,
        'bombs': 10,
        'timer': 20
    }

    NORMAL = {
        'rows': 16,
        'columns': 16,
        'bombs': 40,
        'timer': 120
    }

    HARD = {
        'rows': 16,
        'columns': 30,
        'bombs': 99,
        'timer': 220
    }

    def __init__(self):
        self._field = None
        self.is_game_over = False
        self.nightmare_mode = True
        # self.nightmare_mode = False
        self.timer_start_value = 0
        self.closed_cells = 0
        self.flags_count = 0

    def start(self, complexity):
        self._field = Field(complexity)
        if self.nightmare_mode:
            self.timer_start_value = complexity['timer']
        self.closed_cells = self._field.size - self._field.bombs
        self.flags_count = self._field.bombs

        minesweeper = GameWindow(self._field.rows, self._field.columns)
        # minesweeper.flags_update()

        timer = Timer(minesweeper.timer_update, self.timer_start_value, self.nightmare_mode)
        timer.start()

        minesweeper.ShowDialog()

    def new_easy_game(self, sender, args):
        form = sender.OwnerItem.OwnerItem.Owner.Parent
        form.Hide()
        form.Close()
        self.is_game_over = False
        self.nightmare_mode = form.checkBox.Checked
        self.start(Game.EASY)

    def new_normal_game(self, sender, args):
        form = sender.OwnerItem.OwnerItem.Owner.Parent
        form.Hide()
        form.Close()
        self.is_game_over = False
        self.nightmare_mode = form.checkBox.Checked
        self.start(Game.NORMAL)

    def new_hard_game(self, sender, args):
        form = sender.OwnerItem.OwnerItem.Owner.Parent
        form.Hide()
        form.Close()
        self.is_game_over = False
        self.nightmare_mode = form.checkBox.Checked
        self.start(Game.HARD)

    def game_over(self, game_window):
        self.is_game_over = True
        if not self.closed_cells:
            game_window.final_alert('You Win!')
            self.enabled_cells(game_window)
        else:
            game_window.final_alert('You Lose')
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
