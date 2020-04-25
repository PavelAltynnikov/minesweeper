# -*- coding: utf-8 -*-
import time
from threading import Thread


class Timer(Thread):
    def __init__(self, method, start_value, nightmare_mode):
        Thread.__init__(self)
        self.daemon = True
        self._stop = False
        self._value = start_value
        self._nightmare_mode = nightmare_mode
        self._delegate_timer_update_in_view = method

    def run(self):
        while self._value >= 0 and not self._stop:
            self._delegate_timer_update_in_view(self._value)
            if self._nightmare_mode:
                self._value -= 1
            else:
                self._value += 1
            time.sleep(1)

    def stop_timer(self):
        self._stop = True
        self._Thread__stop()
