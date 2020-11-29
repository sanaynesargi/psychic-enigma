import pygame

pygame.init()

class Node:

    def __init__(self, grid, square, row, col, parent=None):

        self.grid = grid
        self.square = square
        self.id = self.square.id
        self.parent = parent
        self.color = self.square.color
        self.x, self.y = self.square.x, self.square.y
        self.dist = None
        self.row = row
        self.column = col
    
    def get_neighbors(self):

        return self.grid.get_neighbors(self.id)


    def check_destination(self, end_id):

        return (self.id == end_id)

    def set_parent(self, parent):

        self.parent = parent

    
    def draw(self):
        self.square.color = self.color
        self.square.draw()

    def check_clicked(self, x, y):
        return self.square.check_clicked(x, y)
