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
        self.vidas = 3
        self.nivel = 1
        self.duracion_nivel = 20000
        self.tiempo_inicio_nivel = pygame.time.get_ticks()
        self.puntuacion = 0
        self.esperando_continuar = False


        self.fin_de_nivel = False
        self.planeta_x = self.ancho
        self.planeta_y = self.alto // 2 - 200
        self.planeta_imagen = pygame.image.load("assets/planeta.png")
        self.planeta_imagen = pygame.transform.scale(self.planeta_imagen, (400, 400))

        self.nave = Nave(self.ancho, self.alto, "assets/nav.png")

        self.obstaculos = []
        self.tiempo_generar_obstaculo = 1250
        self.ultimo_obstaculo = pygame.time.get_ticks()

     
    def pantalla_inicial(self):
        self.ventana.fill(self.color_fondo)

    # Fuentes
        fuente_titulo = pygame.font.Font(None, 50)
        fuente_texto = pygame.font.Font(None, 25)

    # Textos principales
        texto_titulo = fuente_titulo.render("The Quest: La búsqueda de otro planeta", True, (255, 255, 255))
        texto_historia1 = fuente_texto.render("En un futuro distante, la Tierra ya no es habitable.", True, (200, 200, 200))
        texto_historia2 = fuente_texto.render("Como piloto de una nave espacial, tu misión es vital:", True, (200, 200, 200))
        texto_historia3 = fuente_texto.render("Explorar el cosmos en busca de un nuevo hogar para la humanidad.", True, (200, 200, 200))

    # Instrucciones
        texto_instrucciones1 = fuente_texto.render("Instrucciones:", True, (255, 255, 255))
        texto_instrucciones2 = fuente_texto.render("- Usa las flechas para mover la nave y esquivar los obstáculos.", True, (200, 200, 200))
        texto_instrucciones3 = fuente_texto.render("- Pulsa ENTER para comenzar tu aventura.", True, (200, 200, 200))

    # Posicionar textos en la pantalla
        self.ventana.blit(texto_titulo, (self.ancho // 2 - texto_titulo.get_width() // 2, 50))

        self.ventana.blit(texto_historia1, (self.ancho // 2 - texto_historia1.get_width() // 2, 150))
        self.ventana.blit(texto_historia2, (self.ancho // 2 - texto_historia2.get_width() // 2, 180))
        self.ventana.blit(texto_historia3, (self.ancho // 2 - texto_historia3.get_width() // 2, 210))

        self.ventana.blit(texto_instrucciones1, (self.ancho // 2 - texto_instrucciones1.get_width() // 2, 300))
        self.ventana.blit(texto_instrucciones2, (self.ancho // 2 - texto_instrucciones2.get_width() // 2, 330))
        self.ventana.blit(texto_instrucciones3, (self.ancho // 2 - texto_instrucciones3.get_width() // 2, 360))

    
        pygame.display.flip()
        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                esperando = False

    def generar_obstaculo(self):
        """Genera un obstáculo nuevo en una posición aleatoria."""
        if not self.fin_de_nivel:
            tipo = random.choice(["meteorito", "satelite"])
            nuevo_obstaculo = Obstaculo(self.ancho, self.alto, tipo, self.nivel)
            self.obstaculos.append(nuevo_obstaculo)

    def actualizar_obstaculos(self):
        """Actualiza el movimiento de los obstáculos y los elimina si salen de la pantalla."""
        for obstaculo in self.obstaculos[:]:
            obstaculo.mover()
            if obstaculo.fuera_de_pantalla():
                self.obstaculos.remove(obstaculo)
                self.puntuacion += 10

    def detectar_colisiones(self):
        """Detecta colisiones entre la nave y los obstáculos."""
        nave_rect = pygame.Rect(self.nave.x, self.nave.y, self.nave.tamano, self.nave.tamano)
        for obstaculo in self.obstaculos:
            obstaculo_rect = pygame.Rect(obstaculo.x, obstaculo.y, obstaculo.ancho, obstaculo.alto)
            if nave_rect.colliderect(obstaculo_rect) and not obstaculo.colisionado:
                obstaculo.colisionado = True
                pygame.mixer.Sound("assets/explosion.wav").play()
                self.vidas -= 1
                if self.vidas <= 0:
                    self.ejecutando = False
                else:
                    self.nave.x = 50
                    self.nave.y = self.alto // 2 - self.nave.tamano // 2
                    pygame.time.delay(1000)

    def gestionar_nivel(self):
        """Controla la progresión entre niveles."""
        tiempo_actual = pygame.time.get_ticks()
        if not self.fin_de_nivel and tiempo_actual - self.tiempo_inicio_nivel > self.duracion_nivel:
            self.fin_de_nivel = True
            self.obstaculos.clear()

    def mostrar_hud(self):
        """Muestra el HUD con vidas, puntuación y nivel."""
        fuente = pygame.font.Font(None, 26)
        texto_vidas = fuente.render(f"VIDAS: {self.vidas}", True, (255, 255, 255))
        texto_puntuacion = fuente.render(f"PUNTOS: {self.puntuacion}", True, (155, 155, 155))
        texto_nivel = fuente.render(f"NIVEL: {self.nivel}", True, (155, 155, 155))
        self.ventana.blit(texto_vidas, (10, 10))
        self.ventana.blit(texto_puntuacion, (10, 50))
        self.ventana.blit(texto_nivel, (10, 90))

    def dibujar_planeta(self):
        """Dibuja el planeta y lo mueve hacia la izquierda."""
        if self.fin_de_nivel:
            if self.planeta_x > 150:
                self.planeta_x -= 2
            self.ventana.blit(self.planeta_imagen, (self.planeta_x, self.planeta_y))


    def mostrar_cartel(self, texto):
    
        fuente = pygame.font.Font(None, 50)
        texto_render = fuente.render(texto, True, (255, 255, 255))
        rect_texto = texto_render.get_rect(center=(self.ancho // 2, self.alto // 2))
        self.ventana.blit(texto_render, rect_texto)

    def avanzar_nivel(self):

        self.nivel += 1
        self.tiempo_inicio_nivel = pygame.time.get_ticks()
        self.fin_de_nivel = False
        self.planeta_x = self.ancho
        self.obstaculos.clear()
        self.nave.x = 50
        self.nave.y = self.alto // 2 - self.nave.tamano // 2
        self.esperando_continuar = False

    def bucle_principal(self):
        while self.ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Manejar el evento para avanzar de nivel
                if self.esperando_continuar and evento.type == pygame.KEYDOWN:
                    self.avanzar_nivel()

        # Si estamos esperando continuar, solo mostramos el cartel y pausamos el juego
            if self.esperando_continuar:
                self.ventana.fill(self.color_fondo)
                self.mostrar_cartel("Pulse cualquier tecla para continuar")
                pygame.display.flip()
                self.reloj.tick(60)
                continue

        # Movimiento de la nave solo si no estamos al final del nivel
            if not self.fin_de_nivel:
                self.nave.mover()

        # Generar obstáculos según el tiempo transcurrido
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.ultimo_obstaculo > self.tiempo_generar_obstaculo and not self.fin_de_nivel:
                self.generar_obstaculo()
                self.ultimo_obstaculo = tiempo_actual

        # Actualizar obstáculos y detectar colisiones
            self.actualizar_obstaculos()
            if not self.fin_de_nivel:
                self.detectar_colisiones()

        # Gestión del nivel
            self.gestionar_nivel()

        # Dibujar elementos del juego
            self.ventana.fill(self.color_fondo)  # Fondo
            self.dibujar_planeta()  # Planeta
            self.nave.dibujar(self.ventana)  # Nave
            for obstaculo in self.obstaculos:  # Obstáculos
                obstaculo.dibujar(self.ventana)

        # Mostrar el HUD
            self.mostrar_hud()

        # Gestión del aterrizaje al final del nivel
            if self.fin_de_nivel:
                self.nave.girar_y_aterrizar(self.planeta_x + 50, self.planeta_y + 200)
                if self.nave.aterrizando:
                    self.esperando_continuar = True

        # Actualizar pantalla
            pygame.display.flip()
            self.reloj.tick(60)

