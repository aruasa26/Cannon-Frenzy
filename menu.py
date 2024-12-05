import pygame
from constants import *

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 72)
        self.small_font = pygame.font.Font(None, 36)
        self.menu_bg_image = pygame.image.load("assets/images/backgrounds/clouds.jpg")
        self.menu_bg_image = pygame.transform.scale(self.menu_bg_image, (800, 600))

    def start_menu(self):
