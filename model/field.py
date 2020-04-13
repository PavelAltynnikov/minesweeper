# -*- coding: utf-8 -*-
import random


class Field(object):
    TEST = {
        'rows': 3,
        'columns': 4,
        'bombs': 1
    }

    EASY = {
        'rows': 9,
        'columns': 9,
        'bombs': 10
    }

    NORMAL = {
        'rows': 16,
        'columns': 16,
        'bombs': 40
    }

    HARD = {
        'rows': 16,
        'columns': 30,
        'bombs': 99
    }

    def __init__(self, complexity):
        self._rows = complexity['rows']
        self._columns = complexity['columns']
        self._size = self._rows * self._columns
        self._count_bombs = complexity['bombs']
        self._found_bombs = 0
        self._bombs = self._generate_bombs()
        self._hints = self._generate_hints()
        self._game_over = False

    def _generate_bombs(self):
        bombs = [[0 for x in range(self._columns)] for y in range(self._rows)]
        for _ in range(self._count_bombs):
            while True:
                y = random.randrange(self._rows)
                x = random.randrange(self._columns)
                if not bombs[y][x]:
                    bombs[y][x] = 1
                    break
        return bombs

    def _generate_hints(self):
        hints = [[0 for x in range(self._columns)] for y in range(self._rows)]
        for y, row in enumerate(self._bombs):
            for x, cell in enumerate(row):
                if cell:
                    hints[y][x] = 'B'
                else:
                    hints[y][x] = self._find_bombs_around(x, y)
        return hints

    def _find_bombs_around(self, current_x, current_y):
        count = 0
        for dy in (-1, 0, 1):
            y = current_y + dy
            if 0 <= y < self._rows:
                for dx in (-1, 0, 1):
                    x = current_x + dx
                    if 0 <= x < self._columns:
                        if self._bombs[y][x]:
                            count += 1
        return str(count)

    @property
    def rows(self):
        return self._rows

    @property
    def columns(self):
        return self._columns

    @property
    def size(self):
        return self._size

    @property
    def bombs(self):
        return self._count_bombs

    @bombs.setter
    def bombs(self, value):
        self._count_bombs = value

    def get_hint_value(self, y, x):
        value = self._hints[y][x]
        if value == '0':
            return ''
        else:
            return value

    @staticmethod
    def test_print(lst):
        for row in lst:
            for cell in row:
                print cell,
            print
        print


if __name__ == '__main__':
    f = Field(Field.TEST)
    Field.test_print(f._bombs)
    Field.test_print(f._hints)
