from utils import Coordinate
from referee import Referee
import logging

#Constantes
VACIO = 0
BLANCO = 1
NEGRO = -1

log = logging.getLogger( 'src.othello.board' )
log.setLevel( logging.DEBUG )

class Board:
    def __init__(self, d=4, v=VACIO):
        self.__casilla = []
        self.__dimension = d
        #Lleno el tablero de espacios vacios
        for _ in xrange(d):
            self.__casilla.append([v]*d)
        self.__can_fichas_blancas = 0
        self.__can_fichas_negras = 0
        self.__conf_inicial = []

    def set_up(self, conf_inicial=[]):
        if not conf_inicial == []:
            for pieza in conf_inicial:
                self.__casilla[pieza["posicion"][0]][pieza["posicion"][1]] = pieza["color"]
            self.update_pieces_counters()
        elif not self.__conf_inicial == []:
            for pieza in self.__conf_inicial:
                self.__casilla[pieza["posicion"][0]][pieza["posicion"][1]] = pieza["color"]
            self.update_pieces_counters()
        else:
            #Coloco las fichas iniciales
            pos_inicial = (self.__dimension/2) - 1
            self.__casilla[pos_inicial][pos_inicial] = BLANCO
            self.__casilla[pos_inicial][pos_inicial+1] = NEGRO
            self.__casilla[pos_inicial+1][pos_inicial] = NEGRO
            self.__casilla[pos_inicial+1][pos_inicial+1] = BLANCO
            #Inicializo las variables donde contar la cantidad de fichas negras y blancas en el tablero
            self.__can_fichas_blancas = 2
            self.__can_fichas_negras = 2

    def save_initial_configuration(self, conf_inicial):
        self.__conf_inicial = conf_inicial

    def get_dimension(self):
        return self.__dimension

    def view(self):
        for i in xrange(self.__dimension):
            print self.__casilla[i]

    def state(self):
        return self.__casilla

    def get_casillas(self):
        return self.__casilla

    def set_casillas(self,mat_casillas):
        try:
            for i in xrange(0,self.__dimension):
                for j in xrange(0, self.__dimension):
                    self.__casilla[i][j] = mat_casillas[i][j]
        except:
            raise Exception("No se pueden copiar las casillas de un tablero en el otro")

    def copy(self):
        n_tablero = Board(self.__dimension)
        n_tablero.set_casillas(self.get_casillas())
        n_tablero.__can_fichas_blancas = self.__can_fichas_blancas
        n_tablero.__can_fichas_negras = self.__can_fichas_negras
        return n_tablero

    def get_can_fichas_blancas(self):
        return self.__can_fichas_blancas

    def get_can_fichas_negras(self):
        return self.__can_fichas_negras

    def valid_pos(self, pos):
        if pos < 0 or pos > self.__dimension-1:
            return False
        return True

    def get_valor_casilla(self,i,j):
        return self.__casilla[i][j]

    def valid_coord(self, coord):
        if not self.valid_pos(coord.x) or not self.valid_pos(coord.y):
            return False
        return True

    """
        Set the piece in the coordinate given as a parameter and turn the opponent pieces

        Params:
        - coord: coordinate to set the piece
        - color: color of the piece
        Return:
        - True if it is a valid move, False otherwise
    """
    def set_piece(self, coord, color):
        if self.valid_coord(coord):
            #Verifico que sea una jugada valida
            if Referee.is_valid_move(color, coord, self):
                self.__casilla[coord.x][coord.y] = color
                self.update_pieces_counters()
                return True
            else:
                return False
        else:
            return False

    def set_piece_and_turn_oponent_pieces(self, coord, color):
        self.__casilla[coord.x][coord.y] = color
        #Doy vuelta las piezas del oponente
        self.turn_pieces(color, coord)

    def turn_pieces(self, color, pos_ini):
        pos_fin = Coordinate(pos_ini.x, pos_ini.y)

        for inc_fila in xrange(-1,2):
            for inc_col in xrange(-1,2):
                pos_fin.x = pos_ini.x + inc_fila
                pos_fin.y = pos_ini.y + inc_col
                #Verifica que haya al menos una ficha del color opuesto para voltear
                if Referee.can_turn(color, pos_ini, inc_fila, inc_col, self):
                    #Voltear las fichas
                    while True:
                        self.__casilla[pos_fin.x][pos_fin.y] = color
                        pos_fin.x += inc_fila
                        pos_fin.y += inc_col
                        if not self.__casilla[pos_fin.x][pos_fin.y] == -color:
                            break
        #Actualizo los contadores de las fichas blancas o negras dependiendo del color
        self.update_pieces_counters()

    def turn_pieces2(self, coord, color):
        self.__casilla[coord.x][coord.y] = color
        #Actualizo los contadores de las fichas blancas o negras dependiendo del color
        self.update_pieces_counters()

    def get_lines(self,color,coord):
        pos_fin = Coordinate(coord.x,coord.y)
        pos_inicial = Coordinate(coord.x,coord.y)
        can_fichas_volteables = 0
        vec_lineas = []
        for inc_fila in xrange(-1,2):
            for inc_col in xrange(-1,2):
                pos_fin.x = pos_inicial.x + inc_fila
                pos_fin.y = pos_inicial.y + inc_col
                #Verifica que haya al menos una ficha del color opuesto para voltear
                if Referee.can_turn(color, pos_inicial, inc_fila, inc_col, self):
                    hash_linea = {}
                    vec_casillas = []
                    #Contar las fichas volteables en esa linea
                    while True:
                        can_fichas_volteables += 1
                        vec_casillas.append(Coordinate(pos_fin.x,pos_fin.y))
                        pos_fin.x += inc_fila
                        pos_fin.y += inc_col
                        if not self.__casilla[pos_fin.x][pos_fin.y] == -color:
                            break
                    hash_linea["casilla_inicial"] = pos_inicial
                    hash_linea["casilla_final"] =  Coordinate(pos_fin.x,pos_fin.y)
                    hash_linea["can_fichas_volteables"] = can_fichas_volteables
                    hash_linea["casillas_volteables"] = vec_casillas
                    vec_lineas.append(hash_linea)
                    can_fichas_volteables = 0

        return vec_lineas

    def update_pieces_counters(self):
        self.__can_fichas_blancas = 0
        self.__can_fichas_negras = 0
        for i in xrange(self.__dimension):
            for j in xrange(self.__dimension):
                if self.__casilla[i][j] == BLANCO:
                    self.__can_fichas_blancas += 1
                elif self.__casilla[i][j] == NEGRO:
                    self.__can_fichas_negras += 1

    def __update_number_pieces(self,color,i=-1,j=-1):
        if i != -1 and j != - 1:
            if self.__casilla[i][j] == BLANCO:
                self.__can_fichas_blancas -= 1
            elif self.__casilla[i][j] == NEGRO:
                self.__can_fichas_negras -= 1
        if color == BLANCO:
            self.__can_fichas_blancas += 1
        elif color == NEGRO:
            self.__can_fichas_negras += 1

    def get_number_white_pieces(self):
        return self.__can_fichas_blancas

    def get_number_black_pieces(self):
        return self.__can_fichas_negras

    #Se utilizan los metodos de abajo solo para el caso en que se quiere terminar
    #una partida de forma rapida
    def set_can_fichas_blancas(self, valor):
        self.__can_fichas_blancas = valor

    def set_can_fichas_negras(self, valor):
        self.__can_fichas_negras = valor