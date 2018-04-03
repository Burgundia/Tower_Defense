from tower_place import TowerPlace
from collections import deque
CELL_SIZE = 32


class Unity:
    @staticmethod
    def identifier(level):
        access_cells = []
        tower_places = []
        x = y = 0
        branch_start = None
        branch_end = None
        for row in level:
            for col in row.rstrip():
                if col != ' ':
                    point = [x, y]
                    if col == '.':
                        access_cells.append(point)
                    elif col == 'T':
                        tower = TowerPlace(x, y)
                        tower_places.append(tower)
                    elif col == 'S':
                        if 'start' in locals():
                            raise ValueError("Must be one start")
                        start = point
                    elif col == 'F':
                        if 'finish' in locals():
                            raise ValueError("Must be one finish")
                        finish = point
                    elif col == 'B':
                        if branch_start is not None:
                            raise ValueError("Unfortunately, at the moment you can't play with multiple branches")
                        branch_start = point
                    elif col == 'E':
                        if branch_end is not None:
                            raise ValueError("Unfortunately, at the moment you can't play with multiple branches")
                        branch_end = point
                    else:
                        raise NotImplementedError
                x += CELL_SIZE
            y += CELL_SIZE
            x = 0
        return access_cells, tower_places, start, finish, branch_start,\
            branch_end

    @staticmethod
    def build_way(access_cells, start, finish, branch_start, branch_end):
        access_cells = list(access_cells)
        if branch_start is None and branch_end is None:
            return [deque(Unity.build_simple_way(access_cells, start, finish))]
        start_way = Unity.build_simple_way(access_cells, start, branch_start)
        incident_cells = [cell for cell in access_cells if
                          Unity.is_next_cell(branch_start, cell)]
        branch_ways = [[cell] + Unity.build_simple_way(access_cells, cell,
                                                       branch_end) for cell in
                       incident_cells]
        end_way = Unity.build_simple_way(access_cells, branch_end, finish)
        for i in range(len(branch_ways)):
            branch_ways[i] = deque(start_way + branch_ways[i] + end_way)
        return branch_ways

    @staticmethod
    def build_simple_way(access_cells, start, finish):
        way = []
        access_cells.append(finish)
        cell = start
        if cell in access_cells:
            access_cells.remove(cell)
        while access_cells:
            for next_cell in access_cells:
                if Unity.is_next_cell(cell, next_cell):
                    way.append(next_cell)
                    access_cells.remove(next_cell)
                    cell = next_cell
                    break
            else:
                raise ValueError("Bad map. Can't find way from {} to {}".format(start, finish))
            if cell == finish:
                break
        return way

    @staticmethod
    def is_next_cell(cell, next_cell):
        return (cell[0] == next_cell[0] and abs(cell[1] - next_cell[1]) == 32)\
            or (cell[1] == next_cell[1] and abs(cell[0] - next_cell[0]) == 32)

    @staticmethod
    def take_new_coordinates(creep):
        x = creep.rect[0] + creep.motion[0]
        y = creep.rect[1] + creep.motion[1]
        rect = (x, y, x + CELL_SIZE, y + CELL_SIZE)
        return rect

    @staticmethod
    def make_direction(creep, speed):
        next_cell = creep.way.popleft()
        if creep.rect[2] == next_cell[0] and creep.rect[1] == next_cell[1]:
            motion = [speed, 0]
        if creep.rect[0] == next_cell[0] + CELL_SIZE and \
           creep.rect[1] == next_cell[1]:
            motion = [-speed, 0]
        if creep.rect[1] == next_cell[1] + CELL_SIZE and \
           creep.rect[0] == next_cell[0]:
            motion = [0, -speed]
        if creep.rect[3] == next_cell[1] and creep.rect[0] == next_cell[0]:
            motion = [0, speed]
        return motion, next_cell
