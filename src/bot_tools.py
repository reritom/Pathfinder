import math as maths

class Location:
    def __init__(self, position: tuple, heuristic):
        self.position = position
        self.heuristic = heuristic

class PriorityQueue(list):
    def add(self, new_item):
        # If we already contain the item, check the new heuristic and replace it if it is better
        if new_item.position in self.position_list:
            # It already exists
            existing_index = self.position_list.index(new_item.position)

            if self[existing_index].heuristic > new_item.heuristic:
                self.pop(existing_index)
                return self.add(new_item)
            elif self[existing_index].heuristic == new_item.heuristic:
                # TODO Handle this better
                return
            else:
                return

        # It doesn't already exist, so find the right place to insert it
        for index, existing_item in enumerate(self[:]):
            if new_item.heuristic <= existing_item.heuristic:
                super().insert(index, new_item)
        else:
            return super().append(new_item)

    @property
    def top(self):
        return self[0]

    def pop_top(self):
        return self.pop(0)

    def get_item_by_position(self, position):
        index = self.positon_list.index(position)
        return self[index]

    @property
    def position_list(self):
        return [item.position for item in self[:]]

def distance_between(point_a, point_b):
    dy = abs(point_a[1] - point_b[1])
    dx = abs(point_a[0] - point_b[0])
    return abs(maths.sqrt(dx**2 + dy**2))
