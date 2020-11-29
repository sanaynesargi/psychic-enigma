import pygame

pygame.init()

class Square:

    def __init__(self, x, y, width, height, color, surf, id):

        self.x = x
        self.y = y
        self.id = id
        self.color = color
        self.width = width
        self.height = height
        self.surface = surf

    def draw(self):
        
        if self.color == None:
            pygame.draw.rect(self.surface, (0, 0, 0), (self.x, self.y, self.width, self.height), 2)
        else:
            pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height), 0)

    def check_clicked(self, mousex, mousey):

        return ((mousex >= self.x and mousex <= (self.x + self.width)) and (mousey >= self.y and mousey <= (self.y + self.height)))

