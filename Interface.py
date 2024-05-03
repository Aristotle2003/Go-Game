import pygame
from InterfaceElement import *
import json

class Interface():
    
    def __init__(self,tag,main):
        self._tag = tag
        self._elements = []
        self.main = main

        self.main.window.add_to_array("interfaces",self)

    def update(self):
        
        for element in self._elements:
            element.update()

    def find_element(self,element_to_find):

        element_to_return = None

        for element in self._elements:
            if element.get_attribute("tag") == element_to_find:
                element_to_return = element

        return element_to_return

    def change_element_text(self,*args):

        element = args[0]
        new_text = args[1]
        
        for e in self._elements:
            if e.get_attribute("tag") == element:
                if len(args) == 2:
                    e.update_text(0,new_text)
                else:
                    e.update_text(args[2],new_text)
                
    def delete_self(self):
     
        self._elements = []
        self.main.window.remove_from_array("interfaces",self)

    def __create_elements(self):
        pass
    

    def get_attribute(self,attribute):

        if attribute == "tag":
            return self._tag
        elif attribute == "elements":
            return self._elements

    def add_element(self,new):
        
        self._elements.append(new)

    def remove_element(self,remove_tag):
        
        if isinstance(remove_tag,str):
            for element in self._elements:
                if element.get_attribute("tag") == remove_tag:
                    self._elements.remove(element)
        else:
            for element in self._elements:
                if element == remove_tag:
                    self._elements.remove(element)

class GameElements(Interface):

    def __init__(self,main):

        super().__init__("game elements",main)
        self.__create_elements()

    def __create_elements(self):
        
        new_element = Plane((0,0),(800,800),self.main.colours["MAIN BLUE"],"bg",self)
        self._elements.append(new_element)

        sx = self.main.sx
        sy = self.main.sy
        lens = self.main.lens
        step = lens / (self.main.board_size - 1)

        for i in range(0,self.main.board_size):
            x = sx
            y = sy + step * i
            new_element = Plane((lens,2),(x,y),self.main.colours["GREY"],"line",self)
            self._elements.append(new_element)

        for i in range(0,self.main.board_size):
            x = sx + step * i
            y = sy
            new_element = Plane((2,lens),(x,y),self.main.colours["GREY"],"line",self)
            self._elements.append(new_element)
      
        new_element = Plane((200,400),(800,10),self.main.colours["GAME BACKGROUND"],"infobox",self)              
        new_element.write("Current Player : black",(3,3),"biome",self.main.colours["WHITE"],20)
        self._elements.append(new_element)

        new_element = Button((300,50),(800,600),self.main.colours["SECONDARY BLUE"],"Return",self)
        new_element.write("Return",(10,0),"Arial",self.main.colours["MAIN BLUE"],40)
        self._elements.append(new_element)
   

class MainMenu(Interface):
    
    def __init__(self,main):

        super().__init__("main menu",main)
        self.__create_elements()

    def __create_elements(self):
             
        new_element = Plane((1000,800),(0,0),self.main.colours["MAIN BLUE"],"mainsurf",self)
        new_element.write("CHINESE GO",(420,100),"biome",self.main.colours["WHITE"],40)
        self._elements.append(new_element)
    
        new_element = Button((300,50),(350,200),self.main.colours["SECONDARY BLUE"],"P V P",self)
        new_element.write("P V P",(10,0),"Arial",self.main.colours["MAIN BLUE"],40)
        self._elements.append(new_element)
    
        new_element = Button((300,50),(350,300),self.main.colours["SECONDARY BLUE"],"P V AI-Random",self)
        new_element.write("P V AI-Random",(10,0),"Arial",self.main.colours["MAIN BLUE"],40)
        self._elements.append(new_element)

        new_element = Button((300,50),(350,400),self.main.colours["SECONDARY BLUE"],"P V AI-Heuristic",self)
        new_element.write("P V AI-Heuristic",(10,0),"Arial",self.main.colours["MAIN BLUE"],40)
        self._elements.append(new_element)

        new_element = Button((300,50),(350,500),self.main.colours["SECONDARY BLUE"],"P V AI-MonteCarlo",self)
        new_element.write("P V AI-MonteCarlo",(10,0),"Arial",self.main.colours["MAIN BLUE"],40)
        self._elements.append(new_element)
