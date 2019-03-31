from .tools import surroundings_of

class Context:
    def __init__(self):
        self.points = {
            'surroundings': set(),
            'blocks': set(),
            'perimeter': set(),
            'intersects': set()
        }

    @property
    def intersects(self):
        return self.points['intersects']

    @intersects.setter
    def intersects(self, value):
        self.points['intersects'] = value

    @property
    def surroundings(self):
        return self.points['surroundings']

    @surroundings.setter
    def surroundings(self, value):
        self.points['surroundings'] = value

    @property
    def blocks(self):
        return self.points['blocks']

    @blocks.setter
    def blocks(self, value):
        self.points['blocks'] = value

    @property
    def perimeter(self):
        return self.points['perimeter']

    @perimeter.setter
    def perimeter(self, value):
        self.points['perimeter'] = value

    def clean(self, x, y):
        # Strip any points outside of the grid
        for key in self.points.keys():
            points_to_pop = list()
            for point in self.points[key]:
                if point[0] < 0 or point[0] >= x:
                    points_to_pop.append(point)
                    continue
                if point[1] < 0 or point[1] >= y:
                    points_to_pop.append(point)
                    continue

            for point in points_to_pop:
                self.points[key].discard(point)

        # Remove the blocks from the surrounding
        # TODO remove this once raytracing is implemented
        #print("Cleaning, removing {} blocks".format(len(self.blocks)))
        for block in self.points['blocks']:
            self.points['surroundings'].discard(block)

        return self.points['surroundings']
