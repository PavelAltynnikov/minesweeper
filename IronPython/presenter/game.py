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
        self.model = None
        self.timer = None
        self.view = None
        self.is_game_over = False
        self.nightmare_mode = False
        self.closed_cells = 0
        self.flags_count = 0

    def start(self, complexity):
        self.model = Field(complexity)
        self.game_initialize()
        self.view_initialize(complexity)
        self.timer_initialize(complexity)
        self.view.ShowDialog()

    def game_initialize(self):
        self.closed_cells = self.model.size - self.model.bombs
        self.flags_count = self.model.bombs

    def view_initialize(self, complexity):
        self.view = GameWindow(complexity['rows'], complexity['columns'])
        self.view.add_handler_new_game_buttons(self.new_game)
        self.view.set_cell_click_handler(self.mouse_button_down)
        self.view.set_flags_counter(self.flags_count)

    def timer_initialize(self, complexity):
        self.timer = Timer(self.view.timer_update, complexity['timer'], self.nightmare_mode)
        self.timer.event_hendler_end_game = self.game_over
        self.timer.start()

    def mouse_button_down(self, cell, args):
        if not cell.is_checked:
            if args.Button == MouseButtons.Right:
                self.right_click(cell)
            elif args.Button == MouseButtons.Left:
                self.left_click(cell)

    def right_click(self, cell):
        if cell.Text != 'F':
            if self.flags_count:
                cell.set_value('F')
                self.flags_count -= 1
        else:
            cell.set_value('')
            self.flags_count += 1
        self.view.set_flags_counter(self.flags_count)

    def left_click(self, cell):
        self.closed_cells -= 1
        value = self.model[cell.y][cell.x]
        if self.model.is_bomb(cell.y, cell.x):
            self.game_over()
        else:
            cell.change_view(value, False)
        if value == '0':
            self.check_neighboring_cells(cell)
        if not self.closed_cells:
            self.game_over()

    def new_game(self, sender, args):
        self.hide_previus_game(sender)
        self.game_reset(sender)
        if 'Easy' in args.Text:
            self.start(Game.EASY)
        elif 'Normal' in args.Text:
            self.start(Game.NORMAL)
        elif 'Hard' in args.Text:
            self.start(Game.HARD)

    def hide_previus_game(self, game_window):
        game_window.Hide()
        game_window.Close()

    def game_reset(self, game_window):
        self.is_game_over = False
        self.nightmare_mode = game_window.checkBox.Checked

    def game_over(self):
        self.is_game_over = True
        if not self.closed_cells:
            self.view.set_final_message('You Win!')
            self.disabled_cells()
        else:
            self.view.set_final_message('You Lose')
            self.show_and_activated_all_bombs()
        # надо пересмотреть это решение так как это вызывается в самом таймере
        self.timer.stop_timer()

    def check_neighboring_cells(self, cell):
        for dy in (-1, 0, 1):
            y = cell.y + dy
            if 0 <= y < self.model.rows:
                for dx in (-1, 0, 1):
                    x = cell.x + dx
                    if 0 <= x < self.model.columns:
                        neighbro_cell = self.view[y][x]
                        if not neighbro_cell.is_checked:
                            neighbro_cell.programmable_mouse_down()

    def show_and_activated_all_bombs(self):
        for row in self.view:
            for cell in row:
                if self.model.is_bomb(cell.y, cell.x):
                    if not cell.is_checked:
                        cell.change_view(self.model[cell.y][cell.x], True)
                cell.Enabled = False

    def disabled_cells(self):
        for row in self.view:
            for cell in row:
                if cell.Enabled:
                    cell.Enabled = False
