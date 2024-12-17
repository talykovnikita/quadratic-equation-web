import math


class Solution:

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def _round_rule(self, x):
        tmp = "{0:g}".format(round(x, 2))
        return float(tmp) if "." in tmp else int(tmp)

    def calc_d(self):
        return self.b * self.b - 4 * self.a * self.c

    def calc_x1(self):
        d = self.calc_d()
        if d < 0:
            raise RuntimeError("d < 0")

        x1 = (-self.b + math.sqrt(d)) / (2 * self.a)
        return self._round_rule(x1)

    def calc_x2(self):
        d = self.calc_d()
        if d < 0:
            raise RuntimeError("d < 0")

        x2 = (-self.b - math.sqrt(d)) / (2 * self.a)
        return self._round_rule(x2)
