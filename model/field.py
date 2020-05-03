# -*- coding: utf-8 -*-
import random


class Field(object):
    def __init__(self, complexity):
        self._rows = complexity['rows']
        self._columns = complexity['columns']
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
        return self._rows * self._columns

    @property
    def bombs(self):
        return self._count_bombs

    # def get_hint_value(self, y, x):
    #     value = self._hints[y][x]
    #     if value == '0':
    #         return ''
    #     else:
    #         return value

    def is_bomb(self, y, x):
        if self._bombs[y][x]:
            return True
        else:
            return False

    def __getitem__(self, index):
        return self._hints[index]


if __name__ == '__main__':
    def test_print(data):
        for row in data:
            for cell in row:
                print cell,
            print
        print


    test_complexity = {
        'rows': 3,
        'columns': 4,
        'bombs': 1,
        'timer': 5
    }

    f = Field(test_complexity)
    test_print(f._bombs)
    test_print(f)

    print f[0][0]
    print f[1][1]
    print f[2][2]
