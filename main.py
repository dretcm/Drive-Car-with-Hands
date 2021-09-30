import pygame, sys
from pygame.locals import *
from player import Player, GenerateCars, GenerateVia
from utils import exit_keys

pygame.init()
pygame.mixer.init()

def RunGame():
        player = Player(WINDOW_SIZE)
        gencars = GenerateCars(WINDOW_SIZE)
        genvia = GenerateVia(WINDOW_SIZE)
        
        while True:
                for event in pygame.event.get():
                        exit_keys(event)
##                        if event.type == KEYDOWN:
##                                player.down_key(event.key)
##                        if event.type == KEYUP:
##                                player.up_key(event.key)
                                
                screen.fill((128, 128, 128))
                
                genvia.show_via(screen, player)
                gencars.show_cars(screen, player)
                player.moving_player(screen)

                if player.is_death():
                        break
                
                pygame.display.update()
                clock.tick(fps)
                
        del(player)
        del(gencars)
        del(genvia)
        push_button()


def push_button():
        font = pygame.font.Font(None,70)

        midle_x, midle_y = list(map(lambda x: x//2, WINDOW_SIZE))

        pos_yes = (midle_x-110, midle_y+50)
        yes = pygame.Rect(pos_yes[0], pos_yes[1], 90,50)
        message_yes = font.render('Yes', 1, (0,0,0))

        pos_no = (midle_x+20, midle_y+50)
        no = pygame.Rect(pos_no[0], pos_no[1], 80,50)
        message_no = font.render('No', 1, (0,0,0))
                
        message = font.render(" Do you want to play again? ",1,(0,0,0))
        lenght = message.get_width()
        pos_msg = ((WINDOW_SIZE[0] - lenght)//2,midle_y-40)

        #screen.fill((0,0,0))

        while True:
                for event in pygame.event.get():
                        exit_keys(event)
                        if event.type == MOUSEBUTTONDOWN:
                                if event.button == 1 and yes.collidepoint(event.pos):
                                        RunGame()
                                if event.button == 1 and no.collidepoint(event.pos):
                                        pygame.quit()
                                        sys.exit()
                                                
                        pygame.draw.rect(screen, (255,100,0), yes)
                        screen.blit(message_yes, pos_yes)
                        
                        pygame.draw.rect(screen, (255,100,0), no)
                        screen.blit(message_no, pos_no)
                        
                        pygame.draw.rect(screen, (255,255,255), [pos_msg[0], pos_msg[1],lenght, 60])
                        screen.blit(message, pos_msg)
                        
                        pygame.display.update()
                        clock.tick(fps)
                        
if __name__ == '__main__':
        clock = pygame.time.Clock()
        fps = 30
                
        WINDOW_SIZE = (1000,600)
        screen = pygame.display.set_mode(WINDOW_SIZE)
        
        RunGame()
        print('end game')

