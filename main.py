#!main/bin/python3.8
from sys import path
path.clear()
path.append("main/lib/site/python3.8")
path.append("main/lib/python3.8/site-packages/")
import pygame
from pygame.locals import *
from random import randint
pygame.init()


# -------  FUNCIONES ----

def print_map(screen):
    global cell_list, current_torch_form, current_torch_frame
    x = 0 - rect.x
    y = screen_height - rect.y 
    cell_list = []
    for line in game_map:
        for character in line:
            if character == '1':
                imagen = dirt_img
            elif character == '2':
                imagen = grass_img
            elif character == '3':
                imagen = torch_list[current_torch_form]
                if current_torch_frame == frames_per_torch:
                    current_torch_form += 1
                    current_torch_frame = 0
                    if current_torch_form > len(torch_list)-1:
                        current_torch_form = 0
                else:
                    current_torch_frame += 1
            if character != '0':
                cell_list.append( pygame.Rect( [ x , y , blocks_width , blocks_height ] ) )
                screen.blit( imagen , (x , y) )
            x += blocks_width
        y += blocks_height
        x = 0 - rect.x


def load_map():
    with open('mapa.txt', 'r') as file_:
        game_map  = []
        curr_line = 0
        for line in file_:
            game_map.append([])
            for character in line:
                if character != '\n':
                    game_map[curr_line].append(character)
            curr_line += 1
    return game_map

def get_image_ready(nombre, width, height, color_key = None, alpha_activated = False):
    if not alpha_activated:
        imagen = pygame.image.load(f'{nombre}').convert()
    else:
        imagen = pygame.image.load(f'{nombre}').convert_alpha()
    if color_key != None:
        imagen = pygame.transform.scale(imagen, (width, height))
        imagen.set_colorkey(color_key)
    else:
        imagen = pygame.transform.scale(imagen, (width, height))
    return imagen

def event_handling(event):
    global y_momentum, moviendo_derecha, moviendo_izquierda, current_jumping_form, jumping_form_y_start_pos, jumping_form_x_start_pos
    if event.key == K_RIGHT:
        if not collision_check( [ velocidad, 0 ], 'derecha' , wanna_fix = True):
            rect.x += velocidad
            moviendo_derecha = True
            moviendo_izquierda = False
            if rect.right >= screen_width:
                rect.right = screen_width
            else:
                if y_momentum == 0 and len(collision_check( [ 0 , velocidad ], 'abajo')) > 0:
                    if not current_form == 'running right':
                        reset_form('running right')
    elif event.key == K_LEFT:
        if not collision_check( [ -velocidad , 0 ] , 'izquierda' , wanna_fix = True):
            rect.x -= velocidad
            moviendo_derecha = False
            moviendo_izquierda = True
            if rect.left <= 0:
                rect.left = 0
            else:
                if y_momentum == 0 and len(collision_check( [ 0 , velocidad ], 'abajo')) > 0:
                    if not current_form == 'running left':
                        reset_form('running left')
    elif event.key == K_UP:
        if not modo_libre and y_momentum == 0: 
            colisionando_con_obstaculo_abajo = collision_check( [ 0 , velocidad ], 'abajo', wanna_fix = True)
            if colisionando_con_obstaculo_abajo:
                y_momentum += -20
                jumping_form_y_start_pos = rect.y
                jumping_form_x_start_pos = rect.x
                if moviendo_derecha:
                    reset_form('jumping right')
                elif moviendo_izquierda:
                    reset_form('jumping left')
                current_jumping_form = 0
        elif modo_libre:
            if not collision_check( [ 0 , -velocidad ] , 'arriba' , wanna_fix = True):
                rect.y -= velocidad
                if rect.top <= 0:
                    rect.top = 0
    elif event.key == K_DOWN:
        if modo_libre:
            if not collision_check( [ 0 , velocidad ] , 'abajo' , wanna_fix = True):
                rect.y += velocidad
                if rect.bottom >= screen_height:
                    rect.bottom = screen_height



def collision_check(movement, direccion, wanna_fix = False):
    rect.x      += movement[0]
    rect.y      += movement[1]
    if not wanna_fix:
        obstaculos  = []
    for obstaculo in cell_list:
        if direccion == 'derecha':
            if (obstaculo.colliderect(rect)) and (obstaculo.left <= rect.right) and (obstaculo.bottom+ rect.height >= obstaculo.top >= obstaculo.top - rect.height):
                if not wanna_fix:
                    obstaculos.append(obstaculo) 
                else:
                    rect.right = obstaculo.left
                    return True
        elif direccion == 'izquierda':
            if (obstaculo.colliderect(rect)) and (obstaculo.right  >= rect.left) and (obstaculo.bottom + rect.height >= obstaculo.top >= obstaculo.top - rect.height):
                if not wanna_fix:
                    obstaculos.append(obstaculo) 
                else:
                    rect.left = obstaculo.right
                    return True
        elif direccion == 'abajo':
            if (obstaculo.colliderect(rect)) and (obstaculo.top <= rect.bottom) and ( obstaculo.right + rect_width  >= obstaculo.left >= obstaculo.left - rect_width ):
                if not wanna_fix:
                    obstaculos.append(obstaculo) 
                else:
                    rect.bottom = obstaculo.top
                    return True
        elif direccion == 'arriba':
            if (obstaculo.colliderect(rect)) and (obstaculo.bottom >= rect.top) and (obstaculo.right + rect_width  >= obstaculo.left >= obstaculo.left - rect_width):
                if not wanna_fix:
                    obstaculos.append(obstaculo) 
                else:
                    rect.top = obstaculo.bottom
                    return True
    rect.x      -= movement[0]
    rect.y      -= movement[1]
    if not wanna_fix:
        return obstaculos
    else:
        return False



def check_y_momentum():
    global y_momentum
    if y_momentum < 20:
        y_momentum += 1
    else:
        y_momentum -= 1
    if not y_momentum == 0:
        hay_colisiones_abajo_al_aplicar_momentum_positivo = None
        hay_colisiones_arriba_al_aplicar_momentum_negativo = None
        if y_momentum > 0:
            hay_colisiones_abajo_al_aplicar_momentum_positivo  = collision_check( [ 0, y_momentum ], 'abajo', wanna_fix = True )
        elif y_momentum < 0:
            hay_colisiones_arriba_al_aplicar_momentum_negativo  = collision_check( [ 0, y_momentum ], 'arriba', wanna_fix = True )
        if (y_momentum > 0)  and (hay_colisiones_abajo_al_aplicar_momentum_positivo != None) and (not hay_colisiones_abajo_al_aplicar_momentum_positivo):
            rect.y += y_momentum
        else:
            if hay_colisiones_abajo_al_aplicar_momentum_positivo != None and hay_colisiones_abajo_al_aplicar_momentum_positivo:
                y_momentum = 0
                if 'jumping' in current_form:
                    if moviendo_derecha:
                        reset_form('stand right')
                    elif moviendo_izquierda:
                        reset_form('stand left')

            elif (y_momentum < 0) and  (not hay_colisiones_arriba_al_aplicar_momentum_negativo):
                rect.y += y_momentum
            else:
                collision_check( [ 0 , y_momentum ], 'arriba', wanna_fix = True )

def image_generator(direccion, jumping = False):
    forms = {
            'stand right'     : ['stand2.png'                                                                                                                               ], 
            'stand left'      : ['stand2_left.png'                                                                                                                          ], 
            'running right'   : ['running_right_1.png', 'running_right_2.png', 'running_right_3.png'                                                                        ], 
            'running left'    : ['running_left_1.png' , 'running_left_2.png' , 'running_left_3.png'                                                                         ], 
            'jumping right'   : ['jumping2_momentum_negativo.png', 'jumping2_momentum_positivo.png'                ],
            'jumping left'    : ['jumping2_momentum_negativo_left.png', 'jumping2_momentum_positivo_left.png' ],
            'stand right look': ['stand1.png'                                                                                                                               ], 
            'stand left look' : ['stand1_left.png'                                                                                                                          ], 
            }
    images = []
    for image in forms[direccion]:
        images.append( get_image_ready( 'megaman/' + image,player_width, player_height, ( 0, 0, 0 )   ) )
    return images

def reset_form(direccion):
    global current_form_iter, current_forms_list, current_form
    current_forms_list = image_generator(direccion)
    current_form_iter = 0
    current_form = direccion

class Laser:
    def __init__(self, rect, direccion):
        self.rect = rect
        self.direccion = direccion

def attack():
    global cantidad_de_disparos_derecha, cantidad_de_disparos_izquierda, lasers_list
    if moviendo_derecha:
        reset_form('stand right look')
        cantidad_de_disparos_derecha += 1
        if (cantidad_de_disparos_derecha%2 == 0):
            laser_rect = pygame.Rect( [ rect.right, rect.top + 10, 10,10 ] ) 
        else:
            laser_rect = pygame.Rect( [ rect.right, rect.top, 10,10 ] ) 
        lasers_list.append(Laser(laser_rect, 'derecha'))
    elif moviendo_izquierda:
        reset_form('stand left look')
        cantidad_de_disparos_izquierda += 1
        if cantidad_de_disparos_izquierda%2 == 0:
            laser_rect = pygame.Rect( [ rect.left, rect.top + 10, 10,10 ] ) 
        else:
            laser_rect = pygame.Rect( [ rect.left, rect.top, 10,10 ] ) 
        lasers_list.append(Laser(laser_rect, 'izquierda'))
    efecto_disparo()

def efecto_disparo():
    pygame.mixer.init()
    pygame.mixer.Sound('musica/laser.wav').play()

# -------  SCREEN ----
screen_width        = 1000
screen_height       = 750
background_color    = [ 0 , 0   , 0 ]
screen              = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Megaman')
pygame.display.set_icon(get_image_ready('megaman/stand1.png', 20,20,(0,0,0)))

# ------ PLAYER ----
player_width            = 50
player_height           = 60
moviendo_derecha        = True
moviendo_izquierda      = False
saltando                = False
controles_de_movimiento = {
        K_UP    : 'arriba',
        K_DOWN  : 'abajo', 
        K_RIGHT : 'derecha',
        K_LEFT  : 'izquierda'
        }
current_form            =  'jumping right'
current_forms_list      = image_generator(current_form)
current_form_iter       = 0
frames_iter             = 0
frames_per_image        = 3

# -------  RECT ----
rect_width       = player_width
rect_height      = player_height
rect             = pygame.Rect( [ 0, 0, rect_width, rect_height ] )
rect_color       = [ 0 , 255 , 0 ]
velocidad        = 4
y_momentum       = 0

# ----- MAPA -----
blocks_width    = 20
blocks_height   = 20
dirt_img        = get_image_ready('platform/dirt.png' , blocks_width, blocks_height)
grass_img       = get_image_ready('platform/grass.png', blocks_width, blocks_height)
game_map        = load_map()
cell_list       = []

# ----- OTROS -----
salir               = False
tecla_pulsada       = False
ultimo_evento       = None
modo_libre          = False
fps                 = pygame.time.Clock()
second_rect_scroll  = rect.y//20 + 100
other_images        = []

# ------ LASER --- 
attack_key                     = ' ' 
lasers_list                    = []
laser_velocity                 = 20
cantidad_de_disparos_derecha   = 0
cantidad_de_disparos_izquierda = 0
laser_width                    = 20
laser_height                   = 10
laser_form                     = get_image_ready('laser.png', laser_width, laser_height, ( 255 , 255 , 255))

# ---- SONIDOS DE FONDO ---
pygame.mixer.music.load('musica/megaman_fondo.wav')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(loops = 100)

# --- JUMP EFECT ---
current_jumping_form = -1
jumping_right_form_list = []
jumping_left_form_list = []
for i in range(1,7):
    jumping_right_form_list.append(get_image_ready(f'estela/right/{i}.png', i+5*10, i+5*10, alpha_activated = True))
for i in range(1,7):
    jumping_left_form_list.append(get_image_ready(f'estela/left/{i}.png', i+5*10, i+5*10, alpha_activated = True))
jumping_form_max_frame = 3
jumping_form_current_frame = 0
jumping_form_y_start_pos = None
jumping_form_x_start_pos = None
jumping_form_list = None

# ----- TORCH ---
torch_list = []
for i in range(1,10):
    imagen = get_image_ready(f'antorcha_2/{i}.png', 20,30).convert_alpha()
    torch_list.append(imagen)
current_torch_form = 0
frames_per_torch = 5
current_torch_frame = 0



while not salir:
    screen.fill(background_color)
    print_map(screen)
    if not modo_libre:
        check_y_momentum()
    screen.blit(current_forms_list[current_form_iter], rect)


    # ---- PLAYER FORM CHECK
    frames_iter += 1
    if frames_iter == frames_per_image:
        current_form_iter += 1
        frames_iter = 0
        if current_form_iter > len(current_forms_list)-1:
            current_form_iter = 0

    if 'jumping' in current_form:
        if y_momentum < 0:
            current_form_iter = 0
        elif y_momentum > 0:
            current_form_iter = 1

    if 'running' in current_form:
        if moviendo_derecha:
            if not rect.right + velocidad//2 > screen_width:
                if not collision_check( [ velocidad//2 , 0 ], 'derecha', wanna_fix = True ):
                    rect.x += velocidad//2
                else:
                    reset_form('stand right')
            else:
                rect.right = screen_width
                reset_form('stand right')
        elif moviendo_izquierda:
            if not rect.left - velocidad//2 < 0:
                if not collision_check( [ -velocidad//2 , 0 ], 'izquierda', wanna_fix = True ):
                    rect.x -= velocidad//2
                else:
                    reset_form('stand left')
            else:
                rect.left = 0 
                reset_form('stand left')

    # ---- ATTACKS CHECK
    for laser in lasers_list:
        if laser.direccion == 'derecha':
            laser.rect.x += laser_velocity
            if laser.rect.left > screen_width:
                lasers_list.remove(laser)
            else:
                screen.blit(laser_form, laser.rect)
        elif laser.direccion == 'izquierda':
            laser.rect.x -= laser_velocity
            if laser.rect.right < 0:
                lasers_list.remove(laser)
            else:
                screen.blit(laser_form, laser.rect)

    for event in pygame.event.get():
        if event.type == QUIT:
            salir = True
        elif event.type == KEYDOWN: 
            tecla_pulsada = True
            ultimo_evento = event
            if event.key in controles_de_movimiento:
                event_handling(event)
            elif (event.unicode.lower() == attack_key) and ('stand' in current_form):
                attack()
            elif event.key == 27:
                salir = True
        elif event.type == KEYUP and event.key == ultimo_evento.key:
            tecla_pulsada = False
            if (current_form == 'stand right look' or current_form == 'stand left look') and (event.unicode.lower() == attack_key) or ('running' in current_form):
                if moviendo_derecha:
                    reset_form('stand right')
                elif moviendo_izquierda:
                    reset_form('stand left')
    if tecla_pulsada:
        if ultimo_evento.key in controles_de_movimiento:
            event_handling(ultimo_evento)


# ---------- JUMPING EFECT CHECK
    if (y_momentum > -20) and  ('jumping' in current_form) and current_jumping_form != -1:
        if current_jumping_form >= 0:
            if jumping_form_list == None:
                jumping_form_list = jumping_left_form_list if moviendo_derecha else jumping_right_form_list
            if not current_jumping_form > len(jumping_form_list)-1:
                screen.blit(jumping_form_list[current_jumping_form], (jumping_form_x_start_pos+20 if moviendo_izquierda else jumping_form_x_start_pos-20, jumping_form_y_start_pos + (jumping_form_y_start_pos - rect.y)))
                if jumping_form_current_frame == jumping_form_max_frame:
                    current_jumping_form += 1
                    jumping_form_current_frame = 0
                else:
                    jumping_form_current_frame += 1
            else:
                current_jumping_form = -1
                jumping_form_y_pos = None
                jumping_form_list = None


    pygame.display.update()
    fps.tick(50)

pygame.quit()
