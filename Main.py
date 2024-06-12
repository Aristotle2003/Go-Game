import pygame
import os

class Main():
    
    def __init__(self):
        self.__clock = pygame.time.Clock()
        self.__last_pressed_key_uni = ""
        self.__in_game = False
        self.__left_mouse_up = False
        self.__left_mouse_down = False
        self.__last_pressed_key = None
        self.__mouse_pos = (0,0)

        self.running = True
        self.random_territories = True
        self.cards_enabled = False
        self.colours = {"BLACK":(0,0,0),"WHITE":(254,254,254),"MAIN BLUE":(112,181,230),"OCEAN BLUE":(29,148,199),"GAME BACKGROUND":(66, 79, 102),
                        "SECONDARY BLUE":(47,94,128),"CLICKED BLUE":(39,80,110),"RED":(255,0,0),"GREEN":(0,255,0),"GREY":(186,189,194),"BG":(256,256,256)}

        self.board_size = 19 # 9x9   13x13   19x19
        self.sx = 50
        self.sy = 50
        self.lens = 700

    def setWinGame(self,win,game):
        self.window = win
        self.game = game

    def loop(self):

        self.__mouse_pos = pygame.mouse.get_pos()

        self.__event_check()

        self.window.update()

        if self.__in_game:
            self.game.update()
            
        self.__clock.tick(500)
        
        pygame.display.flip()

    def unclick(self):

        self.__left_mouse_up = False

    def __event_check(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                self.running = False

            if event.type == pygame.KEYDOWN:
                
                self.__last_pressed_key_uni = str(event.unicode)
                self.__last_pressed_key = event.key

                if event.key == pygame.K_ESCAPE:
                    self.running = False

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.__left_mouse_up = True
                
            else:
                self.__left_mouse_up = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.__left_mouse_down = True
            else:
                self.__left_mouse_down = False

    def get_attribute(self,attribute):

        if attribute == "mouse pos":
            return self.__mouse_pos
        elif attribute == "last pressed key":
            return self.__last_pressed_key
        elif attribute == "last pressed key uni":
            return self.__last_pressed_key_uni
        elif attribute == "in game":
            return self.__in_game
        elif attribute == "left mouse up":
            return self.__left_mouse_up
        elif attribute == "left mouse down":
            return self.__left_mouse_down

    def set_attribute(self,attribute,new):

        if attribute == "in game":
            self.__in_game = new
        elif attribute == "last pressed key":
            self.__last_pressed_key = new
        elif attribute == "last pressed key uni":
            self.__last_pressed_key_uni = new

