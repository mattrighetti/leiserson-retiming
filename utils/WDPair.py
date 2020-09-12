class WDPair:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.y == other.y and self.x == other.x

    def __lt__(self, other):
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x

    def __add__(self, other):
        if isinstance(other, int):
            return self
        else:
            return WDPair(self.x + other.x, self.y + other.y)