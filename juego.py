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
        self.nivel = 1  # Nivel inicial
        self.duracion_nivel = 20000  # 20 segundos por nivel
        self.tiempo_inicio_nivel = pygame.time.get_ticks()
        self.puntuacion = 0

        # Inicializar la nave
        ruta_imagen_nave = "assets/nav.png"
        self.nave = Nave(self.ancho, self.alto, ruta_imagen_nave)

        # Obstáculos
        self.obstaculos = []
        self.tiempo_generar_obstaculo = 1250  # Cada 1.25 segundos
        self.ultimo_obstaculo = pygame.time.get_ticks()

    def generar_obstaculo(self):
        """Genera un obstáculo nuevo en una posición aleatoria."""
        tipo = random.choice(["meteorito", "satelite"])  # Tipos de obstáculos
        y = random.randint(50, self.alto - 50)  # Posición vertical aleatoria
        nuevo_obstaculo = Obstaculo(self.ancho, y, tipo, self.nivel)
        self.obstaculos.append(nuevo_obstaculo)

    def actualizar_obstaculos(self):
        """Actualiza el movimiento de los obstáculos y los elimina si salen de la pantalla."""
        for obstaculo in self.obstaculos[:]:  # Copiamos la lista para evitar problemas al eliminar
            obstaculo.mover()
            if obstaculo.fuera_de_pantalla():
                self.obstaculos.remove(obstaculo)
                self.puntuacion += 10  # Sumar puntos por esquivar un obstáculo

    def dibujar_obstaculos(self):
        """Dibuja todos los obstáculos en la pantalla."""
        for obstaculo in self.obstaculos:
            obstaculo.dibujar(self.ventana)

    def mostrar_vidas(self):
        fuente = pygame.font.Font(None, 32)  # Fuente de texto
        texto = fuente.render(f"VIDAS: {self.vidas}", True, (255, 255, 255))
        self.ventana.blit(texto, (10, 10))  # Esquina superior izquierda

    def mostrar_puntuacion(self):
        fuente = pygame.font.Font(None, 28)
        texto = fuente.render(f"PUNTOS: {self.puntuacion}", True, (155, 155, 155))
        self.ventana.blit(texto, (10, 50))  # Debajo de las vidas

    def mostrar_nivel(self):
        fuente = pygame.font.Font(None, 26)
        texto = fuente.render(f"NIVEL: {self.nivel}", True, (155, 155, 155))
        self.ventana.blit(texto, (10, 90))  # Debajo de la puntuación

    def detectar_colisiones(self):
        nave_rect = pygame.Rect(self.nave.x, self.nave.y, self.nave.tamano, self.nave.tamano)
        for obstaculo in self.obstaculos:
            obstaculo_rect = pygame.Rect(obstaculo.x, obstaculo.y, obstaculo.ancho, obstaculo.alto)
            if nave_rect.colliderect(obstaculo_rect) and not obstaculo.colisionado:
                obstaculo.colisionado = True
                print("¡Colisión detectada!")
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

    def gestionar_nivel(self):
        """Controla la progresión entre niveles."""
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_inicio_nivel > self.duracion_nivel:
            self.nivel += 1
            self.tiempo_inicio_nivel = tiempo_actual
            # Aumentar la dificultad
            self.tiempo_generar_obstaculo = max(500, self.tiempo_generar_obstaculo - 200)  # Más rápidos
            for obstaculo in self.obstaculos:
                obstaculo.velocidad += 2  # Obstáculos más rápidos
            print(f"¡Avanzaste al nivel {self.nivel}!")

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

            # Gestionar niveles
            self.gestionar_nivel()

            # Dibujar todo en la pantalla
            self.ventana.fill(self.color_fondo)  # Fondo
            self.nave.dibujar(self.ventana)      # Nave
            self.dibujar_obstaculos()           # Obstáculos
            self.mostrar_vidas()                # Vidas
            self.mostrar_puntuacion()           # Puntuación
            self.mostrar_nivel()                # Nivel

            # Actualizar la pantalla
            pygame.display.flip()
            self.reloj.tick(60)  # 60 FPS

