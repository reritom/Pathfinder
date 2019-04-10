from typing import List, Tuple
import math as maths
from .bot_tools import Location, PriorityQueue, distance_between, get_path
from .tools import is_adjacent, surroundings_of, lies_between, none_lie_between, cache, is_further_from
import random

class Bot:
    def __init__(self, position: tuple, destination: tuple):
        self.position = position
        self.destination = destination
        self.target = destination
        self.locations = dict()
        self.previous_positions = [position]
        self.waypoint = None
        self.priority_queue = PriorityQueue()
        self.processed = []
        self.blocks = set()
        self.cache = {}

    def run_round(self, context) -> tuple:
        if self.position == self.target:
            return

        self.blocks = self.blocks.union(context.blocks)
        surroundings = context.surroundings

        # For any new surrounding, add it to the locations with a static heuristic
        for surrounding in surroundings:
            if surrounding not in self.locations:
                self.locations[surrounding] = {
                    'static': self.calculate_static_heuristic(surrounding),
                    'steps': 0
                }

        # If we have already set a waypoint, lets continue with that for now
        if self.waypoint:
            self.position = self.waypoint.pop(0)
            return self.move_to(self.position)

        # We need to determine the waypoint depending on the available positions
        dynamic_heuristics = self.get_dynamic_heuristics(only_untravelled=True)
        location_to_aim_for = self.get_most_valuable_position(dynamic_heuristics)
        self.ltaf = location_to_aim_for

        # If the aim is in the immediate area, we will move there directly
        if is_adjacent(location_to_aim_for, self.position):
            return self.move_to(location_to_aim_for)

        # Else we need to find the best route to the place we are aiming for and create a waypoint
        self.waypoint = get_path(
            start=self.position,
            finish=self.ltaf,
            positions=[
                location
                for location
                in self.locations.keys()
            ]
        )

        return self.move_to(self.waypoint.pop(0))

    def get_most_valuable_position(self, dynamic_locations):
        lowest_key, lowest_value = None, None

        for key, value in dynamic_locations.items():
            if value is None:
                continue

            if lowest_key is None:
                lowest_key, lowest_value = key, value
                continue

            if value < lowest_value:
                lowest_key, lowest_value = key, value

        #print(f'Most valuable position is {lowest_key}, dynamics are {dynamic_locations}')
        return lowest_key

    def move_to(self, position):
        self.previous_positions.append(position)
        self.position = position
        self.locations[position]['steps'] += 1

    def calculate_static_heuristic(self, point: tuple):
        return distance_between(self.target, point)

    def get_static_heuristics(self, only_untravelled=False):
        if only_untravelled:
            return {
                location: value['static']
                for location, value in self.location.items()
                if location not in self.previous_positions
            }

        return {location: value['static'] for location, value in self.locations.items()}

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

    @cache('dynamic')
    def get_dynamic_heuristic(self, location: tuple, cacher=None):
        static = self.locations[location]['static']
        dynamic = static + distance_between(self.position, location)
        #print("Static {}, dynamic between {} {} {}".format(static, self.position, location, dynamic))
        """
        surroundings = [
            surrounding
            for surrounding
            in surroundings_of(location)
            if surrounding in self.previous_positions
            and lies_between(surrounding, location, self.target)
        ]

        dynamic = dynamic*1.5**len(surroundings)
        """

        # Repetition multiplier
        dynamic = dynamic*1.1**self.locations[location]['steps']
        """
        for previous in self.previous_positions:
            if location != previous:
                #print(f'{location}, {previous}')
                if is_further_from(position=location, reference=previous, target=self.target):
                    if none_lie_between(self.blocks, location, previous):
                        # If we have the cache hook, we'll cache this value
                        if cacher:
                            cacher.cache()
                        return None
                    else:
                        #print("Lol")
                        pass
        """

        return dynamic
