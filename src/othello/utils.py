import logging

log = logging.getLogger( 'src.othello.utils' )
log.setLevel( logging.DEBUG )

"""
    Modulo que contiene todo lo que no cabe dentro de las otros modulos.
"""

class Coordinate():

    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return "("+str(self.x)+", "+str(self.y)+")"

    """
        Invest the coordinates because x(row) and y(column) in the board are y and x in the screen
    """
    def invest(self):
        return Coordinate(self.y,self.x)

    def set(self, coord):
        self.x = coord.x
        self.y = coord.y

    def equal(self,coord):
        if coord.x == self.x and coord.y == self.y:
            return True
        else:
            return False

    def equal_xy(self, x, y):
        if self.x == x and self.y == y:
            return True
        else:
            return False

    def to_string(self):
        return "("+str(self.x)+", "+str(self.y)+")"


def get_number_word(num, turno=False, medallas=False):
        if num == 1:
            if medallas:
                return "una"
            else:
                return "uno"
        elif num == 2:
            return "dos"
        elif num == 3:
            return "tres"
        elif num == 4:
            return "cuatro"
        elif num == 5:
            return "cinco"
        elif num == 6:
            return "seis"
        elif num == 7:
            return "siete"
        elif num == 8:
            return "ocho"
        elif num == 9:
            return "nueve"
        elif num == 0:
            return "cero"
        elif num == 10:
            return "diez"
        elif num == 11:
            return "once"
        elif num == 12:
            return "doce"
        elif num == 13:
            return "trece"
        elif num == 14:
            return "catorce"
        elif num == 15:
            return "quince"
        elif num == 16:
            return "dieciseis"
        elif num == 17:
            return "diecisiete"
        elif num == 18:
            return "dieciocho"
        elif num == 19:
            return "diecinueve"
        elif num == 20:
            return "veinte"
        elif num == 21:
            if turno:
                return "veintiuno"
            else:
                return "veintiun"
        elif num == 22:
            return "veintidos"
        elif num == 23:
            return "veintitres"
        elif num == 24:
            return "veinticuatro"
        elif num == 25:
            return "veinticinco"
        elif num == 26:
            return "veintiseis"
        elif num == 27:
            return "veintisiete"
        elif num == 28:
            return "veintiocho"
        elif num == 29:
            return "veintinueve"
        elif num == 30:
            return "treinta"
        elif num == 31:
            if turno:
                return "treintayuno"
            else:
                return "treintayun"
        elif num == 32:
            return "treintaydos"
        elif num == 33:
            return "treintaytres"
        elif num == 34:
            return "treintaycuatro"
        elif num == 35:
            return "treintaycinco"
        elif num == 36:
            return "treintayseis"
        elif num == 37:
            return "treintaysiete"
        elif num == 38:
            return "treintayocho"
        elif num == 39:
            return "treintaynueve"
        elif num == 40:
            return "cuarenta"
        elif num == 41:
            if turno:
                return "cuarentayuno"
            else:
                return "cuarentayun"
        elif num == 42:
            return "cuarentaydos"
        elif num == 43:
            return "cuarentaytres"
        elif num == 44:
            return "cuarentaycuatro"
        elif num == 45:
            return "cuarentaycinco"
        elif num == 46:
            return "cuarentayseis"
        elif num == 47:
            return "cuarentaysiete"
        elif num == 48:
            return "cuarentayocho"
        elif num == 49:
            return "cuarentaynueve"
        elif num == 50:
            return "cinquenta"
        elif num == 51:
            if turno:
                return "cinquentayuno"
            else:
                return "cinquentayun"
        elif num == 52:
            return "cinquentaydos"
        elif num == 53:
            return "cinquentaytres"
        elif num == 54:
            return "cinquentaycuatro"
        elif num == 55:
            return "cinquentaycinco"
        elif num == 56:
            return "cinquentayseis"
        elif num == 57:
            return "cinquentaysiete"
        elif num == 58:
            return "cinquentayocho"
        elif num == 59:
            return "cinquentaynueve"
        elif num == 60:
            return "sesenta"
        elif num == 61:
            if turno:
                return "sesentayuno"
            else:
                return "sesentayun"
        elif num == 62:
            return "sesentaydos"
        elif num == 63:
            return "sesentaytres"
        elif num == 64:
            return "sesentaycuatro"
        elif num == 65:
            return "sesentaycinco"
        elif num == 66:
            return "sesentayseis"
        elif num == 67:
            return "sesentaysiete"
        elif num == 68:
            return "sesentayocho"
        elif num == 69:
            return "sesentaynueve"
        elif num == 70:
            return "setenta"
        elif num == 71:
            if turno:
                return "setentayuno"
            else:
                return "setentayun"
        elif num == 72:
            return "setentaydos"
        elif num == 73:
            return "setentaytres"
        elif num == 74:
            return "setentaycuatro"
        elif num == 75:
            return "setentaycinco"
        elif num == 76:
            return "setentayseis"
        elif num == 77:
            return "setentaysiete"
        elif num == 78:
            return "setentayocho"
        elif num == 79:
            return "setentaynueve"
        elif num == 80:
            return "ochenta"
        elif num == 81:
            if turno:
                return "ochentayuno"
            else:
                return "ochentayun"
        elif num == 82:
            return "ochentaydos"
        elif num == 83:
            return "ochentaytres"
        elif num == 84:
            return "ochentaycuatro"
        elif num == 85:
            return "ochentaycinco"
        elif num == 86:
            return "ochentayseis"
        elif num == 87:
            return "ochentaysiete"
        elif num == 88:
            return "ochentayocho"
        elif num == 89:
            return "ochentaynueve"
        elif num == 90:
            return "noventa"
        elif num == 91:
            if turno:
                return "noventayuno"
            else:
                return "noventayun"
        elif num == 92:
            return "noventaydos"
        elif num == 93:
            return "noventaytres"
        elif num == 94:
            return "noventaycuatro"
        elif num == 95:
            return "noventaycinco"
        elif num == 96:
            return "noventayseis"
        elif num == 97:
            return "noventaysiete"
        elif num == 98:
            return "noventayocho"
        elif num == 99:
            return "noventaynueve"
        elif num == 100:
            return "cien"
