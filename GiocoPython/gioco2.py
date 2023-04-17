import pygame
import random

# impostazioni della finestra di gioco
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 400
BG_COLOR = (255, 255, 255)

# impostazioni del giocatore
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_COLOR = (255, 0, 0)

# impostazioni degli ostacoli
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 50
OBSTACLE_COLOR = (0, 0, 255)

# impostazioni del gioco
TICK_RATE = 60  # numero di tick al secondo
OBSTACLE_SPEED = 5  # numero di pixel per tick

# inizializzazione di Pygame
pygame.init()

# creazione della finestra di gioco
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# creazione del giocatore
player_x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
player_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 10
player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)

# inizializzazione degli ostacoli
obstacles = []
obstacle_tick = 0

class Obstacle:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def move_down(self):
        self.row += 1

    def draw(self, screen):
        rect = pygame.Rect(self.column * 100, self.row * 100, 100, 100)
        pygame.draw.rect(screen, (255, 0, 0), rect)

class player:
    def __init__(self, column):
        self.column = column

    def move_left(self):
        if self.column > 0:
            self.column -= 1

    def move_right(self):
        if self.column < 2:
            self.column += 1

    def collides_with(self, obstacle):
        return self.column == obstacle.column and self.column == obstacle.column

    def draw(self, screen):
        rect = pygame.Rect(self.column * 100, 2 * 100, 100, 100)
        pygame.draw.rect(screen, (0, 0, 255), rect)


# creazione del font per il punteggio
score_font = pygame.font.SysFont("Arial", 20)

# loop principale del gioco
clock = pygame.time.Clock()
running = True
score = 0
while running:
    # gestione degli eventi
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_rect.move_ip(-10, 0)
            elif event.key == pygame.K_RIGHT:
                player_rect.move_ip(10, 0)

    # generazione degli ostacoli
    obstacle_tick += 1
    if obstacle_tick >= TICK_RATE:
        obstacle_tick = 0
        if random.random() < 0.5:
            obstacles.append(pygame.Rect(random.randint(0, SCREEN_WIDTH - OBSTACLE_WIDTH), 0, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        else:
            obstacles.append(pygame.Rect(random.randint(0, SCREEN_WIDTH - OBSTACLE_WIDTH * 2), 0, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
            obstacles.append(pygame.Rect(random.randint(OBSTACLE_WIDTH, SCREEN_WIDTH - OBSTACLE_WIDTH), 0, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

    # movimento degli ostacoli
    for obstacle in obstacles:
        obstacle.move_ip(0, OBSTACLE_SPEED)

    # rimozione degli ostacoli fuori dalla finestra di gioco
    obstacles = [obstacle for obstacle in obstacles if obstacle.bottom <= SCREEN_HEIGHT]

    # controllo delle collisioni
    for obstacle in obstacles:
        if player_rect.colliderect(obstacle):
            running = False

    # disegno degli elementi del gioco
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, PLAYER_COLOR, player_rect)
    for obstacle in obstacles:
        pygame.draw.rect(screen, OBSTACLE_COLOR, obstacle)
    score_text = score_font.render("Score: {}".format(score), True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # aggiornamento della finestra di gioco
    pygame.display.flip()

        # avanzamento del punteggio
    score += 1

    # inserimento di uno o due ostacoli nella riga più in alto
    if random.random() < 0.5:
        obstacles.append(Obstacle(1, random.randint(0, 2)))
    else:
        obstacles.append(Obstacle(1, random.randint(0, 1)))
        obstacles.append(Obstacle(1, random.randint(1, 2)))

    # movimento degli ostacoli
    for obstacle in obstacles:
        obstacle.move_down()

    # rimozione degli ostacoli usciti dalla griglia di gioco
    obstacles = [obstacle for obstacle in obstacles if obstacle.row < 3]

    # gestione delle collisioni tra il giocatore e gli ostacoli
    for obstacle in obstacles:
        if player.collides_with(obstacle):
            running = False
            break

    # gestione degli eventi
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move_left()
            elif event.key == pygame.K_RIGHT:
                player.move_right()

    # aggiornamento della schermata di gioco
    screen.fill((255, 255, 255))
    for obstacle in obstacles:
        obstacle.draw(screen)
    player.draw(screen)
    score_font = pygame.font.SysFont("Arial", 20)
    score_text = score_font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

    # controllo della fine del gioco
    if not running:
        gameover_font = pygame.font.SysFont("Arial", 40)
        gameover_text = gameover_font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(gameover_text, (SCREEN_WIDTH // 2 - gameover_text.get_width() // 2, SCREEN_HEIGHT // 2 - gameover_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        break

    # aggiornamento del timer
    clock.tick(TICK_RATE)

# uscita dal gioco
pygame.quit()




