import pygame
import sys
from pygame.locals import *
from random import randint
from settings import *

# bloques --
def create_block(left=0, top=0, width=50, height=50, color= (255, 255, 255)):
    return {"block": pygame.Rect(left, top, width, height), "color": color}

def create_player():
    return create_block(player_x, player_y, player_width, player_height)

def create_suelo():
    return create_block(0,500,1000,100, GREEN)

def create_enemy(min_velocidad:int, max_velocidad:int, direccion:str):
    if direccion == "izq":
        enemigo_x = randint(WIDTH, maximo_spawn)
        velocidad = randint(-max_velocidad, -min_velocidad)
    elif direccion == "der":
        enemigo_x = randint(minimo_spawn , 0 - enemigo_width)
        velocidad = randint(min_velocidad, max_velocidad)
    enemigo = create_block(enemigo_x, enemigo_y, enemigo_width, enemigo_height, RED)
    enemigo["speed"] = velocidad
    enemigo["dir"] = direccion
    return enemigo

def cargar_lista_enemigos(lista:list, cantidad_enemigos:int, min_velocidad:int, max_velocidad:int, direccion:str):
    for _ in range(cantidad_enemigos):
        lista.append(create_enemy(min_velocidad, max_velocidad, direccion))

def create_flecha(coordenada_spawn:tuple[int, int], imagen, direccion:str):
    flecha = {"block":pygame.Rect(0, 0, flecha_width, flecha_height), "dir":direccion, "imagen":imagen}
    if direccion == "der":
        flecha["block"].midright = coordenada_spawn
        flecha["speed"] = flecha_speed
    if direccion == "izq":
        flecha["block"].midleft = coordenada_spawn
        flecha["speed"] = -flecha_speed
    return flecha

def crear_poder():
    return create_block(WIDTH, 350, 40, 40, BLUE)

def crear_escudo(cordenada_spawn:tuple[int, int]):
    escudo = {"block":pygame.Rect(0, 0, escudo_width, escudo_height), "color": BLUE}
    escudo["block"].center = cordenada_spawn
    return escudo

# colisiones --
def detectar_colision(rect_1, rect_2):
    if punto_en_rectangulo(rect_1.topleft, rect_2) or \
       punto_en_rectangulo(rect_1.topright, rect_2) or\
       punto_en_rectangulo(rect_1.bottomleft, rect_2) or\
       punto_en_rectangulo(rect_1.bottomright, rect_2) or\
       punto_en_rectangulo(rect_2.topleft, rect_1) or \
       punto_en_rectangulo(rect_2.topright, rect_1) or\
       punto_en_rectangulo(rect_2.bottomleft, rect_1) or\
       punto_en_rectangulo(rect_2.bottomright, rect_1):
        return True
    else:
        return False
        

def punto_en_rectangulo(punto, rect):
    x, y = punto
    return x >= rect.left and x <= rect.right and y >= rect.top and y <= rect.bottom

def distancia_entre_puntos(pto_1:tuple[int, int], pto_2:tuple[int, int])->float:
    return ((pto_1[0] - pto_2[0])**2 + (pto_1[1] - pto_2[1])**2)** 0.5

def calcular_radio(rect)->int:
    return rect.width // 2

def detectar_colision_circulos(rect_1, rect_2)->bool:
    r1 = calcular_radio(rect_1)
    r2 = calcular_radio(rect_2)
    distancia = distancia_entre_puntos(rect_1.center, rect_2.center)
    return distancia <= r1 + r2

def mostrar_texto(superficie: pygame.Surface, coordenada: tuple[int, int], texto: str, fuente:pygame.font.Font, color: tuple[int, int, int] = WHITE, color_de_fondo: tuple[int, int, int] = None):
    sup_texto = fuente.render(texto, True, color, color_de_fondo)
    rect_texto = sup_texto.get_rect(center = coordenada)
    superficie.blit(sup_texto, rect_texto)

def terminar():
    pygame.quit()
    sys.exit()

def get_path_actual(nombre_archivo):
    import os
    directorio_actual = os.path.dirname(__file__)
    return os.path.join(directorio_actual, nombre_archivo)

def cargar_archivo_csv(nombre_archivo:str, lista:list)->None:
    with open(get_path_actual(nombre_archivo), "r", encoding="utf-8") as archivo:
        encabezado = archivo.readline().strip("\n").split(",")

        for linea in archivo.readlines():
            usuario = {}
            linea = linea.strip("\n").split(",")

            name, score = linea
            usuario["name"] = name
            usuario["score"] = int(score)
            lista.append(usuario)

def generar_archivo_csv(lista:list, nombre_archivo:str):
    with open(get_path_actual(nombre_archivo), "w", encoding="utf-8") as archivo:
        encabezado = ",".join(list(lista[0].keys())) + "\n"
        archivo.write(encabezado)
        for elemento in lista:
            values = list(elemento.values())
            l = []
            for value in values:
                if isinstance(value, int):
                    l.append(str(value))
                elif isinstance(value, float):
                    l.append(str(value))
                else:
                    l.append(value)
            linea = ",".join(l) + "\n"
            archivo.write(linea)


def swap_dict(lista:list, i:int, j:int)->None:
    """swapea elementos de una lista

    Args:
        lista (list): lista de diccionarios
        i (int): indice comparado
        j (int): indice con el que se compara
    """
    aux_diccionario = lista[i]
    lista[i] = lista[j]
    lista[j] = aux_diccionario

def ordenar_lista(lista:list)->None:
    """ordena la lista de forma descendente

    Args:
        lista (list): lista a ordenar
    """
    tam = len(lista)
    for i in range(tam -1):
        for j in range(i +1, tam):
            if lista[i]["score"] < lista[j]["score"]:
                swap_dict(lista, i, j)

def leer_json(nombre_archivo:str, lista:list):
    import json
    with open(get_path_actual(nombre_archivo), "r", encoding="utf-8") as archivo:
        lista = json.load(archivo)


def cargar_json(nombre_archivo:str, lista:list):
    import json
    with open(get_path_actual(nombre_archivo), "w", encoding="utf-8") as archivo:
        json.dump(lista, archivo, indent=4)
