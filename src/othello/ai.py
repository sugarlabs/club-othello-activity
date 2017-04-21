from referee import Referee
from utils import Coordinate
from board import *
import logging

MAS_INFI = 100000
MEN_INFI = -100000
MAX = 1
MIN = -1
ESTADO_GANADOR = 50000
ESTADO_PERDEDOR = -50000
ESTADO_EMPATE = 0

log = logging.getLogger( 'src.othello.ai' )
log.setLevel( logging.DEBUG )

class State:
    def __init__(self, tablero, turno=NEGRO, etiqueta=MAX, profundidad=0, cantidad_hnos=0):
        self.tablero = tablero.copy()
        self.etiqueta = etiqueta
        self.profundidad = profundidad
        self.turno = turno
        self.cantidad_hnos = cantidad_hnos
        #Guardo la coordenada para llegar al mejor sucesor de este estado
        self.mejor_sucesor = Coordinate()
        #Guardo la accion que dio nacimiento al estado
        self.iniciador = Coordinate()

class Ai:
    #NIVELES
    FACIL = 1
    MEDIO = 2
    DIFICIL = 3

    def __init__(self, nivel=1):
        if nivel == Ai.FACIL:
            self.__profundidad_maxima = 1
            self.__frontera_peso = 1      #Cuanto mas fichas tengas en la frontera es peor
            self.__movilidad_peso = 0     #Cuantas jugadas posible se tiene
            self.__estabilidad_peso = 0   #Cuantas mas fichas logres estabilizar en la jugada mejor
            self.__diferencia_cantidad_fichas_peso = 8
        elif nivel == Ai.MEDIO:
            self.__profundidad_maxima = 2
            self.__frontera_peso = 1      #Cuanto mas fichas tengas en la frontera es peor
            self.__movilidad_peso = 0     #Cuantas jugadas posible se tiene
            self.__estabilidad_peso = 3   #Cuantas mas fichas logres estabilizar en la jugada mejor
            self.__diferencia_cantidad_fichas_peso = 1
        elif nivel == Ai.DIFICIL:
            self.__profundidad_maxima = 3
            self.__frontera_peso = 2      #Cuanto mas fichas tengas en la frontera es peor
            self.__movilidad_peso = 1     #Cuantas jugadas posible se tiene
            self.__estabilidad_peso = 5  #Cuantas mas fichas logres estabilizar en la jugada mejor
            self.__diferencia_cantidad_fichas_peso = 4
        else:
            raise Exception("Nivel desconocido (Ai Class)")
        #Guardo la ultima jugada de la PC
        self.__ultima_jugada = Coordinate(0,0)

    def get_last_move(self):
        return self.__ultima_jugada

    def play(self, tablero, turno):
        profundidad_raiz = 0
        cantidad_hnos_raiz = 0
        if Referee.is_at_least_one_move(turno, tablero):
            estado_raiz = State(tablero,turno,MAX,profundidad_raiz,cantidad_hnos_raiz)
            self.__negamax(estado_raiz, MEN_INFI, MAS_INFI)
            self.__ultima_jugada.set(estado_raiz.mejor_sucesor)
            return True
        else:
            return False

    def __negamax(self, estado, alpha, beta):
        if self.__is_goal_state(estado):
            return self.__goal_state_value(estado)
        elif self.__is_leaf(estado):
            l = self.__value(estado)
            return l
        else:
            e = MEN_INFI
            n_estados = self.__childrens(estado)
            for nuevo_estado in n_estados:
                e = -1 * self.__negamax(nuevo_estado, -1*beta, -1*alpha)
                if beta <= e:
                    return e
                if alpha < e:
                    alpha = e
                    estado.mejor_sucesor = nuevo_estado.iniciador
            return e

    def __is_goal_state(self,estado):
        #Si no existen mas jugadas para ninguno de los colores con el tablero actual entonces el juego termino y estamos en una hoja
        if not Referee.is_at_least_one_move(estado.turno, estado.tablero):
            if not Referee.is_at_least_one_move(-1*estado.turno, estado.tablero):
                return True
            else:
                return False
        else:
            return False

    def __goal_state_value(self,estado):
        diferencia_fichas = estado.tablero.get_can_fichas_blancas() - estado.tablero.get_can_fichas_negras()
        #Ganaron las blancas
        if diferencia_fichas > 0:
            if estado.turno == BLANCO:
                return ESTADO_GANADOR + diferencia_fichas
            else:
                return ESTADO_PERDEDOR + diferencia_fichas
        #Ganaron las negras
        elif diferencia_fichas < 0:
            if estado.turno == NEGRO:
                return ESTADO_GANADOR + diferencia_fichas
            else:
                return ESTADO_PERDEDOR + diferencia_fichas
        #Empate
        else:
            return ESTADO_EMPATE

    def __is_leaf(self,estado):
        #Si la profundidad del nodo actual es mayor (nunca deberia llegar) o igual ya estamos en la hoja del recorrido actual
        if estado.profundidad >= self.__profundidad_maxima:
            return True
        else:
            if len(Referee.possibles_moves(estado.turno,estado.tablero)) == 0:
                return True
            else:
                return False

    def __childrens(self,estado):
        n_etiqueta = estado.etiqueta * -1
        n_profundidad = estado.profundidad + 1
        n_turno = estado.turno * -1
        aux_tablero = Board(estado.tablero.get_dimension())
        aux_tablero.set_casillas(estado.tablero.get_casillas())
        nuevos_estados = []

        lista_jugadas = Referee.possibles_moves(estado.turno,estado.tablero)
        can_hijos = len(lista_jugadas)
        for jugada in lista_jugadas:
            aux_tablero.set_piece_and_turn_oponent_pieces(jugada,estado.turno)
            #Creo el nuevo estado
            n_estado = State(aux_tablero,n_turno,n_etiqueta,n_profundidad,can_hijos)
            n_estado.iniciador = jugada
            nuevos_estados.append(n_estado)
            aux_tablero.set_casillas(estado.tablero.get_casillas())

        return nuevos_estados

    def __value(self,estado):
        tablero = estado.tablero
        if estado.turno == BLANCO:
            fichas_jugador = tablero.get_can_fichas_blancas()
            fichas_oponente = tablero.get_can_fichas_negras()
        else:
            fichas_jugador = tablero.get_can_fichas_negras()
            fichas_oponente = tablero.get_can_fichas_blancas()
        movimientos_validos_oponente = estado.cantidad_hnos
        jugador_frontera = self.__border_pieces(tablero, estado.turno)
        oponente_frontera = self.__border_pieces(tablero, -1*estado.turno)
        movimientos_validos = Referee.number_of_successors(estado.turno, tablero)
        fichas_estables_jugador = self.__stable_pieces(tablero, estado.turno)
        fichas_estables_oponente = self.__stable_pieces(tablero, -1*estado.turno)
        dif_can_fichas = fichas_jugador - fichas_oponente

        v = self.__frontera_peso * (oponente_frontera - jugador_frontera) + self.__movilidad_peso * estado.turno * (movimientos_validos - movimientos_validos_oponente) + self.__estabilidad_peso * (fichas_estables_jugador - fichas_estables_oponente) + self.__diferencia_cantidad_fichas_peso * dif_can_fichas
        return v

    def __border_pieces(self,tablero, color):
        can_fichas_frontera = 0
        dim = tablero.get_dimension()

        for i in xrange(0,dim):
            for j in xrange(0,dim):
                es_frontera = False
                if tablero.get_valor_casilla(i,j) == color:
                    aux_coord = Coordinate()
                    for inc_fila in xrange(-1,2):
                        for inc_col in xrange(-1,2):
                            aux_coord.x = i + inc_fila
                            aux_coord.y = j + inc_col
                            if not (inc_fila == 0 and inc_col == 0 and tablero.valid_pos(aux_coord) and tablero.get_valor_casilla(aux_coord.x,aux_coord.y) == VACIO):
                                es_frontera = True
                                inc_fila = 2
                                break
                if es_frontera:
                    can_fichas_frontera += 1

        return can_fichas_frontera

    #Retorna el numero de fichas estables del color dado.
    def __stable_pieces(self,tablero, color):
        can_fichas_estables = 0
        dim = tablero.get_dimension()

        estables = self.__number_stable_boxes(tablero)

        for i in xrange(0,dim):
            for j in xrange(0,dim):
                if tablero.get_valor_casilla(i,j) == color and estables[i][j]:
                    can_fichas_estables += 1

        return can_fichas_estables

    #Retorna una matriz que indica cuales casillas son estables, es decir,
    #cuales casillas ya no pueden ser volteadas en lo que resta del juego.
    def __number_stable_boxes(self,tablero):
        pos = Coordinate()
        estables = []
        dim = tablero.get_dimension()
        for _ in xrange(dim):
            estables.append([False]*dim)

        cambio_estado = True
        while (cambio_estado):
            cambio_estado = False
            for i in xrange(0,dim):
                for j in xrange(0,dim):
                    pos.x = i
                    pos.y = j
                    if tablero.get_valor_casilla(i,j) != VACIO and not estables[i][j] and not self.__can_turn(pos, tablero, estables):
                        estables[i][j] = True
                        cambio_estado = True

        return estables

    #Retorna false si la ficha en dicha casilla ya no puede ser volteada en lo que resta del juego.
    #Una ficha puede ser volteada si hay una casilla vacia a ambos lados o
    #si hay una casilla vacia a un lado y una ficha inestable o una del contrario al otro lado.
    def __can_turn(self,casilla,tablero,estables):
        dim = tablero.get_dimension()
        #Obtiene el color de la ficha.
        color_ficha = tablero.get_valor_casilla(casilla.x,casilla.y)

        #Verifica cada eje posible (horizontal, vertical y diagonales)
        #Se verifica horizontalmente
        lado_uno_vacio = False
        lado_uno_inseguro = False
        lado_dos_vacio = False
        lado_dos_inseguro = False
        #Lado izquierdo.
        j = 0
        while j < casilla.y and not lado_uno_vacio:
            if tablero.get_valor_casilla(casilla.x,j) == VACIO:
                lado_uno_vacio = True
            elif tablero.get_valor_casilla(casilla.x,j) != color_ficha or not estables[casilla.x][j]:
                lado_uno_inseguro = True
            j += 1
        #Lado derecho.
        j = casilla.y + 1
        while j < dim and not lado_dos_vacio:
            if tablero.get_valor_casilla(casilla.x,j) == VACIO:
                lado_dos_vacio = True
            elif tablero.get_valor_casilla(casilla.x,j) != color_ficha or not estables[casilla.x][j]:
                lado_dos_inseguro = True
            j += 1
        if (lado_uno_vacio and lado_dos_vacio) or (lado_uno_vacio and lado_dos_inseguro) or (lado_uno_inseguro and lado_dos_vacio):
            return True

        #Se verifica verticalmente.
        lado_uno_vacio = False
        lado_dos_vacio = False
        lado_uno_inseguro = False
        lado_dos_inseguro = False
        #Hacia arriba.
        i = 0
        while i < casilla.x and not lado_uno_vacio:
            if tablero.get_valor_casilla(i,casilla.y) == VACIO:
                lado_uno_vacio = True
            elif tablero.get_valor_casilla(i,casilla.y) != color_ficha or not estables[i][casilla.y]:
                lado_uno_inseguro = True
            i += 1
        #Hacia abajo.
        i = casilla.x + 1
        while i < dim and not lado_dos_vacio:
            if tablero.get_valor_casilla(i,casilla.y) == VACIO:
                lado_dos_vacio = True
            elif tablero.get_valor_casilla(i,casilla.y) != color_ficha or not estables[i][casilla.y]:
                lado_dos_inseguro = True
            i += 1
        if (lado_uno_vacio and lado_dos_vacio) or (lado_uno_vacio and lado_dos_inseguro) or (lado_uno_inseguro and lado_dos_vacio):
            return True

        #Se verifica la diagonal \
        lado_uno_vacio = False
        lado_dos_vacio = False
        lado_uno_inseguro = False
        lado_dos_inseguro = False
        #Arriba izquierda.
        i = casilla.x - 1
        j = casilla.y - 1
        while i >= 0 and j >= 0 and not lado_uno_vacio:
            if tablero.get_valor_casilla(i,j) == VACIO:
                lado_uno_vacio = True
            elif tablero.get_valor_casilla(i,j) != color_ficha or not estables[i][j]:
                lado_uno_inseguro = True
            i = i - 1
            j = j - 1
        #Abajo derecha.
        i = casilla.x + 1
        j = casilla.y + 1
        while i < dim and j < dim and not lado_dos_vacio:
            if tablero.get_valor_casilla(i,j) == VACIO:
                lado_dos_vacio = True
            elif tablero.get_valor_casilla(i,j) != color_ficha or not estables[i][j]:
                lado_dos_inseguro = True
            i += 1
            j += 1
        if (lado_uno_vacio and lado_dos_vacio) or (lado_uno_vacio and lado_dos_inseguro) or (lado_uno_inseguro and lado_dos_vacio):
            return True

        #Se verifica la diagonal /
        lado_uno_vacio = False
        lado_dos_vacio = False
        lado_uno_inseguro = False
        lado_dos_inseguro = False
        #Arriba derecha.
        i = casilla.x - 1
        j = casilla.y + 1
        while i >= 0 and j < dim and not lado_uno_vacio:
            if tablero.get_valor_casilla(i,j) == VACIO:
                lado_uno_vacio = True
            elif tablero.get_valor_casilla(i,j) != color_ficha or not estables[i][j]:
                lado_uno_inseguro = True
            i = i - 1
            j += 1
        #Abajo izquierda.
        i = casilla.x + 1
        j = casilla.y - 1
        while i < dim and j >= 0 and not lado_dos_vacio:
            if tablero.get_valor_casilla(i,j) == VACIO:
                lado_dos_vacio = True
            elif tablero.get_valor_casilla(i,j) != color_ficha or not estables[i][j]:
                lado_dos_inseguro = True
            i += 1
            j = j - 1
        if (lado_uno_vacio and lado_dos_vacio) or (lado_uno_vacio and lado_dos_inseguro) or (lado_uno_inseguro and lado_dos_vacio):
            return True

        #Todas las direcciones son estables, la casilla es estable.
        return False


