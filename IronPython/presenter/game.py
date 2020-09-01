# -*- coding: utf-8 -*-
'''
EASY    9х9   = 81  -> 10 бомб -> 12.3%
MEDIUM  16х16 = 256 -> 40 бомб -> 15.6%
HARD    30х16 = 480 -> 99 бомб -> 20.6%
NIGHTMARE - таймер идёт на убыль
'''
from model.field import Field
from model.timer import Timer
from view.game_window import GameWindow

import clr
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import MouseButtons


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
        self._timer = None
        self._view = None
        self._is_game_over = False
        self._nightmare_mode = False
        self._closed_cells = 0
        self._flags_count = 0

    def start(self, complexity):
        self._model = Field(complexity)
        self._game_initialize()
        self._view_initialize(complexity)
        self._timer_initialize(complexity)
        self._view.ShowDialog()

    def _game_initialize(self):
        self._closed_cells = self._model.size - self._model.bombs
        self._flags_count = self._model.bombs

    def _view_initialize(self, complexity):
        self._view = GameWindow(complexity['rows'], complexity['columns'])
        self._view.add_handler_new_game_buttons(self._new_game)
        self._view.set_cell_click_handler(self._mouse_button_down)
        self._view.set_flags_counter(self._flags_count)

    def _timer_initialize(self, complexity):
        self._timer = Timer(
            complexity['timer'],
            self._nightmare_mode,
            self._view.timer_update,
            self._game_over
        )
        self._timer.start()

    def _mouse_button_down(self, cell, args):
        if not cell.is_checked:
            if args.Button == MouseButtons.Right:
                self._right_click(cell)
            elif args.Button == MouseButtons.Left:
                self._left_click(cell)

    def _right_click(self, cell):
        if cell.Text != 'F':
            if self._flags_count:
                cell.set_value('F')
                self._flags_count -= 1
        else:
            cell.set_value('')
            self._flags_count += 1
        self._view.set_flags_counter(self._flags_count)

    def _left_click(self, cell):
        self._closed_cells -= 1
        value = self._model[cell.y][cell.x]
        if self._model.is_bomb(cell.y, cell.x):
            self._game_over()
        else:
            cell.change_view(value, False)
        if value == '0':
            self._check_neighboring_cells(cell)
        if not self._closed_cells:
            self._game_over()

    def _new_game(self, sender, event_args):
        self._hide_previus_game(sender)
        self._game_reset(sender)
        if 'Easy' in event_args.Text:
            self.start(Game.EASY)
        elif 'Normal' in event_args.Text:
            self.start(Game.NORMAL)
        elif 'Hard' in event_args.Text:
            self.start(Game.HARD)

    def _hide_previus_game(self, game_window):
        game_window.Hide()
        game_window.Close()

    def _game_reset(self, game_window):
        self._is_game_over = False
        self._nightmare_mode = game_window.checkBox.Checked

    def _game_over(self):
        self._is_game_over = True
        if not self._closed_cells:
            self._view.set_final_message('You Win!')
            self._disabled_cells()
        else:
            self._view.set_final_message('You Lose')
            self._show_and_activated_all_bombs()
        self._timer.stop_timer()

    def _check_neighboring_cells(self, cell):
        for dy in (-1, 0, 1):
            y = cell.y + dy
            if not (0 <= y < self._model.rows):
                continue
            for dx in (-1, 0, 1):
                x = cell.x + dx
                if not (0 <= x < self._model.columns):
                    continue
                neighbro_cell = self._view[y][x]
                if not neighbro_cell.is_checked:
                    neighbro_cell.programmable_mouse_down()

    def _show_and_activated_all_bombs(self):
        for row in self._view:
            for cell in row:
                if self._model.is_bomb(cell.y, cell.x):
                    if not cell.is_checked:
                        cell.change_view(self._model[cell.y][cell.x], True)
                cell.Enabled = False

    def _disabled_cells(self):
        for row in self._view:
            for cell in row:
                if cell.Enabled:
                    cell.Enabled = False
