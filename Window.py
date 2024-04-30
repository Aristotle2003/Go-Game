import pygame

class Window():
    
    def __init__(self,main):

        self.screen = pygame.display.set_mode((1000,800))
        self.main = main
        
        self.__background = self.main.colours["SECONDARY BLUE"]
        self.__height,self.__width = pygame.display.Info().current_h, pygame.display.Info().current_w
        self.__grid_height,self.__grid_width = self.__height - 100,self.__width - 140

        self.__interfaces = []

    def update(self):
        
        self.screen.fill(self.__background)

        for interface in self.__interfaces:
            interface.update()

    def update_instruction_box(self,line,new_text):
        self.find_interface("game elements").change_element_text("instructionbox",new_text,line)

    def update_info_box(self,line,new_text):
        self.find_interface("game elements").change_element_text("infobox",new_text,line)

    def find_interface(self,interface_to_find):

        for interface in self.__interfaces:
            if interface.get_attribute("tag") == interface_to_find:
                return interface

    def delete_interface(self,interface_to_delete):
        
        for interface in self.__interfaces:
            if interface.get_attribute("tag") == interface_to_delete:
                interface.delete_self()
          
    def get_attribute(self,attribute):

        if attribute == "background":
            return self.__background
        elif attribute == "height":
            return self.__height
        elif attribute == "width":
            return self.__width
        elif attribute == "grid height":
            return self.__grid_height
        elif attribute == "grid width":
            return self.__grid_width
        elif attribute == "interfaces":
            return self.__interfaces

    def set_attribute(self,attribute,new):

        if attribute == "background":
            self.__background = new
        if attribute == "interfraces":
            self.__interfaces = new

    def add_to_array(self,array,new):

        if array == "interfaces":
            self.__interfaces.append(new)

    def remove_from_array(self,array,removed):

        if array == "interfaces":
            self.__interfaces.remove(removed)