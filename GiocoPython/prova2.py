import pygame as pg
import sys
import time
from pygame.locals import *
import random

#larghezza e altezza della finestra
width = 1280
height = 720


pg.init()
run = True
screen = pg.display.set_mode((width, height))
clock = pg.time.Clock()



#inizializzazione colori
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

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

player_width = 50
player_height = 50
player_x = (width - player_width) / 2
player_y = height - player_height - 10
player_speed = 5

#giocatore

class Player(pg.sprite.Sprite):
    def init(self, width, height, x, y, speed):
        super().init()
        #self.image = pygame.Surface((width, height))
        self.image.fill(red) # colore rosso
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    
        def update(self):
            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT]:
                self.rect.x -= self.speed
            if keys[pg.K_RIGHT]:
                self.rect.x += self.speed
            if keys[pg.K_UP]:
                self.rect.y -= self.speed
            if keys[pg.K_DOWN]:
                self.rect.y += self.speed

    # controlla se il player è fuori dalla finestra
            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > width:
                self.rect.right = width
            if self.rect.top < 0:
                self.rect.top = 0
            elif self.rect.bottom > height:
                self.rect.bottom = height
                
screen = pg.display.set_mode((width, height))
clock = pg.time.Clock()
screen = pg.display.set_mode((width, height), 0, 32)
player = Player(player_width, player_height, player_x, player_y, player_speed)
all_sprites = pg.sprite.Group(player)
        
        
while run:

    for event in pg.event.get():

        if event.type == pg.QUIT:
            run =False

    screen.fill(white)
    #pg.display.update()
    all_sprites.update()
    all_sprites.draw(screen)
    pg.display.flip()
    clock.tick(60)
    
    pg.draw.rect(screen, black, (column1_x, 0, column_width, column_height))
    pg.draw.rect(screen, black, (column2_x, 0, column_width, column_height))
    pg.draw.rect(screen, black, (column3_x, 0, column_width, column_height))
    pg.draw.rect(screen, black, (0, linea1_y,  linea_width, linea_height))
    pg.draw.rect(screen, black, (0, linea2_y, linea_width, linea_height))
    pg.draw.rect(screen, black, (0, linea3_y, linea_width, linea_height))
    pg.display.update()
    
pg.quit()
sys.exit()