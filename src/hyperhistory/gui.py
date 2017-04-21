import pygame
from main.constants import ARRIBA, ABAJO, IZQUIERDA, DERECHA, RESOLUTION1, RESOLUTION2
from resources.images import Images
import thread

class Gui:
    def __init__(self, ventana, resolucion):
        self.ventana = ventana
        self.__resolucion = resolucion
        #Creo una superficie donde almacenar la habitacion actual
        self.__sup_hab_actual = pygame.Surface(self.__resolucion)
        #Propiedades que utilizo para la animacion de puerta y/o ascensor
        self.__anim_image1 = ""
        self.__anim_image2 = ""
        self.__mostrar_puerta_seleccionada = True
        self.__ejecutar_animacion = True
        self.__obj_animation_type = ""
        self.__navegation = Navegation(self.ventana,resolucion)

    def get_current_room_surface(self):
        return self.__sup_hab_actual

    def refresh_room(self):
        self.ventana.blit(self.__sup_hab_actual, (0,0))
        #pygame.display.update()

    def __show_logo(self):
        imagen = Images.get_images_file_names(self.__resolucion, "etc")["logo"]
        self.__sup_hab_actual.blit(pygame.image.load(imagen['archivo']).convert_alpha(), (120,200))

    def show_room(self, habitacion):
        self.__render_room(habitacion)
        if habitacion.get_name() == 'entrada':
            self.__show_logo()
        self.ventana.blit(self.__sup_hab_actual, (0,0))
        #pygame.display.update()

    def show_character(self, personaje):
        imagen = Images.get_images_file_names(self.__resolucion, "personajes")[personaje.get_name()]
        self.__sup_hab_actual.blit(pygame.image.load(imagen['archivo']).convert_alpha(), imagen['pos_xy_f'])
        self.ventana.blit(self.__sup_hab_actual, (0,0))
        #pygame.display.update()

    def __render_room(self, habitacion, extra=""):
        archivo_imagen = Images.get_images_file_names(self.__resolucion, "habitaciones")[habitacion.get_name()]
        self.__sup_hab_actual.blit(pygame.image.load(archivo_imagen).convert(), (0,0))
        #Copio la imagen del personaje si no es piso la nueva habitacion y tiene un personaje asociado
        if not habitacion.is_floor():
            personaje = habitacion.get_owner()
            if personaje != "":
                imagen = Images.get_images_file_names(self.__resolucion, "personajes")[personaje.get_name()]
                self.__sup_hab_actual.blit(pygame.image.load(imagen['archivo']).convert_alpha(), imagen['pos_xy'])
        else:
            #Colocar las puertas y el ascensor
            #ASCENSOR
            imagen_as = Images.get_images_file_names(self.__resolucion, "puertas")["ascensor"]
            imagen_as_botones = Images.get_images_file_names(self.__resolucion, "etc")["asc_botones"]
            self.__sup_hab_actual.blit(pygame.image.load(imagen_as['archivo']).convert_alpha(), imagen_as['pos_xy'])
            self.__sup_hab_actual.blit(pygame.image.load(imagen_as_botones['archivo']).convert_alpha(), imagen_as_botones['pos_xy'])
            #PUERTAS
            if habitacion.get_left_room() != "":
                hab_izq = habitacion.get_left_room().get_name()
                imagen_puerta1 = Images.get_images_file_names(self.__resolucion, "puertas")[hab_izq]
                self.__sup_hab_actual.blit(pygame.image.load(imagen_puerta1['archivo']).convert_alpha(), imagen_puerta1['pos_xy'])
            if habitacion.get_right_room() != "":
                hab_der = habitacion.get_right_room().get_name()
                imagen_puerta2 = Images.get_images_file_names(self.__resolucion, "puertas")[hab_der]
                self.__sup_hab_actual.blit(pygame.image.load(imagen_puerta2['archivo']).convert_alpha(), imagen_puerta2['pos_xy'])
        if extra == "introduccion":
            #Muestro a Pablo Gris en el nuevo piso (1er piso)
            imagen = Images.get_images_file_names(self.__resolucion, "personajes")["pablo gris"]
            self.__sup_hab_actual.blit(pygame.image.load(imagen['archivo']).convert_alpha(), imagen['pos_xy_f'])
        elif extra == "presentacion_sofia":
            #Muestro a Sofia Dulce en la nueva habitacion (2do piso)
            imagen = Images.get_images_file_names(self.__resolucion, "personajes")["sofia dulce"]
            self.__sup_hab_actual.blit(pygame.image.load(imagen['archivo']).convert_alpha(), imagen['pos_xy_f'])
        elif extra == "final_juego":
            #Muestro a todos los personajes en el pasillo para el final del juego
            imagen_sofia = Images.get_images_file_names(self.__resolucion, "personajes")["sofia dulce"]
            imagen_don_cano = Images.get_images_file_names(self.__resolucion, "personajes")["don cano"]
            imagen_protasio = Images.get_images_file_names(self.__resolucion, "personajes")["protasio"]
            imagen_pablo_gris = Images.get_images_file_names(self.__resolucion, "personajes")["pablo gris"]
            imagen_pedro_madera = Images.get_images_file_names(self.__resolucion, "personajes")["pedro madera"]
            self.__sup_hab_actual.blit(pygame.image.load(imagen_don_cano['archivo']).convert_alpha(), imagen_don_cano['pos_xy_end'])
            self.__sup_hab_actual.blit(pygame.image.load(imagen_protasio['archivo']).convert_alpha(), imagen_protasio['pos_xy_end'])
            self.__sup_hab_actual.blit(pygame.image.load(imagen_pablo_gris['archivo']).convert_alpha(), imagen_pablo_gris['pos_xy_end'])
            self.__sup_hab_actual.blit(pygame.image.load(imagen_pedro_madera['archivo']).convert_alpha(), imagen_pedro_madera['pos_xy_end'])
            self.__sup_hab_actual.blit(pygame.image.load(imagen_sofia['archivo']).convert_alpha(), imagen_sofia['pos_xy_end'])

    def __animation_thread_running(self):
        if self.__anim_image1 == "" and self.__anim_image2 == "":
            return False
        else:
            return True

    def launch_door_animation(self,extra=""):
        try:
            self.__ejecutar_animacion = True
            thread.start_new_thread(self.__do_door_animation,(extra,))
        except Exception, e:
            print e
            raise Exception ("Ocurrio un problema en el hilo de animacion de puertas")

    def end_door_animation(self):
        if self.__ejecutar_animacion:
            self.__ejecutar_animacion = False
            pygame.time.wait(100)
            self.ventana.blit(self.__sup_hab_actual, (0,0))
            self.__anim_image1 = ""
            self.__anim_image2 = ""

    def pause_door_animation(self):
        self.__ejecutar_animacion = False
        pygame.time.wait(50)

    def select_animation(self, obj):
        hay_animacion = self.__animation_thread_running()
        self.__obj_animation_type = obj['tipo']
        if self.__obj_animation_type == 'habitacion':
            nombre_hab = obj['habitacion'].get_name()
            self.__anim_image1 = Images.get_images_file_names(self.__resolucion, "puertas")[nombre_hab+" sel"]
            self.__anim_image2 = Images.get_images_file_names(self.__resolucion, "puertas")[nombre_hab]
            self.ventana.blit(self.__sup_hab_actual, (0,0))
            if not hay_animacion:
                self.launch_door_animation()
        elif self.__obj_animation_type == 'ascensor':
            self.__anim_image1 = Images.get_images_file_names(self.__resolucion, "puertas")["ascensor"]
            self.__anim_image1_1 = Images.get_images_file_names(self.__resolucion, "etc")["asc_botones"]
            self.__anim_image2_1 = Images.get_images_file_names(self.__resolucion, "etc")["asc_botones_sel"]
            if obj['direccion'] == ARRIBA:
                self.__anim_image2 = Images.get_images_file_names(self.__resolucion, "puertas")["asc_subida"]
            elif obj['direccion'] == ABAJO:
                self.__anim_image2 = Images.get_images_file_names(self.__resolucion, "puertas")["asc_bajada"]
            else:
                print "El ascensor tiene una direccion desconocida"
            self.ventana.blit(self.__sup_hab_actual, (0,0))
            if not hay_animacion:
                self.launch_door_animation()
        else:
            raise Exception("Objeto de animacion desconocido! (Class Video)")

    def __run_extra(self, extra):
        for f in extra:
            f["nombre"](f["parametros"])

    def __do_door_animation(self, extra=""):
        while self.__ejecutar_animacion:
            if self.__mostrar_puerta_seleccionada:
                self.ventana.blit(pygame.image.load(self.__anim_image1['archivo']).convert_alpha(), self.__anim_image1['pos_xy'])
                if self.__obj_animation_type == 'ascensor':
                    self.ventana.blit(pygame.image.load(self.__anim_image1_1['archivo']).convert_alpha(), self.__anim_image1_1['pos_xy'])
                self.__mostrar_puerta_seleccionada = False
            else:
                self.ventana.blit(pygame.image.load(self.__anim_image2['archivo']).convert_alpha(), self.__anim_image2['pos_xy'])
                if self.__obj_animation_type == 'ascensor':
                    self.ventana.blit(pygame.image.load(self.__anim_image2_1['archivo']).convert_alpha(), self.__anim_image2_1['pos_xy'])
                self.__mostrar_puerta_seleccionada = True
            if extra != "":
                text_box = extra[0]
                up_text_box = text_box.is_up()
                if up_text_box:
                    text_box.refresh_text_box(self.ventana)
                    #dim_text_box = text_box.get_final_position()
                    #update_rect = pygame.Rect((0, 0), (self.ventana.get_width(), dim_text_box[1]+10))
                    #pygame.display.update(update_rect)
            #self.__run_extra(extra)
            pygame.display.update()
            pygame.time.wait(200)

    def move_to_another_room(self, hab_nueva, direccion, extra=""):
        s_hab_vieja = self.__sup_hab_actual.copy()
        self.__render_room(hab_nueva, extra)
        s_hab_nueva = self.__sup_hab_actual.copy()
        self.__navegation.move_to_room(s_hab_vieja, s_hab_nueva, direccion)

    def move_to_another_floor(self, piso_nuevo, direccion, extra=""):
        s_piso_viejo = self.__sup_hab_actual.copy()
        self.__render_room(piso_nuevo,extra)
        s_piso_nuevo = self.__sup_hab_actual.copy()
        self.__navegation.move_to_floor(s_piso_viejo, s_piso_nuevo, direccion)

class Navegation:
    def __init__(self, ventana="", resolucion=RESOLUTION1):
        self.__resolucion = resolucion
        if ventana == "":
            raise Exception ("Error!, la navegacion del club no se puede instanciar sin una ventana (Navegation Class)")
        self.__ventana = ventana
        #Propiedades para la animacion al pasar de piso y habitacion
        self.__xs = ""
        self.__ys = ""

    def __init_params_animation_move_room(self):
        if self.__resolucion == RESOLUTION1:
            self.__velocidad_anim = 600.
            self.__xs = {'izquierda' : {'x1' : -900., 'x2' : 0, 'x3' : -100.},
                         'derecha' : {'x1' : 900., 'x2' : 0, 'x3' : 800.}}
            self.__x_black_sprite = 100
        elif self.__resolucion == RESOLUTION2:
            self.__velocidad_anim = 600.
            self.__xs = {'izquierda' : {'x1' : -1350., 'x2' : 0, 'x3' : -150.},
                         'derecha' : {'x1' : 1350., 'x2' : 0, 'x3' : 1200.}}
            self.__x_black_sprite = 150

    def move_to_room(self, hab_actual, hab_nueva, direccion):
        if self.__xs == "":
            self.__init_params_animation_move_room()
        black_sprite = pygame.Surface((self.__x_black_sprite,self.__resolucion[1]))
        main_sprite = pygame.Surface((self.__resolucion[0],self.__resolucion[1]))
        if direccion == IZQUIERDA:
            self.__move_to_left_room(hab_actual, hab_nueva, black_sprite, main_sprite)
        elif direccion == DERECHA:
            self.__move_to_right_room(hab_actual, hab_nueva, black_sprite, main_sprite)

    def __move_to_left_room(self, sprite_hab_vieja, sprite_hab_nueva, sprite_black, main_sprite):
        x1, x2, x3 = self.__xs['izquierda']['x1'], self.__xs['izquierda']['x2'], self.__xs['izquierda']['x3']
        reloj = pygame.time.Clock()
        while x1 <= 0:
            x1_anterior = x1
            main_sprite.blit(sprite_hab_nueva, (x1,0))
            main_sprite.blit(sprite_black, (x3,0))
            main_sprite.blit(sprite_hab_vieja, (x2,0))
            tiempo_pasado = reloj.tick(10)
            tiempo_pasado_segundos = tiempo_pasado / 1000.0
            distancia = tiempo_pasado_segundos * self.__velocidad_anim
            x1 += distancia
            x2 += distancia
            x3 += distancia
            if x1_anterior < 0 and x1 > 0:
                x1 = 0
            self.__ventana.blit(main_sprite, (0,0))
            pygame.display.update()

    def __move_to_right_room(self, sprite_hab_vieja, sprite_hab_nueva, sprite_black, main_sprite):
        x1, x3, x2 = self.__xs['derecha']['x1'], self.__xs['derecha']['x3'], self.__xs['derecha']['x2']
        reloj = pygame.time.Clock()
        while x1 >= 0:
            x1_anterior = x1
            main_sprite.blit(sprite_hab_nueva, (x1,0))
            main_sprite.blit(sprite_black, (x3,0))
            main_sprite.blit(sprite_hab_vieja, (x2,0))
            tiempo_pasado = reloj.tick(10)
            tiempo_pasado_segundos = tiempo_pasado / 1000.0
            distancia = tiempo_pasado_segundos * self.__velocidad_anim
            x1 = x1 - distancia
            x2 = x2 - distancia
            x3 = x3 - distancia
            if x1_anterior > 0 and x1 < 0:
                x1 = 0
            self.__ventana.blit(main_sprite, (0,0))
            pygame.display.update()

    def __init_params_animation_move_floor(self):
        if self.__resolucion == RESOLUTION1:
            self.__velocidad_anim = 600.
            self.__ys = {'arriba' : {'y1' : -700., 'y2' : 0, 'y3' : -100.},
                         'abajo' : {'y1' : 700., 'y2' : 0, 'y3' : 600.}}
            self.__y_black_sprite = 100
        elif self.__resolucion == RESOLUTION2:
            self.__velocidad_anim = 600.
            self.__ys = {'arriba' : {'y1' : -1050., 'y2' : 0, 'y3' : -150.},
                         'abajo' : {'y1' : 1050., 'y2' : 0, 'y3' : 900.}}
            self.__y_black_sprite = 150

    def move_to_floor(self, piso_actual, piso_nuevo, direccion):
        if self.__ys == "":
            self.__init_params_animation_move_floor()
        black_sprite = pygame.Surface((self.__resolucion[0],150))
        main_sprite = pygame.Surface((self.__resolucion[0],self.__resolucion[1]))
        if direccion == ARRIBA:
            self.__move_to_up_floor(piso_nuevo, piso_actual, black_sprite, main_sprite)
        else:
            self.__move_to_down_floor(piso_nuevo, piso_actual, black_sprite, main_sprite)

    def __move_to_up_floor(self, pn_sprite, pv_sprite, b_sprite, m_sprite):
        y1 = self.__ys['arriba']['y1']
        y2 = self.__ys['arriba']['y2']
        y3 = self.__ys['arriba']['y3']
        reloj = pygame.time.Clock()
        while y1 <= 0:
            y1_anterior = y1
            m_sprite.blit(pn_sprite, (0,y1))
            m_sprite.blit(b_sprite, (0,y3))
            m_sprite.blit(pv_sprite, (0,y2))
            tiempo_pasado = reloj.tick(10)
            tiempo_pasado_segundos = tiempo_pasado / 1000.0
            distancia = tiempo_pasado_segundos * self.__velocidad_anim
            y1 = y1 + distancia
            y2 = y2 + distancia
            y3 = y3 + distancia
            if y1_anterior < 0 and y1 > 0:
                y1 = 0
            self.__ventana.blit(m_sprite, (0,0))
            pygame.display.update()

    def __move_to_down_floor(self, pn_sprite, pv_sprite, b_sprite, m_sprite):
        y1 = self.__ys['abajo']['y1']
        y2 = self.__ys['abajo']['y2']
        y3 = self.__ys['abajo']['y3']
        reloj = pygame.time.Clock()
        while y1 >= 0:
            y1_anterior = y1
            m_sprite.blit(pn_sprite, (0,y1))
            m_sprite.blit(b_sprite, (0,y3))
            m_sprite.blit(pv_sprite, (0,y2))
            tiempo_pasado = reloj.tick(10)
            tiempo_pasado_segundos = tiempo_pasado / 1000.0
            distancia = tiempo_pasado_segundos * self.__velocidad_anim
            y1 = y1 - distancia
            y2 = y2 - distancia
            y3 = y3 - distancia
            if y1_anterior > 0 and y1 < 0:
                y1 = 0
            self.__ventana.blit(m_sprite, (0,0))
            pygame.display.update()
