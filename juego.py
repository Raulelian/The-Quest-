import pygame
from nave import Nave
from obstaculo import Obstaculo
import sys
import random

class Juego:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.ancho = 800
        self.alto = 600
        self.color_fondo = (10, 10, 50)
        self.ventana = pygame.display.set_mode((self.ancho, self.alto))

        pygame.display.set_caption("The Quest")
        self.reloj = pygame.time.Clock()

        self.ejecutando = True
        self.vidas = 3  # Número de vidas del jugador
        
        # Inicializar la nave
        ruta_imagen_nave = "assets/nav.png"
        self.nave = Nave(self.ancho, self.alto, ruta_imagen_nave)

        # Obstáculos
        self.obstaculos = []
        self.tiempo_generar_obstaculo = 1250  # Cada 2 segundos
        self.ultimo_obstaculo = pygame.time.get_ticks()

    def generar_obstaculo(self):
        """Genera un obstáculo nuevo en una posición aleatoria."""
        tipo = random.choice(["meteorito", "satelite"])  # Tipos de obstáculos
        y = random.randint(50, self.alto - 50)  # Posición vertical aleatoria
        nuevo_obstaculo = Obstaculo(self.ancho, y, tipo)
        self.obstaculos.append(nuevo_obstaculo)

    def actualizar_obstaculos(self):
        """Actualiza el movimiento de los obstáculos y los elimina si salen de la pantalla."""
        for obstaculo in self.obstaculos[:]:  # Copiamos la lista para evitar problemas al eliminar
            obstaculo.mover()
            if obstaculo.fuera_de_pantalla():
                self.obstaculos.remove(obstaculo)

    def dibujar_obstaculos(self):
        """Dibuja todos los obstáculos en la pantalla."""
        for obstaculo in self.obstaculos:
            obstaculo.dibujar(self.ventana)

    
    def mostrar_vidas(self):
        fuente = pygame.font.Font(None, 36)  # Fuente de texto
        texto = fuente.render(f"VIDAS: {self.vidas}", True, (255, 255, 255))
        self.ventana.blit(texto, (10, 10))  # Esquina superior izquierda

    def detectar_colisiones(self):
        nave_rect = pygame.Rect(self.nave.x, self.nave.y, self.nave.tamano, self.nave.tamano)
        for obstaculo in self.obstaculos:
            obstaculo_rect = pygame.Rect(obstaculo.x, obstaculo.y, obstaculo.ancho, obstaculo.alto)
            if nave_rect.colliderect(obstaculo_rect) and not obstaculo.colisionado:
                print("¡Colisión detectada!")
                obstaculo.colisionado = True  # Marcar obstáculo como colisionado
                sonido_explosion = pygame.mixer.Sound("assets/explosion.wav")
                sonido_explosion.play()
                self.vidas -= 1  # Resta una vida
                if self.vidas <= 0:
                    print("¡Juego terminado!")
                    pygame.time.delay(2000)  # Pausa para mostrar la explosión
                    self.ejecutando = False
                else:
                    self.nave.x = 50
                    self.nave.y = self.alto // 2 - self.nave.tamano // 2
                    pygame.time.delay(1000)  # Pausa breve antes de continuar




    def bucle_principal(self):
        while self.ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        # Movimiento de la nave
            self.nave.mover()

        # Generar obstáculos en intervalos regulares
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.ultimo_obstaculo > self.tiempo_generar_obstaculo:
                self.generar_obstaculo()
                self.ultimo_obstaculo = tiempo_actual

        # Actualizar obstáculos
            self.actualizar_obstaculos()

        # Detectar colisiones
            self.detectar_colisiones()

        # Dibujar todo en la pantalla
            self.ventana.fill(self.color_fondo)  # Fondo
            self.nave.dibujar(self.ventana)      # Nave
            self.dibujar_obstaculos()           # Obstáculos

        # Mostrar las vidas
            self.mostrar_vidas()

        # Actualizar la pantalla
            pygame.display.flip()
            self.reloj.tick(60)  # 60 FPS

