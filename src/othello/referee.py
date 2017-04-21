import board, logging
from utils import Coordinate

log = logging.getLogger( 'src.othello.referee' )
log.setLevel( logging.DEBUG )

class Referee:

    """
        Check if is valid to play the color in the position given as a parameter

        Params:
        - color: White or Black
        - posicion: coordinate to play
        - tablero: actual state of board
        Return:
        - True or False
    """
    @staticmethod
    def is_valid_move(color, posicion, tablero):
        # Si la posicion sale del rango del tablero retorna false.
        if not tablero.valid_coord(posicion):
            return False
        # Si la casilla donde se quiere jugar no esta vacia retorna false.
        if tablero.get_casillas()[posicion.x][posicion.y] != board.VACIO:
            return False
        # Se verifica si hay fichas a voltear en al menos una direccion
        dimension = tablero.get_dimension()
        for inc_fila in range(-1,2):
            for inc_col in range(-1,2):
                if Referee.can_turn(color, posicion, inc_fila, inc_col, tablero):
                    return True

        # Si no hay fichas que voltear en ninguna direccion se retorna false.
        return False

    """
        Check in the horizontal and vertical direction if exists pieces to turn

        Params:
        -color: Black or White
        -pos_ini: Start position
        -dir_horizontal: Horizontal direction
        -dir_vertical: Vertical direction
        -tablero: actual state of board
        Return:
        - True or False
    """
    @staticmethod
    def can_turn(color, pos_ini, dir_horizontal, dir_vertical, tablero):
        pos_fin = Coordinate(pos_ini.x + dir_horizontal, pos_ini.y + dir_vertical)
        if not tablero.valid_coord(pos_fin):
            return False

        # Verifica que haya al menos una ficha del color opuesto en esa direccion
        if tablero.get_casillas()[pos_fin.x][pos_fin.y] != -1 * color:
            return False

        # Ejecuto el while mientras la casilla del tablero contenga piezas del color opuesto,
        # es decir no sea VACIO, ni de mi color, ni este fuera del tablero
        while True:
            pos_fin.x += dir_horizontal
            pos_fin.y += dir_vertical
            if not tablero.valid_coord(pos_fin):
                return False
            if tablero.get_casillas()[pos_fin.x][pos_fin.y] == board.VACIO:
                return False
            elif tablero.get_casillas()[pos_fin.x][pos_fin.y] == color:
                return True

    """
        Check if exist at least one move for the color given as a parameter

        Params:
        - color: White or Black
        - tablero: actual state of board
        Return:
        - True or False
    """
    @staticmethod
    def is_at_least_one_move(color, tablero):
        dimension = tablero.get_dimension()
        pos = Coordinate()

        for i in range (0,dimension):
            for j in range (0, dimension):
                pos.x = i
                pos.y = j
                if Referee.is_valid_move(color, pos, tablero):
                    return True

        return False

    """
        Return a list of possibles moves for the color given as a parameter

       Params:
       -color (White or Black)
       -tablero: actual state of board
       Return:
       -List of possible moves
    """
    @staticmethod
    def possibles_moves(color, tablero):
        coordenadas = []
        pos = Coordinate()
        dimension = tablero.get_dimension()

        for i in range (0,dimension):
            for j in range (0, dimension):
                pos.x = i
                pos.y = j
                if Referee.is_valid_move(color, pos, tablero):
                    nueva_pos = Coordinate(i, j)
                    coordenadas.append(nueva_pos)

        return coordenadas

    """
        Calculate the number of successors for the given color in the state of board

        Params:
        -color: White or Black
        -tablero: actual state of board
        Return:
        -Number of successors
    """
    @staticmethod
    def number_of_successors(color, tablero):
        cant_sucesores = 0
        pos = Coordinate()
        dimension = tablero.get_dimension()

        for i in range (0,dimension):
            for j in range (0, dimension):
                pos.x = i
                pos.y = j
                if Referee.is_valid_move(color, pos, tablero):
                    cant_sucesores += 1

        return cant_sucesores