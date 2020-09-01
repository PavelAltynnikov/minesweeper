# -*- coding: utf-8 -*-
import sys
import os
try:
    main_dir_path = os.path.dirname(os.path.dirname(__file__))
except Exception as e:
    main_dir_path = r'D:\WORK\BIM Planet\Погружение в IronPython и Revit API' \
                    r'\Модуль 2\2.4\Для видео\11 RPS and Dynamo'
sys.path.append(os.path.join(main_dir_path, 'IronPython'))
from presenter.game import Game

__window__.Close()
game = Game()
game.start(Game.EASY)
