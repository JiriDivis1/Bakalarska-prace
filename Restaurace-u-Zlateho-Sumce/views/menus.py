import pygame
import time

from model import *
from player import *

class Button():
    def __init__(self, image, x_pos, y_pos, text_input):
        super().__init__()
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center = (self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = main_font.render(self.text_input, True, BLACK)
        self.text_rect = self.text.get_rect(center = (self.x_pos, self.y_pos - BUTTON_HEIGHT * 0.1))
        self.mask = pygame.mask.from_surface(self.image)
        
    def get_image(self):
        return self.image
    
    def set_image(self, image):
        self.image = image
        return self
    
    def get_rect(self):
        return self.rect
    
    def get_text(self):
        return self.text
    
    def get_text_rect(self):
        return self.text_rect
    
    def set_text_rect(self, text_rect):
        self.text_rect = text_rect
        return self
    
    def get_mask(self):
        return self.mask
    
#Vykreslení tlačítka        
    def drawButton(self):
        SCREEN.blit(self.get_image(), self.get_rect())
        if self.get_text() != None:
            SCREEN.blit(self.get_text(), self.get_text_rect())

#Zkontruluje, zda uživatel klikl na tlačítko
    def isButtonClicked(self, position):
        if position[0] in range(self.get_rect().left, self.get_rect().right) and position[1] in range(self.get_rect().top, self.get_rect().bottom):
            return True
        else:
            return False
        
    def buttonHover(self, position, image):
        pos_in_mask = position[0] - self.get_rect().x, position[1] - self.get_rect().y
        touching = self.get_rect().collidepoint(*position) and self.get_mask().get_at(pos_in_mask)
        
        if touching:
            self.set_image(image)
            self.drawButton()
        else:
            self.set_image(YELLOW_BUTTON)
            self.drawButton()
            
BUTTON_WIDTH = int(WIDTH // 2)

original_wooden_height = HEIGHT                         #pozice y wooden texture při spuštění
wooden_height = int(HEIGHT // 2 - HEIGHT * 0.1)         #pozice y wooden texture po přesunu

shift = original_wooden_height - wooden_height          #počet pixelů o kolik se menu posune

"""
TLAČÍTKA
"""
#startMenu
hratHru = Button(YELLOW_BUTTON, BUTTON_WIDTH, int(HEIGHT * 0.55 + shift), "Hrát hru")
nastaveni = Button(YELLOW_BUTTON, BUTTON_WIDTH, int(HEIGHT * 0.70 + shift), "Nastavení")
ukoncitHru = Button(YELLOW_BUTTON, BUTTON_WIDTH, int(HEIGHT * 0.85 + shift), "Ukončit hru")

#selectPlayer
alphaVerze = Button(YELLOW_BUTTON, int(WIDTH * 0.75), int(HEIGHT * 0.85), "Alpha verze")

#selectCharacter
cisnik = Button(YELLOW_BUTTON, int(WIDTH * 0.75), int(HEIGHT * 0.85), "Číšník")
cisnice = Button(YELLOW_BUTTON, int(WIDTH * 0.25), int(HEIGHT * 0.85), "Číšnice")

cisniceFotka = Button(WAITRESS_PHOTO, int(WIDTH * 0.25), HEIGHT // 2 - 30, None)
cisnikFotka = Button(WAITER_PHOTO, int(WIDTH * 0.75), HEIGHT // 2 - 30, None )

def startMenu():
    global original_wooden_height
    actualEvent = "startMenu"
    SCREEN.fill(WHITE)
    WOODEN_TEXTURE_RECT = WOODEN_TEXTURE.get_rect(topleft = (int(WIDTH // 2 - (WIDTH // 3) // 2), original_wooden_height))
    SCREEN.blit(WOODEN_TEXTURE, WOODEN_TEXTURE_RECT)
    hratHru.drawButton()
    hratHru.buttonHover(pygame.mouse.get_pos(), GOLD_BUTTON)
    nastaveni.drawButton()
    nastaveni.buttonHover(pygame.mouse.get_pos(), GOLD_BUTTON)
    ukoncitHru.drawButton()
    ukoncitHru.buttonHover(pygame.mouse.get_pos(), GOLD_BUTTON)
    
#PŘÍCHOD MENU ZE SPODU NA HORU
    if original_wooden_height >= wooden_height:
        speed = 6
        original_wooden_height -= speed
        hratHru.get_rect().y -= speed
        hratHru.get_text_rect().y -= speed
        nastaveni.get_rect().y -= speed
        nastaveni.get_text_rect().y -= speed
        ukoncitHru.get_rect().y -= speed
        ukoncitHru.get_text_rect().y -= speed
        
def selectPlayer():
    actualEvent = "selectPlayer"
    
    SCREEN.fill(WHITE)
    headline = main_font.render("Výběr hráčů", True, GREEN)
    headline_rect = headline.get_rect(topleft = (0, 0))
    SCREEN.blit(headline, headline_rect)
    description = text_font.render("Zatím nelze vytvořit profil, hraješ na profilu Default", True, BLACK)
    description_rect = description.get_rect(topleft = (0, 70))
    SCREEN.blit(description, description_rect)
    
    alphaVerze.drawButton()
    alphaVerze.buttonHover(pygame.mouse.get_pos(), GOLD_BUTTON)
    
def playerMenu():
    actualEvent = "playerMenu"
    SCREEN.fill(WHITE)
    
def selectCharacter():
    actualEvent = "selectCharacter"
    SCREEN.fill(WHITE)
    headline = main_font.render("Vyber si postavu", True, GREEN)
    headline_rect = headline.get_rect(topleft = (0, 0))
    
    SCREEN.blit(headline, headline_rect)
    cisnikFotka.drawButton()
    cisnik.drawButton()
    cisnik.buttonHover(pygame.mouse.get_pos(), GOLD_BUTTON)
    
    cisniceFotka.drawButton()
    cisnice.drawButton()
    cisnice.buttonHover(pygame.mouse.get_pos(), GOLD_BUTTON)
    
    #SCREEN.blit(WAITRESS_PHOTO, (cisnice.get_rect().left, 100))
    
    
    