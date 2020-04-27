# -*- coding: utf-8 -*-
import sys
sys.path.append(r'D:\Development\Programming\Python\IronPython\minesweeper')
from controller.game import Game

game = Game()
game.start(Game.EASY)
