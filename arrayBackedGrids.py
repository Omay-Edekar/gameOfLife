"""
 Pygame base template for opening a window
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/vRB_983kUMc
"""
 
import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Define some variables
grid = [[0 for x in range(10)] for y in range(10)]
grid[1][5] = 1

pygame.init()
 
# Set the width and height of the screen [width, height]
size = (255, 255)

width = 20
height = 20
margin = 5

screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while not done:

    click = False

    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True
 
    # --- Game logic should go here
    if click == True:
        pos = pygame.mouse.get_pos()
        row = pos[1]//(width + margin)
        column = pos[0]//(height + margin)
        grid[row][column] = 1
        print("Row:", row, " Column:", column)

    # --- Screen-clearing code goes here
 
    # Here, we clear the screen to black. Don't put other drawing commands
    # above this, or they will be erased with this command.
 
    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(BLACK)
 
    # --- Drawing code should go here

    for row in range(10):
        for column in range(10):
            color = WHITE
            if grid[row][column] == 1:
                color = GREEN
            pygame.draw.rect(screen, color, (0 + column*width + (column+1)*margin, 0 + row*width + (row+1)*margin, width, height))

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()