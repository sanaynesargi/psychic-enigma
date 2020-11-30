import pygame
from square import Square
from node import Node
import time, random
from collections import deque

pygame.init()


class NotFound(Exception): pass

class Grid:

    def __init__(self, squares_per_row, surf):

        self.squares_per_row = squares_per_row
        self.surface = surf
        self.grid = self.get_grid()
        self.walls = []
        self.stop_counting = True
        self.start = 0
        self.end = 399

    def get_grid(self):

        grid = []
        x, y = 10, 10
        id = 0
        self.squares_per_row = 25
        self.num_of_squares = 500 // self.squares_per_row

        for i in range(self.num_of_squares):
            grid.append([])
            x = 10
            for j in range(self.num_of_squares):
                current_sqr = Square(x, y, self.num_of_squares, self.num_of_squares, None, self.surface, id)
                grid[i].append(Node(self, current_sqr, i, j))
                id += 1
                x += self.squares_per_row

            y += self.squares_per_row  
        
        return grid


    def draw_grid(self):
        for row in self.grid:
            for square in row:
                square.draw()
                


    def draw(self):
        
        self.draw_grid()
        
        pygame.display.update()

    def change_color_by_coordinates(self, x, y, color):

        for i in range(self.num_of_squares):
            for j in range(self.num_of_squares):
                if self.grid[i][j].check_clicked(x, y):
                    
                    self.grid[i][j].color = color
                    return self.grid[i][j].id

    def check_column(self, id):
        
        
        r = list(range(9, 390, 20))
        l = list(range(10, 391, 20))
        
        if id == 0:
            return 0

        if len(str(id)) > 1 and str(id)[-1] == '0' and id % 2 == 0 and id not in l:
            
            return 0

        if str(id)[-1] == '9' and id % 2 != 0 and id not in r:

            return 1

        return -1

    def get_neighbors(self, id):

        possible_ids = {"up": id - self.num_of_squares, "down": id + self.num_of_squares, "right": id + 1, "left": id - 1}
        ids = []

        possible_ids["d-d-l"] = id + 19

        if self.check_column(id) == 0:

            possible_ids = {"up": id - self.num_of_squares, "down": id + self.num_of_squares, "right": id + 1}
            
            
            possible_ids["d-u-l"] = id + self.num_of_squares + 1
            possible_ids["d-u-r"] = id - self.num_of_squares + 1

        if self.check_column(id) == 1:
            possible_ids = {"up": id - self.num_of_squares, "down": id + self.num_of_squares, "left": id - 1}
            possible_ids["d-d-l"] = id + self.num_of_squares - 1
            possible_ids["d-d-r"] = id - self.num_of_squares - 1

        if self.check_column(id) == -1:
           
            possible_ids["d-u-l"] = id + self.num_of_squares + 1
            possible_ids["d-u-r"] = id - self.num_of_squares - 1
            possible_ids["d-d-l"] = id + self.num_of_squares - 1
            possible_ids["d-d-r"] = id - self.num_of_squares + 1

        for val in possible_ids.values():
            if (val <= (self.num_of_squares**2 - 1) and val > -1):
                if val not in self.walls:
                    ids.append(val)

        return ids
                
    def get_id_by_coordinates(self, x, y):

        for i in range(self.num_of_squares):
            for j in range(self.num_of_squares):
                
                if self.grid[i][j].check_clicked(x, y):
                    return self.grid[i][j].id

    def get_index_by_id(self, id):

        for i in range(self.num_of_squares):
            for j in range(self.num_of_squares):
                if self.grid[i][j].id == id:
                    return str(i) + str(j)

    def get_coordinates_by_id(self, id):

        for i in range(self.num_of_squares):
            for j in range(self.num_of_squares):
                if self.grid[i][j].id == id:
                    return (self.grid[i][j].x, self.grid[i][j].y)

    def print_ascii(self):

        for i in range(self.num_of_squares):
            for j in range(self.num_of_squares):
                if self.grid[i][j].g > 0:
                    print(self.grid[i][j].id)

    def update(self, event):

        if not self.stop_counting:
            start_string = self.get_coordinates_by_id(self.start)
            sx, sy = start_string
        
            end_string = self.get_coordinates_by_id(self.end)
            ex, ey = end_string
        
            self.change_color_by_coordinates(sx, sy, (0, 0, 255))
            self.change_color_by_coordinates(ex, ey, (255, 0, 0))   


        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            wall = self.get_id_by_coordinates(x, y)
            if wall not in self.walls:
                if not self.stop_counting:
                    self.walls.append(self.change_color_by_coordinates(x, y, (0, 0, 0)))
                    pass
                
    def preload_neighbors(self):

        neighbours = dict()

        for row in self.grid:
            for square in row:
                neighbours[square.id] = self.get_neighbors(square.id)

    
        return neighbours



    def Solve(self):

        graph = self.preload_neighbors() # create an associative table mapping each node to its neighbors
        
        visited = {self.start: None} # create a dictionary to store the values for each node and its parent
        queue = deque([self.start]) # make a queue to store nodes

        # run a loop while the queue is not empty
        while queue:
            node = queue.popleft() # get a node by popping the first node of the queue

            # check if this node is the end node
            if node == self.end:
                path = [] # make a path array to store the path
                while node is not None: # run a loop while the node in the queue is not none (0) is the end of this
                    path.append(node) # append the node to the path array that stores the path to the end
                    node = visited[node] # for each node, mark the one it came from
                    
                return path[::-1] # return a reversed path from 0 to end

            # if the node is not the end
            for neighbour in graph[node]:
                # if the neighbor has not been visited
                if neighbour not in visited:
                    visited[neighbour] = node # add an entry for this neighbor and make its parent the node that it came from
                    queue.append(neighbour) # add this neighbor to the queue and restart the loop
        
        
        raise NotFound('No path from {} to {}'.format(self.start, self.end))
        
    def clear(self):

        for row in self.grid:

            for square in row:

                square.color = None
   

    def find_diagonal(self, id1, id2):

        pass