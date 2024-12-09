import pygame

import sys

pygame.init()

ANCHO = 800
ALTO= 600

NEGRO = (0,0,0)

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

    ventana.fill(NEGRO)

    pygame.display.flip()
    reloj.tick(60)


if __name__ == "__main__":
    main()


    
