import pygame
import sys
from funciones import *
from settings import *

def show_ranking(screen):
    clock = pygame.time.Clock()
    running = True

    fondo = pygame.image.load("./assets/fondo_ranking.jpg")

    # Leer los scores desde un archivo
    scores = []
    try:
        cargar_archivo_csv("scores.csv", scores)
    except FileNotFoundError:
        scores = []

    # Ordeno la lista de forma descendente
    ordenar_lista(scores)

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminar()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        screen.blit(fondo, COORDENADA_ORIGEN)

        font_titulo = pygame.font.Font("./assets/fonts/Alagard.otf", 50)
        font = pygame.font.Font("./assets/fonts/Alagard.otf", 36)
        mostrar_texto(screen, RANKING_POS, f'RANKING', font_titulo, BLACK)
        y_offset = 100
        for score in scores:
            mostrar_texto(screen, (WIDTH // 2, y_offset), f'{score["name"]}: {score["score"]}', font, YELLOW)
            y_offset += 40

        pygame.display.flip()
