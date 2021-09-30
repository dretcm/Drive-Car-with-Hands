import pygame, sys
from pygame.locals import *
from player import Player, GenerateCars, GenerateVia
from utils import exit_keys

pygame.init()
pygame.mixer.init()

class Game:
        def __init__(self):
                self.clock = pygame.time.Clock()
                self.fps = 60
                        
                self.WINDOW_SIZE = (1000,600)
                self.screen = pygame.display.set_mode(self.WINDOW_SIZE)

                self.player = Player(self.WINDOW_SIZE)
                self.gencars = GenerateCars(self.WINDOW_SIZE)
                self.genvia = GenerateVia(self.WINDOW_SIZE)


        def RunGame(self):
                self.refresh()
                while True:
                        for event in pygame.event.get():
                                exit_keys(event)
        ##                        if event.type == KEYDOWN:
        ##                                player.down_key(event.key)
        ##                        if event.type == KEYUP:
        ##                                player.up_key(event.key)
                                        
                        self.screen.fill((128, 128, 128))
                        
                        self.genvia.show_via(self.screen, self.player)
                        self.gencars.show_cars(self.screen, self.player)
                        self.player.moving_player(self.screen)

                        if self.player.is_death():
                                break
                        
                        pygame.display.update()
                        self.clock.tick(self.fps)

                self.push_button()


        def push_button(self):
                font = pygame.font.Font(None,70)

                midle_x, midle_y = list(map(lambda x: x//2, self.WINDOW_SIZE))

                pos_yes = (midle_x-110, midle_y+50)
                yes = pygame.Rect(pos_yes[0], pos_yes[1], 90,50)
                message_yes = font.render('Yes', 1, (0,0,0))

                pos_no = (midle_x+20, midle_y+50)
                no = pygame.Rect(pos_no[0], pos_no[1], 80,50)
                message_no = font.render('No', 1, (0,0,0))
                        
                message = font.render(" Do you want to play again? ",1,(0,0,0))
                lenght = message.get_width()
                pos_msg = ((self.WINDOW_SIZE[0] - lenght)//2,midle_y-40)

                #screen.fill((0,0,0)

                while True:
                        for event in pygame.event.get():
                                exit_keys(event)
                                if event.type == MOUSEBUTTONDOWN:
                                        if event.button == 1 and yes.collidepoint(event.pos):
                                                self.RunGame()
                                        if event.button == 1 and no.collidepoint(event.pos):
                                                pygame.quit()
                                                sys.exit()
                                                        
                                pygame.draw.rect(self.screen, (255,100,0), yes)
                                self.screen.blit(message_yes, pos_yes)
                                
                                pygame.draw.rect(self.screen, (255,100,0), no)
                                self.screen.blit(message_no, pos_no)
                                
                                pygame.draw.rect(self.screen, (255,255,255), [pos_msg[0], pos_msg[1],lenght, 60])
                                self.screen.blit(message, pos_msg)
                                
                                pygame.display.update()
                                self.clock.tick(self.fps)

        def refresh(self):
                self.player.refresh()
                self.gencars.refresh()
                self.genvia.refresh()
                        
if __name__ == '__main__':
        game = Game()
        game.RunGame()
        print('end game')

