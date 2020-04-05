# -*- coding: utf-8 -*-
import sys
sys.path.append(r'D:\Development\Programming\Python\IronPython\minesweeper')
from model.field import Field
from view.game_window import GameWindow

game = GameWindow(Field(Field.TEST))
game.ShowDialog()
