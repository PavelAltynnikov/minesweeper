# -*- coding: utf-8 -*-
import sys
sys.path.append(r'D:\Development\Programming\Python\IronPython\minesweeper')
from controller.game import Game
from model.field import Field

game = Game()
game.start(Field(Field.EASY))
