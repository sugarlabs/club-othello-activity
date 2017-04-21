import pygame
from pygame.locals import *
from sys import exit
from board import Board, BLANCO, NEGRO, VACIO
from utils import *
from resources.sounds import Sounds
from resources.fonts import Fonts
from resources.images import Images
from referee import Referee
import thread, logging
from player import PC, HUMANO
from input_output.audio import Channel
from main.constants import RESOLUTION1, RESOLUTION2, IZQUIERDA, DERECHA, ARRIBA, ABAJO, STANDART_BOARD_DIMENSION


log = logging.getLogger( 'src.othello.gui' )
log.setLevel( logging.DEBUG )

class GraphicBoard:
    def __init__(self, tablero_logico="", resolucion=RESOLUTION1):
        if tablero_logico == "":
            self.__tablero = Board(STANDART_BOARD_DIMENSION)
        else:
            self.__tablero = tablero_logico
        #Inicializo el una matriz donde guardo las coordenadas de pantalla de cada celda
        self.__coordenadas = []
        for _ in xrange(self.__tablero.get_dimension()):
            self.__coordenadas.append([None]*self.__tablero.get_dimension())
        #Inicializo las variables x e y de las posiciones iniciales del tablero dependiendo de la resolucion
        self.__init_constants(resolucion)
        #Inicializo las imagenes del tablero
        self.__init_images(resolucion)
        #Inicializo las fuentes
        self.__init_fonts()
        #Incializo variables que se utilizan en el algoritmo para la animacion de la celda seleccionada
        self.__nro_imagen = 0
        self.__factor = -1
        self.__cambiar_imagen = 0
        #Cargo en un vector las imagenes utilizadas en la animacion de la celda seleccionada
        efectos = Images.get_images_file_names(resolucion, "animacion_celda")
        self.__imagenes_celda_animada = [pygame.image.load(efectos["chica"]).convert(),pygame.image.load(efectos["mediana"]).convert(),pygame.image.load(efectos["grande"]).convert()]
        self.__animated_cell = Coordinate()
        #Inicializo un reloj que utilizo para la animacion de la celda
        self.__reloj = pygame.time.Clock()
        self.lista_jugadas = []
        #Inicializo constantes para identificar las esquinas del tablero
        self.__IARRIBA = 2
        self.__IABAJO = 3
        self.__DARRIBA = 4
        self.__DABAJO = 5
        #Inicializo la superficie donde voy a guardar el tablero
        self.__init_surface()
        self.__do_animation_cell = True
        self.__marcador = Score()
        self.__render_board()
        self.__up_images = []

    def __init_images(self,resolucion):
        na_imagenes_tablero = Images.get_images_file_names(resolucion, "tablero")
        na_imagenes_piezas = Images.get_images_file_names(resolucion, "piezas")
        #Cargo la imagen de la celda vacia
        self.__imagen_celda = pygame.image.load(na_imagenes_tablero["celda_vacia"]).convert()
        #Cargo la imagen de las cabeceras del tablero
        self.__imagen_tablero_bordev = pygame.image.load(na_imagenes_tablero["borde_vertical"]).convert()
        self.__imagen_tablero_bordeh = pygame.image.load(na_imagenes_tablero["borde_horizontal"]).convert()
        #Cargo las imagenes de las piezas
        self.__imagen_pieza_blanca = pygame.image.load(na_imagenes_piezas["blanca"]).convert_alpha()
        self.__imagen_pieza_negra = pygame.image.load(na_imagenes_piezas["negra"]).convert_alpha()
        self.__imagen_marca = pygame.image.load(na_imagenes_tablero["marca"]).convert_alpha()

    def __init_constants(self,resolucion):
        #Si la resolucion es de 800x600
        if resolucion == RESOLUTION1:
            self.__pos_ini = Coordinate(0,0)
            #Constantes que se utilizan en la funcion que renderea el tablero
            self.__inc_numero_borde_h = Coordinate(25,-5)
            self.__inc_numero_borde_vi = Coordinate(8,10)
            self.__inc_numero_borde_vd = Coordinate(7,10)
            self.__inc_borde_vd = Coordinate(70,0)
            self.__mitad_tam_celda = 35
            self.__tam_celda = 70
            if self.__tablero.get_dimension() == 4:
                self.__pos_graphic_board = Coordinate(200,0)
            else:
                self.__pos_graphic_board = Coordinate(155,0)
            self.__tam_fuente = 35
            self.__current_cell = Coordinate(0,0)
        #Si al resolucion es de 1200x900
        elif resolucion == RESOLUTION2:
            self.__pos_ini = Coordinate(0,0)
            #Constantes que se utilizan en la funcion que renderea el tablero
            self.__inc_numero_borde_h = Coordinate(35,-7)
            self.__inc_numero_borde_vi = Coordinate(10,17)
            self.__inc_numero_borde_vd = Coordinate(11,17)
            self.__inc_borde_vd = Coordinate(105,0)
            self.__mitad_tam_celda = 52
            self.__tam_celda = 105
            if self.__tablero.get_dimension() == 4:
                self.__pos_graphic_board = Coordinate(340,0)
            else:
                self.__pos_graphic_board = Coordinate(225,0)
            self.__tam_fuente = 50
            self.__current_cell = Coordinate(0,0)
        else:
            raise Exception("Resolucion desconocida (GraphicBoard Class)")

    def __init_fonts(self):
        self.__fuente = pygame.font.Font(Fonts.get_fonts_file_names()["fuente1"],self.__tam_fuente)

    def __init_surface(self):
        tam = (self.__mitad_tam_celda * 2) + (self.__tam_celda * self.__tablero.get_dimension())
        self.__surface = pygame.Surface((tam, tam), SRCALPHA,32)
        self.__conf_surface = pygame.Surface((tam, tam), SRCALPHA,32)

    def set_coord_selected_cell(self, nueva_coord):
        self.__current_cell.set(nueva_coord)

    def get_coord_selected_cell(self):
        return self.__current_cell

    def get_logical_board(self):
        return self.__tablero

    def get_board_pos(self):
        return self.__pos_graphic_board

    def get_board_surface(self):
        return self.__surface

    def get_configuration_surface(self):
        return self.__conf_surface

    """

        Render a piece in a specific position on the board

        Params:
            - valor_casilla : BLACK or WHITE
            - x_s, y_s : surface render coordinate
            - superficie : render surface
    """
    def __render_piece(self,valor_casilla,x_s,y_s,superficie):
        if valor_casilla == BLANCO:
            superficie.blit(self.__imagen_pieza_blanca, (x_s,y_s))
        elif valor_casilla == NEGRO:
            superficie.blit(self.__imagen_pieza_negra, (x_s,y_s))

    """

        Render an empty cell in the screen

        Params:
            - celda_coord : cell screen coordinate
            - tablero_coord : cell board coordinate
            - ventana : render screen
    """
    def __render_cell(self,celda_coord, superficie):
        #Coordenadas de pantalla
        x = celda_coord.x
        y = celda_coord.y
        #Muestro la celda en blanco
        superficie.blit(self.__imagen_celda, (x,y))

    def render(self):
        #self.__set_corner_pixels(self.__surface)
        #self.__render_all_corners()
        #self.__render_board()
        return self.__surface
        #superficie.blit(self.__surface,(self.__pos_graphic_board.x,self.__pos_graphic_board.y))

    """

        Render the board in the graphic board surface

        Params:
            None
    """
    def __render_board(self):
        x = self.__pos_ini.x + self.__mitad_tam_celda
        for j in xrange(0, self.__tablero.get_dimension()):
            y = self.__pos_ini.y
            for i in xrange(0, self.__tablero.get_dimension()):
                #Muestro el borde horizontal junto con el numero si es la primera fila
                if i == 0:
                    self.__surface.blit(self.__imagen_tablero_bordeh, (x,y))
                    #Numero del borde horizontal superior
                    nro_horizontal = self.__fuente.render(str(j+1), True, (255,255,0))
                    nx = x + self.__inc_numero_borde_h.x
                    ny = y + self.__inc_numero_borde_h.y
                    self.__surface.blit(nro_horizontal, (nx,ny))
                    y += self.__mitad_tam_celda
                #Calculo el numero a imprimir en el borde vertical
                nro_vertical = str(self.__tablero.get_dimension() - i)
                nro_vertical_text = self.__fuente.render(nro_vertical, True, (255,255,0))
                #Muestro el borde vertical izquierda junto con el numero si es la primera columna
                if j == 0:
                    self.__surface.blit(self.__imagen_tablero_bordev, (self.__pos_ini.x,y))
                    #Numero del borde vertical izquierda
                    nx = self.__pos_ini.x + self.__inc_numero_borde_vi.x
                    ny = y + self.__inc_numero_borde_vi.y
                    self.__surface.blit(nro_vertical_text, (nx,ny))
                #Render una celda vacio
                self.__render_cell(Coordinate(x,y), self.__surface)
                #Guardo la coordenada de pantalla de la celda
                self.__coordenadas[i][j] = Coordinate(x,y)
                #Muestro el borde vertical derecha junto con los numeros si es la ultima columna
                if j == self.__tablero.get_dimension() - 1:
                    nx = x + self.__inc_borde_vd.x
                    ny = y + self.__inc_borde_vd.y
                    self.__surface.blit(self.__imagen_tablero_bordev, (nx,ny))
                    #Numero del borde vertical izquierda
                    nx = nx + self.__inc_numero_borde_vd.x
                    ny = ny + self.__inc_numero_borde_vd.y
                    self.__surface.blit(nro_vertical_text, (nx,ny))
                #Muestro el borde horizontal si es la ultima fila
                if i == self.__tablero.get_dimension() - 1:
                    y += self.__tam_celda
                    self.__surface.blit(self.__imagen_tablero_bordeh, (x,y))
                    #Numero del borde horizontal inferior
                    nx = x + self.__inc_numero_borde_h.x
                    ny = y + self.__inc_numero_borde_h.y
                    self.__surface.blit(nro_horizontal, (nx,ny))
                y += self.__tam_celda
            x += self.__tam_celda

    def render_configuration(self, ventana=""):
        #self.__render_board()
        tam = (self.__mitad_tam_celda * 2) + (self.__tam_celda * self.__tablero.get_dimension())
        self.__conf_surface = pygame.Surface((tam, tam),SRCALPHA,32)
        dim = self.__tablero.get_dimension()
        #superficie = self.__surface
        for i in xrange(0,dim):
            for j in xrange(0,dim):
                valor_casilla = self.__tablero.get_valor_casilla(i,j)
                if valor_casilla != VACIO:
                    x_s = self.__coordenadas[i][j].x
                    y_s = self.__coordenadas[i][j].y
                    self.__render_piece(valor_casilla, x_s, y_s, self.__conf_surface)
        ventana.blit(self.__surface,(self.__pos_graphic_board.x,self.__pos_graphic_board.y))
        ventana.blit(self.__conf_surface,(self.__pos_graphic_board.x,self.__pos_graphic_board.y))

    def __render_background_corner(self,esquina):
        if esquina == self.__IARRIBA:
            x_ini = self.__pos_ini.x
            y_ini = self.__pos_ini.y
            esquina = self.__esquinaiarriba
        elif esquina == self.__IABAJO:
            x_ini = self.__pos_ini.x
            y_ini = self.__mitad_tam_celda + (self.__tam_celda * self.__tablero.get_dimension())
            esquina = self.__esquinaiabajo
        elif esquina == self.__DARRIBA:
            x_ini = self.__pos_ini.x + self.__mitad_tam_celda + (self.__tam_celda * self.__tablero.get_dimension())
            y_ini = self.__pos_ini.y
            esquina = self.__esquinadarriba
        elif esquina == self.__DABAJO:
            x_ini = self.__pos_ini.x + self.__mitad_tam_celda + (self.__tam_celda * self.__tablero.get_dimension())
            y_ini = self.__mitad_tam_celda + (self.__tam_celda * self.__tablero.get_dimension())
            esquina = self.__esquinadabajo
        for i in xrange(0,self.__mitad_tam_celda):
            x = x_ini + i
            for j in xrange(0,self.__mitad_tam_celda):
                y = y_ini + j
                self.__surface.set_at((x,y),esquina[i][j])

    def __render_all_corners(self):
        self.__render_background_corner(self.__IARRIBA)
        self.__render_background_corner(self.__IABAJO)
        self.__render_background_corner(self.__DARRIBA)
        self.__render_background_corner(self.__DABAJO)

    def __get_corner_pixels(self,x_ini,y_ini,ventana):
        esquina = []
        for _ in xrange(self.__mitad_tam_celda):
            esquina.append([None]*self.__mitad_tam_celda)

        for i in xrange(0,self.__mitad_tam_celda):
                for j in xrange(0,self.__mitad_tam_celda):
                    x = x_ini + i
                    y = y_ini + j
                    esquina[i][j] = ventana.get_at((x,y))
        return esquina

    def __set_corner_pixels(self,ventana):
        #Esquina Izquierda Arriba
        x_ini = self.__pos_graphic_board.x
        y_ini = self.__pos_graphic_board.y
        self.__esquinaiarriba = self.__get_corner_pixels(x_ini,y_ini,ventana)
        #Esquina Izquierda Abajo
        y_ini = self.__mitad_tam_celda + (self.__tam_celda * self.__tablero.get_dimension())
        self.__esquinaiabajo = self.__get_corner_pixels(x_ini, y_ini, ventana)
        #Esquina Derecha Arriba
        x_ini = self.__pos_graphic_board.x + self.__mitad_tam_celda + (self.__tam_celda * self.__tablero.get_dimension())
        y_ini = self.__pos_graphic_board.y
        self.__esquinadarriba = self.__get_corner_pixels(x_ini, y_ini, ventana)
        #Esquina Derecha Abajo
        y_ini = self.__mitad_tam_celda + (self.__tam_celda * self.__tablero.get_dimension())
        self.__esquinadabajo = self.__get_corner_pixels(x_ini, y_ini, ventana)

    def __seleccion_is_on_corner(self):
        #coord_logica = self.graphic_coord_to_logic_coord(self.__current_cell)
        coord_logica = self.__current_cell
        dim = self.__tablero.get_dimension()
        if (coord_logica.x == 0 or coord_logica.x == dim - 1) and \
           (coord_logica.y == 0 or coord_logica.y == dim - 1):
            return True
        else:
            return False

    def __seleccion_is_on_border(self):
        #coord_logica = self.graphic_coord_to_logic_coord(self.__current_cell)
        coord_logica = self.__current_cell
        dim = self.__tablero.get_dimension()
        if coord_logica.x == 0 or coord_logica.x == dim - 1 or \
           coord_logica.y == 0 or coord_logica.y == dim - 1:
            return True
        else:
            return False

    def end_animation_cell(self):
        self.__do_animation_cell = False
        pygame.time.wait(200)

    def animation_cell_running(self):
        return self.__do_animation_cell

    def set_up_image(self, hash_image):
        self.__up_images.append(hash_image)

    def remove_up_images(self):
        self.__up_images = []

    def __re_calculate_update_rect(self):
        dim = self.__tablero.get_dimension()
        coord_logica = self.__current_cell
        coord_actual = Coordinate(self.__coordenadas[coord_logica.x][coord_logica.y].x, self.__coordenadas[self.__current_cell.x][self.__current_cell.y].y)
        if self.__seleccion_is_on_corner():
            if coord_logica.x == 0 and coord_logica.y == 0:
                #Esquina Izquierda Arriba
                x = coord_actual.x - self.__imagen_tablero_bordev.get_width()
                y = coord_actual.y - self.__imagen_tablero_bordeh.get_height()
            elif coord_logica.x == 0 and coord_logica.y == dim - 1:
                #Esquina Derecha Arriba
                x = coord_actual.x - self.__imagen_celda.get_width()
                y = coord_actual.y - self.__imagen_tablero_bordeh.get_height()
            elif coord_logica.x == dim - 1 and coord_logica.y == 0:
                #Esquina Izquierda Abajo
                x = coord_actual.x - self.__imagen_tablero_bordev.get_width()
                y = coord_actual.y - self.__imagen_celda.get_height()
            else:
                #Esquina Derecha Abajo
                x = coord_actual.x - self.__imagen_celda.get_width()
                y = coord_actual.y - self.__imagen_celda.get_height()
            w = 2 * self.__imagen_celda.get_width() + self.__imagen_tablero_bordev.get_width()
            h = 2 * self.__imagen_celda.get_height() + self.__imagen_tablero_bordeh.get_height()
        elif self.__seleccion_is_on_border():
            #log.debug("La seleccion esta en un borde")
            if coord_logica.x == 0:
                #Borde Arriba
                x = coord_actual.x - self.__imagen_celda.get_width()
                y = coord_actual.y - self.__imagen_tablero_bordeh.get_height()
                w = 3 * self.__imagen_celda.get_width()
                h = 2 * self.__imagen_celda.get_height() + self.__imagen_tablero_bordeh.get_height()
            elif coord_logica.y == dim - 1:
                #Borde Derecha
                x = coord_actual.x - self.__imagen_celda.get_width()
                y = coord_actual.y - self.__imagen_celda.get_height()
                w = 2 * self.__imagen_celda.get_width() + self.__imagen_tablero_bordev.get_width()
                h = 3 * self.__imagen_celda.get_height()
            elif coord_logica.y == 0:
                #Borde Izquierdo
                x = coord_actual.x - self.__imagen_tablero_bordev.get_width()
                y = coord_actual.y - self.__imagen_celda.get_height()
                w = 2 * self.__imagen_celda.get_width() + self.__imagen_tablero_bordev.get_width()
                h = 3 * self.__imagen_celda.get_height()
            else:
                #Borde Abajo
                x = coord_actual.x-self.__imagen_celda.get_width()
                y = coord_actual.y-self.__imagen_celda.get_height()
                w = 3 * self.__imagen_celda.get_width()
                h = 2 * self.__imagen_celda.get_height() + self.__imagen_tablero_bordeh.get_height()
        else:
            x = coord_actual.x-self.__imagen_celda.get_width()
            y = coord_actual.y-self.__imagen_celda.get_height()
            w = 3 * self.__imagen_celda.get_width()
            h = 3 * self.__imagen_celda.get_height()
        rect = pygame.Rect((x,y),(w,h))
        return rect

    """

        Render the animated cell

        Params:
            - pos_casilla : animated cell coordinate
            - ventana : render screen
    """
    def render_animation_cell(self, superficie):
        #update_rect = pygame.Rect((self.__pos_graphic_board.x, self.__pos_graphic_board.y), (self.__surface.get_width(), self.__surface.get_height()))
        self.__set_corner_pixels(superficie)
        self.__do_animation_cell = True
        while self.__do_animation_cell:
            render_all_board = False
            if not self.__current_cell.equal(self.__animated_cell):
                self.__animated_cell.set(self.__current_cell)
                self.__factor = -1
                self.__nro_imagen = 0
                render_all_board = True
            #Coordenadas de pantalla
            x = self.__coordenadas[self.__current_cell.x][self.__current_cell.y].x + self.__pos_graphic_board.x
            y = self.__coordenadas[self.__current_cell.x][self.__current_cell.y].y + self.__pos_graphic_board.y
            i = self.__nro_imagen
            f = self.__factor
            if i == 2 or i == 0:
                f *= -1
            i = i + f
            if self.__seleccion_is_on_corner():
                self.__render_all_corners()
            if render_all_board:
                superficie.blit(self.__surface,(self.__pos_graphic_board.x,self.__pos_graphic_board.y))
                superficie.blit(self.__conf_surface,(self.__pos_graphic_board.x,self.__pos_graphic_board.y))
                rect_sub_sup = self.__re_calculate_update_rect()
            else:
                sub_sup_tablero = self.__surface.subsurface(rect_sub_sup)
                sub_sup_conf = self.__conf_surface.subsurface(rect_sub_sup)
                superficie.blit(sub_sup_tablero,(rect_sub_sup.left+self.__pos_graphic_board.x,rect_sub_sup.top+self.__pos_graphic_board.y))
                superficie.blit(sub_sup_conf,(rect_sub_sup.left+self.__pos_graphic_board.x,rect_sub_sup.top+self.__pos_graphic_board.y))
            superficie.blit(self.__imagenes_celda_animada[i], (x-(i+i),y-(i+i)))
            #Muestro alguna pieza si es que existe alguna en la celda animada
            valor_casilla = self.__tablero.get_valor_casilla(self.__current_cell.x,self.__current_cell.y)
            if valor_casilla != VACIO:
                self.__render_piece(valor_casilla,x,y,superficie)
            else:
                #Si es una casilla vacia muestro alguna marca si es que existe alguna en la celda animada
                self.__render_possible_move(self.__current_cell, superficie)
            self.__nro_imagen = i
            self.__factor = f
            if not render_all_board:
                #Si no rendereo todo el tablero, el rectangulo de actualizacion es solo el tamano del sub rectangulo.
                update_rect = pygame.Rect((rect_sub_sup.left + self.__pos_graphic_board.x,rect_sub_sup.top + self.__pos_graphic_board.y),(rect_sub_sup.width,rect_sub_sup.height))
            else:
                update_rect = pygame.Rect((self.__pos_graphic_board.x, self.__pos_graphic_board.y), (self.__surface.get_width(), self.__surface.get_height()))
            if not self.__up_images == []:
                for image in self.__up_images:
                    rect_img = pygame.Rect(image['posicion'],(image['imagen'].get_width(),image['imagen'].get_height()))
                    if rect_img.colliderect(update_rect):
                        superficie.blit(image['imagen'],image['posicion'])
            pygame.time.wait(150)
            pygame.display.update(update_rect)

    def __print_log(self, archivo, mensaje):
        if archivo != "":
            print >> archivo, mensaje

    def do_move(self, direccion, audio, archivo_juego=""):
        #No Pudo realizar el movimiento
        if  not self.__set_new_coordinates(direccion):
            audio.play_fx_sound("board","mal_mov")
            if direccion == ARRIBA:
                dir_mov = "arriba"
            elif direccion == ABAJO:
                dir_mov = "abajo"
            elif direccion == DERECHA:
                dir_mov = "derecha"
            else:
                dir_mov = "izquierda"
            self.__print_log(archivo_juego, "ERROR!, estaba en: " + str(self.__current_cell) + " e hizo un movimiento " + dir_mov)
        else:
            volumen_laterales = {"volumen":self.__stereo_pan(self.__current_cell.y)}
            self.play_box_sound(audio, self.__current_cell, self.lista_jugadas, volumen_laterales)

    def __set_new_coordinates(self, direccion):
        nueva_coord = self.get_new_coordinates(direccion)
        if not nueva_coord == False:
            self.__current_cell = nueva_coord
            return True
        else:
            return False

    """

        Get the new coordinate from the actual coordinate

        Params:
            - direccion : new coordinate direction (left,right,up,down)
            - coordenada_actual : actual coordinate
    """
    def get_new_coordinates(self,direccion):
        coordenada_nueva = self.__current_cell

        if direccion == IZQUIERDA:
            if self.__current_cell.y > 0:
                coordenada_nueva.y -= 1
            else:
                return False
        elif direccion == DERECHA:
            if self.__current_cell.y < self.__tablero.get_dimension() - 1:
                coordenada_nueva.y += 1
            else:
                return False
        elif direccion == ARRIBA:
            if self.__current_cell.x > 0:
                coordenada_nueva.x -= 1
            else:
                return False
        elif direccion == ABAJO:
            if self.__current_cell.x < self.__tablero.get_dimension() - 1:
                coordenada_nueva.x += 1
            else:
                return False

        return coordenada_nueva

    """

        Render a possible move if exist in the list of possibles moves
        Params:
            - coord : possible move coordinate
            - ventana : render screen
    """
    def __render_possible_move(self,coord,ventana):
        coordenadas = self.__coordenadas
        for c in self.lista_jugadas:
            if c.x == coord.x and c.y == coord.y:
                x = coordenadas[c.x][c.y].x + self.__pos_graphic_board.x
                y = coordenadas[c.x][c.y].y + self.__pos_graphic_board.y
                #Muestro la marca en el tablero
                ventana.blit(self.__imagen_marca, (x,y))
                break

    """

        Render a list of possibles moves

        Params:
            - ventana : render screen
    """
    def render_list_possible_moves(self, ventana):
        coordenadas = self.__coordenadas
        for c in self.lista_jugadas:
            x = coordenadas[c.x][c.y].x
            y = coordenadas[c.x][c.y].y
            #Muestro la marca en el tablero
            self.__conf_surface.blit(self.__imagen_marca, (x,y))
            ventana.blit(self.__conf_surface,(self.__pos_graphic_board.x,self.__pos_graphic_board.y))

    def __render_animation_image(self,imagen,inc,coord,ventana):
        x = self.__coordenadas[coord.x][coord.y].x + self.__pos_graphic_board.x
        y = self.__coordenadas[coord.x][coord.y].y + self.__pos_graphic_board.y
        ventana.blit(imagen, (x-inc,y-inc))
        self.__render_piece(self.__tablero.get_valor_casilla(coord.x,coord.y),x,y,ventana)

    def __render_line_animation(self,linea,color,sonido,audio,ventana):
        audio.play_voice_sound("board","linea_entre")
        graphic_coord = self.convert_logic_coord_to_graphic_coord(linea["casilla_inicial"])
        volumen_laterales = {"volumen":self.__stereo_pan(linea["casilla_inicial"].y)}
        self.__play_coordinate_sound(audio, graphic_coord,volumen_laterales)
        audio.play_voice_sound("otros","y")
        volumen_laterales = {"volumen":self.__stereo_pan(linea["casilla_final"].y)}
        graphic_coord = self.convert_logic_coord_to_graphic_coord(linea["casilla_final"])
        self.__play_coordinate_sound(audio, graphic_coord,volumen_laterales)
        i = self.__nro_imagen
        f = self.__factor
        can_casillas_v = linea["can_fichas_volteables"] - 1
        update_rect = pygame.Rect((self.__pos_graphic_board.x, self.__pos_graphic_board.y), (self.__surface.get_width(), self.__surface.get_height()))
        while can_casillas_v >= 0:
            if audio.silence_channel():
                self.__tablero.turn_pieces2(linea["casillas_volteables"][can_casillas_v],color)
                can_casillas_v = can_casillas_v - 1
                volumen_laterales = {"volumen":self.__stereo_pan(linea["casillas_volteables"][can_casillas_v].y)}
                audio.play_fx_sound("board",sonido,volumen_laterales)
                self.render_configuration(ventana)
            if i == 2:
                f *= -1
            elif i == 0:
                f *= -1
            i = i + f
            ventana.blit(self.__surface,(self.__pos_graphic_board.x,self.__pos_graphic_board.y))
            ventana.blit(self.__conf_surface,(self.__pos_graphic_board.x,self.__pos_graphic_board.y))
            self.__render_animation_image(self.__imagenes_celda_animada[i], i+i, linea["casilla_inicial"], ventana)
            for casilla in linea["casillas_volteables"]:
                self.__render_animation_image(self.__imagenes_celda_animada[i], i+i, casilla, ventana)
            self.__render_animation_image(self.__imagenes_celda_animada[i], i+i, linea["casilla_final"], ventana)
            pygame.display.update(update_rect)
            pygame.time.wait(150)
        ventana.blit(self.__surface,(self.__pos_graphic_board.x,self.__pos_graphic_board.y))
        ventana.blit(self.__conf_surface,(self.__pos_graphic_board.x,self.__pos_graphic_board.y))
        pygame.display.update(update_rect)

    def __play_coordinate_sound(self, audio, coord, vol):
        audio.play_voice_sound("numero",get_number_word(coord.y),vol)
        audio.play_voice_sound("numero",get_number_word(coord.x),vol)

    def __play_move_sound(self, audio, coord):
        volumen_laterales = {"volumen":self.__stereo_pan(coord.y)}
        audio.play_voice_sound("board","jugada_en",volumen_laterales)
        graphic_coord = self.convert_logic_coord_to_graphic_coord(coord)
        self.__play_coordinate_sound(audio, graphic_coord,volumen_laterales)

    def set_piece(self, coord, color, sonido_color, audio, ventana):
        pudo_colocar = self.__tablero.set_piece(coord,color)
        if pudo_colocar:
            self.lista_jugadas = []
            self.render_configuration(ventana)
            volumen_laterales = {"volumen":self.__stereo_pan(coord.y)}
            audio.play_fx_sound("board",sonido_color,volumen_laterales)
            self.__play_move_sound(audio, coord)
            update_rect = pygame.Rect((self.__pos_graphic_board.x, self.__pos_graphic_board.y), (self.__surface.get_width(), self.__surface.get_height()))
            pygame.display.update(update_rect)
            return True
        else:
            return False

    def convert_logic_coord_to_graphic_coord(self, logic_coord):
        return Coordinate(self.__tablero.get_dimension()-logic_coord.x,logic_coord.y+1)

    def graphic_coord_to_logic_coord(self, coord_grafica):
        return Coordinate(self.__tablero.get_dimension()-coord_grafica.x,coord_grafica.y-1)

    def do_line_animation(self, coord, color, sonido, canal, marcador, ventana):
        lineas_formadas = self.get_logical_board().get_lines(color,coord)
        for linea in lineas_formadas:
            self.__render_line_animation(linea,color,sonido,canal,ventana)
            marcador.render_numbers(self.get_logical_board(),color,ventana)

    def play_possible_moves_sound(self, audio):
        audio.play_voice_sound("board","jugada_posible")
        can_jp = len(self.lista_jugadas)
        con = 0
        if can_jp > 0:
            for jp_coord in self.lista_jugadas:
                con += 1
                if con == can_jp:
                    audio.play_voice_sound("otros","y_en")
                else:
                    audio.play_voice_sound("otros","en")
                graphic_coord = self.convert_logic_coord_to_graphic_coord(jp_coord)
                volumen_laterales = {"volumen":self.__stereo_pan(jp_coord.y)}
                self.__play_coordinate_sound(audio, graphic_coord, volumen_laterales)
                audio.play_voice_sound("otros","silencio")
        else:
            audio.play_voice_sound("board","no_hay_jugadas_posibles")

    def play_count_pieces_sound(self, audio, juego=""):
        if juego != "":
            jugador = juego.get_turn()
            can_jugadas_posibles = len(juego.get_list_possible_moves())
        else:
            can_jugadas_posibles = len(self.lista_jugadas)
        audio.play_voice_sound("board","tablero_tiene")
        can_fichas_blancas = self.__tablero.get_number_white_pieces()
        can_fichas_negras = self.__tablero.get_number_black_pieces()
        if can_fichas_blancas > 1:
            audio.play_voice_sound("numero",get_number_word(can_fichas_blancas))
            audio.play_voice_sound("board","fichas_blancas")
        else:
            audio.play_voice_sound("numero","una")
            audio.play_voice_sound("board","ficha_blanca")
        if can_fichas_negras > 1:
            audio.play_voice_sound("numero",get_number_word(can_fichas_negras))
            audio.play_voice_sound("board","fichas_negras")
        else:
            audio.play_voice_sound("numero","una")
            audio.play_voice_sound("board","ficha_negra")
        if juego == "" or (juego != "" and not juego.game_ended()):
            audio.play_voice_sound("otros","y")
            if not can_jugadas_posibles == 1:
                if can_jugadas_posibles == 0 and (jugador != "" and jugador.get_name() == HUMANO):
                    audio.play_voice_sound("game","no_hay_jugadas_posbiles")
                    return False
                else:
                    audio.play_voice_sound("numero",get_number_word(can_jugadas_posibles))
                    audio.play_voice_sound("board","jugadas_posibles")
                    return True
            else:
                audio.play_voice_sound("numero","una")
                audio.play_voice_sound("board","jugada_posible")
                return True

    def __stereo_pan(self, coord_columna):
        volumen_derecha = float(coord_columna) / (self.__tablero.get_dimension() - 1)
        volumen_izquierda = 1.0 - volumen_derecha
        return {"derecha":volumen_derecha, "izquierda":volumen_izquierda}

    def __play_coordinate_sound_extra_info(self, audio, coord, volumen):
        graphic_coord = self.convert_logic_coord_to_graphic_coord(coord)
        audio.play_voice_sound("board","columna",volumen)
        audio.play_voice_sound("numero",get_number_word(graphic_coord.y),volumen)
        audio.play_voice_sound("board","fila",volumen)
        audio.play_voice_sound("numero",get_number_word(graphic_coord.x),volumen)

    def play_box_info_sound(self, audio, coord=""):
        if coord == "":
            coord = self.__current_cell
        volumen_laterales = {"volumen":self.__stereo_pan(coord.y)}
        self.__play_coordinate_sound_extra_info(audio, coord, volumen_laterales)
        self.play_box_sound(audio, coord, [], volumen_laterales)

    def play_box_sound(self, audio, coord, lista_jugadas, volumen_laterales):
        tablero = self.__tablero
        jugada_posible = False
        for jugada in lista_jugadas:
            if jugada.x == coord.x and jugada.y == coord.y:
                audio.play_fx_sound("board","jugada_posible",volumen_laterales)
                audio.play_voice_sound("board","jugada_posible",volumen_laterales)
                jugada_posible = True
                break
        if not jugada_posible:
            valor_casilla = tablero.get_valor_casilla(coord.x,coord.y)
            if valor_casilla == VACIO:
                audio.play_fx_sound("board","vacio",volumen_laterales)
                audio.play_voice_sound("board","vacio",volumen_laterales)
            elif valor_casilla == BLANCO:
                audio.play_fx_sound("board","blanco",volumen_laterales)
                audio.play_voice_sound("board","blanco",volumen_laterales)
            elif valor_casilla == NEGRO:
                audio.play_fx_sound("board","negro",volumen_laterales)
                audio.play_voice_sound("board","negro",volumen_laterales)
            else:
                raise Exception("Error!, valor de casilla desconocido (Othello.Gui Class)")

class Score:
    def __init__(self, resolucion=(800,600)):
        #Inicilializo las constasntes graficas dependiendo de la resolucion
        self.__init_constants(resolucion)
        self.__resolucion = resolucion
        #Inicializo las fuentes
        self.__init_fonts()
        #Inicializo las imagenes
        self.__init_images(resolucion)
        self.__sup_marcador_izq = ""
        self.__sup_marcador_der = ""

    def __init_constants(self,resolucion):
        #Si la resolucion es de 800x600
        if resolucion == RESOLUTION1:
            self.__barra = Coordinate(0,0)
            self.__bandera = Coordinate(6,6)
            self.__tam_fuente = 60
            self.__x_marcador = 15
            self.__y_marcador = 300
        #Si la resolucion es de 1200x900
        elif resolucion == RESOLUTION2:
            self.__barra = Coordinate(0,0)
            self.__bandera = Coordinate(9,7)
            self.__tam_fuente = 80
            self.__x_marcador = 25
            self.__y_marcador = 350
        else:
            raise Exception("Resolucion desconocida (Score Class)")
        #Iniciliazo los colores de las fuentes
        self.__color_negro = (0,0,0)
        self.__color_amarillo = (255,255,0)

    def __init_fonts(self):
        self.__fuente = pygame.font.Font(Fonts.get_fonts_file_names()["fuente1"],self.__tam_fuente)

    def __init_images(self, resolucion):
        na_imagenes_marcador = Images.get_images_file_names(resolucion, "marcador")
        self.__imagen_barra_negra = pygame.image.load(na_imagenes_marcador["barra_negra"]).convert_alpha()
        self.__imagen_barra_amarilla = pygame.image.load(na_imagenes_marcador["barra_amarilla"]).convert_alpha()
        self.__imagen_bandera_negra = pygame.image.load(na_imagenes_marcador["bandera_negra"]).convert_alpha()
        self.__imagen_bandera_blanca = pygame.image.load(na_imagenes_marcador["bandera_blanca"]).convert_alpha()

    def refresh(self, ventana):
        if not self.__sup_marcador_der == "" and not self.__sup_marcador_izq == "":
            ventana.blit(self.__sup_marcador_izq,(0,0))
            ventana.blit(self.__sup_marcador_der,(self.__resolucion[0] - self.__sup_marcador_der.get_width(),0))
            x1 = self.__resolucion[0] - self.__imagen_barra_negra.get_width()
            x2 = self.__imagen_barra_negra.get_width()
            y2 = self.__imagen_barra_negra.get_height()
            update_rect_izq = pygame.Rect((0, 0), (x2, y2))
            update_rect_der = pygame.Rect((x1, 0), (x2, y2))
            pygame.display.update([update_rect_izq,update_rect_der])

    def render_numbers(self, tablero, turno, ventana):
        self.__render(tablero, ventana, turno)
        x1 = self.__resolucion[0] - self.__imagen_barra_negra.get_width()
        x2 = self.__imagen_barra_negra.get_width()
        y2 = self.__imagen_barra_negra.get_height() / 2
        update_rect_izq = pygame.Rect((0, 0), (x2, y2))
        update_rect_der = pygame.Rect((x1, 0), (x2, y2))
        pygame.display.update([update_rect_izq,update_rect_der])

    def render_all(self, tablero, turno, ventana):
        self.__render(tablero, ventana, turno)
        x1 = self.__resolucion[0] - self.__imagen_barra_negra.get_width()
        x2 = self.__imagen_barra_negra.get_width()
        y2 = self.__imagen_barra_negra.get_height()
        update_rect_izq = pygame.Rect((0, 0), (x2, y2))
        update_rect_der = pygame.Rect((x1, 0), (x2, y2))
        #pygame.display.update([update_rect_izq,update_rect_der])

    def __render(self,tablero,ventana,turno):
        self.__sup_marcador_izq = self.render_left_score(tablero, turno)
        self.__sup_marcador_der = self.render_right_score(tablero, turno)
        #Pego las superficies de los marcadores a la ventana
        ventana.blit(self.__sup_marcador_izq,(0,0))
        ventana.blit(self.__sup_marcador_der,(self.__resolucion[0] - self.__sup_marcador_der.get_width(),0))

    def render_left_score(self, tablero, turno):
        superficie = pygame.Surface(self.__imagen_barra_amarilla.get_size(),SRCALPHA,32)
        #Copio la barra izquierda del marcador cambiando el color dependiendo del turno
        if turno == BLANCO:
            superficie.blit(self.__imagen_barra_amarilla, (self.__barra.x,self.__barra.y))
            color_fuente_barra_iz = self.__color_negro
        else:
            superficie.blit(self.__imagen_barra_negra, (self.__barra.x,self.__barra.y))
            color_fuente_barra_iz = self.__color_amarillo
        #Copio la bandera blanca sobre la barra
        superficie.blit(self.__imagen_bandera_blanca, (self.__bandera.x,self.__bandera.y))
        marcador_blancas = tablero.get_number_white_pieces()
        if marcador_blancas < 10:
            marcador_blancas = "0" + str(marcador_blancas)
        else:
            marcador_blancas = str(marcador_blancas)
        #Muestro los marcadores
        superficie.blit(self.__fuente.render(marcador_blancas, True, color_fuente_barra_iz), (self.__x_marcador,self.__y_marcador))
        self.__sup_marcador_izq = superficie
        return superficie

    def render_right_score(self, tablero, turno):
        superficie = pygame.Surface(self.__imagen_barra_negra.get_size(),SRCALPHA,32)
        #Copio la barra derecha del marcador
        if turno == NEGRO:
            superficie.blit(self.__imagen_barra_amarilla, (self.__barra.x,self.__barra.y))
            color_fuente_barra_de = self.__color_negro
        else:
            superficie.blit(self.__imagen_barra_negra, (self.__barra.x,self.__barra.y))
            color_fuente_barra_de = self.__color_amarillo
        #Copio la bandera negra sobre la barra
        superficie.blit(self.__imagen_bandera_negra, (self.__bandera.x,self.__bandera.y))
        marcador_negras = tablero.get_number_black_pieces()
        if marcador_negras < 10:
            marcador_negras = "0" + str(marcador_negras)
        else:
            marcador_negras = str(marcador_negras)
        #Muestro los marcadores
        superficie.blit(self.__fuente.render(marcador_negras, True, color_fuente_barra_de), (self.__x_marcador,self.__y_marcador))
        self.__sup_marcador_der = superficie
        return superficie