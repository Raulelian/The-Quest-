import pygame
import random
import os

class Obstaculo:
    def __init__(self, ancho_pantalla, alto_pantalla, tipo):
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla

        self.ancho = 50
        self.alto = 50
        self.x = ancho_pantalla
        self.y = random.randint(0, alto_pantalla - self.alto)
        self.velocidad = random.randint(5, 9)
        self.tipo = tipo

        self.colisionado = False  # Nuevo atributo

        # Cargar imagen según el tipo
        if self.tipo == "meteorito":
            ruta_imagen = "assets/meteorito.png"
        elif self.tipo == "satelite":
            ruta_imagen = "assets/satelite.png"
        else:
            ruta_imagen = None  # En caso de no tener tipo válido

        if ruta_imagen and os.path.exists(ruta_imagen):
            self.imagen = pygame.image.load(ruta_imagen)
            self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto))
        else:
            self.imagen = None  # No usar imagen si no existe o no es válida
            self.color = (255, 0, 0)  # Rojo por defecto


    def mover(self):
        self.x -= self.velocidad

    def dibujar(self, pantalla):
        if self.imagen:
            pantalla.blit(self.imagen, (self.x, self.y))  # Dibujar la imagen
        else:
            pygame.draw.rect(pantalla, self.color, (self.x, self.y, self.ancho, self.alto))

    def fuera_de_pantalla(self):
        return self.x < -self.ancho
