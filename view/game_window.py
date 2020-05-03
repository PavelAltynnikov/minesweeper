# -*- coding: utf-8 -*-
import clr
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import (CheckBox, Form, FormBorderStyle, FlatStyle, Label, MenuStrip, ToolStripControlHost,
                                  MouseButtons, ToolStripMenuItem, TextRenderer)
clr.AddReference('System.Drawing')
from System.Drawing import ContentAlignment, Size, Point, Color
from view.cell import Cell


class GameWindow(Form):
    def __init__(self, rows, columns):
        self._indent_top = 50
        self._indent_left = 10
        self._indent_right = 10
        self._indent_bottom = 10
        self._cell_side = 30
        self._cell_size = Size(self._cell_side, self._cell_side)
        self._cells = []
        self._rows = rows
        self._columns = columns
        self.FormBorderStyle = FormBorderStyle.Fixed3D
        self._initialize_components()
        self.CenterToScreen()

    def _initialize_components(self):
        self.MainMenuStrip = self._generate_menu_strip()
        self.Size = self._generate_window_size()
        self._create_buttons()

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
        self._flags_counter.Location = Point(45, 30)
        self._flags_counter.Size = Size(30, 20)

        self._label_timer = Label()
        self._label_timer.Parent = self
        self._label_timer.TextAlign = ContentAlignment.MiddleRight
        self._label_timer.Location = Point(self.Size.Width - 60, 30)
        self._label_timer.Size = Size(40, 20)

    def _generate_menu_strip(self):
        menu_strip = MenuStrip()
        menu_strip.Parent = self

        file_item = ToolStripMenuItem("&File")
        menu_strip.Items.Add(file_item)

        new_game = ToolStripMenuItem("&New game")
        file_item.DropDownItems.Add(new_game)

        self._easy = ToolStripMenuItem("&Easy")
        new_game.DropDownItems.Add(self._easy)

        self._normal = ToolStripMenuItem("&Normal")
        new_game.DropDownItems.Add(self._normal)

        self._hard = ToolStripMenuItem("&Hard")
        new_game.DropDownItems.Add(self._hard)

        self.checkBox = CheckBox()
        self.checkBox.Text = "Nightmare"
        self.checkBox.Size = Size(100, 20)
        self.checkBox.Checked = False
        nightmare = ToolStripControlHost(self.checkBox)
        nightmare.Size = Size(100, 20)
        new_game.DropDownItems.Add(nightmare)

        self._exit = ToolStripMenuItem("&Exit")
        self._exit.Click += self._exit_game
        file_item.DropDownItems.Add(self._exit)

        return menu_strip

    def _generate_window_size(self):
        width = self._indent_left + self._columns * self._cell_side + self._indent_right + 16  # 10
        height = self._indent_top + self._rows * self._cell_side + self._indent_bottom + 39  # 33
        return Size(width, height)

    def _create_buttons(self):
        for y in range(self._rows):
            row = []
            for x in range(self._columns):
                cell = Cell(y, x)
                cell.Parent = self
                cell.Size = self._cell_size
                cell.Location = Point(self._indent_left + x * self._cell_side,
                                      self._indent_top + y * self._cell_side)
                row.append(cell)
            self._cells.append(row)

    def set_flags_counter(self, value):
        self._flags_counter.Text = str(value)

    def timer_update(self, value):
        self._label_timer.Text = str(value)

    def final_message(self, message):
        self._result.Text = message
        self._result.Size = TextRenderer.MeasureText(self._result.Text, self._result.DefaultFont)
        self._result.Location = Point(self.Size.Width / 2 - self._result.Size.Width / 2 - 5, 30)

    def event_handler_buttons_click(self, method):
        for row in self._cells:
            for cell in row:
                cell.MouseDown += method

    def event_handler_new_easy_game(self, method):
        self._easy.Click += method

    def event_handler_new_normal_game(self, method):
        self._normal.Click += method

    def event_handler_new_hard_game(self, method):
        self._hard.Click += method

    def _exit_game(self, sender, args):
        self.Close()

    def __getitem__(self, index):
        return self._cells[index]


if __name__ == '__main__':
    game = GameWindow()
    game.ShowDialog()
