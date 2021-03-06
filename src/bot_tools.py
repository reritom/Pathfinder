import math as maths
from typing import List, Optional
from .tools import surroundings_of, get_artificial_blocks

def print_heuristics_lowest_first(heuristics):
    for key in sorted(heuristics, key=heuristics.get):
        print(f"{key} {heuristics[key]}")

def get_neighbours(position: tuple, positions: List[tuple]):
    return [
        surrounding
        for surrounding in surroundings_of(position)
        if surrounding in positions
    ]

def get_path(start: tuple, finish: tuple, positions: List[tuple]) -> List[tuple]:
    queue = PriorityQueue()
    finished = PriorityQueue()
    queue.add(
        Location(
            position=start,
            path_cost=0,
            heuristic=distance_between(start, finish),
            route=None
        )
    )

    reached_finish = False

    while queue.positions:
        # Take the top priority item
        top_priority = queue.pop_top()

        if top_priority.position == finish:
            # We've found the finish
            finished.add(top_priority)
            reached_finish = True
            break

        # All the technically available neighbouring positions
        neighbours = get_neighbours(top_priority.position, positions)

        # As the bot can't move diagonally between two blocks, we determine the blocks, then determine any artificial blocks
        neighbour_blocks = {
            surrounding
            for surrounding in surroundings_of(top_priority.position)
            if surrounding not in neighbours
        }

        neighbour_blocks = neighbour_blocks.union(
            get_artificial_blocks(
                top_priority.position,
                neighbour_blocks
            )
        )

        neighbours = {
            neighbour
            for neighbour in neighbours
            if neighbour not in neighbour_blocks
        }

        for neighbour in neighbours:
            queue.add(
                Location(
                    position=neighbour,
                    path_cost=top_priority.path_cost + distance_between(top_priority.position, neighbour),
                    heuristic=distance_between(top_priority.position, neighbour) + distance_between(neighbour, finish),
                    route=top_priority.position
                )
            )

        finished.add(top_priority)

    # Looking at the completed queue, we can find the route
    if reached_finish:
        finish_item = finished.top
        route = [finish]
        item_to_get = finish
    else:
        finish_item = finished.top
        route = [finish_item.position]
        item_to_get = finish_item.position

    while finished.get_item_by_position(item_to_get).route is not None:
        item = finished.get_item_by_position(item_to_get)
        route.append(item.route)
        item_to_get = item.route

    route.reverse()
    return route


class Location:
    def __init__(self, position: tuple, heuristic: int, path_cost: int, route: Optional[tuple]):
        self.position = position
        self.heuristic = heuristic
        self.path_cost = path_cost
        self.route = route

class PriorityQueue():
    def __init__(self):
        self.queue_items = []
        self.positions = []
        self.processed = []

    def add(self, new_item):
        # If we already contain the item, check the new heuristic and replace it if it is better
        if new_item.position in self.positions:
            #print("{} IN queue".format(new_item.position))
            # It already exists
            existing_index = self.positions.index(new_item.position)
            #print("index is {}".format(existing_index))

            if self.queue_items[existing_index].heuristic > new_item.heuristic:
                #print("new heuristic is better")
                self.queue_items[existing_index] = new_item
            elif self.queue_items[existing_index].heuristic == new_item.heuristic:
                #print("heuristic is equal")
                # TODO Handle this better
                return
            else:
                return

        if new_item.position in self.processed:
            return

        # It doesn't already exist, so find the right place to insert it
        #print("{} Doesnt exist, adding it".format(new_item.position))
        for index, existing_item in enumerate(self.queue_items):
            if new_item.heuristic <= existing_item.heuristic:
                #print("Inserting")
                self.queue_items.insert(index, new_item)
                self.positions.insert(index, new_item.position)
                break
        else:
            #print("Appending")
            self.positions.append(new_item.position)
            self.queue_items.append(new_item)

    @property
    def top(self):
        return self.queue_items[0]

    def pop_top(self):
        self.processed.append(self.positions.pop(0))
        return self.queue_items.pop(0)

    def get_item_by_position(self, position):
        try:
            index = self.positions.index(position)
            return self.queue_items[index]
        except:
            return None

def distance_between(point_a, point_b):
    dy = abs(point_a[1] - point_b[1])
    dx = abs(point_a[0] - point_b[0])
    return abs(maths.sqrt(dx**2 + dy**2))
