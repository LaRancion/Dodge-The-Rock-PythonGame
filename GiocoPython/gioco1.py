import pygame
import random

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Initialize Pygame
pygame.init()

# Set dimensions of window
WINDOW_SIZE = [1280,720]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of window
pygame.display.set_caption("3x3 Grid")

# Load background image
background_image = pygame.image.load("maxresdefault.jpg").convert()

# Set font for text
font = pygame.font.SysFont('Arial', 25)

# Set dimensions of grid squares
SQUARE_SIZE = 250

# Set margin between squares
MARGIN = 1

# Create grid
grid = []
for row in range(3):
    grid.append([])
    for column in range(3):
        grid[row].append(0)
        


# Set coordinates for top-left corner of grid
x = (WINDOW_SIZE[0] - (SQUARE_SIZE * 3 + MARGIN * 2)) / 2
y = (WINDOW_SIZE[1] - (SQUARE_SIZE * 3 + MARGIN * 2)) / 2

# Loop until the user clicks the close button
done = False

last_object_time = pygame.time.get_ticks()

# Main program loop
while not done:
    # Handle events
    #for event in pygame.event.get():
        #if event.type == pygame.QUIT:
            #done = True

    # Blit background image onto screen
    screen.blit(background_image, [0, 0])

    # Draw grid
    for row in range(3):
        for column in range(3):
            pygame.draw.rect(screen, BLACK, [x + column * (SQUARE_SIZE + MARGIN),
                                             y + row * (SQUARE_SIZE + MARGIN),
                                             SQUARE_SIZE, SQUARE_SIZE], 2)

    


 
   
    # Update screen
    pygame.display.flip()

    # Set frame rate
    clock = pygame.time.Clock()
    clock.tick(60)

# Quit Pygame
pygame.quit()

