import pygame
import random

class Obstaculo:
    def __init___(self,x,y,tipo):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.velocidad = random.randit (5,10)

        if tipo == "obstaculo1":
             self.imagen = pygame.image.load("assets/obstaculo1.png")

        elif tipo == "obstaculo2":
             self.imagen = pygame.image.load("assets/obstaculo2.png")
        
        self.imagen = pygame.transform.scale(self.imagen, (50, 50))
        self.rect = self.imagen.get_rect()
        self.rect.topleft = (self.x, self.y)
