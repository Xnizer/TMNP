class Point:
    def __init__(self, x: int, y: int):
        self.X = x
        self.Y = y

    def copy(self):
        return Point(self.X, self.Y)

    def __eq__(self, p):
        if isinstance(p, Point):
            return (self.X == p.X) and (self.Y == p.Y)
        else:
            return False

    def __ne__(self, p):
        return not (self == p)

    def __mul__(self, p):
        return Point(self.X * p.X, self.Y * p.Y)

    def __add__(self, p):
        return Point(self.X + p.X, self.Y + p.Y)
    
    def __sub__(self, p):
        return Point(self.X - p.X, self.Y - p.Y)
    
    def __floordiv__(self, p):
        return Point(self.X // p.X, self.Y // p.Y)
    
    def __truediv__(self, p):
        return self // p