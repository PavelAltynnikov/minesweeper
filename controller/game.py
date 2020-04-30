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

import clr
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import MouseButtons, FlatStyle
clr.AddReference('System.Drawing')
from System.Drawing import ContentAlignment, Size, Point, Color


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
        self._model = None
        self._view = None
        self.is_game_over = False
        self._nightmare_mode = True
        # self._nightmare_mode = False
        self._timer_start_value = 0
        self._closed_cells = 0
        self._flags_count = 0

    def start(self, complexity):
        self._model = Field(complexity)

        if self._nightmare_mode:
            self._timer_start_value = complexity['timer']
        self._closed_cells = self._model.size - self._model.bombs
        self._flags_count = self._model.bombs

        self._view = GameWindow(self._model.rows, self._model.columns)
        self._view.event_handler_new_easy_game(self.new_easy_game)
        self._view.event_handler_new_normal_game(self.new_normal_game)
        self._view.event_handler_new_hard_game(self.new_hard_game)
        self._view.event_handler_buttons_click(self.mouse_button_down)
        self._view.set_flags_counter(self._flags_count)
        # self._view.event_handler_exit_game(self.close)
        # self._view.event_handler_flags_update(self._flags_count)
        self._delegate_final_alert = self._view.final_alert

        timer = Timer(self._view.timer_update, self._timer_start_value, self._nightmare_mode)
        timer.event_hendler_end_game = self.game_over
        timer.start()

        self._view.ShowDialog()

    def mouse_button_down(self, cell, args):
        if not cell.is_checked:
            if args.Button == MouseButtons.Right:
                self.right_click(cell)
            elif args.Button == MouseButtons.Left:
                pass
                # self.left_click(cell)

    def right_click(self, cell):
        if cell.Text != 'F':
            if self._flags_count:
                cell.set_value('F')
                self._flags_count -= 1
        else:
            cell.set_value('')
            self._flags_count += 1
        self._view.set_flags_counter(self._flags_count)

    def left_click(self, cell):
        self._closed_cells -= 1
        value = self._model.get_hint_value(cell.y, cell.x)
        if self.is_bomb(cell.y, cell.x):
            self.game_over(self)
        else:
            cell.change_view(cell)
        if value == '':
            self._check_neighboring_cells(cell)
        if not self._closed_cells:
            self.game_over()

    # def _change_view(self, cell, is_bomb=False):
    #     if is_bomb:
    #         cell.BackColor = Color.FromArgb(250, 0, 0)
    #     else:
    #         cell.BackColor = Color.FromArgb(192, 192, 192)
    #     cell.Enabled = False
    #     cell.is_checked = True
    #     cell.Text = self._model.get_hint_value(cell.y, cell.x)
    #     cell.FlatAppearance.BorderSize = 1
    #     cell.FlatAppearance.BorderColor = Color.FromArgb(128, 128, 128)
    #     cell.FlatStyle = FlatStyle.Flat

    def new_easy_game(self, sender, args):
        form = sender.OwnerItem.OwnerItem.Owner.Parent
        self._hide_previus_game(form)
        self._game_reset(sender)
        self.start(Game.EASY)

    def new_normal_game(self, sender, args):
        form = sender.OwnerItem.OwnerItem.Owner.Parent
        self._hide_previus_game(form)
        self._game_reset(sender)
        self.start(Game.NORMAL)

    def new_hard_game(self, sender, args):
        form = sender.OwnerItem.OwnerItem.Owner.Parent
        self._hide_previus_game(form)
        self._game_reset(form)
        self.start(Game.HARD)

    def _hide_previus_game(self, game_window):
        game_window.Hide()
        game_window.Close()

    def _game_reset(self, game_window):
        self.is_game_over = False
        self._timer_start_value = 0
        self._nightmare_mode = game_window.checkBox.Checked

    def game_over(self):
        self.is_game_over = True
        if not self._closed_cells:
            self._delegate_final_alert('You Win!')
            # self.enabled_cells(game_window)
        else:
            self._delegate_final_alert('You Lose')
            # self.show_and_activated_all_bombs(game_window)

    # def show_and_activated_all_bombs(self, game_window):
    #     for row in game_window._cells:
    #         for cell in row:
    #             if self.is_bomb(cell.y, cell.x):
    #                 if not cell.is_checked:
    #                     game_window._change_view(cell, is_bomb=True)
    #             cell.Enabled = False

    def enabled_cells(self, game_window):
        for row in game_window._cells:
            for cell in row:
                if cell.Enabled:
                    cell.Enabled = False

    def is_bomb(self, y, x):
        if self._model._bombs[y][x]:
            return True
        else:
            return False

    def close(self, sender, args):
        pass
