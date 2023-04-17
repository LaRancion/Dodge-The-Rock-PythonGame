#idee aggiungere le vite
#modificare tutte le variabili 
#modificare le immagini
#modificare impostazioni del gioco

import pygame
from pygame.locals import *
import random

pygame.init()

# create the window
width = 500
height = 500
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('SpaceX')

# colors
gray = (100, 100, 100)
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)

# road and marker sizes
road_width = 300 
marker_width = 10
marker_height = 50

# lane coordinates
left_lane = 150 #linea dove corrono le macchine e non serve per il player
center_lane = 250
right_lane = 350
lanes = [left_lane, center_lane, right_lane]

# road and edge markers
road = (100, 0, road_width, height)
left_edge_marker = (95, 0, marker_width, height) #bordi della strada
right_edge_marker = (395, 0, marker_width, height)

# for animating movement of the lane markers
lane_marker_move_y = 0 #fa muovere line trattegiate bianche in base alla velocità

# player's starting coordinates
player_x = 350
player_y = 400 #calcola come piano cartesiano 

# frame settings
clock = pygame.time.Clock() #?
fps = 120

# game settings
gameover = False
speed = 2 
score = 0

class Vehicle(pygame.sprite.Sprite): #?
    
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        # scale the image down so it's not wider than the lane
        image_scale = 45 / image.get_rect().width #da modificare quando cambiamo immagine modifica anche oggetto player e ostacolo
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (new_width, new_height)) #?
        
        self.rect = self.image.get_rect() #?
        self.rect.center = [x, y]
        
class PlayerVehicle(Vehicle):
    
    def __init__(self, x, y):
        image = pygame.image.load('images/spaceship.png')#('images/car.png')
        super().__init__(image, x, y)
        
# sprite groups (in teoria per importare le immagini agli oggetti)
player_group = pygame.sprite.Group() #?
vehicle_group = pygame.sprite.Group()

# create the player's car
player = PlayerVehicle(player_x, player_y) #assegna player a player vehicle e gli assegna l'immagine
player_group.add(player) #?

# load the vehicle images
image_filenames = ['asteroid.png']#  ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png'] #spawn viene richiamato random?
vehicle_images = []
for image_filename in image_filenames:
    image = pygame.image.load('images/' + image_filename)
    vehicle_images.append(image)
    
# load the crash image
crash = pygame.image.load('images/crash.png')
crash_rect = crash.get_rect() #? probabilmente incluso in un rettangolo

# game loop
running = True
while running:
    
    clock.tick(fps)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False #per interrompere il ciclo
            
        # move the player's car using the left/right arrow keys
        if event.type == KEYDOWN: #contenitore quando premi un tasto lo rileva
            
            if event.key == K_LEFT and player.rect.center[0] > left_lane: #se modifico possono spostare 4 volte 
                player.rect.x -= 100
            elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                player.rect.x += 100
                
            # check if there's a side swipe collision after changing lanes #solo per le collisioni laterali
            for vehicle in vehicle_group:
                if pygame.sprite.collide_rect(player, vehicle): #controlla le collisioni
                    

                    #aggiungere if per le le vite con sprite e counter 

                    gameover = True
                    
                    # place the player's car next to other vehicle
                    # and determine where to position the crash image
                    if event.key == K_LEFT:
                        player.rect.left = vehicle.rect.right
                        crash_rect.center = [player.rect.left, (player.rect.center[1] + vehicle.rect.center[1]) / 2] #per decidere dove far spawnare l'immagine dell'esplosione
                    elif event.key == K_RIGHT:
                        player.rect.right = vehicle.rect.left
                        crash_rect.center = [player.rect.right, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
            
            
    # draw the grass
    screen.fill(green) #da modificare il colore
    
    # draw the road
    pygame.draw.rect(screen, gray, road) #? da modificare il colore
    
    # draw the edge markers
    #pygame.draw.rect(screen, yellow, left_edge_marker)
    #pygame.draw.rect(screen, yellow, right_edge_marker)
    
    # draw the lane markers
    #lane_marker_move_y += speed * 2
    #if lane_marker_move_y >= marker_height * 2:
     #   lane_marker_move_y = 0
    #for y in range(marker_height * -2, height, marker_height * 2):
     #   pygame.draw.rect(screen, white, (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
      #  pygame.draw.rect(screen, white, (center_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        
    # draw the player's car
    player_group.draw(screen)
    
    # add a vehicle
    if len(vehicle_group) < 2: #spawn rate delle macchine
        
        # ensure there's enough gap between vehicles
        add_vehicle = True
        for vehicle in vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 1.5: #? si può fare random per renderlo diverso
                add_vehicle = False
                
        if add_vehicle:
            
            # select a random lane
            lane = random.choice(lanes)
            
            # select a random vehicle image
            image = random.choice(vehicle_images)
            vehicle = Vehicle(image, lane, height / - 1000 ) #per modificare la posizione di spawn default(-2)
            vehicle_group.add(vehicle) #?
    
    # make the vehicles move
    for vehicle in vehicle_group:
        vehicle.rect.y += speed
        
        # remove vehicle once it goes off screen
        if vehicle.rect.top >= height:
            vehicle.kill()
            
            # add to score
            score += 1
            
            # speed up the game after passing 5 vehicles
            if score > 0 and score % 5 == 0: #da modificare per vedere la difficoltà
                speed += 1
    
    # draw the vehicles
    vehicle_group.draw(screen)
    
    # display the score                            #lo score è dentro un rettangono
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render('Score: ' + str(score), True, white)
    text_rect = text.get_rect()
    text_rect.center = (50, 100) #per posizione score
    screen.blit(text, text_rect)   #?
    
    # check if there's a head on collision #collisioni frontali
    if pygame.sprite.spritecollide(player, vehicle_group, True): #metodo diverso
        gameover = True
        crash_rect.center = [player.rect.center[0], player.rect.top] #dove spawnare l'immagine
            
    # display game over
    if gameover:
        screen.blit(crash, crash_rect) #?
        
        pygame.draw.rect(screen, red, (0, 50, width, 100))
        
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render('Game over. Play again? (Enter Y or N)', True, white)
        text_rect = text.get_rect()
        text_rect.center = (width / 2, 100)
        screen.blit(text, text_rect)
            
    pygame.display.update()

    # wait for user's input to play again or exit
    while gameover:
        
        clock.tick(fps)
        
        for event in pygame.event.get():
            
            if event.type == QUIT: #se premi la x in alto o chiudi il gioco
                gameover = False
                running = False
                
            # get the user's input (y or n)
            if event.type == KEYDOWN: #running mai in false
                if event.key == K_y:
                    # reset the game
                    gameover = False
                    speed = 2
                    score = 0
                    vehicle_group.empty()
                    player.rect.center = [player_x, player_y]
                elif event.key == K_n:
                    # exit the loops
                    gameover = False
                    running = False

pygame.quit()