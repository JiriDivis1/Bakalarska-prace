import pygame
import time
import sys
sys.path.insert(1, 'views')
sys.path.insert(1, 'model')

from model import *
from menus import *
from settings import *
from game import *
from player import *

"""
Pomocné funkce
"""
def isBehindBar(source_position, click_position):
    if source_position[0] < POSITION_BEHIND_BAR[0] and source_position[1] < POSITION_BEHIND_BAR[1]:
        return True
    else:
        return False

def goBehindBar(source_position, click_position):
    if click_position[0] < POSITION_BEHIND_BAR[0] and click_position[1] < POSITION_BEHIND_BAR[1]:
        return True
    else:
        return False

class Controller(object):
    
    """
    Zpracuje vstupy uživatelů
    """
  
    def events(self, events):
        global actualEvent
        global actualPlayer
        
        for event in events:
            if event.type == pygame.QUIT:
                return False
        #Herní menu
            if actualEvent == "startMenu":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  #1 = levé tlačítko na myši
                    if hratHru.isButtonClicked(pygame.mouse.get_pos()):
                        actualEvent = "selectPlayer"
                        #loadPlayers()
                    elif nastaveni.isButtonClicked(pygame.mouse.get_pos()):
                        actualEvent = "settings"
                    elif ukoncitHru.isButtonClicked(pygame.mouse.get_pos()):
                        SCREEN.fill(WHITE)
                        back_text = main_font.render("Na shledanou, přijďte zas", True, RED)
                        back_text_rect = back_text.get_rect(center = (WIDTH // 2, HEIGHT // 2))
                        SCREEN.blit(back_text, back_text_rect)
                        pygame.display.update()
                        time.sleep(2)
                        running = False
        #Nastavení
            if actualEvent == "settings":
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_b:
                        actualEvent = "startMenu"
        #Výběr hráčů
            if actualEvent == "selectPlayer":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        actualEvent = "startMenu"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if alphaVerze.isButtonClicked(pygame.mouse.get_pos()):
                        actualEvent = "selectCharacter"
                        continue
        #Výběr postavy
            if actualEvent == "selectCharacter":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        actualEvent = "startMenu"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    #Zacatek hry + nastavení postavy
                    if cisnik.isButtonClicked(pygame.mouse.get_pos()) or cisnikFotka.isButtonClicked(pygame.mouse.get_pos()):
                        actualPlayer.set_selectedWaiter("waiter")
                        print("Hraješ za číšníka")
                        actualEvent = "game"
                    if cisnice.isButtonClicked(pygame.mouse.get_pos()) or cisniceFotka.isButtonClicked(pygame.mouse.get_pos()):
                        actualPlayer.set_selectedWaiter("waitress")
                        print("Hraješ za číšnici")
                        actualEvent = "game"               
                
        #SAMOTNÁ HRA---------------------EVENTY-----------
            if actualEvent == "game":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    click_position = event.pos
                    if bar.isClicked(click_position):
                        print("Klikl jsi na bar")
                    elif walls.isClicked(click_position):
                        print("klikl jsi na stěnu")
                    elif table2.isClicked(click_position):
                        print("klikl jsi na stůl")
                    elif floor.isClicked(click_position) and floor.priority != 0:   #(protože po kliknutí na tlačítko alpha verze kliknu zároveň i na podlahu)
                        #print(event.pos)
                        source_position = (waiter.get_rect().centerx, waiter.get_rect().bottom)
                        positions = []
                        #Jsem za barem
                        if isBehindBar(source_position, click_position) and not goBehindBar(source_position, click_position):
                            dest_position = []
                            source_position = []
                            source_position.append((waiter.get_rect().centerx, waiter.get_rect().bottom))
                            direct_x = []
                            direct_y = []
                            
                            if click_position[0] > POSITION1[0]:
                                dest_position.append(POSITION1)
                                source_position.append(POSITION1)
                            if click_position[0] > POSITION2[0]:
                                dest_position.append(POSITION2)
                                source_position.append(POSITION2)
                            
                            dest_position.append(click_position)
                                
                            index = 0   #index pro tento foc cyklus
                            for source_pos in source_position:
                                #Půjdeme doprava
                                if source_pos[0] <= dest_position[index][0]:
                                    direct_x.append(SPEED_OF_PEOPLES)
                                #Půjdeme doleva
                                else:
                                    direct_x.append(-1 * SPEED_OF_PEOPLES)
                                
                                #Půjdeme dolů
                                if source_pos[1] <= dest_position[index][1]:
                                    direct_y.append(SPEED_OF_PEOPLES)
                                #Půjdeme nahoru
                                else:
                                    direct_y.append(-1 * SPEED_OF_PEOPLES)   
                                index += 1 
                            index = 0
                        
                        #Jdu za bar
                        elif goBehindBar(source_position, click_position) and not isBehindBar(source_position, click_position):
                            dest_position = [POSITION2, POSITION1, click_position]
                            source_position = [(waiter.get_rect().centerx, waiter.get_rect().bottom), POSITION2, POSITION1]
                            direct_x = []
                            direct_y = []
                            index = 0   #index pro tento foc cyklus
                            for source_pos in source_position:
                                #Půjdeme doprava
                                if source_pos[0] <= dest_position[index][0]:
                                    direct_x.append(SPEED_OF_PEOPLES)
                                #Půjdeme doleva
                                else:
                                    direct_x.append(-1 * SPEED_OF_PEOPLES)
                                
                                #Půjdeme dolů
                                if source_pos[1] <= dest_position[index][1]:
                                    direct_y.append(SPEED_OF_PEOPLES)
                                #Půjdeme nahoru
                                else:
                                    direct_y.append(-1 * SPEED_OF_PEOPLES)   
                                index += 1 
                            index = 0
                        #Nejsem za barem a nejdu za bar
                        else:
                            dest_position = click_position
                        
                            #Půjdeme doprava
                            if source_position[0] <= dest_position[0]:
                                direct_x = SPEED_OF_PEOPLES
                            #Půjdeme doleva
                            else:
                                direct_x = -1 * SPEED_OF_PEOPLES
                            
                            #Půjdeme dolů
                            if source_position[1] <= dest_position[1]:
                                direct_y = SPEED_OF_PEOPLES
                            #Půjdeme nahoru
                            else:
                                direct_y = -1 * SPEED_OF_PEOPLES
                            
                        waiter.set_movement(dest_position, direct_x, direct_y)
                    
        if actualEvent == "startMenu":
            startMenu()
        #alphaVerze tlačítko
        elif actualEvent == "selectPlayer":
            selectPlayer()
        elif actualEvent == "selectCharacter":
            selectCharacter()
        elif actualEvent == "settings":
            settings()
        elif actualEvent == "game":
            game()
                
        #pygame.display.update()
        return True