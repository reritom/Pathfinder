class Maze:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.blocks = set()

    def get_surroundings(self, position, view_range=1):
        # For a given position, return the surrounding positions
        centre_x, centre_y = position

        if view_range == 0:
            return set(position)

        surroundings = set()
        for radius in range(view_range):
            surroundings = surroundings.union(self.bresenhams_circle(centre_x, centre_y, radius))

        return surroundings

    def add_block(self, x, y):
        self.blocks = self.blocks.union((x, y))

    def remove_block(self, x, y):
        pass

    def bresenhams_circle(self, centre_x: int, centre_y: int, radius: int) -> list:
        def clone_octant(centre_x, centre_y, x, y):
            return [
                (centre_x + x, centre_y + y),
                (centre_x - x, centre_y + y),
                (centre_x + x, centre_y - y),
                (centre_x - x, centre_y - y),
                (centre_x + y, centre_y + x),
                (centre_x - y, centre_y + x),
                (centre_x + y, centre_y - x),
                (centre_x - y, centre_y - x),
            ]

        x = 0
        y = radius
        d = 3 - 2 * radius
        boundaries = set()
        boundaries = boundaries.union(clone_octant(centre_x, centre_x, x, y))

        while (y >= x):
            x = x + 1
            if d > 0:
                y = y - 1
                d = d + 4 * (x - y) + 10
            else:
                d = d + 4 * x + 6

            boundaries = boundaries.union(clone_octant(centre_x, centre_x, x, y))

        return boundaries