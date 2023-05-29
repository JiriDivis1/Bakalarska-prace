import pygame
import os

actualEvent = "startMenu"       #Proměnná ve které je uložená aktuální událost ve hře (startMenu, settings, selectPlayer, ...)
running = True                  #False = konec hry
clock = pygame.time.Clock()     #FPS

#Jestli budu hrát za číšníka nebo číšníci
character = "waiter"

"""
KONSTANTY
"""
FPS = 60
WIDTH = 1280
HEIGHT = 720

BUTTON_WIDTH = WIDTH // 4
BUTTON_HEIGHT = BUTTON_WIDTH // 3.5

CHANGE_PEOPLE = 10           #konstanta určující jak moc se má měnit velikost lidí při pohybu po ose y
SPEED_OF_PEOPLES = 7        #rychlost pohybu lidí

"""
BARVY
"""
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

"""
OBRÁZKY
"""

#ICON = pygame.image.load('model\Data\Pictures\icon.png')

#MENU
WOODEN_TEXTURE = pygame.image.load(os.path.join('model', 'Data', 'Pictures', 'Menu', 'Start_menu', 'wooden_texture.jpg'))
WOODEN_TEXTURE = pygame.transform.rotate(WOODEN_TEXTURE, 90)
WOODEN_TEXTURE = pygame.transform.scale(WOODEN_TEXTURE, (int(WIDTH // 3), int(HEIGHT)))
YELLOW_BUTTON = pygame.image.load(os.path.join('model', 'Data', 'Pictures', 'Menu', 'Start_menu', 'yellow_button.png'))
YELLOW_BUTTON = pygame.transform.scale(YELLOW_BUTTON, (int(BUTTON_WIDTH), int(BUTTON_HEIGHT)))
GOLD_BUTTON = pygame.image.load(os.path.join('model', 'Data', 'Pictures', 'Menu', 'Start_menu', 'gold_button.png'))
GOLD_BUTTON = pygame.transform.scale(GOLD_BUTTON, (int(BUTTON_WIDTH), int(BUTTON_HEIGHT)))
PRESS_BUTTON = pygame.image.load(os.path.join('model', 'Data', 'Pictures', 'Menu', 'Start_menu', 'press_button.png'))
PRESS_BUTTON = pygame.transform.scale(PRESS_BUTTON, (int(BUTTON_WIDTH), int(BUTTON_HEIGHT)))

WAITRESS_PHOTO = pygame.image.load(os.path.join('model', 'Data', 'Pictures', 'Menu', 'SelectCharacter_menu', 'waitress_photo.png'))
WAITRESS_PHOTO = pygame.transform.scale(WAITRESS_PHOTO, (450 // 3, 450))
WAITER_PHOTO = pygame.image.load(os.path.join('model', 'Data', 'Pictures', 'Menu', 'SelectCharacter_menu', 'waiter_photo.png'))
WAITER_PHOTO  = pygame.transform.scale(WAITER_PHOTO , (450 // 3, 450))

#Restaurace
MAX_PEOPLE_START_HEIGHT = HEIGHT // 3
MAX_PEOPLE_START_WIDTH = MAX_PEOPLE_START_HEIGHT // 3
MIN_PEOPLE_START_HEIGHT = HEIGHT // 4
MIN_PEOPLE_START_WIDTH = MIN_PEOPLE_START_HEIGHT // 3
#COSTUMER1 = pygame.image.load(os.path.join('Data', 'Pictures', 'Peoples', 'Waiters', 'Waitress_basic_F.png'))

FLOOR = pygame.image.load(os.path.join('model', 'Data', 'Pictures', 'Things', 'floor.png'))
FLOOR = pygame.transform.scale(FLOOR, (WIDTH, HEIGHT))
WALLS = pygame.image.load(os.path.join('model', 'Data', 'Pictures', 'Things', 'walls.png'))
WALLS = pygame.transform.scale(WALLS, (WIDTH, HEIGHT))
BAR = pygame.image.load(os.path.join('model', 'Data', 'Pictures', 'Things', 'bar.png'))
BAR = pygame.transform.scale(BAR, (WIDTH, HEIGHT))
TABLE2 = pygame.image.load(os.path.join('model', 'Data', 'Pictures', 'Things', 'table2.png'))
TABLE2 = pygame.transform.scale(TABLE2, (144, 192))

WAITER = pygame.image.load(os.path.join('model', 'Data', 'Pictures', 'Peoples', 'Waiters', 'waiter_basic_F.png'))
WAITER = pygame.transform.scale(WAITER, (MAX_PEOPLE_START_WIDTH, MAX_PEOPLE_START_HEIGHT))

#%Ať jsou tyto rozměry relativní k rozlišení%
POSITION_BEHIND_BAR = (290, 450)
POSITION1 = (75, 590)       #1. pozice kam jít když chci obejít bar
POSITION2 = (415, 590)      #2. pozice kam jít když chci obejít bar

"""
OBJEKTY V RESTAURACI
"""

"""
FONTY
"""
pygame.font.init()  #načtení fontu
main_font = pygame.font.SysFont("cambria", 60)
text_font = pygame.font.SysFont("cambria", 40)
important_font = pygame.font.SysFont("cambria", 200)

"""
OBRAZOVKA
"""
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Restaurace u Zlatého Sumce")
#pygame.display.set_icon(icon)