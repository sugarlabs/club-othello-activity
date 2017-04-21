# -*- coding: utf-8 -*-
import pygame
from pygame.locals import SRCALPHA
from main.constants import RESOLUTION1, RESOLUTION2, ARRIBA, ABAJO, BRONZE, PLATA, ORO, MARFIL, MADERA
from hyperhistory.gui import Gui
from resources.images import Images
from resources.fonts import Fonts
from othello.gui import GraphicBoard, Score
from othello.board import BLANCO
from othello.utils import Coordinate, get_number_word
from othello.referee import Referee
from othello.player import HUMANO
import thread, string, logging, pyfestival

log = logging.getLogger( 'src.input_output.video' )
log.setLevel( logging.DEBUG )


class Video():
    def __init__(self, engine="", titulo_ventana="Club de Othello"):
        try:
            pygame.init()
            #Averiguo la resolucion necesario para crear la ventana
            self.__resolucion = self.__get_initial_resolution()
            #Creo la ventana
            self.ventana = pygame.display.set_mode(self.__resolucion, 0, 32)
            #Coloco el titulo a la ventana
            pygame.display.set_caption(titulo_ventana)
            pygame.mouse.set_visible(False)
            self.club = Gui(self.ventana,self.__resolucion)
            self.board = ""
            self.text_box = TextBox(self.__resolucion)
            self.__init_animation_values()
            self.marcador = Score(self.__resolucion)
            self.__tablero_arriba = False
            self.__marcador_visible = False
        except pygame.error, e:
            raise Exception("ERROR! al inicilizar el video. La aplicacion se cerrara\n"+str(e))

    def __get_initial_resolution(self):
        maxima_resolucion = pygame.display.list_modes()[0]
        if maxima_resolucion[0] >= RESOLUTION2[0] and maxima_resolucion[1] >= RESOLUTION2[1]:
            return RESOLUTION2
        else:
            return RESOLUTION1

    def get_resolution(self):
        return self.__resolucion

    def set_window_background(self, imagen):
        self.__window_background.blit(imagen,(0,0))

    def refresh_window(self, area=""):
        if area == "":
            pygame.display.update()
        else:
            pygame.display.update(area)

    def __init_animation_values(self):
        if self.__resolucion == RESOLUTION1:
            self.__vel_anim_tablero = 600.
            self.__vel_anim_score = 500.
            self.__vel_anim_medals = 500.
        elif self.__resolucion == RESOLUTION2:
            self.__vel_anim_tablero = 800.
            self.__vel_anim_score = 700.
            self.__vel_anim_medals = 1000.
        else:
            raise Exception("Error!, resolucion desconocida (Video Class)")

    def __do_set_up_game_elements(self, juego):
        self.board.render_configuration(self.ventana)
        if juego.with_possibles_moves():
            self.board.lista_jugadas = Referee.possibles_moves(juego.get_turn().get_color(),self.board.get_logical_board())
            self.board.render_list_possible_moves(self.ventana)
        self.show_board(con_configuracion=True)
        self.show_scores(juego.get_turn().get_color())
        self.board.set_coord_selected_cell(Coordinate(1,1))
        if self.board.animation_cell_running():
            self.board.end_animation_cell()
        thread.start_new_thread(self.board.render_animation_cell,(self.ventana,))

    def init_game_elements(self, juego, audio):
        self.__do_set_up_game_elements(juego)
        audio.play_voice_sound("game", "inicio", {'grupo_sonido':'inicio_turno'})
        dim_tablero = self.board.get_logical_board().get_dimension()
        audio.play_board_size_sound(dim_tablero)
        audio.play_init_turn_sounds(self.board,juego)

    def init_leason_elements(self, juego, audio):
        self.__do_set_up_game_elements(juego)
        audio.play_voice_sound("game", "inicio_leccion", {'grupo_sonido':'inicio_turno'})
        dim_tablero = self.board.get_logical_board().get_dimension()
        audio.play_board_size_sound(dim_tablero)

    def init_challenge_elements(self, nombre_desafio, juego, audio):
        self.__do_set_up_game_elements(juego)
        audio.play_voice_sound("game", "exp_"+str(nombre_desafio), {'grupo_sonido':'inicio_turno'})
        audio.play_voice_sound("game", "inicio_desafio", {'grupo_sonido':'inicio_turno'})
        dim_tablero = self.board.get_logical_board().get_dimension()
        audio.play_board_size_sound(dim_tablero)

    def create_graphic_board(self, logical_board=""):
        try:
            self.board.end_animation_cell()
            self.board = GraphicBoard(tablero_logico=logical_board,resolucion=self.__resolucion)
            self.text_box.set_up_graphic_board(self.board)
        except:
            self.board = GraphicBoard(tablero_logico=logical_board,resolucion=self.__resolucion)
            self.text_box.set_up_graphic_board(self.board)

    def create_selection_list(self, titulo="", tipo=""):
        self.selection_list = SelectionList(self.__resolucion, self.ventana, titulo, tipo)

    def show_selection_list(self):
        self.selection_list.draw()
        list_sup = self.selection_list.render_options()
        self.ventana.blit(list_sup,self.selection_list.get_screen_position())
        if not self.board == "":
            self.board.set_up_image({'imagen':list_sup, 'posicion':self.selection_list.get_screen_position()})
        pygame.display.update()

    def remove_selection_list(self):
        self.selection_list.remove()
        if not self.board == "":
            self.board.remove_up_images()

    def show_medal(self, medalla):
        na_imagenes_medallas = Images.get_images_file_names(self.__resolucion, "medallas")
        if medalla == ORO:
            imagen_medalla = pygame.image.load(na_imagenes_medallas["oro"]["archivo"]).convert_alpha()
            pos_final_medalla = na_imagenes_medallas["oro"]["pos_xy"]
        elif medalla == PLATA:
            imagen_medalla= pygame.image.load(na_imagenes_medallas["plata"]["archivo"]).convert_alpha()
            pos_final_medalla = na_imagenes_medallas["plata"]["pos_xy"]
        elif medalla == BRONZE:
            imagen_medalla= pygame.image.load(na_imagenes_medallas["bronze"]["archivo"]).convert_alpha()
            pos_final_medalla = na_imagenes_medallas["bronze"]["pos_xy"]
        update_rect = pygame.Rect((pos_final_medalla[0], 0), (imagen_medalla.get_width(), pos_final_medalla[1]+imagen_medalla.get_height()))
        velocidad = self.__vel_anim_medals
        reloj = pygame.time.Clock()
        y_max = pos_final_medalla[1]
        y = -imagen_medalla.get_height()
        while y < y_max:
            y_anterior = y
            tiempo_pasado = reloj.tick()
            tiempo_pasado_segundos = tiempo_pasado / 1000.0
            distancia = tiempo_pasado_segundos * velocidad
            y = y + distancia  #distancia
            if y_anterior < y_max and y > y_max:
                y = y_max
            self.ventana.blit(self.club.get_current_room_surface(), update_rect, update_rect)
            self.ventana.blit(imagen_medalla, (pos_final_medalla[0], y))
            pygame.display.update(update_rect)

    def dissapear_medal(self, medalla):
        na_imagenes_medallas = Images.get_images_file_names(self.__resolucion, "medallas")
        if medalla == ORO:
            imagen_medalla = pygame.image.load(na_imagenes_medallas["oro"]["archivo"]).convert_alpha()
            pos_inicial_medalla = na_imagenes_medallas["oro"]["pos_xy"]
        elif medalla == PLATA:
            imagen_medalla= pygame.image.load(na_imagenes_medallas["plata"]["archivo"]).convert_alpha()
            pos_inicial_medalla = na_imagenes_medallas["plata"]["pos_xy"]
        elif medalla == BRONZE:
            imagen_medalla= pygame.image.load(na_imagenes_medallas["bronze"]["archivo"]).convert_alpha()
            pos_inicial_medalla = na_imagenes_medallas["bronze"]["pos_xy"]
        update_rect = pygame.Rect((pos_inicial_medalla[0], 0), (imagen_medalla.get_width(), pos_inicial_medalla[1]+imagen_medalla.get_height()))
        velocidad = self.__vel_anim_medals
        reloj = pygame.time.Clock()
        y_max = -imagen_medalla.get_height()
        y = pos_inicial_medalla[1]
        while y > y_max:
            y_anterior = y
            tiempo_pasado = reloj.tick()
            tiempo_pasado_segundos = tiempo_pasado / 1000.0
            distancia = tiempo_pasado_segundos * velocidad
            y = y - distancia  #distancia
            if y_anterior < y_max and y > y_max:
                y = y_max
            self.ventana.blit(self.club.get_current_room_surface(), update_rect, update_rect)
            self.ventana.blit(imagen_medalla, (pos_inicial_medalla[0], y))
            pygame.display.update(update_rect)

    def show_trophy(self, trofeo):
        na_imagenes_trofeos = Images.get_images_file_names(self.__resolucion, "trofeos")
        if trofeo == ORO:
            imagen_trofeo = pygame.image.load(na_imagenes_trofeos["oro"]["archivo"]).convert_alpha()
            pos_final_trofeo = na_imagenes_trofeos["oro"]["pos_xy"]
        elif trofeo == MARFIL:
            imagen_trofeo= pygame.image.load(na_imagenes_trofeos["marfil"]["archivo"]).convert_alpha()
            pos_final_trofeo = na_imagenes_trofeos["marfil"]["pos_xy"]
        elif trofeo == MADERA:
            imagen_trofeo= pygame.image.load(na_imagenes_trofeos["madera"]["archivo"]).convert_alpha()
            pos_final_trofeo = na_imagenes_trofeos["madera"]["pos_xy"]
        update_rect = pygame.Rect((pos_final_trofeo[0], 0), (imagen_trofeo.get_width(), pos_final_trofeo[1]+imagen_trofeo.get_height()))
        velocidad = self.__vel_anim_medals
        reloj = pygame.time.Clock()
        y_max = pos_final_trofeo[1]
        y = -imagen_trofeo.get_height()
        while y < y_max:
            y_anterior = y
            tiempo_pasado = reloj.tick()
            tiempo_pasado_segundos = tiempo_pasado / 1000.0
            distancia = tiempo_pasado_segundos * velocidad
            y = y + distancia  #distancia
            if y_anterior < y_max and y > y_max:
                y = y_max
            self.ventana.blit(self.club.get_current_room_surface(), update_rect, update_rect)
            self.ventana.blit(imagen_trofeo, (pos_final_trofeo[0], y))
            pygame.display.update(update_rect)

    def dissapear_trophy(self, trofeo):
        na_imagenes_trofeos = Images.get_images_file_names(self.__resolucion, "trofeos")
        if trofeo == ORO:
            imagen_trofeo = pygame.image.load(na_imagenes_trofeos["oro"]["archivo"]).convert_alpha()
            pos_final_trofeo = na_imagenes_trofeos["oro"]["pos_xy"]
        elif trofeo == MARFIL:
            imagen_trofeo= pygame.image.load(na_imagenes_trofeos["marfil"]["archivo"]).convert_alpha()
            pos_final_trofeo = na_imagenes_trofeos["marfil"]["pos_xy"]
        elif trofeo == MADERA:
            imagen_trofeo= pygame.image.load(na_imagenes_trofeos["madera"]["archivo"]).convert_alpha()
            pos_final_trofeo = na_imagenes_trofeos["madera"]["pos_xy"]
        update_rect = pygame.Rect((pos_final_trofeo[0], 0), (imagen_trofeo.get_width(), pos_final_trofeo[1]+imagen_trofeo.get_height()))
        velocidad = self.__vel_anim_medals
        reloj = pygame.time.Clock()
        y_max = -imagen_trofeo.get_height()
        y = pos_final_trofeo[1]
        while y > y_max:
            y_anterior = y
            tiempo_pasado = reloj.tick()
            tiempo_pasado_segundos = tiempo_pasado / 1000.0
            distancia = tiempo_pasado_segundos * velocidad
            y = y - distancia  #distancia
            if y_anterior < y_max and y > y_max:
                y = y_max
            self.ventana.blit(self.club.get_current_room_surface(), update_rect, update_rect)
            self.ventana.blit(imagen_trofeo, (pos_final_trofeo[0], y))
            pygame.display.update(update_rect)

    def show_board(self, con_configuracion=False):
        self.__x_board = self.board.get_board_pos().x
        if not self.__tablero_arriba:
            self.__do_board_animation_show(configuracion=con_configuracion)
            self.__tablero_arriba = True
        else:
            tablero_sup = self.board.render()
            if con_configuracion:
                conf_sup = self.board.get_configuration_surface()
            update_rect = pygame.Rect((self.__x_board, 0), (tablero_sup.get_width(), tablero_sup.get_height()))
            self.ventana.blit(tablero_sup, (self.__x_board, 0))
            self.ventana.blit(conf_sup, (self.__x_board, 0))
            pygame.display.update(update_rect)

    def dissapear_board(self):
        if self.__tablero_arriba:
            self.__tablero_arriba = False
            self.board.end_animation_cell()
            self.__do_board_animation_show(factor=-1, configuracion=True)

    def show_scores(self, turno=BLANCO):
        if not self.__marcador_visible:
            self.__fondo = self.ventana.copy()
            self.__do_score_animation_show(turno=turno)
            self.__marcador_visible = True
        else:
            marcador_der = self.marcador.render_right_score(self.board.get_logical_board(), turno)
            marcador_izq = self.marcador.render_left_score(self.board.get_logical_board(), turno)
            x1 = self.__resolucion[0] - marcador_der.get_width()
            x2 = marcador_izq.get_width()
            y2 = marcador_izq.get_height()
            update_rect_izq = pygame.Rect((0, 0), (x2, y2))
            update_rect_der = pygame.Rect((x1, 0), (x2, y2))
            xi = 0
            xd = self.__resolucion[0] - marcador_der.get_width()
            self.ventana.blit(marcador_izq, (xi, 0))
            self.ventana.blit(marcador_der, (xd, 0))
            if self.text_box.up:
                self.text_box.refresh_text_box(self.ventana)
            pygame.display.update([update_rect_izq,update_rect_der])

    def dissapear_scores(self):
        if self.__marcador_visible:
            self.__marcador_visible = False
            self.__do_score_animation_show(factor=-1)

    def dissapear_game_elements(self):
        self.dissapear_board()
        self.dissapear_scores()

    def __do_score_animation_show(self, turno=BLANCO, factor=1):
        marcador_der = self.marcador.render_right_score(self.board.get_logical_board(), turno)
        marcador_izq = self.marcador.render_left_score(self.board.get_logical_board(), turno)
        x1 = self.__resolucion[0] - marcador_der.get_width()
        x2 = marcador_izq.get_width()
        y2 = marcador_izq.get_height()
        update_rect_izq = pygame.Rect((0, 0), (x2, y2))
        update_rect_der = pygame.Rect((x1, 0), (x2, y2))
        velocidad = self.__vel_anim_score
        reloj = pygame.time.Clock()
        if factor > 0:
            xi = -marcador_izq.get_width()
            xd = self.__resolucion[0]
            xi_max = 0
            xd_max = self.__resolucion[0] - marcador_der.get_width()
        else:
            xi = 0
            xd = self.__resolucion[0] - marcador_der.get_width()
            xi_max = -marcador_izq.get_width()
            xd_max = self.__resolucion[0]
        condicion = True
        while condicion:
            x_anterior = xi
            tiempo_pasado = reloj.tick()
            tiempo_pasado_segundos = tiempo_pasado / 1000.0
            distancia = tiempo_pasado_segundos * velocidad
            xi = xi + (distancia * factor)
            xd = xd - (distancia * factor)
            if x_anterior < xi_max and xi > xi_max:
                xi, xd = xi_max, xd_max
            self.ventana.blit(self.__fondo,update_rect_izq,update_rect_izq)
            self.ventana.blit(self.__fondo,update_rect_der,update_rect_der)
            self.ventana.blit(marcador_izq, (xi, 0))
            self.ventana.blit(marcador_der, (xd, 0))
            if self.text_box.up:
                self.text_box.refresh_text_box(self.ventana)
            pygame.display.update([update_rect_izq,update_rect_der])
            if factor > 0:
                condicion = xi < xi_max
            else:
                condicion = xi > xi_max
        #self.ventana.blit(self.club.get_current_room_surface(),(0,0))
        #self.ventana.blit(marcador_izq, (xi, 0))
        #self.ventana.blit(marcador_der, (xd, 0))
        #pygame.display.update([update_rect_izq,update_rect_der])

    def __do_board_animation_show(self, factor=1, configuracion=False):
        tablero_sup = self.board.render()
        if configuracion:
            conf_sup = self.board.get_configuration_surface()
        update_rect = pygame.Rect((self.__x_board, 0), (tablero_sup.get_width(), tablero_sup.get_height()))
        velocidad = self.__vel_anim_tablero
        reloj = pygame.time.Clock()
        if factor > 0:
            y_max = 0
            y = -tablero_sup.get_height()
        else:
            y = 0
            y_max = -tablero_sup.get_height()
        condicion = True
        while condicion:
            y_anterior = y
            tiempo_pasado = reloj.tick()
            tiempo_pasado_segundos = tiempo_pasado / 1000.0
            distancia = tiempo_pasado_segundos * velocidad
            y = y + (distancia * factor)  #distancia
            if y_anterior < y_max and y > y_max:
                y = y_max
            self.ventana.blit(self.club.get_current_room_surface(), update_rect, update_rect)
            self.ventana.blit(tablero_sup, (self.__x_board, y))
            if configuracion:
                self.ventana.blit(conf_sup, (self.__x_board, y))
            if factor > 0:
                condicion = y < y_max
            else:
                condicion = y > y_max
            pygame.display.update(update_rect)
        #self.ventana.blit(self.club.get_current_room_surface(), (0, 0))
        #self.ventana.blit(tablero_sup, (self.__x_board, y))
        #pygame.display.update(update_rect)




class TextBox:
    def __init__(self, resolucion=RESOLUTION1):
        na_otras_imagenes = Images.get_images_file_names(resolucion, "etc")
        self.__image = pygame.image.load(na_otras_imagenes["caja_texto"]).convert_alpha()
        self.__resolucion = resolucion
        self.__init_constants(resolucion)
        self.__init_fonts()
        self.__contenido = ""
        self.__encoding = 'iso-8859-15'
        self.__sup_fondo = pygame.Surface(resolucion)
        self.up = False
        self.__tablero_g = ""

    def __init_constants(self,resolucion):
        #Si la resolucion es de 800x600
        if resolucion == RESOLUTION1:
            self.__y_max = 350
            self.__y_inicial = 600.
            self.__velocidad = 650.
            self.__pos_ini_text = (30,380)
            self.__tam_fuente = 30
            self.__text_area = (700,250)
        elif resolucion == RESOLUTION2:
            self.__tam_fuente = 40
            self.__y_max = 530
            self.__y_inicial = 900.
            self.__velocidad = 1500.
            self.__text_area = (1100,300)
            self.__pos_ini_text = (40,580)
        else:
            raise Exception("Resolucion desconocida (Text Box Class)")
        self.__text_color = (0,0,0)
        self.__update_rect = pygame.Rect((0, self.__y_max), (self.__image.get_width(), self.__image.get_height()))

    def __init_fonts(self):
        self.__fuente = pygame.font.Font(Fonts.get_fonts_file_names()["fuente1"] ,self.__tam_fuente)

    def get_image(self):
        return self.__image

    def get_sprite(self):
        return self.__sprite

    def get_final_position(self):
        return (0,self.__y_max)

    def is_up(self):
        return self.up

    def set_up_graphic_board(self, tablero_g):
        self.__tablero_g = tablero_g

    def __render_textrect(self, string, font, rect, text_color, justification=0):
        """Returns a surface containing the passed text string, reformatted
        to fit within the given rect, word-wrapping as necessary. The text
        will be anti-aliased.

        Takes the following arguments:

        string - the text you wish to render. \n begins a new line.
        font - a Font object
        rect - a rectstyle giving the size of the surface requested.
        text_color - a three-byte tuple of the rgb value of the
        background_color - a three-byte tuple of the rgb value of the surface.
        justification - 0 (default) left-justified
                        1 horizontally centered
                        2 right-justified

        Returns the following values:

        Success - a surface object with the text rendered onto it.
        Failure - raises a Exception if the text won't fit onto the surface.
        """


        final_lines = []

        requested_lines = string.splitlines()

        # Create a series of lines that will fit on the provided
        # rectangle.

        for requested_line in requested_lines:
            if font.size(requested_line)[0] > rect[0]:
                words = requested_line.split(' ')
                # if any of our words are too long to fit, return.
                for word in words:
                    if font.size(word)[0] >= rect[0]:
                        raise Exception("The word " + word + " is too long to fit in the rect passed.")
                # Start a new line
                accumulated_line = ""
                for word in words:
                    test_line = accumulated_line + word + " "
                    # Build the line while the words fit.
                    if font.size(test_line)[0] < rect[0]:
                        accumulated_line = test_line
                    else:
                        final_lines.append(accumulated_line)
                        accumulated_line = word + " "
                final_lines.append(accumulated_line)
            else:
                final_lines.append(requested_line)

        # Let's try to write the text out on the surface.

        surface = pygame.Surface(rect,SRCALPHA,32)

        accumulated_height = 0
        for line in final_lines:
            if accumulated_height + font.size(line)[1] >= rect[1]:
                raise Exception("Once word-wrapped, the text string was too tall to fit in the rect.")
            if line != "":
                tempsurface = font.render(line, True, text_color)
                if justification == 0:
                    surface.blit(tempsurface, (0, accumulated_height))
                    #self.__sup_texto.blit(tempsurface, (0, accumulated_height))
                elif justification == 1:
                    surface.blit(tempsurface, ((rect[0] - tempsurface.get_width()) / 2, accumulated_height))
                    #self.__sup_texto.blit(tempsurface, ((rect[0] - tempsurface.get_width()) / 2, accumulated_height))
                elif justification == 2:
                    surface.blit(tempsurface, (rect[0] - tempsurface.get_width(), accumulated_height))
                    #self.__sup_texto.blit(tempsurface, (rect[0] - tempsurface.get_width(), accumulated_height))
                else:
                    raise Exception("Invalid justification argument: " + str(justification))
            accumulated_height += font.size(line)[1]

        return surface

    def write(self,texto):
        texto = unicode(texto,'latin-1')
        texto = texto.encode(self.__encoding)
        self.__contenido = self.__render_textrect(texto, self.__fuente, self.__text_area, self.__text_color, 0)

    def show_text(self, superficie, texto):
        self.write(texto)
        if self.__contenido != "":
            if self.up:
                self.refresh_text_box(superficie)
            else:
                self.show(superficie)
                self.refresh_text_box(superficie)
            if not self.__tablero_g == "":
                dim = self.__tablero_g.get_logical_board().get_dimension()
                if dim == 6:
                    sup_text_box_and_text = pygame.Surface(self.__contenido.get_size(),SRCALPHA,32)
                    sup_text_box_and_text.blit(self.__image, (0,0))
                    sup_text_box_and_text.blit(self.__contenido, (self.__pos_ini_text[0],self.__pos_ini_text[1]-self.__y_max))
                    self.__tablero_g.set_up_image({'imagen':sup_text_box_and_text, 'posicion':(0,self.__y_max)})
                    #self.__tablero_g.set_up_image({'imagen':self.__image, 'posicion':(0,self.__y_max)})
                    #self.__tablero_g.set_up_image({'imagen':self.__contenido, 'posicion':self.__pos_ini_text})

    def refresh_text_box(self, superficie):
        superficie.blit(self.__image, (0, self.__y_max))
        superficie.blit(self.__contenido, self.__pos_ini_text)
        self.up = True
        pygame.display.update(self.__update_rect)

    def delete_text(self):
        self.__contenido = pygame.Surface(self.__text_area,SRCALPHA,32)

    def show(self, superficie):
        self.__sup_fondo = superficie.copy()
        y = self.__y_inicial
        velocidad = self.__velocidad
        reloj = pygame.time.Clock()
        while y > self.__y_max:
            y_anterior = y
            tiempo_pasado = reloj.tick()
            tiempo_pasado_segundos = tiempo_pasado / 1000.0
            distancia = tiempo_pasado_segundos * velocidad
            y -= distancia #30
            if y_anterior > self.__y_max and y < self.__y_max:
                y = self.__y_max
            superficie.blit(self.__image, (0, y))
            pygame.display.update(self.__update_rect)
        self.up = True
        #if not self.__tablero_g == "":
        #    dim = self.__tablero_g.get_logical_board().get_dimension()
        #    if dim == 6:
        #        self.__tablero_g.set_up_image({'imagen':self.__image, 'posicion':(0,self.__y_max)})


    def disappear(self, superficie):
        if self.up:
            if not self.__tablero_g == "":
                dim = self.__tablero_g.get_logical_board().get_dimension()
                if dim == 6:
                    self.__tablero_g.remove_up_images()
            y = self.__y_max
            velocidad = self.__velocidad
            reloj = pygame.time.Clock()
            while y < self.__y_inicial:
                y_anterior = y
                tiempo_pasado = reloj.tick()
                tiempo_pasado_segundos = tiempo_pasado / 1000.0
                distancia = tiempo_pasado_segundos * velocidad
                y += distancia #30
                if y_anterior < self.__y_max and y > self.__y_max:
                    y = self.__y_inicial
                superficie.blit(self.__sup_fondo, self.__update_rect, self.__update_rect)
                superficie.blit(self.__image, (0, y))
                pygame.display.update(self.__update_rect)
            self.up = False

class SelectionList:
    NEGRO = -500
    AMARILLO = -501

    def __init__(self, resolucion=RESOLUTION2, ventana="", titulo="", tipo=""):
        self.__resolucion = resolucion
        self.__ventana = ventana
        self.__init_constants(tipo)
        self.__init_fonts()
        self.__opciones = []
        self.__opciones_visibles = []
        if titulo == "":
            self.__titulo = "OPCIONES"
        else:
            self.__titulo = titulo
        self.__color_destello = self.AMARILLO

    def __init_constants(self, tipo):
        if self.__resolucion == RESOLUTION1:
            if tipo == "secretaria":
                self.__tam = (650,262)
                self.__tam_frente = (640,192)
                self.__tam_seleccion = (630,50)
                self.__pos_pantalla =(80,200)
            elif tipo == "sin_jugadas_posibles":
                self.__tam = (480,262)
                self.__tam_frente = (470,192)
                self.__tam_seleccion = (460,50)
                self.__pos_pantalla =(300,90)
            else:
                self.__tam = (400,262)
                self.__tam_frente = (390,192)
                self.__tam_seleccion = (380,50)
                self.__pos_pantalla =(380,90)
            self.__formato_titulo = {"tamano" : 25, "color": (216,216,0)}
            self.__formato_opciones = {"tamano" : 25, "color" : (0,0,0)}
            self.__formato_opcion = {"tamano" : 25, "color" : (216,216,0)}
        elif self.__resolucion == RESOLUTION2:
            if tipo == "secretaria":
                self.__tam = (850,394)
                self.__tam_frente = (840,324)
                self.__tam_seleccion = (830,55)
                self.__pos_pantalla = (120,300)
            elif tipo == "sin_jugadas_posibles":
                self.__tam = (720,324)
                self.__tam_frente = (705,254)
                self.__tam_seleccion = (690,55)
                self.__pos_pantalla =(450,200)
            else:
                self.__tam = (600,324)
                self.__tam_frente = (590,254)
                self.__tam_seleccion = (580,55)
                self.__pos_pantalla = (550,200)
            self.__formato_titulo = {"tamano" : 35, "color": (216,216,0)}
            self.__formato_opciones = {"tamano" : 35, "color" : (0,0,0)}
            self.__formato_opcion = {"tamano" : 35, "color" : (216,216,0)}
        self.__tam_max = 3

    def __init_fonts(self):
        self.__fuente_titulo = pygame.font.Font(Fonts.get_fonts_file_names()["fuente1"] ,self.__formato_titulo["tamano"])
        self.__fuente_opciones = pygame.font.Font(Fonts.get_fonts_file_names()["fuente1"] ,self.__formato_opciones["tamano"])
        self.__fuente_opcion = pygame.font.Font(Fonts.get_fonts_file_names()["fuente1"] ,self.__formato_opcion["tamano"])

    def get_screen_position(self):
        return self.__pos_pantalla

    def draw(self):
        self.__fondo = self.__ventana.copy()
        self.__main_surface = pygame.Surface(self.__tam)
        frente = pygame.Surface(self.__tam_frente)
        frente.fill(((216, 216, 0)))
        self.__main_surface.blit(frente, (5,65))
        titulo = self.__fuente_titulo.render(self.__titulo, True, self.__formato_titulo["color"])
        pos_x = (self.__tam[0] - titulo.get_width()) / 2
        self.__main_surface.blit(titulo,(pos_x,5))
        return self.__main_surface

    def add_options(self, opciones):
        c_opciones = 1
        for o in opciones:
            opcion = {}
            opcion["descripcion"] = o["descripcion"]
            opcion["id"] = o["id"]
            opcion["visible"] = o["visible"]
            if "medalla" in o:
                opcion["medalla"] = o["medalla"]
            if c_opciones == 1:
                opcion["seleccionada"] = True
            else:
                opcion["seleccionada"] = False
            if opcion["visible"]:
                self.__opciones_visibles.append(opcion)
            self.__opciones.append(opcion)
            c_opciones += 1
        #self.__render_options()

    def render_options(self):
        y = 100
        for o in self.__opciones_visibles:
            if o["seleccionada"]:
                opcion = self.__fuente_opcion.render(o["descripcion"], True, self.__formato_opcion["color"])
                rect_sup = pygame.Surface((self.__tam_seleccion))
                rect_sup.fill((0,0,0))
                self.__main_surface.blit(rect_sup, (10,y-5))
                pos_x = (self.__tam_frente[0] - opcion.get_width()) / 2
                self.__main_surface.blit(opcion, (pos_x,y))
            else:
                opcion = self.__fuente_opciones.render(o["descripcion"], True, self.__formato_opciones["color"])
                pos_x = (self.__tam_frente[0] - opcion.get_width()) / 2
                self.__main_surface.blit(opcion, (pos_x,y))
            o["posicion_pantalla"] = (pos_x,y)
            y += 60
        return self.__main_surface

    def change_selection_options(self, direccion, audio):
        indice_sel_anterior = self.__index_option_selected_visible_list()
        can_opciones = len(self.__opciones)
        if direccion == ARRIBA:
            for i in xrange(0,can_opciones):
                if self.__opciones[i]["seleccionada"]:
                    if not i == 0:
                        self.__opciones[i]["seleccionada"] = False
                        self.__opciones[i-1]["seleccionada"] = True
                        self.__opciones[i-1]["visible"] = True
                        nueva_opcion_visible = self.__opciones[i-1]
                        break
                    else:
                        self.__opciones[i]["seleccionada"] = False
                        self.__opciones[can_opciones-1]["seleccionada"] = True
                        self.__opciones[can_opciones-1]["visible"] = True
                        nueva_opcion_visible = self.__opciones[can_opciones-1]
                        break
        elif direccion == ABAJO:
            cambio_seleccion = False
            for i in xrange(0,can_opciones):
                if self.__opciones[i]["seleccionada"]:
                    if not i == can_opciones-1 and not cambio_seleccion:
                        self.__opciones[i]["seleccionada"] = False
                        self.__opciones[i+1]["seleccionada"] = True
                        self.__opciones[i+1]["visible"] = True
                        nueva_opcion_visible = self.__opciones[i+1]
                        cambio_seleccion = True
                    elif i == can_opciones-1 and not cambio_seleccion:
                        self.__opciones[i]["seleccionada"] = False
                        self.__opciones[0]["seleccionada"] = True
                        cambio_seleccion = True
                        self.__opciones[0]["visible"] = True
                        nueva_opcion_visible = self.__opciones[0]
        else:
            raise Exception("Error!, direccion desconocida (SelectionList Class)")
        if len(self.__opciones_visibles) == self.__tam_max:
            if indice_sel_anterior == 0 and direccion == ARRIBA or \
               indice_sel_anterior == (self.__tam_max-1) and direccion == ABAJO:
                self.__update_visibles_options_list(nueva_opcion_visible, direccion)
        frente = pygame.Surface(self.__tam_frente)
        frente.fill((216, 216, 0))
        self.__main_surface.blit(frente, (5,65))
        list_sup = self.render_options()
        self.__ventana.blit(list_sup,self.__pos_pantalla)
        self.read_option(audio)

    def __index_option_selected_visible_list(self):
        for o in self.__opciones_visibles:
            if o["seleccionada"]:
                indice =  self.__opciones_visibles.index(o)
                return indice

    def __update_visibles_options_list(self, nueva_op_visible, direccion):
        if direccion == ABAJO:
            self.__opciones_visibles.pop(0)
            self.__opciones_visibles.append(nueva_op_visible)
        else:
            self.__opciones_visibles.pop()
            self.__opciones_visibles.insert(0,nueva_op_visible)

    def read_option(self, audio):
        for o in self.__opciones:
            if o["seleccionada"]:
                nombre_audio = o["id"]
                if type(nombre_audio) == type(""):
                    if not nombre_audio.find("chal") == -1:
                        audio.play_voice_sound("selector","tomar")
                        audio.play_voice_sound("selector","desafio")
                        audio.play_voice_sound("selector",nombre_audio.split("_chal_")[1])
                        if not o["medalla"] == "":
                            audio.play_voice_sound("selector","actualmente_tiene_la")
                            if o["medalla"] == BRONZE:
                                audio.play_voice_sound("selector","medalla_bronze")
                            elif o["medalla"] == PLATA:
                                audio.play_voice_sound("selector","medalla_plata")
                            elif o["medalla"] == ORO:
                                audio.play_voice_sound("selector","medalla_oro")
                    elif not nombre_audio.find("progreso") == -1:
                        progreso = nombre_audio.split("-")
                        audio.play_voice_sound("selector",progreso[0])
                        numero = get_number_word(int(progreso[1]))
                        audio.play_voice_sound("numero",numero)
                        audio.play_voice_sound("selector","porciento")
                    elif not nombre_audio.find("medallas") == -1:
                        str_medallas = nombre_audio.split("-")
                        audio.play_voice_sound("selector",str_medallas[0])
                        vec_medallas = str_medallas[1].split(".")
                        medallas_bronze = int(vec_medallas[0])
                        medallas_plata = int(vec_medallas[1])
                        medallas_oro = int(vec_medallas[2])
                        medallas_total = medallas_bronze + medallas_plata + medallas_oro
                        audio.play_voice_sound("numero", get_number_word(medallas_bronze,medallas=True))
                        if medallas_bronze == 1:
                            audio.play_voice_sound("selector","medalla_bronze")
                        else:
                            audio.play_voice_sound("selector","medallas_bronze")
                        audio.play_voice_sound("numero", get_number_word(medallas_plata,medallas=True))
                        if medallas_plata == 1:
                            audio.play_voice_sound("selector","medalla_plata")
                        else:
                            audio.play_voice_sound("selector","medallas_plata")
                        audio.play_voice_sound("numero", get_number_word(medallas_oro,medallas=True))
                        if medallas_oro == 1:
                            audio.play_voice_sound("selector","medalla_oro")
                        else:
                            audio.play_voice_sound("selector","medallas_oro")
                        audio.play_voice_sound("numero", get_number_word(medallas_total,medallas=True))
                        if medallas_total == 1:
                            audio.play_voice_sound("selector","medalla_total")
                        else:
                            audio.play_voice_sound("selector","medallas_total")

                    else:
                        audio.play_voice_sound("selector",nombre_audio)
                else:
                    #Estamos en el salon de encuentros leyendo las opciones de oponentes, para ello usamos festival
                    pass
                    #pyfestival.Festival().say(o["descripcion"])

    def option_more_info(self, audio):
        for o in self.__opciones:
            if o["seleccionada"]:
                nombre_audio = o["id"]
                try:
                    if type(nombre_audio) == type(""):
                        if not nombre_audio.find("progreso") == -1:
                            nombre_audio = nombre_audio.split("-")[0]
                        elif not nombre_audio.find("medallas") == -1:
                            nombre_audio = nombre_audio.split("-")[0]
                        audio.play_voice_sound("selector",nombre_audio+"_desc")
                    else:
                        pyfestival.Festival().say(o["descripcion"])
                except:
                    log.warning("No hay descripcion para la opcion seleccionada")

    def get_selected_option(self):
        for o in self.__opciones:
            if o["seleccionada"]:
                return o

    def blink_option(self):
        opcion_seleccionada = self.get_selected_option()
        if self.__color_destello == self.AMARILLO:
            b_opcion =  self.__fuente_opciones.render(opcion_seleccionada["descripcion"], True, self.__formato_opciones["color"])
            self.__color_destello = self.NEGRO
        else:
            b_opcion =  self.__fuente_opcion.render(opcion_seleccionada["descripcion"], True, self.__formato_opcion["color"])
            self.__color_destello = self.AMARILLO
        self.__main_surface.blit(b_opcion, opcion_seleccionada["posicion_pantalla"])
        self.__ventana.blit(self.__main_surface,self.get_screen_position())
        update_rect = pygame.Rect(self.__pos_pantalla, self.__tam)
        pygame.time.wait(100)
        pygame.display.update(update_rect)

    def remove(self):
        update_rect = pygame.Rect(self.__pos_pantalla, self.__tam)
        self.__ventana.blit(self.__fondo,update_rect,update_rect)
        pygame.display.update(update_rect)
