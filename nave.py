import pygame
import os

class Nave:

    def __init__(self, ancho_pantalla, alto_pantalla, ruta_imagen):
        self.x = 50  
        self.y = alto_pantalla // 2  
        self.velocidad = 5
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla
        self.tamano = 40


        if not os.path.exists(ruta_imagen):
            raise FileNotFoundError(f"No se encontró la imagen en la ruta: {ruta_imagen}")
        
        self.imagen = pygame.image.load(ruta_imagen)
        self.imagen = pygame.transform.scale(self.imagen, (self.tamano * 2, self.tamano * 2))
  
    def mover(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP] and self.y > 0:  
            self.y -= self.velocidad
        if teclas[pygame.K_DOWN] and self.y < self.alto_pantalla - self.imagen.get_height():  
            self.y += self.velocidad

    def dibujar(self, ventana):
        ventana.blit(self.imagen, (self.x, self.y))
