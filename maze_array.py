import numpy as np


class Node:
    def __init__(self, index, parent=None, g=0, h=0):
        self.index = index
        self.parent = parent
        self.g = g
        self.h = h
        self.f = self.g + self.h

    def display(self):
        print("Index: {}".format(self.index))
        print("Parent: {}".format(self.parent))
        print("G: {}".format(self.g))
        print("H: {}".format(self.h))
        print("F: {}".format(self.f))


class Maze:
    def __init__(self, size_x, size_y):
        self.array = np.zeros((size_x, size_y))
        np.put(self.array, np.random.choice(range(size_x * size_y), int(size_x * size_y * 0.25), replace=False), 1)
        self.start_index = tuple(map(int, input("Enter the start index values: ").split()))
        self.end_index = tuple(map(int, input("Enter the end index values: ").split()))
        self.array[self.start_index[0]][self.start_index[1]] = 2
        self.array[self.end_index[0]][self.end_index[1]] = 2
        self.startNode = Node(self.start_index)
        self.open_list = list([self.startNode])
        print(self.array)

    def is_valid(self, neighbor_x, neighbor_y):
        return 0 <= neighbor_x < self.array.shape[0] and 0 <= neighbor_y < self.array.shape[1]

    def neighbors(self, current):
        # top - index
        if self.is_valid(current[0] - 1, current[1]):
            yield (current[0] - 1, current[1])
        # top-right index
        if self.is_valid(current[0] - 1, current[1] + 1):
            yield (current[0] - 1, current[1] + 1)
        # top-left index
        if self.is_valid(current[0] - 1, current[1] - 1):
            yield (current[0] - 1, current[1] - 1)
        # bottom - index
        if self.is_valid(current[0] + 1, current[1]):
            yield (current[0] + 1, current[1])
        # bottom-right index
        if self.is_valid(current[0] + 1, current[1] + 1):
            yield (current[0] + 1, current[1] + 1)
        # bottom-left index
        if self.is_valid(current[0] + 1, current[1] - 1):
            yield (current[0] + 1, current[1] - 1)
        # left - index
        if self.is_valid(current[0], current[1] - 1):
            yield (current[0], current[1] - 1)
        # right - index
        if self.is_valid(current[0], current[1] + 1):
            yield (current[0], current[1] + 1)

    def lowest_f_cost(self):
        if len(self.open_list) == 1:
            return self.open_list[0]
        else:
            current_f = self.open_list[0].f
            current = self.open_list[0]
            for node in self.open_list:
                if node.f < current_f:
                    current = node
            return current

    def update_open_list(self, neighbor):
        flag = True
        if self.open_list is not None:
            for node in self.open_list:
                if node.index == neighbor.index:
                    flag = False
                    if neighbor.f < node.f:
                        node.f = neighbor.f
                        node.parent = neighbor.parent
            if flag:
                self.open_list.append(neighbor)

    @staticmethod
    def distance(start, end):
        dist_x = abs(start[0] - end[0])
        dist_y = abs(start[1] - end[1])

        if dist_x > dist_y:
            return 14 * dist_y + 10 * (dist_x - dist_y)
        else:
            return 14 * dist_x + 10 * (dist_y - dist_x)

    def shortest_path(self, end):
        while end is not self.startNode:
            yield end.index
            end = end.parent
        yield self.start_index

    def a_star(self):
        closed_list = []
        flag = True
        while self.open_list:
            current = self.lowest_f_cost()
            self.open_list.remove(current)
            closed_list.append(current.index)

            if current.index == self.end_index:
                flag = False
                self.path = []
                for node_index in self.shortest_path(current):
                    self.path.append(node_index)
                self.show_path()
                return

            if self.neighbors(current.index):
                for neighbor in self.neighbors(current.index):
                    if neighbor in closed_list or self.array[neighbor[0]][neighbor[1]] == 1:
                        continue
                    else:
                        new_g = current.g + self.distance(current.index, neighbor)
                        new_h = self.distance(neighbor, self.end_index)
                        new_node = Node(neighbor, current, new_g, new_h)
                        self.update_open_list(new_node)
        if flag:
            print("No Solution")
            return

    def show_path(self):
        print("Path indices : ", end = " ")
        for node in self.path[::-1]:
            print(node, end=" ")
            self.array[node[0]][node[1]] = 2
        print()
        print(self.array)


x, y = map(int, input("Enter the dimension of the maze: ").split())
ob = Maze(x, y)
ob.a_star()


