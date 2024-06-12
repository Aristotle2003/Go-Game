import pygame
import os
from Main import Main
from Window import Window
from core.gogame import Game

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (40,100)
pygame.init()
pygame.font.init()

if __name__ == "__main__":    

    main = Main()
    game = Game(main)
    window = Window(main)    
    main.setWinGame(window,game)

    from Interface import MainMenu
    new_interface = MainMenu(main)  

    while main.running:
        main.loop()
    
pygame.quit()