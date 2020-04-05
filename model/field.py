# -*- coding: utf-8 -*-
import random


class Field(object):
    TEST = {
        'rows': 4,
        'columns': 5,
        'bombs': 6
    }

    EASY = {
        'rows': 9,
        'columns': 9,
        'bombs': 10
    }

    MEDIUM = {
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
        self._bombs = self._generate_bomds()
        self._hints = self._generate_hints()
        self._game_over = False

    def _generate_bomds(self):
        bombs = []
        max_count_bombs = self._count_bombs
        for y in range(self._rows):
            row = []
            for x in range(self._columns):
                if max_count_bombs:
                    row.append(int(round(random.uniform(0, 1))))
                    max_count_bombs -= 1
                else:
                    row.append(0)
            bombs.append(row)
        return bombs

    def _generate_hints(self):
        hints = [[0 for x in range(self._columns)] for y in range(self._rows)]
        for y, row in enumerate(self._bombs):
            for x, cell in enumerate(row):
                if cell:
                    hints[y][x] = 'B'
                else:
                    hints[y][x] = self._find_bombs_around(y, x)
        return hints

    def _find_bombs_around(self, y, x):
        count = 0
        for dy in (-1, 0, 1):
            Y = y + dy
            if 0 <= Y < self._rows:
                for dx in (-1, 0, 1):
                    X = x + dx
                    if 0 <= X < self._columns:
                        if self._bombs[Y][X]:
                            count += 1
        return count

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

    @property
    def game_over(self):
        return self._game_over

    @game_over.setter
    def game_over(self, value):
        self._game_over = value

    def get_cell_value(self, location):
        return self._hints[location[1]][location[0]]

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
