import pygame

from model import *

class Player():
    def __init__(self, name, selectedWaiter):
        self.name = name                        #Jméno hráče
        self.selectedWaiter = selectedWaiter    #Waiter, pokud hraji za číšníka, Waitress, pokud hraji za číšnici

    def get_name(self):
        return self.name

    def get_selectedWaiter(self):
        return self.selectedWaiter

    def set_name(self, name):
        self.name = name
        return self
    
    def set_selectedWaiter(self, selectedWaiter):
        self.selectedWaiter =  selectedWaiter
        return self
    
listOfPlayers = []
actualPlayer = None
    
"""
Metoda která načte účty hráčů ze souborů json
"""
def loadPlayers():
    global listOfPlayers, actualPlayer
    
    listOfPlayers = []
    actualPlayer = Player("Default", "waiter")
    
loadPlayers()

#print(actualPlayer.get_selectedWaiter())