import pygame
from settings import *
from funciones import *
from game import game_loop
from config import config_menu
from ranking import show_ranking

# Inicializar Pygame
pygame.init()

# Configurar la pantalla
screen = pygame.display.set_mode(SIZE_SCREEN)
pygame.display.set_caption('Goblin Hunter')
clock = pygame.time.Clock()

# Cargo las imagenes
fondo = pygame.image.load("./assets/Fondo_menu.jpg")
banner = pygame.image.load("./assets/Banner.png")
rect_banner = banner.get_rect(center = TITULO_POS)
boton_jugar = pygame.transform.scale(pygame.image.load("./assets/Button_Blue.png"), (250, 100))
rect_boton_jugar = boton_jugar.get_rect(center = BOTON_PLAY_POS)
boton_config = pygame.transform.scale(pygame.image.load("./assets/Button_Blue.png"), (560, 100))
rect_boton_config = boton_config.get_rect(center = BOTON_CONFIG_POS)
boton_ranking = pygame.transform.scale(pygame.image.load("./assets/Button_Blue.png"), (400, 100))
rect_boton_ranking = boton_ranking.get_rect(center = BOTON_RANKING_POS)
boton_salir = pygame.transform.scale(pygame.image.load("./assets/Button_Red.png"), (250, 100))
rect_boton_salir = boton_salir.get_rect(center = BOTON_SALIR_POS)

# Cargo los sonidos
pygame.mixer_music.load("./assets/musica/Musica_menu.mp3")
pygame.mixer_music.set_volume(0.1)
pygame.mixer_music.play(-1, 0.0)

# Fuente
font_titulo = pygame.font.Font("./assets/fonts/Alagard.otf", 60)
font = pygame.font.Font("./assets/fonts/Alagard.otf", 50)

def main_menu():
    clock.tick(FPS)
    while True:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                terminar()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if punto_en_rectangulo(evento.pos, rect_boton_jugar):
                        game_loop(screen)
                    elif punto_en_rectangulo(evento.pos, rect_boton_config):
                        config_menu(screen)
                    elif punto_en_rectangulo(evento.pos, rect_boton_ranking):
                        show_ranking(screen)
                    elif punto_en_rectangulo(evento.pos, rect_boton_salir):
                        terminar()

        screen.blit(fondo, COORDENADA_ORIGEN)

        screen.blit(banner, rect_banner)
        screen.blit(boton_jugar, rect_boton_jugar)
        screen.blit(boton_config, rect_boton_config)
        screen.blit(boton_ranking, rect_boton_ranking)
        screen.blit(boton_salir, rect_boton_salir)

        mostrar_texto(screen, TITULO_POS, "GOBLIN HUNTER", font_titulo, BLACK)
        mostrar_texto(screen, BOTON_PLAY_POS, "JUGAR", font, BLACK)
        mostrar_texto(screen, BOTON_CONFIG_POS, "CONFIGURACION", font, BLACK)
        mostrar_texto(screen, BOTON_RANKING_POS, "RANKING", font, BLACK)
        mostrar_texto(screen, BOTON_SALIR_POS, "SALIR", font, BLACK)

        pygame.display.flip()

if __name__ == '__main__':
    main_menu()
