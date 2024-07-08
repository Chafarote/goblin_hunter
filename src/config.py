import pygame
from pygame.locals import *
from settings import *
from funciones import *

def config_menu(screen):
    clock = pygame.time.Clock()
    running = True

    fondo = pygame.image.load("./assets/Fondo_menu.jpg")
    fondo_opciones = pygame.transform.scale(pygame.image.load("./assets/UI/opciones.png"), (100, 100))
    rect_fondo_musica = fondo_opciones.get_rect(center = MUSICA_CONFIG_POS)
    boton_mas = pygame.transform.scale(pygame.image.load("./assets/UI/boton_mas.png"), (50, 50))
    boton_menos = pygame.transform.scale(pygame.image.load("./assets/UI/boton_menos.png"), (50, 50))

    boton_mas_music = create_block(WIDTH // 2 + 60, 200, 50, 50)
    boton_menos_music = create_block(WIDTH // 2 - 110, 200, 50, 50)

    fuente_titulo = pygame.font.Font(None, 70)
    fuente = pygame.font.Font(None, 50)

    while running:
        clock.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == QUIT:
                terminar()
            elif evento.type == KEYDOWN and evento.key == K_ESCAPE:
                running = False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if punto_en_rectangulo(evento.pos, boton_mas_music["block"]) and pygame.mixer.music.get_volume() < 1.0:
                        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.1)
                    elif punto_en_rectangulo(evento.pos, boton_menos_music["block"]) and pygame.mixer.music.get_volume() > 0.0:
                        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.1)

        # Dibujar elementos de configuración aquí

        screen.blit(fondo, COORDENADA_ORIGEN)

        mostrar_texto(screen, TITULO_POS, "CONFIGURACION", fuente_titulo, BLACK)
        mostrar_texto(screen, MUSICA_TEXT_POS, "VOLUMEN DE MUSICA", fuente, BLACK)

        screen.blit(fondo_opciones, rect_fondo_musica)
        screen.blit(boton_mas, boton_mas_music["block"])
        screen.blit(boton_menos, boton_menos_music["block"])

        pygame.display.flip()
    

