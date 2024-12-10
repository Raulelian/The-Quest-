import pygame

import sys

class Juego:
    def __init__(self):
        pygame.init()
        self.ancho = 800
        self.alto= 600
        self.color_fondo= (10,10,50)
        self.ventana = pygame.display.set_mode((self.ancho, self.alto))
