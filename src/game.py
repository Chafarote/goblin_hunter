import pygame
from pygame.locals import *
import sys
from settings import *
from funciones import *

def game_loop(screen):
    clock = pygame.time.Clock()

    # timers
    aumento_enemigo = pygame.event.custom_type()
    pygame.time.set_timer(aumento_enemigo, 10000)

    timer_poder = pygame.event.custom_type()
    pygame.time.set_timer(timer_poder, 8000)

    # configuro la ventana
    screen = pygame.display.set_mode(SIZE_SCREEN)
    pygame.display.set_caption("Fire Knight")

    # cargo imagenes
    player_imagen_der = pygame.image.load("./assets/player_der.png")
    player_imagen_izq = pygame.image.load("./assets/player_izq.png")
    suelo_imagen = pygame.image.load("./assets/Suelo.png")
    arrow_der = pygame.image.load("./assets/arrow.png")
    arrow_izq = pygame.transform.rotate(arrow_der, 180)
    escudo_imagen = pygame.image.load("./assets/Escudo.png")
    goblin_der = pygame.image.load("./assets/Goblin_Der.png")
    goblin_izq = pygame.image.load("./assets/Goblin_Izq.png")
    poder_imagen = pygame.image.load("./assets/Poder.png")
    corazon = pygame.image.load("./assets/corazon.png")

    # Cargo la musica
    pygame.mixer_music.load("./assets/musica/Musica_batalla.mp3")
    pygame.mixer_music.set_volume(0.1)
    pygame.mixer_music.play(-1, 0.0)

    #cargo los sonidos
    sonido_disparo = pygame.mixer.Sound("./assets/sonidos/Disparo_del_arco.mp3")
    impacto_en_enemigo = pygame.mixer.Sound("./assets/sonidos/Impacto_en_enemigo.mp3")
    impacto_en_jugador = pygame.mixer.Sound("./assets/sonidos/Impacto_jugador.mp3")
    agarro_poder = pygame.mixer.Sound("./assets/sonidos/Poder_fx.mp3")
    pierdo_poder = pygame.mixer.Sound("./assets/sonidos/Escudo_fuera.mp3")
    game_over_sound = pygame.mixer.Sound("./assets/sonidos/Game_over.mp3")


    # configuro la fuente
    fuente = pygame.font.Font("./assets/fonts/Alagard.otf", 48)

    # creo las entidades
    suelo = create_suelo()
    player = create_player()
    cantidad_enemigos = 1

    enemigos = []

    # HUD
    vidas = [corazon, corazon, corazon, corazon, corazon, corazon]
    score = 0
    life_text = fuente.render(f"vidas: {vidas}", True, RED)

    # seteo las banderas
    move_left = False
    move_right = False
    move_salto = False
    contador_salto = 0
    dir_player = "der"

    flecha = None
    poder = None
    escudo = False

    is_running = True

    while is_running:
        clock.tick(FPS)
        # detecto los eventos
        for evento in pygame.event.get():
            if evento.type == QUIT:
                is_running = False

            # detecto las entradas del teclado
            if evento.type == KEYDOWN:
                if evento.key == K_LEFT:
                    move_left = True
                    move_right = False
                    dir_player = "izq"
                if evento.key == K_RIGHT:
                    move_right = True
                    move_left = False
                    dir_player = "der"
                if evento.key == K_UP:
                    move_salto = True
                if evento.key == K_f:
                    if not flecha:
                        sonido_disparo.play()
                        if dir_player == "der":
                            flecha = create_flecha(player["block"].midright, arrow_der, dir_player)
                        if dir_player == "izq":
                            flecha = create_flecha(player["block"].midleft, arrow_izq, dir_player)

            if evento.type == KEYUP:
                if evento.key == K_LEFT:
                    move_left = False
                if evento.key == K_RIGHT:
                    move_right = False

            if evento.type == aumento_enemigo:
                cantidad_enemigos += 1

            if evento.type == timer_poder:
                poder = crear_poder()

        # movimiento del personaje
        if move_left and player["block"].left > 0:
            player["block"].x -= SPEED
            if player["block"].left < 0:
                player["block"].left = 0
        if move_right and player["block"].right < WIDTH:
            player["block"].x += SPEED
            if player["block"].right > WIDTH:
                player["block"].right = WIDTH
        if move_salto and player["block"].bottom <= suelo["block"].top:
            player["block"].y -= SPEED
            contador_salto += SPEED
            if contador_salto >= 100:
                move_salto = False
        if move_salto == False:
            player["block"].y += SPEED
            contador_salto -= SPEED
            if player["block"].bottom > suelo["block"].top:
                player["block"].bottom = suelo["block"].top
                contador_salto = 0

        # movimiento enemigo
        for enemigo in enemigos:
            enemigo["block"].move_ip( enemigo["speed"], 0)
            if enemigo["dir"] == "izq" and enemigo["block"].right < 0:
                enemigo["block"].left = WIDTH
            if enemigo["dir"] == "der" and enemigo["block"].left > WIDTH:
                enemigo["block"].right = 0

        if poder:
            poder["block"].move_ip(velocidad_poder, 0)
            if poder["block"].right < 0:
                poder = None

        # movimiento del disparo
        if flecha:
            flecha["block"].move_ip(flecha["speed"], 0)
            if flecha["block"].left > WIDTH or flecha["block"].right < 0:
                flecha = None

        # colision del poder con el jugador
        if poder:
            if detectar_colision(player["block"], poder["block"]):
                agarro_poder.play()
                escudo = True
                poder = None

        if escudo:
            escudito = crear_escudo(player["block"].center)

        # colisiones
        for enemigo in enemigos[:]:
            if escudo and detectar_colision_circulos(escudito["block"], enemigo["block"]):
                    pierdo_poder.play()
                    enemigos.remove(enemigo)
                    score += 1
                    escudo = False
                    score_text = fuente.render(f"Score: {score}", True, BLUE)
            # ---
            if flecha and detectar_colision(flecha["block"], enemigo["block"]):
                    impacto_en_enemigo.play()
                    enemigos.remove(enemigo)
                    flecha = None
                    score += 1
                    score_text = fuente.render(f"Score: {score}", True, BLUE)
            # ---
            if detectar_colision(enemigo["block"], player["block"]):
                impacto_en_jugador.play()
                try:
                    enemigos.remove(enemigo)
                    vidas.pop()
                    life_text = fuente.render(f"vidas: {vidas}", True, RED)
                except ValueError:
                    game_over_sound.play()

        # Carga de enemigos
        if len(enemigos) == 0:
            cargar_lista_enemigos(enemigos, cantidad_enemigos, min_velocidad_enemigo, max_velocidad_enemigo, "der")
            cargar_lista_enemigos(enemigos, cantidad_enemigos, min_velocidad_enemigo, max_velocidad_enemigo, "izq")

        if len(vidas) == 0:
            game_over_sound.play()
            is_running = False
            pygame.mixer_music.stop()

        # ----dibujar pantalla

        # dibujo escenario
        screen.fill(CUSTOM_BLUE)
        pygame.draw.rect(screen, suelo["color"], suelo["block"])
        screen.blit(suelo_imagen, (0, HEIGHT - 190))

        mostrar_texto(screen, SCORE_POS, f"Score: {score}", fuente, BLUE)
        separacion_x = 50
        for vida in vidas:
            screen.blit(vida, (separacion_x, 50))
            separacion_x += 30

        # dibujo el disparo
        if flecha:
            screen.blit(flecha["imagen"], flecha["block"])

        # Dibujo el power up
        if poder:
            screen.blit(poder_imagen, poder["block"])

        # dibujo el personaje
        if dir_player == "der":
            screen.blit(player_imagen_der, player["block"])
        if dir_player == "izq":
            screen.blit(player_imagen_izq, player["block"])

        # Dibujo el escudo
        if escudo:
            screen.blit(escudo_imagen, escudito["block"])

        # Dibujo a los enemigos
        for enemigo in enemigos:
            if enemigo["dir"] == "der":
                screen.blit(goblin_der, enemigo["block"])
            if enemigo["dir"] == "izq":
                screen.blit(goblin_izq, enemigo["block"])

        # actualizo la pantalla
        pygame.display.flip()

    # Llamar a la pantalla de game over
    from game_over import game_over_screen
    game_over_screen(screen, score)