import pygame
import random

# initialize pygame
pygame.init()

# set up the screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# set up the game clock
clock = pygame.time.Clock()

# set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# set up player attributes
player_width = 50
player_height = 50
player_x = (screen_width - player_width) / 2
player_y = screen_height - player_height - 10
player_speed = 5

# set up column attributes
column_width = 10
column_height = screen_height
column1_x = 0
column2_x = screen_width / 3
column3_x = (screen_width / 3) * 2

# set up falling object attributes
object_width = 275
object_height = 30
object_speed = 4
object_spawn_rate = 50
objects = []

# set up score
score = 0
font = pygame.font.SysFont(None, 30)

# game loop
running = True
while running:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed
    
    # spawn falling objects
    if random.randint(0, object_spawn_rate) == 0:
        objects.append([random.choice([column1_x, column2_x, column3_x]), 0]) 
    
    # move falling objects
    for obj in objects:
        obj[1] += object_speed
    
    # check for collisions with falling objects
    for obj in objects:
        if player_x < obj[0] + object_width and player_x + player_width > obj[0] and player_y < obj[1] + object_height and player_y + player_height > obj[1]:
            # collision detected
            running = False
    
    # remove off-screen falling objects
    objects = [obj for obj in objects if obj[1] < screen_height]
    
    # draw everything
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, (column1_x, 0, column_width, column_height))
    pygame.draw.rect(screen, BLACK, (column2_x, 0, column_width, column_height))
    pygame.draw.rect(screen, BLACK, (column3_x, 0, column_width, column_height))
    pygame.draw.rect(screen, RED, (player_x, player_y, player_width, player_height))
    for obj in objects:
        pygame.draw.rect(screen, BLACK, (obj[0], obj[1], object_width, object_height))
    score_text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))
    pygame.display.update()
    
    # increment score
    score += 1
    
    # tick the game clock
    clock.tick(60)

screen.fill(WHITE)
game_over_text = font.render("Game Over", True, BLACK)
screen.blit(game_over_text, (screen_width/2 - game_over_text.get_width()/2, screen_height/2 - game_over_text.get_height()/2))
score_text = font.render("Score: " + str(score), True, BLACK)
screen.blit(score_text, (screen_width/2 - score_text.get_width()/2, screen_height/2 - score_text.get_height()/2 + 50))
pygame.display.update()

# wait for user to quit
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    
    # add a delay to reduce CPU usage
    pygame.time.delay(100)

