# -*- coding: utf-8 -*-
import time
from threading import Thread


class Timer(Thread):
    def __init__(self, method, start_value, nightmare_mode):
        Thread.__init__(self)
        self.daemon = True
        self._stop = False
        self._nightmare_mode = nightmare_mode
        self._value = self._define_start_value(start_value)
        self._delegate_timer_update_in_view = method
        self.event_handler_end_game = None

    def _define_start_value(self, value):
        if self._nightmare_mode:
            return value
        else:
            return 0

    def run(self):
        while self._value >= 0 and not self._stop:
            self._delegate_timer_update_in_view(self._value)
            if self._nightmare_mode:
                self._value -= 1
            else:
                self._value += 1
            time.sleep(1)
        self.event_hendler_end_game()

    def stop_timer(self):
        self._stop = True
        self._Thread__stop()

    def get_value(self):
        return self._value
