import pygame

import sys

pygame.init()

ANCHO = 800
ALTO= 600

AZUL_OSCURO = (10,10,50)

ventana = pygame.display.set_mode((ANCHO,ALTO))

pygame.display.set_caption("The Quest")

reloj = pygame.time.Clock()

def main():
    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    ventana.fill(AZUL_OSCURO)

    pygame.display.flip()
    reloj.tick(60)


if __name__ == "__main__":
    main()


    
