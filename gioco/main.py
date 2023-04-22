#bug animazione esplosione è sempre frontale se muovo con A o D

import pygame
from pygame.locals import *
import random

#pygame inizializzazione
pygame.init()

# dimensioni finestra di gioco
width = 1280
height = 720

screen_size = (width, height) 
screen = pygame.display.set_mode(screen_size) 
pygame.display.set_caption('Dodge The Rock') #nome del gioco


#colori utilizzati nel gioco
red = (200, 0, 0)
white = (255, 255, 255)



# posizioni delle linee immaginarie su cui corrono gli asteroidi e il su cui si sposta il giocatore 
left_lane = 340
center_lane = 640
right_lane = 940
lanes = [left_lane, center_lane, right_lane]


# coordinate d'inizio del giocatore
player_x = 640
player_y = 650

# frame settings
clock = pygame.time.Clock() #?
fps = 120

# impostazioni di gioco
gameover = False
speed = 10
score = 0

#classe generale per gli oggetti del gioco, il player sarà una sotto classe
class Asteroids(pygame.sprite.Sprite): 
    
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        # scala l'immagine perchè sia più piccola della colonna
        image_scale = 100 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (new_width, new_height)) #assegna all'immagine le nuove dimensioni calcolate
        
        self.rect = self.image.get_rect() 
        self.rect.center = [x, y]
        
class SpaceShip(Asteroids):   #classe del player
    
    def __init__(self, x, y):
        image = pygame.image.load('images/ship.png')
        super().__init__(image, x, y)
        


# sprite groups per importare + immagini sugli oggetti 
player_group = pygame.sprite.Group() 
asteroid_group = pygame.sprite.Group()


# crea player utilizzato per calcolare le posizioni e le collisioni
player = SpaceShip(player_x, player_y) #associa a player la classe SpaceShip e gli passa l'immagine
player_group.add(player) #?

# immagini degli asteroidi
image_files = ['A1.png', 'A2.png', 'A3.png', 'A4.png', 'A5.png', 'A6.png', 'A7.png', 'A8.png', 'A9.png', 'A10.png', 'A11.png']
asteroid_images = []
for image_filename in image_files:  #ciclo per variare l'immagine dell'asteroide
    image = pygame.image.load('images/' + image_filename)
    asteroid_images.append(image)
    
# assegna immagine alla collisione e 
collision = pygame.image.load('images/crash.png')
crash_rect = collision.get_rect()

vite = 3

# game loop
running = True
while running:
    
    clock.tick(fps)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False #per interrompere il ciclo
            
                                            # movimenti del player in base ai tasti che si premono
        if event.type == KEYDOWN:           #contenitore quando premi un tasto lo rileva
            if event.key == K_LEFT  and player.rect.center[0] > left_lane: 
                player.rect.x -= 300
            elif event.key == K_a  and player.rect.center[0] > left_lane: 
                player.rect.x -= 300
            elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                player.rect.x += 300
            elif event.key == K_d and player.rect.center[0] < right_lane:
                player.rect.x += 300
                
        
    #ciclo di controllo delle collisioni e delle vite   
    for asteroid in asteroid_group:
        if pygame.sprite.spritecollide(player, asteroid_group, True): #controlla le collisioni e sottrae una vita
            vite -= 1
                    
            if vite == 0:                      #controllo per quando finiscono le vite
                gameover = True                #interrompe il gioco facendo partire il ciclo del gameover
                if event.type == KEYDOWN:      #fix errore del keydown error   
                    if event.key == K_LEFT:    #controlli per le collisioni laterali e per load immagine della collisione nel lato di contatto
                        player.rect.left = asteroid.rect.right
                        crash_rect.center = [player.rect.left, (player.rect.center[1] + asteroid.rect.center[1]) / 2]
                    elif event.key == K_a:
                        player.rect.left = asteroid.rect.right
                        crash_rect.center = [player.rect.left, (player.rect.center[1] + asteroid.rect.center[1]) / 2]
                    elif event.key == K_RIGHT:
                        player.rect.right = asteroid.rect.left
                        crash_rect.center = [player.rect.right, (player.rect.center[1] + asteroid.rect.center[1]) / 2]
                    elif event.key == K_d:
                        player.rect.right = asteroid.rect.left
                        crash_rect.center = [player.rect.right, (player.rect.center[1] + asteroid.rect.center[1]) / 2]
                else:
                    crash_rect.center = [player.rect.center[0], player.rect.top]  #per collisione frontale quindi senza pressione di un tasto

    #print(vite)        
    
    screen.fill(white)
    gameDisplay = pygame.display.set_mode((width,height))

    #immagine di backgroud
    bg = pygame.image.load("images/bg5.jpg")
    gameDisplay.blit(bg, (0, 0))

    # load immagine del cuore
    heart_image = pygame.image.load('images/heart.png')
    heart_rect = heart_image.get_rect()
    heart_x = 50
    heart_y = 250
    heart_rect.center = (heart_x, heart_y)
    screen.blit(heart_image, heart_rect) #la posiziona

    #"disegna" l'immagine del player sullo schermo
    player_group.draw(screen)
    
    # ciclo per lo spawn degli asteroidi
    if len(asteroid_group) < 2: #spawn rate degli oggetti
        
        # controllo del gap tra gli oggetti
        add_asteroid= True
        for asteroid in asteroid_group:
            if asteroid.rect.top < asteroid.rect.height * 1.5: # si può fare random per renderlo diverso e generare meno pattern?
                add_asteroid = False
                
        #controllo in quale colonna spawnare l'oggetto
        if add_asteroid:
            
            lane = random.choice(lanes)
            
            #selezione di un immagine random
            image = random.choice(asteroid_images)
            asteroid = Asteroids(image, lane, height / - 1000 ) #per modificare la posizione di spawn default(-2)
            asteroid_group.add(asteroid) #?
    
    #ciclo per il movimento lungo le colonne degli asteroidi
    for asteroid in asteroid_group:
        asteroid.rect.y += speed
        
        # rimuove gli oggetti quando escono dallo schermo
        if asteroid.rect.top >= height:
            asteroid.kill()
            
            # aumenta lo score quando l'oggetto esce dallo schermo
            score += 1
            
            # aumenta la difficoltà ogni volta che lo score è divisibile per 5 aumentato la velocità di +1
            if score > 0 and score % 5 == 0: #da modificare per aumentare o diminuire la difficoltà
                speed += 1
    
    # "disegna" gli asteroidi
    asteroid_group.draw(screen)
    
    # display dello  score lo score è dentro un rettangono
    font = pygame.font.Font(pygame.font.get_default_font(), 25)
    text = font.render('Score: ' + str(score), True, white)
    text_rect = text.get_rect()
    text_rect.center = (60, 200) #per posizione score
    screen.blit(text, text_rect)  
    
    #display vite
    text = font.render(' '  + str(vite), True, white)
    text_rect = text.get_rect()
    text_rect.center = (90, 250) 
    screen.blit(text, text_rect)  
    
    #diplay tasti da muovere
    font = pygame.font.Font(pygame.font.get_default_font(), 20)
    text = font.render('Moves:'  , True, white)
    text_rect = text.get_rect()
    text_rect.center = (115, 500) 
    screen.blit(text, text_rect)

    text = font.render('left (left_arrow or A )'  , True, white)
    text_rect = text.get_rect()
    text_rect.center = (115, 525) 
    screen.blit(text, text_rect)

    text = font.render('right (right_arrow or D)'  , True, white)
    text_rect = text.get_rect()
    text_rect.center = (115, 550)
    screen.blit(text, text_rect)
    
    #controllo per gameover = TRUE
    if gameover:
        screen.blit(collision, crash_rect) 
        
        #restart
        pygame.draw.rect(screen, red, (0, 0, width, 175))
        text = font.render('Game over! Clicca S per rigiocare o N per chiudere il gioco', True, white)
        text_rect = text.get_rect()
        text_rect.center = (width / 2, 90)
        screen.blit(text, text_rect)
            
    pygame.display.update()

    while gameover:
        
        clock.tick(fps)
        
        for event in pygame.event.get():
            
            if event.type == QUIT: #se premi la x in alto fermi 
                gameover = False
                running = False
                
            # controllo per SI o NO
            if event.type == KEYDOWN:
                if event.key == K_s:
                    # impostazioni di reset
                    vite = 3
                    gameover = False
                    speed = 10
                    score = 0
                    asteroid_group.empty()
                    player.rect.center = [player_x, player_y]
                elif event.key == K_n:
                    # esce dal loop e va su pygame.quit
                    gameover = False
                    running = False

pygame.quit()