import pygame

from models import GameObject
from utils import load_sprite
from models import Player

class DontDie:
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((1280, 720))
        self.background = load_sprite("sfondomario", False)
        self.clock = pygame.time.Clock()
        self.player = Player((0,0)) # 200,200 è la posizione iniziale da cambiare per posizionare il personaggio
       
    
    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()
            
    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Don't Die")
    
    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()
        


    def _process_game_logic(self):
        self.player.move()
        #self.turtle.move()
    
    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        self.player.draw(self.screen)
        self.turtle.draw(self.screen)
        pygame.display.flip()
        print("Collides:", self.player.collides_with(self.turtle)) # da elimiare
        self.clock.tick(60)