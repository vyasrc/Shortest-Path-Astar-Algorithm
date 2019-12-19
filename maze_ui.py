import tkinter as tk
import random
import time
import tkinter.messagebox
import threading


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


class Maze(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        master.title("Maze")
        self.pack()
        self.create_widgets()
        self.no_pressed = 0

    def create_widgets(self):
        floors = [i for i in range(600)]
        self.blocks = [random.randrange(0, 600) for i in range(200)]
        self.buttons = {}
        x_pos = 0
        y_pos = 0
        for floor in floors:
            if(y_pos == 30):
                x_pos = x_pos + 1
                y_pos = 0
            if(x_pos == 20):
                y_pos = 2
            button = tk.Button(self, width=3, command=lambda f=floor: self.pressed(f))
            button.grid(row=x_pos, column=y_pos)
            if floor in self.blocks:
                button.configure(bg="black")
            self.buttons[floor] = button
            y_pos = y_pos +1
        self.QUIT = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy).grid(row=x_pos, column=y_pos)

        self.FIND = tk.Button(self, text="FIND", fg="blue",
                              command=self.thread_func).grid(row=x_pos - 1, column=y_pos)

    def pressed(self, index):
        if self.no_pressed == 0:
            self.startNode = Node(index)
            self.open_list = list([self.startNode])
        elif self.no_pressed == 1:
            self.end = index
        else:
            return
        self.no_pressed += 1
        self.buttons[index].configure(bg="green")

    def is_valid(self, neighbor_x, neighbor_y):
        return 0 <= neighbor_x < 20 and 0 <= neighbor_y < 30

    def get_floor_indices(self, current):
        x = self.buttons[current].grid_info()['row']
        y = self.buttons[current].grid_info()['column']
        return x, y

    def neighbors(self, current):
        curr_row, curr_col = self.get_floor_indices(current)
        # top - index
        if self.is_valid(curr_row - 1, curr_col):
            yield current - 30
        # top-right index
        if self.is_valid(curr_row - 1, curr_col + 1):
            yield current - 29
        # top-left index
        if self.is_valid(curr_row - 1, curr_col - 1):
            yield current - 31
        # bottom - index
        if self.is_valid(curr_row + 1, curr_col):
            yield current + 30
        # bottom-right index
        if self.is_valid(curr_row + 1, curr_col + 1):
            yield current + 31
        # bottom-left index
        if self.is_valid(curr_row + 1, curr_col - 1):
            yield current + 29
        # left - index
        if self.is_valid(curr_row, curr_col - 1):
            yield current - 1
        # right - index
        if self.is_valid(curr_row, curr_col + 1):
            yield current + 1

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

    def distance(self, start, end):
        start_row, start_col = self.get_floor_indices(start)
        end_row, end_col = self.get_floor_indices(end)

        dist_x = abs(start_row - end_row)
        dist_y = abs(start_col - end_col)

        if dist_x > dist_y:
            return 14 * dist_y + 10 * (dist_x - dist_y)
        else:
            return 14 * dist_x + 10 * (dist_y - dist_x)

    def shortest_path(self, end):
        while end is not self.startNode:
            yield end.index
            end = end.parent
        yield self.startNode.index

    def thread_func(self):
        self.thread = threading.Thread(target=self.a_star)
        self.thread.start()


    def a_star(self):
        closed_list = []
        flag = True
        while self.open_list:
            current = self.lowest_f_cost()
            self.open_list.remove(current)
            closed_list.append(current.index)
            if current.index == self.end:
                flag = False
                self.path = []
                for node_index in self.shortest_path(current):
                    self.path.append(node_index)
                self.show_path()
                tkinter.messagebox.showinfo('Success', 'Path Found')
                return

            if self.neighbors(current.index):
                for neighbor in self.neighbors(current.index):
                    if neighbor in closed_list or neighbor in self.blocks:
                        continue
                    else:
                        self.buttons[neighbor].configure(bg="red")
                        time.sleep(.25)
                        new_g = current.g + self.distance(current.index, neighbor)
                        new_h = self.distance(neighbor, self.end)
                        new_node = Node(neighbor, current, new_g, new_h)
                        self.update_open_list(new_node)
        if flag:
            tkinter.messagebox.showinfo('Error', 'No Solution')
            return

    def show_path(self):
        for node in self.path[::-1]:
            self.buttons[node].configure(bg="blue")
            time.sleep(.5)

root = tk.Tk()
app = Maze(master=root)
app.mainloop()