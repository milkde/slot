from collections import deque
from os import system


HEIGHT = 10
WIDTH = 50
BORDER = ["▒", 2]
SCREENSPACE = deque(deque([], WIDTH) for i in range(HEIGHT))

def scrOutput(pixelToDraw):
    for line in range(HEIGHT):
        for pixel in range(WIDTH):
            pixel = pixelToDraw[line][pixel]
            print(pixel, end="")
        print("")
    
def preRender():
    render = SCREENSPACE
    ## Part to draw the border
    for lines in range(HEIGHT):

        ## drawing top border with given thickness
        if lines <= BORDER[1]:
            for lines in range(BORDER[1]):
                for pixel in range(WIDTH):
                    render[lines].append(BORDER[0])
        
        ## content with border
        if BORDER[1] < lines < HEIGHT - BORDER[1]:
            if pixel <= BORDER[1]:
                for pixel in range(BORDER[1]):
                    render[lines].append(BORDER[0])
            if pixel >= WIDTH - BORDER[1]:
                for pixel in range(BORDER[1]):
                    render[lines].append(BORDER[0])
                
            ## actual content
            else:
                for pixel in range(WIDTH - BORDER[1]):
                    render.append("-")
        
        ## drawing bottom border with given thickness
        if lines >= BORDER[1]:
            for lines in range(BORDER[1]):
                for pixel in range(WIDTH):
                    render[lines].append(BORDER[0])
    return render

scrOutput(preRender())
