import pygame

pygame.init()

font = pygame.font.SysFont('comicsans', 20, True)

class Button:

    def __init__(self, x, y, width, height, text, color, surf):
        self.x = x
        self.y = y
        self.surface = surf
        self.color = color
        self.width = width
        self.height = height
        self.text = text
        self.disable = False

    def disengage(self):

        self.disable = True

    def draw(self):
        text = font.render(self.text, True, (0, 0, 0))

        pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height))
        self.surface.blit(text, (self.x + 9, self.y + 9))

    def check_clicked(self, mousex, mousey):

        return  (self.disable == False) and ((mousex > self.x and mousex < (self.x + self.width)) and (mousey > self.y and mousey < (self.y + self.height)))
        