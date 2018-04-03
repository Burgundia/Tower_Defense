CELL_SIZE = 32


class Mine:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = (x, y, x + CELL_SIZE, y + CELL_SIZE)
        self.image = "images/mine.png"

    def intersects(self, obj):
        obj_rect = obj.rect
        if obj_rect[0] >= self.x and obj_rect[2] <= self.x + CELL_SIZE:
            if self.y <= obj_rect[1] and self.y + CELL_SIZE >= obj_rect[3]:
                return True
        return False
