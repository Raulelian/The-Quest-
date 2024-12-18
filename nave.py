import pygame
import os

class Nave:
    def __init__(self, ancho_pantalla, alto_pantalla, ruta_imagen):
        self.x = 50  
        self.tamano = 40
        self.y = alto_pantalla // 2 - self.tamano // 2
        self.velocidad = 5
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla
        self.girada = False  # Para controlar el giro
        self.aterrizando = False  # Estado de aterrizaje

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

    def girar_y_aterrizar(self, destino_x, destino_y):
        if not self.girada:  # Controlar si ya se giró
            self.imagen = pygame.transform.rotate(self.imagen, 270)  # Rotar 90 grados
            self.girada = True
        if self.x < destino_x:
            self.x += 2  # Mover a la derecha
        if self.y < destino_y:
            self.y += 1  # Mover hacia abajo
        elif self.y > destino_y:
            self.y -= 1  # Mover hacia arriba

        # Comprobar si alcanzó el destino
        if abs(self.x - destino_x) < 5 and abs(self.y - destino_y) < 5:
            self.aterrizando = True
        else:
            self.aterrizando = False

    