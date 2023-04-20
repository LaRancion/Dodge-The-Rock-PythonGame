# 1 idee aggiungere le vite
# 3 modificare impostazioni del gioco
# aggiungere i credits


#problemi se collisione frontale crasha e non fa schermata gameover
#riniziare il loop delle vite



import pygame
from pygame.locals import *
import random

pygame.init()

# create the window
width = 1280
height = 720
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('SpaceX')



#colori
red = (200, 0, 0)
white = (255, 255, 255)


#larghezza del campo di gioco
#game_width = 1000


# lane coordinates
left_lane = 340#linea dove corrono le macchine e non serve per il player
center_lane = 640
right_lane = 940
lanes = [left_lane, center_lane, right_lane]


# player's starting coordinates
player_x = 640
player_y = 650#calcola come piano cartesiano 

# frame settings
clock = pygame.time.Clock() #?
fps = 120

# game settings
gameover = False
speed = 4
score = 0

class Asteroids(pygame.sprite.Sprite): #?
    
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        # scale the image down so it's not wider than the lane
        image_scale = 100 / image.get_rect().width #da modificare quando cambiamo immagine modifica anche oggetto player e ostacolo
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (new_width, new_height)) #?
        
        self.rect = self.image.get_rect() #?
        self.rect.center = [x, y]
        
class SpaceShip(Asteroids):
    
    def __init__(self, x, y):
        image = pygame.image.load('images/ship.png')#('images/car.png')
        super().__init__(image, x, y)
        


# sprite groups (in teoria per importare le immagini agli oggetti)
player_group = pygame.sprite.Group() #?
asteroid_group = pygame.sprite.Group()

# create the player's car
player = SpaceShip(player_x, player_y) #assegna player a player vehicle e gli assegna l'immagine
player_group.add(player) #?

# load the vehicle images
image_files = ['A1.png', 'A2.png', 'A3.png', 'A4.png', 'A5.png', 'A6.png', 'A7.png', 'A8.png', 'A9.png', 'A10.png', 'A11.png']
asteroid_images = []
for image_filename in image_files:
    image = pygame.image.load('images/' + image_filename)
    asteroid_images.append(image)
    
# load the crash image
collision = pygame.image.load('images/crash.png')
crash_rect = collision.get_rect() #? probabilmente incluso in un rettangolo

vite = 3




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
                player.rect.x -= 300
            elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                player.rect.x += 300
                
            # check if there's a side swipe collision after changing lanes #solo per le collisioni laterali
            
            
    
    screen.fill(white)
    gameDisplay = pygame.display.set_mode((width,height))

    bg = pygame.image.load("images/bg5.jpg")

    #INSIDE OF THE GAME LOOP
    gameDisplay.blit(bg, (0, 0))


    # draw the player's car
    player_group.draw(screen)
    
    # add a vehicle
    if len(asteroid_group) < 2: #spawn rate delle macchine
        
        # ensure there's enough gap between vehicles
        add_asteroid= True
        for asteroid in asteroid_group:
            if asteroid.rect.top < asteroid.rect.height * 1.5: #? si può fare random per renderlo diverso
                add_asteroid = False
                

        if add_asteroid:
            
            # select a random lane
            lane = random.choice(lanes)
            
            # select a random vehicle image
            image = random.choice(asteroid_images)
            asteroid = Asteroids(image, lane, height / - 1000 ) #per modificare la posizione di spawn default(-2)
            asteroid_group.add(asteroid) #?
    
    # make the vehicles move
    for asteroid in asteroid_group:
        asteroid.rect.y += speed
        
        # remove vehicle once it goes off screen
        if asteroid.rect.top >= height:
            asteroid.kill()
            
            # add to score
            score += 1
            
            # speed up the game after passing 5 vehicles
            if score > 0 and score % 5 == 0: #da modificare per vedere la difficoltà
                speed += 1
    
    for asteroid in asteroid_group:
        if pygame.sprite.collide_rect(player, asteroid): #controlla le collisioni

            vite -= 1
                    #aggiungere if per le le vite con sprite e counter 
            if vite == 0:
                gameover = True
                if event.type == KEYDOWN:      #fix errore del keydown error   
                    if event.key == K_LEFT:
                        player.rect.left = asteroid.rect.right
                        crash_rect.center = [player.rect.left, (player.rect.center[1] + asteroid.rect.center[1]) / 2] #per decidere dove far spawnare l'immagine dell'esplosione
                    elif event.key == K_RIGHT:
                        player.rect.right = asteroid.rect.left
                        crash_rect.center = [player.rect.right, (player.rect.center[1] + asteroid.rect.center[1]) / 2]
                    # place the player's car next to other vehicle
                    # and determine where to position the crash image
        else:
            pygame.sprite.spritecollide(player, asteroid_group, True) #metodo diverso
            crash_rect.center = [player.rect.center[0], player.rect.top] #dove spawnare l'immagine
    print(vite)




    # draw the vehicles
    asteroid_group.draw(screen)
    
    # display the score                            #lo score è dentro un rettangono
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render('Score: ' + str(score), True, white)
    text_rect = text.get_rect()
    text_rect.center = (50, 100) #per posizione score
    screen.blit(text, text_rect)   #?
    
    # check if there's a head on collision #collisioni frontali
    #if pygame.sprite.spritecollide(player, asteroid_group, True): #metodo diverso
    #    gameover = True
     #   crash_rect.center = [player.rect.center[0], player.rect.top] #dove spawnare l'immagine
            
    # display game over
    if gameover:
        screen.blit(collision, crash_rect) #?
        
        pygame.draw.rect(screen, red, (0, 50, width, 100))
        
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render('Game over. Vuoi rigiocare? (Clicca S o N)', True, white)
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
                if event.key == K_s:
                    # reset the game
                    vite = 3
                    gameover = False
                    speed = 2
                    score = 0
                    asteroid_group.empty()
                    player.rect.center = [player_x, player_y]
                elif event.key == K_n:
                    # exit the loops
                    gameover = False
                    running = False

pygame.quit()