# -*- coding: utf-8 -*-
import sys
import os
try:
    main_dir_path = os.path.dirname(os.path.realpath(__file__))
except Exception as e:
    main_dir_path = r'D:\WORK\BIM Planet\Погружение в IronPython и Revit API\Minesweeper\IronPython'
sys.path.append(main_dir_path)
from controller.game import Game

game = Game()
game.start(Game.EASY)
