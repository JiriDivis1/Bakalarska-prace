import pygame

from model import *

def settings():
    actualEvent = "settings"
    SCREEN.fill(GREEN)
    back_text = main_font.render("Nastavení, stiskem b se vrátíš zpět", True, RED)
    back_text_rect = back_text.get_rect(topleft = (0, 0))
    SCREEN.blit(back_text, back_text_rect)