from typing import List, Tuple
import math as maths
from .bot_tools import Location, PriorityQueue, distance_between

class Bot:
    def __init__(self, position: tuple, target: tuple):
        self.position = position
        self.target = target
        self.locations = dict()
        self.previous_positions = [position]
        self.waypoint = None
        self.priority_queue = PriorityQueue()
        self.processed = []
        self.blocks = set()

    def run_round(self, context) -> tuple:
        self.blocks = self.blocks.union(context.blocks)
        surroundings = context.surroundings

        # For any new surrounding, add it to the locations with a static heuristic
        for surrounding in surroundings:
            if surrounding not in self.locations:
                self.locations[surrounding] = self.calculate_static_heuristic(surrounding)
                #self.priority_queue.add(Location(surrounding, self.locations[surrounding]))

        # If we have already set a waypoint, lets continue with that for now
        #if self.waypoint:
        #    self.position = self.waypoint.pop(0)
        #    return self.position



    def move_to(self, position):
        self.previous_positions.append(position)
        self.position = position

    def calculate_static_heuristic(self, point: tuple):
        return distance_between(self.target, point)

    def get_static_heuristics(self):
        return self.locations

    def get_dynamic_heuristics(self):
        return {
            location: self.get_dynamic_heuristic(location)
            for location
            in self.locations.keys()
        }

    def get_dynamic_heuristic(self, location: tuple):
        static = self.locations[location]
        dynamic = static + distance_between(self.position, location)
        print("Static {}, dynamic between {} {} {}".format(static, self.position, location, dynamic))

        # Repetition multiplier
        if location in self.previous_positions:
            dynamic = dynamic*1.1

        # Block surrounding multiplier


        return dynamic
