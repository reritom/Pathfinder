from typing import List, Tuple
import math as maths

class Bot:
    def __init__(self, position: tuple, target: tuple):
        self.position = position
        self.target = target
        self.locations = dict()
        self.previous_positions = []

    def run_round(self, surroundings: List[Tuple]) -> tuple:
        # For any new surrounding, add it to the locations with a static heuristic
        for surrounding in surroundings:
            if surrounding not in self.locations:
                self.locations[surrounding] = self.calculate_static_heuristic(surrounding)

    def calculate_static_heuristic(self, point: tuple):
        print(self.target)
        dy = abs(self.target[1] - point[1])
        dx = abs(self.target[0] - point[0])
        return maths.sqrt(dy**2 + dx**2)

    def get_static_heuristics(self):
        return self.locations
