import pygame
class InterfaceElement():
    
    def __init__(self,dimensions,pos,colour,tag,type_,interface):
        
        self._colour, self._original_colour = colour, colour
        self._surf = pygame.Surface(dimensions)
        self._rect = self._surf.get_rect(topleft=pos)
        self._tag = tag
        self._type = type_
        self._interface = interface

        self._text_objects = []
        self._rect_corners = [(self._rect.topleft,self._rect.topright),(self._rect.topright,self._rect.bottomright),
                             (self._rect.bottomright,self._rect.bottomleft),(self._rect.bottomleft,self._rect.topleft)]

        

    def update(self):
       
        screen = self._interface.main.window.screen
        self._check_interaction()   

        #图片背景就不要再填色了
        if self._colour != self._interface.main.colours["BG"]:
            self._surf.fill(self._colour) 

        for text in self._text_objects:
            self._surf.blit(text.get_attribute("surf"),text.get_attribute("pos"))
            
        screen.blit(self._surf,self._rect)
        self.__draw_outlines(screen)

    def _check_interaction(self):
        pass

    def update_text(self,index,new_text):

        try:
            text_to_change = self._text_objects[index]
            text_to_change.set_attribute("surf",text_to_change.get_attribute("font").render(new_text,True,text_to_change.get_attribute("colour")))
        except IndexError:
            pass
        
    def write(self,text,pos,font,colour,size):
        new_text = Text(text,pos,font,colour,size)
        self._text_objects.append(new_text)

    def delete(self):

        self._interface.delete_self()

    def __draw_outlines(self,screen):
        
        for corner_coord in self._rect_corners:
            pygame.draw.line(screen,self._interface.main.colours["BLACK"],corner_coord[0],corner_coord[1])

    def get_attribute(self,attribute):

        if attribute == "entry text":
            return self._entry_text
        if attribute == "text objects":
            return self._text_objects
        if attribute == "tag":
            return self._tag


class Plane(InterfaceElement):

    def __init__(self,dimensions,pos,colour,tag,interface):

        super().__init__(dimensions,pos,colour,tag,"plane",interface)

class Button(InterfaceElement):

    def __init__(self,dimensions,pos,colour,tag,interface):

        super().__init__(dimensions,pos,colour,tag,"button",interface)

    def _check_interaction(self):
        
        from Interface import MainMenu

        mouse_pos = self._interface.main.get_attribute("mouse pos")
        
        if self._rect.collidepoint(mouse_pos) and self._interface.main.get_attribute("left mouse down") and self._tag[0:11] != "colourblock":          
            self._colour = self._interface.main.colours["CLICKED BLUE"]
        
        if self._interface.main.get_attribute("left mouse up"):

            if self._tag[0:11] != "colourblock":
                self._colour = self._original_colour
            
            if self._rect.collidepoint(mouse_pos):
            
                if self._tag == "exit":                
                    self._interface.main.running = False

                elif self._tag == "P V P":                
                    self.delete()                  
                    self._interface.main.game.start_game(0)

                elif self._tag == "P V AI-Random":                
                    self.delete()                  
                    self._interface.main.game.start_game(1)

                elif self._tag == "P V AI-Heuristic":                
                    self.delete()                  
                    self._interface.main.game.start_game(2)
                    
                elif self._tag == "P V AI-MonteCarlo":                
                    self.delete()                  
                    self._interface.main.game.start_game(3)

                elif self._tag == "exitinter":
                    self.delete()
                    if self._interface.main.game.get_attribute("stage") == "attack":
                        self._interface.main.game.reset_dice()
                        self._interface.main.window.update_instruction_box(0,self._interface.main.game.get_attribute("current player").ID + ", click on one of YOUR territories that has more than")
                        self._interface.main.window.update_instruction_box(1,"one army, then click an adjacent ENEMY territory to attack it.")
                    elif self._interface.main.game.get_attribute("stage") == "reinforce":
                        self._interface.main.game.set_attribute("last clicked territory","")
                        self._interface.main.window.update_instruction_box(0,"Click on one of YOUR territories containing at least 2 armies")
                        self._interface.main.window.update_instruction_box(1,"first, then click another one of YOUR other CONNECTED")
                        self._interface.main.window.update_instruction_box(2,"territories to reinforce it.")
                    elif self._interface.main.game.get_attribute("stage") == "draft":
                        self._interface.main.window.update_instruction_box(0,self._interface.main.game.get_attribute("current player").ID + ", click on one of your territories to draft in some troops.")
                        self._interface.main.window.update_instruction_box(1,"Draft all of your available troops to end the draft stage.")
                 

                elif self._tag == "plus":
                    self._interface.main.game.add_dice()

                elif self._tag == "minus":
                    self._interface.main.game.remove_dice()

                elif self._tag == "tradein":
                    self._interface.main.game.get_attribute("current player").trade_cards_in()
                    
                elif self._tag == "roll":                        
                    self._interface.main.game.roll_dice()

                elif self._tag[0:6] == "toggle":
                    if self._tag[7] == "1":
                        self._interface.main.random_territories = not self._interface.main.random_territories
                        if self._interface.main.random_territories:
                            self.update_text(0,"YES")
                        else:
                            self.update_text(0,"NO")
                    if self._tag[7] == "2":
                        self._interface.main.cards_enabled = not self._interface.main.cards_enabled
                        if self._interface.main.cards_enabled:
                            self.update_text(0,"YES")
                        else:
                            self.update_text(0,"NO")
                            
                elif self._interface.get_attribute("tag") == "colour choice" and self._tag[0:11] == "colourblock":
                    self._interface.main.game.get_attribute("players")[int(self._tag[11])-1].switch_colour()
                    self._colour = self._interface.main.game.get_attribute("players")[int(self._tag[11])-1].get_attribute("colour")

                            
                if self._tag == "endattack":
                    self._interface.main.game.end_attack()
                elif self._tag == "endreinforce":
                    self._interface.main.game.end_reinforce()
                elif self._tag == "cardshow":
                    self._interface.main.window.update_instruction_box(0,"Click trade in if you have an eligible set of cards.")
                    self._interface.main.window.update_instruction_box(1,"")
                    self._interface.main.window.update_instruction_box(2,"")
                elif self._tag == "Return":
                    self._interface.main.game.end_game()
                    
                self._interface.main.unclick()

class TextBox(InterfaceElement):

    def __init__(self,dimensions,pos,colour,tag,interface):

        super().__init__(dimensions,pos,colour,tag,"text box",interface)
        self._entry_text = ""
        
    def _check_interaction(self):
       
        territory_info = self._interface.main.game.get_territory_info()
        last_clicked_territory = self._interface.main.game.get_attribute("last clicked territory")
        stored_territory = self._interface.main.game.get_attribute("stored territory")
        last_pressed_key = self._interface.main.get_attribute("last pressed key")

        if last_pressed_key == pygame.K_BACKSPACE:
            self._entry_text = self._entry_text[:-1]
            self._interface.main.set_attribute("last pressed key", None)

        elif last_pressed_key == pygame.K_RETURN and self._entry_text != "0" and self._entry_text != "":
                
            if self._interface.get_attribute("tag") == "draft":
                self.__draft(territory_info,last_clicked_territory,stored_territory)

            elif self._interface.get_attribute("tag") == "deploy":
                self.__deploy(territory_info,last_clicked_territory,stored_territory)

            elif self._interface.get_attribute("tag") == "reinforce":
                self.__reinforce(territory_info,last_clicked_territory,stored_territory)

            self._interface.main.set_attribute("last pressed key",None)

        else:
            if self._interface.main.get_attribute("last pressed key uni").isdigit() and len(self._entry_text) < 3:                
                self._entry_text += self._interface.main.get_attribute("last pressed key uni")
        self._text_objects[0].set_attribute("surf",self._text_objects[0].get_attribute("font").render(self._entry_text,True,self._text_objects[0].get_attribute("colour"))) 
        self._interface.main.set_attribute("last pressed key uni","")

    def __draft(self,territory_info,last_clicked_territory,stored_territory):

        draft_troops = self._interface.main.game.get_attribute("current player").get_attribute("draft troops")
        if draft_troops >= int(self._entry_text):
            self._interface.main.game.get_attribute("current player").set_attribute("draft troops",(draft_troops - int(self._entry_text))) 
            territory_info[last_clicked_territory].troops += int(self._entry_text)
            self._interface.main.window.find_interface("game elements").update_count(last_clicked_territory)
            self.delete()

        if self._interface.main.game.get_attribute("current player").get_attribute("draft troops") != 0:
            self._interface.main.window.update_instruction_box(0,self._interface.main.game.get_attribute("current player").ID + ", click on one of your territories to draft in some troops.")
            self._interface.main.window.update_instruction_box(1,"Draft all of your available troops to end the draft stage.")

    def __deploy(self,territory_info,last_clicked_territory,stored_territory):
    
        deploy_troops = territory_info[self._interface.main.game.get_attribute("stored territory")].troops - 1
        if deploy_troops >= int(self._entry_text):
            self.__transfer(territory_info,last_clicked_territory,stored_territory)
            self._interface.main.window.update_instruction_box(0,self._interface.main.game.get_attribute("current player").ID + ", click on one of YOUR territories that has more than")
            self._interface.main.window.update_instruction_box(1,"one army, then click an adjacent ENEMY territory to attack it.")
            self._interface.main.game.set_attribute("last clicked territory","")
            self.delete()
            self._interface.main.game.check_players()

    def __reinforce(self,territory_info,last_clicked_territory,stored_territory):
       
        reinforcements = territory_info[stored_territory].troops - 1
        if reinforcements >= int(self._entry_text):
            self.__transfer(territory_info,last_clicked_territory,stored_territory)
            self._interface.main.window.delete_interface("end reinforce")
            self._interface.main.game.set_attribute("last clicked territory","")
            self.delete()
            #self._interface.main.game.switch_turn()

    def __transfer(self,territory_info,last_clicked_territory,stored_territory):
      
        territory_info[last_clicked_territory].troops += int(self._entry_text)
        self._interface.main.window.find_interface("game elements").update_count(last_clicked_territory)
        territory_info[stored_territory].troops -= int(self._entry_text)
        self._interface.main.window.find_interface("game elements").update_count(stored_territory)
                    
class Text():
    
    def __init__(self,text_,pos,font,colour,size):
        
        self.__text = text_
        self.__font = pygame.font.SysFont(font,size)
        self.__colour = colour
        self.__pos = pos
        self.__surf = self.__font.render(self.__text,True,self.__colour)
    
    def get_attribute(self,attribute):

        if attribute == "text":
            return self.__text
        elif attribute == "font":
            return self.__font
        elif attribute == "colour":
            return self.__colour
        elif attribute == "surf":
            return self.__surf
        elif attribute == "pos":
            return self.__pos

    def set_attribute(self,attribute,new):

        if attribute == "surf":
            self.__surf = new
        elif attribute == "text":
            self.__text = new
        elif attribute == "pos":
            self.__pos = new

class BackGroundImg(InterfaceElement):

    def __init__(self,dimensions,pos,colour,tag,interface):    
        super().__init__(dimensions,pos,colour,tag,"plane",interface)
        self._surf = pygame.image.load("IMAGES/OBackGround.png").convert()
        self._surf.set_colorkey((0,0,0),pygame.RLEACCEL)