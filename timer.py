# -*- coding: utf-8 -*-
import time
from threading import Thread


class Timer(Thread):
    def __init__(self, function, game):
        Thread.__init__(self)
        self.daemon = True
        self._update_function = function
        self._game = game

    def run(self):
        i = 0
        while not self._game.is_game_over:
            time.sleep(1)
            i += 1
            self._update_function(i)
