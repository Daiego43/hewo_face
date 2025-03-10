import pygame
import sys

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rectángulo y Elipse")

# Colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Dimensiones del rectángulo
rect_width, rect_height = 100, 300
rect_x, rect_y = (WIDTH - rect_width) // 2, (HEIGHT - rect_height) // 2

# Factor para la elipse (entre 0 y 1)
ellipse_factor = 0.5

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            ellipse_factor += 0.1
            if ellipse_factor > 1.0:
                ellipse_factor = 1.0
        if keys[pygame.K_s]:
            ellipse_factor -= 0.1
            if ellipse_factor < 0.1:
                ellipse_factor = 0.1
            

    # Rellenar la pantalla
    screen.fill(WHITE)

    # Dibujar el rectángulo
    pygame.draw.rect(screen, BLUE, (rect_x, rect_y, rect_width, rect_height))

    # Calcular dimensiones de la elipse en función del factor
    ellipse_width = rect_width * ellipse_factor
    ellipse_height = rect_height * ellipse_factor
    ellipse_x = rect_x + (rect_width - ellipse_width) // 2
    ellipse_y = rect_y + (rect_height - ellipse_height) // 2

    # Dibujar la elipse centrada en el rectángulo
    pygame.draw.ellipse(screen, RED, (ellipse_x, ellipse_y, ellipse_width, ellipse_height))

    # Actualizar la pantalla
    pygame.display.flip()

# Salir de Pygame
pygame.quit()
sys.exit()
