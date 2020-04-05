# -*- coding: utf-8 -*-
import random
import time
from threading import Thread
import clr
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import (Form, FormBorderStyle, FlatStyle, Label, MenuStrip, MouseEventArgs, MouseButtons, ToolStripMenuItem,
                                  ToolStripItemCollection)
clr.AddReference('System.Drawing')
from System.Drawing import ContentAlignment, Size, Point, Color
from cell import Cell


class GameWindow(Form):
    def __init__(self, field):
        self._indent_top = 50
        self._indent_left = 10
        self._indent_right = 10
        self._indent_bottom = 10
        self._cell_side = 30
        self._cell_size = Size(self._cell_side, self._cell_side)
        self._field = field
        self._cells = []
        self.FormBorderStyle = FormBorderStyle.Fixed3D

        self._initialize_components()
        self._run_timer()
        self.CenterToScreen()

    def _initialize_components(self):
        self.MainMenuStrip = self._generate_menu_strip()
        self.Size = self._generate_window_size()
        self._create_buttons()

        self._flags_description = Label()
        self._flags_description.Parent = self
        self._flags_description.Text = 'Флаги:'
        self._flags_description.Location = Point(10, 30)
        self._flags_description.Size = Size(40, 20)

        self._flags_counter = Label()
        self._flags_counter.Parent = self
        self._flags_counter.Text = str(self._field.bombs)
        self._flags_counter.Location = Point(50, 30)
        self._flags_counter.Size = Size(30, 20)

        self._label_timer = Label()
        self._label_timer.Parent = self
        self._label_timer.Text = '0'
        self._label_timer.TextAlign = ContentAlignment.MiddleRight
        self._label_timer.Location = Point(self.Size.Width - 60, 30)
        self._label_timer.Size = Size(40, 20)

    def _run_timer(self):
        thread = Thread(target=self._timer_update)
        thread.daemon = True
        thread.start()

    def _timer_update(self):
        i = 0
        while not self._field.game_over:
            time.sleep(1)
            i += 1
            self._label_timer.Text = str(i)

    def _generate_menu_strip(self):
        _menu_strip = MenuStrip()
        _menu_strip.Parent = self
        _file_item = ToolStripMenuItem("&File")
        _new_game = ToolStripMenuItem("&New game", None)
        _easy = ToolStripMenuItem("&Easy", None)
        _normal = ToolStripMenuItem("&Normal", None)
        _hard = ToolStripMenuItem("&Hard", None)
        _nightmare = ToolStripMenuItem("&Nightmare", None)
        _new_game.DropDownItems.Add(_easy)
        _new_game.DropDownItems.Add(_normal)
        _new_game.DropDownItems.Add(_hard)
        _new_game.DropDownItems.Add(_nightmare)
        _file_item.DropDownItems.Add(_new_game)
        _menu_strip.Items.Add(_file_item)
        return _menu_strip

    def _generate_window_size(self):
        width = self._indent_left + self._field.columns * self._cell_side + self._indent_right + 10
        height = self._indent_top + self._field.rows * self._cell_side + self._indent_bottom + 33
        return Size(width, height)

    def _create_buttons(self):
        for y in range(self._field.rows):
            for x in range(self._field.columns):
                cell = Cell((y, x))
                cell.Parent = self
                cell.Size = self._cell_size
                cell.Location = Point(self._indent_left + x * self._cell_side,
                                      self._indent_top + y * self._cell_side)
                # cell.hidden_value = str(self._field.get_cell_value(x, y))
                cell.FlatStyle = FlatStyle.Standard
                cell.Click += self._on_click_game_cell
                cell.MouseDown += self._on_mouse_down
                cell.GotFocus += self._focus
                self._cells.append(cell)

    def _new_game_click(self, sender, args):
        pass

    def _on_click_game_cell(self, sender, args):
        if not sender.is_active:
            if self._field.get_cell_value(sender.location) == 'B':
                for cell in self._cells:
                    if cell.hidden_value == 'B':
                        if not cell.is_active:
                            self._change_view(cell, is_bomb=True)
                    cell.Enabled = False
                    self._field.game_over = True
            else:
                self._change_view(sender)
        else:
            pass

    def _change_view(self, cell, is_bomb=False):
        cell.is_active = True
        if is_bomb:
            cell.BackColor = Color.FromArgb(250, 0, 0)
        else:
            cell.BackColor = Color.FromArgb(192, 192, 192)
        cell.Text = cell.hidden_value
        cell.FlatAppearance.BorderSize = 1
        cell.FlatAppearance.BorderColor = Color.FromArgb(128, 128, 128)
        cell.FlatStyle = FlatStyle.Flat

    def _on_mouse_down(self, sender, args):
        if args.Button == MouseButtons.Right:
            if not sender.is_active:
                if sender.Text != 'F':
                    if self._field.bombs > 0:
                        sender.Text = 'F'
                        self._field.bombs -= 1
                        self._flags_counter.Text = str(self._field.bombs)
                else:
                    sender.Text = ''
                    self._field.bombs += 1
                    self._flags_counter.Text = str(self._field.bombs)

    def _focus(self, sender, args):
        sender.NotifyDefault(False)


if __name__ == '__main__':
    game = GameWindow()
    game.ShowDialog()
