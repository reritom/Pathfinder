from typing import List, Tuple
import math as maths
from .bot_tools import Location, PriorityQueue, distance_between
from .tools import is_adjacent, surroundings_of
import random

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
        if self.position == self.target:
            return

        self.blocks = self.blocks.union(context.blocks)
        surroundings = context.surroundings

        # For any new surrounding, add it to the locations with a static heuristic
        for surrounding in surroundings:
            if surrounding not in self.locations:
                self.locations[surrounding] = self.calculate_static_heuristic(surrounding)
                #self.priority_queue.add(Location(surrounding, self.locations[surrounding]))

        # If we have already set a waypoint, lets continue with that for now
        if self.waypoint:
            self.position = self.waypoint.pop(0)
            self.move_to(position)
            return self.position

        # We need to determine the waypoint depending on the available positions
        dynamic_heuristics = self.get_dynamic_heuristics(only_untravelled=True)
        location_to_aim_for = self.get_most_valuable_position(dynamic_heuristics)
        self.ltaf = location_to_aim_for

        # If the aim is in the immediate area, we will move there directly
        if is_adjacent(location_to_aim_for, self.position):
            print("location_to_aim_for {} is adjacent to {}".format(location_to_aim_for, self.position))
            self.move_to(location_to_aim_for)
            return self.position

        print("location_to_aim_for {} is NOT adjacent to {}".format(location_to_aim_for, self.position))
        #self.previous_positions.append(location_to_aim_for)
        # Else we need to find the best route to the place we are aiming for and create a waypoint
        available_neighbours = {
            key: dynamic_heuristics[key]
            for key in surroundings_of(self.position)
            if key in dynamic_heuristics
        }

        # We do something random
        best_key, best_value = None, None
        for key, value in available_neighbours.items():
            if best_key is None:
                best_key, best_value = key, value
            else:
                if value < best_value:
                    best_key, best_value = key, value

        self.move_to(best_key)

    def get_most_valuable_position(self, dynamic_locations):
        lowest_key, lowest_value = None, None

        for key, value in dynamic_locations.items():
            if lowest_key is None:
                lowest_key, lowest_value = key, value
                continue

            if value < lowest_value:
                lowest_key, lowest_value = key, value

        return lowest_key

    def move_to(self, position):
        self.previous_positions.append(position)
        self.position = position

    def calculate_static_heuristic(self, point: tuple):
        return distance_between(self.target, point)

    def get_static_heuristics(self, only_untravelled=False):
        if only_untravelled:
            return {
                location: value
                for location, value in self.location.items()
                if location not in self.previous_positions
            }

        return self.locations

    def get_dynamic_heuristics(self, only_untravelled=False):
        if only_untravelled:
            return {
                location: self.get_dynamic_heuristic(location)
                for location in self.locations.keys()
                if location not in self.previous_positions
            }

        return {
            location: self.get_dynamic_heuristic(location)
            for location in self.locations.keys()
        }

    def get_dynamic_heuristic(self, location: tuple):
        static = self.locations[location]
        dynamic = static + distance_between(self.position, location)
        #print("Static {}, dynamic between {} {} {}".format(static, self.position, location, dynamic))

        # Repetition multiplier
        if location in self.previous_positions:
            dynamic = dynamic*1.1

        # Block surrounding multiplier


        return dynamic
