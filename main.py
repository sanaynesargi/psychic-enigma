import pygame
from square import Square
from grid import Grid
from button import Button
import time

pygame.init()

S_WIDTH = 800
S_HEIGHT = 515
DIMENSIONS = (S_WIDTH, S_HEIGHT)

win = pygame.display.set_mode(DIMENSIONS)
pygame.display.set_caption("Pathfinding Visualization")

grid = Grid(25, win)
start = Button(650, 200 - 20, 60, 30, "START", (0, 255, 255), win)
end = Button(650, 400 - 20, 60, 30, "END", (255, 0, 255), win)
restart = Button(650, 500 - 20, 60, 30, "REDO", (255, 255, 0), win)

def mark_path(ids):

    for i in ids:

        x, y = grid.get_coordinates_by_id(i)
        grid.change_color_by_coordinates(x, y, (100, 255, 255))
        pygame.display.update()
        


def find_lowest(lst):
    lowest = lst[0]

    for l in lst:
        if l < lowest:
            lowest = l

    return lowest

def draw():

    win.fill((255, 255, 255))
    start.draw()
    end.draw()
    restart.draw()
    grid.draw()



    pygame.display.update()



def main():

    run = True
    while run:

        draw()

        for event in pygame.event.get():
            x, y = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                #grid.clear()
                if start.check_clicked(x, y):
                    grid.stop_counting = False
                    start.disengage()
                    restart.disable = False
                    restart.color = (255, 255, 0)

                if end.check_clicked(x, y) and grid.stop_counting == False:
                    grid.stop_counting = True
                    vals = grid.Solve()
                    
                    mark_path(vals) # Mark the path
                    restart.disable = False
                    restart.color = (255, 255, 0)
                    pygame.display.update()
                    end.disengage()

                if restart.check_clicked(x, y) and start.disable and end.disable:
                    end.disable = False
                    start.disable = False
                    start.color = (0, 0, 255)   
                    end.color = (255, 0, 255)
                    restart.color = (0, 255, 0)
                    grid.clear()
                    grid.walls = []
                    pygame.display.update()
                    restart.disengage()
                
                ## DEV MODE, UNCOMMENT WALLS AND END BLOCK SHOW
                # try:
                #     n = grid.get_id_by_coordinates(x, y)
                #     neighbors = grid.get_neighbors(n)

                #     #print(n)
                #     for ne in neighbors:
                        
                #         a, b = grid.get_coordinates_by_id(ne)
                #         grid.change_color_by_coordinates(a, b, (200, 100, 100))
                # except Exception as e:
                #     print("Try clicking on the grid")
                #     print(e)

            grid.update(event)
        

            #grid.print_ascii()

            
        
            
    pygame.quit()


if __name__ == "__main__":
    main()