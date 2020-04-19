# -*- coding: utf-8 -*-
import time
from threading import Thread


class Timer(Thread):
    def __init__(self, function, game, nightmare_mode, game_window):
        Thread.__init__(self)
        self.daemon = True
        self._nightmare_mode = nightmare_mode
        self._timer = game.timer - 1
        self._update_function = function
        self._game = game
        self._game_window = game_window

    def run(self):
        if self._nightmare_mode:
            self._nightmare_run(self._game_window)
        else:
            self._normal_run()

    def _normal_run(self):
        i = 0
        while not self._game.is_game_over:
            time.sleep(1)
            i += 1
            self._update_function(i)

    def _nightmare_run(self, game_window):
        while self._timer >= 0 and not self._game.is_game_over:
            time.sleep(1)
            self._update_function(self._timer)
            self._timer -= 1
        self._game.game_over(game_window)
