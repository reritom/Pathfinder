from .tools import surroundings_of

class Context:
    def __init__(self):
        self.points = {
            'surroundings': set(),
            'blocks': set(),
            'obscured': set(),
            'perimeter': set(),
            'outmost': set(),
            'shadows': set()
        }

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
    def obscured(self):
        return self.points['obscured']

    @obscured.setter
    def obscured(self, value):
        self.points['obscured'] = value

    @property
    def perimeter(self):
        return self.points['perimeter']

    @perimeter.setter
    def perimeter(self, value):
        self.points['perimeter'] = value

    @property
    def outmost(self):
        return self.points['outmost']

    @outmost.setter
    def outmost(self, value):
        self.points['outmost'] = value

    @property
    def shadows(self):
        return self.points['shadows']

    @shadows.setter
    def shadows(self, value):
        self.points['shadows'] = value

    def clean(self, x, y):
        # Determine the obscured points
        for shadow in self.shadows:
            surrounding_points = surroundings_of(shadow)
            for surrounding_point in surrounding_points:
                if surrounding_point in self.surroundings:
                    self.obscured.add(shadow)
                    break

        # Discard things from the surroundings
        for block in self.blocks:
            self.surroundings.discard(block)

        for shadow in self.shadows:
            self.surroundings.discard(shadow)

        for obscured in self.obscured:
            self.surroundings.discard(obscured)

        # Strip any points outside of the grid
        for key in self.points.keys():
            points_to_pop = list()
            for point in self.points[key]:
                if point[0] < 0 or point[0] > x:
                    points_to_pop.append(point)
                    continue
                if point[1] < 0 or point[1] > y:
                    points_to_pop.append(point)
                    continue

            for point in points_to_pop:
                self.points[key].discard(point)
