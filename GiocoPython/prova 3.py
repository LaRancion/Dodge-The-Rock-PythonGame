
import pygame
import sys


width = 1280
height = 720

#inizializzazione colori
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

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

class Player(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, speed):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 0, 0))  # colore rosso
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
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

class object:
    def __init__(self, x, column):
        self.x = x
        self.y = 0
        self.column = column
        self.speed = 5
    
    def update(self):
        self.y += self.speed
    
    
    def is_off_screen(self):
        return self.y > height
    
    


# esempio di utilizzo della classe
pygame.init()
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

player = Player(player_width, player_height, player_x, player_y, player_speed)
all_sprites = pygame.sprite.Group(player)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(white)
    pygame.draw.rect(screen, black, (column1_x, 0, column_width, column_height))
    pygame.draw.rect(screen, black, (column2_x, 0, column_width, column_height))
    pygame.draw.rect(screen, black, (column3_x, 0, column_width, column_height))
    pygame.draw.rect(screen, black, (0, linea1_y,  linea_width, linea_height))
    pygame.draw.rect(screen, black, (0, linea2_y, linea_width, linea_height))
    pygame.draw.rect(screen, black, (0, linea3_y, linea_width, linea_height))
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)  # limita il frame rate a 60 fps