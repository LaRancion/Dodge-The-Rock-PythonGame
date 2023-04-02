# importing the required libraries
import pygame as pg
import sys
import time
from pygame.locals import *
import random


# to set width of the game window
width = 1280

# to set height of the game window
height = 720

# to set background color of the
# game window
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# settings  del player
player_width = 50
player_height = 50
player_x = (width - player_width) / 2
player_y = height - player_height - 10
player_speed = 5


# settings delle colonne
column_width = 10
column_height = height
column1_x = 0
column2_x = width / 3
column3_x = (width / 3) * 2

#settings delle linee
linea_width = width
linea_height =  10
linea1_y = height / 3
linea2_y = (height / 3) * 2
linea3_y = 0


# settings degli ostacoli
object_width = 30
object_height = 30
object_speed = 1
object_spawn_rate = 100
objects = []

# inizializzazione punteggio
score = 0

# initializing the pygame window
pg.init()
run = True


# this method is used to build the
# infrastructure of the display
screen = pg.display.set_mode((width, height), 0, 32)

# setting up a nametag for the
# game window
pg.display.set_caption("Gioco Bello")

# loading the images as python object

font = pg.font.SysFont(None, 30)

# resizing images





while run:

    for event in pg.event.get():

        if event.type == pg.QUIT:
            run =False

    screen.fill(white)
    
    pg.draw.rect(screen, black, (column1_x, 0, column_width, column_height))
    pg.draw.rect(screen, black, (column2_x, 0, column_width, column_height))
    pg.draw.rect(screen, black, (column3_x, 0, column_width, column_height))
    pg.draw.rect(screen, black, (0, linea1_y,  linea_width, linea_height))
    pg.draw.rect(screen, black, (0, linea2_y, linea_width, linea_height))
    pg.draw.rect(screen, black, (0, linea3_y, linea_width, linea_height))
    pg.draw.rect(screen, red, (player_x, player_y, player_width, player_height))
    for obj in objects:
        pg.draw.rect(screen, black, (obj[0], obj[1], object_width, object_height))
    score_text = font.render("Score: " + str(score), True, black)
    screen.blit(score_text, (10, 10))
    
    pg.display.update()

    #TASTI GIOCATORE 

    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pg.K_RIGHT] and player_x < width - player_width:
        player_x += player_speed

    #SPAWN OGGETTI

    if random.randint(0, object_spawn_rate) == 0:
        objects.append([random.choice([column1_x, column2_x, column3_x]), 0]) #or objects.append([random.choice([column1_x, column3_x]), 0]) or objects.append([random.choice([column2_x, column3_x]), 0])


    for obj in objects:
        obj[1] += object_speed

   # rimuove gli oggetti
    objects = [obj for obj in objects if obj[1] < height]


pg.quit()

