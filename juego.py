import pygame
from nave import Nave
import sys

class Juego:
    def __init__(self):
        pygame.init()
        self.ancho = 800
        self.alto= 600
        self.color_fondo= (10,10,50)
        self.ventana = pygame.display.set_mode((self.ancho, self.alto))
        pygame.display.set_caption("The Quest")
        self.reloj = pygame.time.Clock()
        self.ejecutando = True
        self.nave = Nave(self.ancho, self.alto)

    def bucle_principal(self):
        while self.ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.nave.mover()

            self.ventana.fill(self.color_fondo)
            self.nave.dibujar(self.ventana)

            pygame.display.flip()
            self.reloj.tick(60)
        
        


