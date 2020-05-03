# -*- coding: utf-8 -*-
import sys
import os

main_dir_path = os.path.dirname(os.path.realpath(__file__))

# sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib')
# main_file_info = str(IN[0])  # noqa
# main_dir_path = os.path.dirname(main_file_info)

# main_dir_path = r'D:\Development\Programming\Python\IronPython\minesweeper'

sys.path.append(main_dir_path)
from controller.game import Game

game = Game()
game.start(Game.EASY)
