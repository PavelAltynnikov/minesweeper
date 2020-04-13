# -*- coding: utf-8 -*-
import clr
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import (CheckBox, Form, FormBorderStyle, FlatStyle, Label, MenuStrip, ToolStripControlHost,
                                  MouseButtons, ToolStripMenuItem, TextRenderer)
clr.AddReference('System.Drawing')
from System.Drawing import ContentAlignment, Size, Point, Color
from view.cell import Cell
from timer import Timer


class GameWindow(Form):
    def __init__(self, rows, columns, game):
        self._indent_top = 50
        self._indent_left = 10
        self._indent_right = 10
        self._indent_bottom = 10
        self._cell_side = 30
        self._cell_size = Size(self._cell_side, self._cell_side)
        self._cells = []
        self._game = game
        self._rows = rows
        self._columns = columns
        self.FormBorderStyle = FormBorderStyle.Fixed3D
        timer = Timer(self.timer_update, self._game)
        timer.start()
        self._initialize_components(rows, columns)
        self.CenterToScreen()

    def _initialize_components(self, rows, columns):
        self.MainMenuStrip = self._generate_menu_strip()
        self.Size = self._generate_window_size(rows, columns)
        self._create_buttons(rows, columns)

        self._flags_description = Label()
        self._flags_description.Parent = self
        self._flags_description.Text = 'Flags:'
        self._flags_description.Location = Point(10, 30)
        self._flags_description.Size = TextRenderer.MeasureText(self._flags_description.Text, self._flags_description.DefaultFont)

        self._result = Label()
        self._result.Parent = self
        self._result.Text = ''
        self._result.Size = TextRenderer.MeasureText(self._result.Text, self._result.DefaultFont)
        self._result.Location = Point(self.Size.Width / 2 - self._result.Size.Width / 2 - 5, 30)

        self._flags_counter = Label()
        self._flags_counter.Parent = self
        self._flags_counter.Text = str(self._game.flags_count)
        self._flags_counter.Location = Point(45, 30)
        self._flags_counter.Size = Size(30, 20)

        self._label_timer = Label()
        self._label_timer.Parent = self
        self._label_timer.Text = '0'
        self._label_timer.TextAlign = ContentAlignment.MiddleRight
        self._label_timer.Location = Point(self.Size.Width - 60, 30)
        self._label_timer.Size = Size(40, 20)

    def timer_update(self, value):
        self._label_timer.Text = str(value)

    def _generate_menu_strip(self):
        menu_strip = MenuStrip()
        menu_strip.Parent = self

        file_item = ToolStripMenuItem("&File")
        menu_strip.Items.Add(file_item)

        new_game = ToolStripMenuItem("&New game")
        file_item.DropDownItems.Add(new_game)

        easy = ToolStripMenuItem("&Easy")
        easy.Click += self._game.new_easy_game
        new_game.DropDownItems.Add(easy)

        normal = ToolStripMenuItem("&Normal")
        normal.Click += self._game.new_normal_game
        new_game.DropDownItems.Add(normal)

        hard = ToolStripMenuItem("&Hard")
        hard.Click += self._game.new_hard_game
        new_game.DropDownItems.Add(hard)

        checkBox = CheckBox()
        checkBox.Text = "Nightmare"
        checkBox.Checked = False
        nightmare = ToolStripControlHost(checkBox)
        new_game.DropDownItems.Add(nightmare)

        _exit = ToolStripMenuItem("&Exit")
        _exit.Click += self._game.close
        file_item.DropDownItems.Add(_exit)

        return menu_strip

    def _generate_window_size(self, rows, columns):
        width = self._indent_left + columns * self._cell_side + self._indent_right + 10
        height = self._indent_top + rows * self._cell_side + self._indent_bottom + 33
        return Size(width, height)

    def _create_buttons(self, rows, columns):
        for y in range(rows):
            row = []
            for x in range(columns):
                cell = Cell(y, x)
                cell.Parent = self
                cell.Size = self._cell_size
                cell.Location = Point(self._indent_left + x * self._cell_side,
                                      self._indent_top + y * self._cell_side)
                cell.MouseDown += self._on_mouse_button_down_on_game_cell
                row.append(cell)
            self._cells.append(row)

    # rename to change cell_status_and_view
    def _change_view(self, cell, is_bomb=False):
        if is_bomb:
            cell.BackColor = Color.FromArgb(250, 0, 0)
        else:
            cell.BackColor = Color.FromArgb(192, 192, 192)
        cell.Enabled = False
        cell.is_checked = True
        cell.Text = self._game._field.get_hint_value(cell.y, cell.x)
        cell.FlatAppearance.BorderSize = 1
        cell.FlatAppearance.BorderColor = Color.FromArgb(128, 128, 128)
        cell.FlatStyle = FlatStyle.Flat

    def _on_mouse_button_down_on_game_cell(self, sender, args):
        if args.Button == MouseButtons.Right:
            if not sender.is_checked:
                if sender.Text != 'F':
                    if self._game.flags_count:
                        sender.Text = 'F'
                        self._game.flags_count -= 1
                else:
                    sender.Text = ''
                    self._game.flags_count += 1
                self._flags_counter.Text = str(self._game.flags_count)
        elif args.Button == MouseButtons.Left:
            if not sender.is_checked:
                self._game.closed_cells -= 1
                if self._game.is_bomb(sender.y, sender.x):
                    self._game.game_over(self)
                else:
                    self._change_view(sender)
                if self._game._field.get_hint_value(sender.y, sender.x) == '':
                    self._check_neighboring_cells(sender)
                if not self._game.closed_cells:
                    self._game.game_over(self)

    def _check_neighboring_cells(self, cell):
        for dy in (-1, 0, 1):
            y = cell.y + dy
            if 0 <= y < self._rows:
                for dx in (-1, 0, 1):
                    x = cell.x + dx
                    if 0 <= x < self._columns:
                        neighbro_cell = self._cells[y][x]
                        if not neighbro_cell.is_checked:
                            self._game.closed_cells -= 1
                            self._change_view(neighbro_cell)
                            if self._game._field.get_hint_value(y, x) == '':
                                self._check_neighboring_cells(neighbro_cell)

    def final_alert(self, alert):
        self._result.Text = alert
        self._result.Size = TextRenderer.MeasureText(self._result.Text, self._result.DefaultFont)
        self._result.Location = Point(self.Size.Width / 2 - self._result.Size.Width / 2 - 5, 30)


if __name__ == '__main__':
    game = GameWindow()
    game.ShowDialog()
