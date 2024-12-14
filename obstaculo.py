import pygame
import random

class Obstaculo:
    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.velocidad = random.randint(5, 10) 

        
        if tipo == "meteorito":
            self.imagen = pygame.image.load("assets/meteorito.png")
        elif tipo == "satelite":
            self.imagen = pygame.image.load("assets/satelite.png")
        
      
        self.imagen = pygame.transform.scale(self.imagen, (50, 50))
        self.rect = self.imagen.get_rect()
        self.rect.topleft = (self.x, self.y)

    def mover(self):
        
        self.x -= self.velocidad
        self.rect.x = self.x

    def dibujar(self, pantalla):
        
        pantalla.blit(self.imagen, (self.x, self.y))

    def fuera_de_pantalla(self):
        
        return self.x < -self.rect.width
