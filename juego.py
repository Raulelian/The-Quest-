import pygame
from nave import Nave
from obstaculo import Obstaculo
import sys
import random

class Juego:
    def __init__(self):
        pygame.init()
        self.ancho = 800
        self.alto = 600
        self.color_fondo = (10, 10, 50)
        self.ventana = pygame.display.set_mode((self.ancho, self.alto))
        pygame.display.set_caption("The Quest")
        self.reloj = pygame.time.Clock()
        self.ejecutando = True

        # Inicializar la nave
        ruta_imagen_nave = "assets/nav.png"
        self.nave = Nave(self.ancho, self.alto, ruta_imagen_nave)

        # Obstáculos
        self.obstaculos = []
        self.tiempo_generar_obstaculo = 2000
        self.ultimo_obstaculo = pygame.time.get_ticks()

    def generar_obstaculo(self):
        tipo = random.choice(["meteorito", "satelite"])
        nuevo_obstaculo = Obstaculo(self.ancho, self.alto, tipo)
        self.obstaculos.append(nuevo_obstaculo)

    def actualizar_obstaculos(self):
        for obstaculo in self.obstaculos[:]:
            obstaculo.mover()
            if obstaculo.fuera_de_pantalla():
                self.obstaculos.remove(obstaculo)

    def detectar_colisiones(self):
        nave_rect = pygame.Rect(self.nave.x, self.nave.y, self.nave.tamano, self.nave.tamano)
        for obstaculo in self.obstaculos:
            obstaculo_rect = pygame.Rect(obstaculo.x, obstaculo.y, obstaculo.ancho, obstaculo.alto)
            if nave_rect.colliderect(obstaculo_rect):
                print("¡Colisión detectada!")
                self.ejecutando = False

    def dibujar_obstaculos(self):
        for obstaculo in self.obstaculos:
            obstaculo.dibujar(self.ventana)

    def bucle_principal(self):
        while self.ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.nave.mover()
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.ultimo_obstaculo > self.tiempo_generar_obstaculo:
                self.generar_obstaculo()
                self.ultimo_obstaculo = tiempo_actual

            self.actualizar_obstaculos()
            self.detectar_colisiones()

            self.ventana.fill(self.color_fondo)
            self.nave.dibujar(self.ventana)
            self.dibujar_obstaculos()

            pygame.display.flip()
            self.reloj.tick(60)

        


