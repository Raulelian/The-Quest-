import pygame


class Nave:

    def __init__(self, ancho_pantalla, alto_pantalla):
        self.x = 50  
        self.y = alto_pantalla // 2  
        self.velocidad = 5
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla
        self.color = (255, 255, 0)  
        self.tamano = 40  

    def mover(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP] and self.y > 0:  
            self.y -= self.velocidad
        if teclas[pygame.K_DOWN] and self.y < self.alto_pantalla - self.tamano:  
            self.y += self.velocidad

    def dibujar(self, ventana):
        pygame.draw.polygon(ventana, (255,255,255), [(self.x,self.y), (self.x-20, self.y+40), (self.x+20,self.y+40 )])
        pygame.draw.rect(ventana, (200,200,200), (self.x-15,self.y+40,30,60))
        pygame.draw.circle(ventana, (150,150,150), (self.x-10,self.y+100),10)
        pygame.draw.circle(ventana, (150,150,150), (self.x-10,self.y +100),10)

