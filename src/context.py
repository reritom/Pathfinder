from .tools import surroundings_of

class Context:
    def __init__(self):
        self.surroundings = set()
        self.blocks = set()
        self.obscured = set()
        self.perimeter = set()
        self.outmost = set()
        self.shadows = set()

    def clean(self, x, y):
        self.x = x
        self.y = y

        # Discard things from the surroundings
        for block in self.blocks:
            self.surroundings.discard(block)

        for shadow in self.shadows:
            self.surroundings.discard(shadow)

        for obscured in self.obscured:
            self.surroundings.discard(obscured)

        # Strip any surroundings outside of the grid
        surroundings_to_pop = list()
        for surrounding in self.surroundings:
            if surrounding[0] < 0 or surrounding[0] > self.x:
                surroundings_to_pop.append(surrounding)
                continue
            if surrounding[1] < 0 or surrounding[1] > self.y:
                surroundings_to_pop.append(surrounding)
                continue

        for surrounding in surroundings_to_pop:
            self.surroundings.discard(surrounding)

        # Strip any outmost outside the grid
        outmost_to_pop = list()
        for outmost in self.outmost:
            if outmost[0] < 0 or outmost[0] > self.x:
                outmost_to_pop.append(outmost)
                continue
            if outmost[1] < 0 or outmost[1] > self.y:
                outmost_to_pop.append(outmost)
                continue

        for outmost in outmost_to_pop:
            self.outmost.discard(outmost)

        # Determine the obscured points
        for shadow in self.shadows:
            surrounding_points = surroundings_of(shadow)
            for surrounding_point in surrounding_points:
                if surrounding_point in self.surroundings:
                    self.obscured.add(shadow)
                    break

        # Strip any obscured which are outside of the grid
        obscured_to_pop = list()
        for obscured in self.obscured:
            if obscured[0] < 0 or obscured[0] > self.x:
                obscured_to_pop.append(obscured)
                continue
            if obscured[1] < 0 or obscured[1] > self.y:
                obscured_to_pop.append(obscured)
                continue

        for obscured in obscured_to_pop:
            self.obscured.discard(obscured)
