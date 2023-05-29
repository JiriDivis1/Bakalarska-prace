import pygame
import time

from model import *
from player import *

"""
Pomocné proměnné
"""
new_direct = 0
new_final_position = 0
move = True                 #pokud False, tak vykonávám obcházení objektu
collide_object  = None      #objekt, který budu obcházet
collide_x = False           #kolidace na ose x
collide_y = False           #kolidace na ose y
first_collide = True        #True inicializace new_final_destination, ...

#Argumenty: id levelu, character
#V __init__ budu načítat data z json souboru
class Level():
    def __init__(self, id, character):
        self.id = id
        self.character = character

    #Hlavní metoda
    def start_level(self):
        global actualPlayer
        
        SCREEN.fill(WHITE)
        
        floor.set_priority(1)   #Kvůli tomu aby uživatel neklikl na podlahu po kliknutí na tlačítko
        
        floor.drawObject()
        walls.drawObject()
        bar.drawObject()
    
        table2.drawObject()
        
        waiter.drawObject()
        pygame.draw.rect(SCREEN, RED, waiter.get_collision_rect())
        

#Objekty v restauraci
class ObjectInRestaurant():
    def __init__(self, image, priority, x_pos, y_pos):
        self.image = image                          
        self.priority = priority        #priority - kvůli překrývání, objekty před vykreslením vložím do pole, to setřídím podle priority a poté až vykreslím
        self.x_pos = x_pos
        self.y_pos = y_pos
        if x_pos == 0 and y_pos == 0 and type(self) is not Waiter:
            self.rect = self.image.get_rect(topleft = (self.x_pos, self.y_pos))
        elif type(self) is Waiter:
            self.rect = self.image.get_rect(topleft = (self.x_pos, self.y_pos))
            self.rect.centerx = self.x_pos
            self.rect.bottom = self.y_pos
        else: 
            self.rect = self.image.get_rect(center = (self.x_pos, self.y_pos))
        
        self.mask = pygame.mask.from_surface(self.image)
        
    def get_image(self):
        return self.image
    
    def set_image(self, image):
        self.image = image
        return self
    
    def get_priority(self):
        return self.priority
    
    def set_priority(self, priority):
        self.priority = priority
        return self
    
    def get_x_pos(self):
        return self.x_pos
    
    def set_x_pos(self, x_pos):
        self.x_pos = x_pos
        return self
    
    def get_y_pos(self):
            return self.y_pos
    
    def set_y_pos(self, y_pos):
        self.y_pos = y_pos
        return self
    
    def get_rect(self):
        return self.rect
    
    def set_rect(self, rect):
        self.rect = rect
        return self
    
    def get_mask(self):
        return self.mask
        
    def drawObject(self):
        if type(self) == WAITER:
            SCREEN.blit(self.get_image(), self.get_rect(), self.get_collision_rect())
        else:
             SCREEN.blit(self.get_image(), self.get_rect())
        
    def isClicked(self, position):
        pos_in_mask = position[0] - self.get_rect().x, position[1] - self.get_rect().y
        touching = self.get_rect().collidepoint(*position) and self.get_mask().get_at(pos_in_mask)
        return touching

#Číšník a zákazníci
class People(ObjectInRestaurant):
    def __init__(self, image, priority, x_pos, y_pos):
        super().__init__(image, priority, x_pos, y_pos)
        self.change_size = 0                            #pomocná proměnná pro změnu velikosti lidí
        
        #Proměnné pro pohyb osoby
        self.signal_movement_x = False                                              #signalizuje, jestli mám pohybovat po ose x
        self.signal_movement_y = False                                              #signalizuje, jestli mám pohybovat po ose y
        self.source_position = self.get_rect().centerx, self.get_rect().bottom      #Pozice osoby při kliknutí myši
        self.final_position = (0, 0)                                                #Pozice kam se má osoba přesunout
        self.direct_x = 1                                                           #označuje směr(doleva, doprava) a rychlost
        self.direct_y = 1                                                           #označuje směr(nahoru, dolů) a rychlost
        
        self.state = "basic"                                                        #stav ve kterém je číšník nebo zákazník (základní, nosí jídelníček, nosí jídlo, ...)
    
    def get_change_size(self):
        return self.change_size
    
    def set_change_size(self, change_size):
        self.change_size = change_size
        return self
    
    def get_signal_movement_x(self):
        return self.signal_movement_x
    
    def set_signal_movement_x(self, signal_movement_x):
        self.signal_movement_x = signal_movement_x
        return self
    
    def get_signal_movement_y(self):
        return self.signal_movement_y
    
    def set_signal_movement_y(self, signal_movement_y):
        self.signal_movement_y = signal_movement_y
        return self
    
    def get_source_position(self):
        return (self.get_rect().centerx, self.get_rect().bottom)
    
    def get_final_position(self):
        return self.final_position
    
    def set_final_position(self, final_position):
        self.final_position = final_position
        return self
    
    def get_direct_x(self):
        return self.direct_x
    
    def set_direct_x(self, direct_x):
        self.direct_x = direct_x
        return self
    
    def get_direct_y(self):
        return self.direct_y
    
    def set_direct_y(self, direct_y):
        self.direct_y = direct_y
        return self
    
    def get_state(self):
        return self.state
    
    def set_state(self, state):
        self.state = state
        return self  
    
    #Signalizuje, jestli se má změnit velikost 1 = zvětšit, 0 = neměnit, -1 = zmenšit
    def checkChangeSize(self, offset):
        self.set_change_size(self.get_change_size() + offset)
        if self.get_change_size() == CHANGE_PEOPLE:
            self.set_change_size(0)
            return 1
        elif self.get_change_size() == -1 * CHANGE_PEOPLE:
            self.set_change_size(0)
            return -1
        else:
            return 0

    """
    Pohyb po ose x, vrací 1, pokud je číšník na pozici final_position, jinak 0
    """
    def movement_x(self, direct_x, final_position):
        source_position = self.get_rect().centerx

        if final_position == None:
            self.get_rect().centerx += direct_x
            self.get_collision_rect().centerx += direct_x
            return 1
        #Půjdeme doprava
        if direct_x > 0:
            if source_position < final_position:
                self.get_rect().centerx += direct_x
                self.get_collision_rect().centerx += direct_x
                return 0
            #Jsme v cíli
            else:
                self.get_rect().centerx = final_position
                self.get_collision_rect().centerx = final_position
                return 1
        #Půjdeme doleva
        else:
            if source_position > final_position:
                self.get_rect().centerx += direct_x
                self.get_collision_rect().centerx += direct_x
                return 0
            else:
                self.get_rect().centerx = final_position
                self.get_collision_rect().centerx = final_position
                return 1
    
    def movement_y(self, direct_y, final_position):
        source_position = self.get_rect().bottom
        if final_position == None:
            if direct_y > 0:
                for i in range(direct_y):
                        self.get_rect().centery += 1
                        self.get_collision_rect().centery += 1
                        if self.checkChangeSize(1) == 1:
                            new_waiter = pygame.image.load(os.path.join('model', 'Data', 'Pictures', 'Peoples', 'Waiters', 'waiter_basic_F.png'))
                            new_waiter = pygame.transform.scale(new_waiter, ((self.get_rect().h + 1) // 3, self.get_rect().h + 1))
                            self.set_image(new_waiter)
                            self.set_rect(self.get_image().get_rect(topleft = (self.get_rect().x, self.get_rect().y)))
            else:
                for i in range(-1 * direct_y):
                    self.get_rect().centery -= 1
                    self.get_collision_rect().centery -= 1
                    if self.checkChangeSize(-1) == -1:
                        new_waiter = pygame.image.load(os.path.join('model', 'Data', 'Pictures', 'Peoples', 'Waiters', 'waiter_basic_F.png'))
                        new_waiter = pygame.transform.scale(new_waiter, ((self.get_rect().h - 1) // 3, self.get_rect().h - 1))
                        self.set_image(new_waiter)
                        self.set_rect(self.get_image().get_rect(topleft = (self.get_rect().x, self.get_rect().y)))
            return None
        #Půjdeme dolů
        if direct_y > 0:
            if source_position < final_position:
                for i in range(direct_y):
                    self.get_rect().centery += 1
                    self.get_collision_rect().centery += 1
                    if self.checkChangeSize(1) == 1:
                        new_waiter = pygame.image.load(os.path.join('model', 'Data', 'Pictures', 'Peoples', 'Waiters', 'waiter_basic_F.png'))
                        new_waiter = pygame.transform.scale(new_waiter, ((self.get_rect().h + 1) // 3, self.get_rect().h + 1))
                        self.set_image(new_waiter)
                        self.set_rect(self.get_image().get_rect(topleft = (self.get_rect().x, self.get_rect().y)))
                return 0
            else:
                self.get_rect().bottom = final_position
                self.get_collision_rect().bottom = final_position
                return 1
        #Půjdeme nahoru
        else:
            if source_position > final_position:
                for i in range(-1 * direct_y):
                    self.get_rect().centery -= 1
                    self.get_collision_rect().centery -= 1
                    if self.checkChangeSize(-1) == -1:
                        new_waiter = pygame.image.load(os.path.join('model', 'Data', 'Pictures', 'Peoples', 'Waiters', 'waiter_basic_F.png'))
                        new_waiter = pygame.transform.scale(new_waiter, ((self.get_rect().h - 1) // 3, self.get_rect().h - 1))
                        self.set_image(new_waiter)
                        self.set_rect(self.get_image().get_rect(topleft = (self.get_rect().x, self.get_rect().y)))
                return 0
            else:
                self.get_rect().bottom = final_position
                self.get_collision_rect().bottom = final_position
                return 1

class Waiter(People):
    def __init__(self, image, priority, x_pos, y_pos):
        super().__init__(image, priority, x_pos, y_pos)
        self.collision_rect = pygame.Rect((self.get_rect().left, self.get_rect().bottom - 30), (self.get_rect().width, 30))
        
    def get_collision_rect(self):
        return self.collision_rect
    
    def set_collision_rect(self, collision_rect):
        self.collision_rect = collision_rect
        return self
    
    #Vrátí True, pokud kolize a objekt, se kterým je kolize
    #% - zkoušet kolizi se všemi objekty, ne jenom s table2
    def check_collision(self):
        if self.get_collision_rect().colliderect(table2.get_rect()):
            return (True, table2.get_rect())
        else:
            return (False, waiter.get_rect())

    """
    Metoda, která nastaví proměnné pro pohyb
    """
    def set_movement(self, click_position, direct_x, direct_y):
        self.set_signal_movement_x(True)
        self.set_signal_movement_y(True)
        self.set_final_position(click_position)
        self.set_direct_x(direct_x)
        self.set_direct_y(direct_y)

    """
    Metoda, která vykoná pohyb
    """
    def execute_movement(self):
        global new_direct, new_final_position, move, collide_object, collide_x, collide_y, first_collide
        
        if move:
            #Pohyb po ose x
            if self.get_signal_movement_x():
                if type(self.get_final_position()) is list:
                    if self.get_final_position() == []:
                        self.set_signal_movement_x(False)
                    else:
                        if self.get_source_position()[0] != self.get_final_position()[0][0]:
                            check_coll = self.check_collision()
                            collide_object = check_coll[1]
                            if check_coll[0]:
                                move = False
                            else:
                                movement_x = self.movement_x(self.get_direct_x()[0], self.get_final_position()[0][0])
 
                else:
                    check_coll = self.check_collision()
                    collide_object = check_coll[1]
                    if check_coll[0]:
                        move = False
                    else:
                        movement_x = self.movement_x(self.get_direct_x(), self.get_final_position()[0])
                        if movement_x:
                            self.set_signal_movement_x(False)
            #Pohyb po ose y        
            if self.get_signal_movement_y():
                if type(self.get_final_position()) is list:
                    if self.get_final_position() == []:
                        self.set_signal_movement_y(False)
                    else:
                        if self.get_source_position()[1] != self.get_final_position()[0][1]:
                            check_coll = self.check_collision()
                            collide_object = check_coll[1]
                            if check_coll[0]:
                                move = False
                            else:
                                movement_y = self.movement_y(self.get_direct_y()[0], self.get_final_position()[0][1])
                                
                else:   
                    check_coll = self.check_collision()
                    collide_object = check_coll[1]
                    if check_coll[0]:
                        move = False
                    else:
                        movement_y = self.movement_y(self.get_direct_y(), self.get_final_position()[1])
                        if movement_y:
                            self.set_signal_movement_y(False)

                                
            if self.get_final_position() != [] and self.get_source_position() == self.get_final_position()[0] and type(self.get_final_position()) is list:
                if len(self.get_final_position()) != 0:
                    self.get_final_position().pop(0)
                    self.get_direct_x().pop(0)
                    self.get_direct_y().pop(0)
        
        #Číšník obchází objekt
        else:
            collision_rect = self.get_collision_rect()
            if type(self.get_final_position()) is list:
                final_position = self.get_final_position()[0]
            else:
                final_position = self.get_final_position()
            
            if first_collide:
                #Jsem vedle objektu
                if collision_rect.right - SPEED_OF_PEOPLES < collide_object.left or collision_rect.left + SPEED_OF_PEOPLES > collide_object.right: 
                    collide_x = True
                    
                    #Vrátíme se zpátky o 1
                    self.movement_x(self.get_direct_x() * -1, None)
                    
                    #Jsem vlevo od objektu, a klikl jsem do stejné oblasti, nebo jsem vpravo od objektu a klikl jsem do stejné oblasti
                    if (final_position[0] > collide_object.left - self.collision_rect.width // 2 and final_position[0] < collide_object.left) and (collision_rect.right > collide_object.left - collision_rect.width // 2 and collision_rect.right < collide_object.left) or (final_position[0] > collide_object.right and final_position[0] < collide_object.right + collision_rect.width // 2) and (collision_rect.left > collide_object.right and collision_rect.left < collide_object.right + collision_rect.width // 2):
                        first_collide = True
                        collide_x = False
                        move = True
                        self.set_signal_movement_x(False)
                        return 0

                    #Jsem v horní půlce objektu
                    if collision_rect.bottom <= collide_object.centery:
                        #Půjdu dolů
                        if final_position[1] >= collide_object.centery:
                            new_direct = SPEED_OF_PEOPLES
                            new_final_position = collide_object.bottom + collision_rect.height
                        #Půjdu nahoru
                        else:
                            new_direct = -1 * SPEED_OF_PEOPLES
                            new_final_position = collide_object.top - collision_rect.height
                    #Jsem v dolní půlce objektu
                    else:
                        #Půjdu dolů
                        if final_position[1] >= collide_object.centery:
                            #print("půjdu dolů")
                            new_direct = SPEED_OF_PEOPLES
                            new_final_position = collide_object.bottom + collision_rect.height
                        #Půjdu nahoru
                        else:
                            #print("půjdu nahoru")
                            new_direct = -1 * SPEED_OF_PEOPLES
                            new_final_position = collide_object.top - collision_rect.height   
                else:
                    collide_y = True
                    
                    #Vrátíme se zpátky o 1
                    self.movement_y(self.get_direct_y() * -1, None)
                    
                    #Jsem nad objektem a klikl jsem do stejné oblasti nebo jsem pod objektem a klikl jsem do stejné oblasti
                    if (final_position[0] > collide_object.left and final_position[0] < collide_object.right) and (final_position[1] > collide_object.top - collision_rect.height // 2 and final_position[1] < collide_object.top + SPEED_OF_PEOPLES) and (collision_rect.bottom > collide_object.top - collision_rect.height // 2 and collision_rect.bottom < collide_object.top):
                        first_collide = True
                        collide_x = False
                        move = True
                        self.set_signal_movement_y(False)
                        return 0
                    
                    #Jsem v levé polovině objektu
                    if collision_rect.centerx <= collide_object.centerx:
                        #Půjdu doleva
                        if final_position[0] <= collide_object.centerx:
                            new_direct = -1 * SPEED_OF_PEOPLES
                            new_final_position = collide_object.left - collision_rect.width
                        #Půjdu doprava
                        else:
                            new_direct = SPEED_OF_PEOPLES
                            new_final_position = collide_object.right + collision_rect.width
                    #Jsem v pravé polovině objektu
                    else:
                        #Půjdu doleva
                        if final_position[0] <= collide_object.centerx:
                            new_direct = -1 * SPEED_OF_PEOPLES
                            new_final_position = collide_object.left - collision_rect.width
                        #Půjdu doprava
                        else:
                            new_direct = SPEED_OF_PEOPLES
                            new_final_position = collide_object.right + collision_rect.width
                        
                first_collide = False
                
            if collide_x:
                new_movement = self.movement_y(new_direct, new_final_position)
                if new_movement:
                    if collision_rect.centerx < collide_object.left:
                        self.movement_x(SPEED_OF_PEOPLES, None)
                    if collision_rect.centerx > collide_object.right:
                        self.movement_x(-1 * SPEED_OF_PEOPLES, None)
                    if collision_rect.bottom > final_position[1]:
                        self.set_direct_y(-1 * SPEED_OF_PEOPLES)
                    else:
                        self.set_direct_y(SPEED_OF_PEOPLES)
                    first_collide = True
                    collide_x = False
                    move = True
                    
            elif collide_y:
                new_movement = self.movement_x(new_direct, new_final_position)
                if new_movement:
                    if collision_rect.centerx > final_position[0]:
                        self.set_direct_x(-1 * SPEED_OF_PEOPLES)
                    else:
                        self.set_direct_x(SPEED_OF_PEOPLES)
                    first_collide = True
                    collide_y = False
                    move = True
    
class Costumer(People):
    def __init__(self, image, priority, x_pos, y_pos):
        super().__init__(image, priority, x_pos, y_pos)
        
"""
OBJEKTY V RESTAURACI
"""

floor = ObjectInRestaurant(FLOOR, 0, 0, 0)
walls = ObjectInRestaurant(WALLS, 1, 0, 0)
bar = ObjectInRestaurant(BAR, 2, 0, 0)
table2 = ObjectInRestaurant(TABLE2, 3, WIDTH // 1.7, HEIGHT // 1.8)

waiter = Waiter(WAITER, 3, WIDTH // 2, HEIGHT)  
    
def game():
    actualEvent = "game"
    level = Level("t01", character)
    level.start_level()
    waiter.execute_movement()