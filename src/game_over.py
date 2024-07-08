import pygame
import sys
import tkinter
import customtkinter
from tkinter.simpledialog import askstring as prompt
from funciones import *

def game_over_screen(screen, score):
    clock = pygame.time.Clock()
    running = True

    fondo = pygame.image.load("./assets/Fondo_menu.jpg")

    # Guardar el puntaje en el archivo
    name = prompt("Game Over","Ingrese sus inicales: ")
    usuario = {"name":name, "score":score}
    # Leer los scores desde un archivo
    scores = []
    try:
        cargar_archivo_csv("scores.csv", scores)
    except FileNotFoundError:
        scores = []

    scores.append(usuario)

    # guardo la lista en formato CSV
    generar_archivo_csv(scores, "scores.csv")
    cargar_json("scores.json", scores)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                running = False
                from main import main_menu
                main_menu()

        screen.blit(fondo, COORDENADA_ORIGEN)
        font_game_over = pygame.font.Font("./assets/fonts/Alagard.otf", 100)
        font = pygame.font.Font("./assets/fonts/Alagard.otf", 60)

        mostrar_texto(screen, GAME_OVER_POS, "GAME OVER", font_game_over, RED)
        mostrar_texto(screen, CENTER_SCREEN, f'Score: {score}', font, BLACK)
        mostrar_texto(screen, PRESIONE_ENTER_POS, "PRESIONE ENTER", font, BLACK)

        pygame.display.flip()
        clock.tick(60)
