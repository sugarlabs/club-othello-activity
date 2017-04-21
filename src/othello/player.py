from board import BLANCO

HUMANO = 8
PC = -8
VIRTUAL = -9

class Player:
    def __init__(self,color_ficha=BLANCO,nombre=PC):
        self.__color = color_ficha
        self.__nombre = nombre

    def get_color(self):
        return self.__color

    def get_name(self):
        return self.__nombre

    def equal(self,other):
        if self.__color == other.__color and self.__nombre == other.__nombre:
            return True
        else:
            return False

    def __str__(self):
        return "Color:" + str(self.__color) + ", Nombre: " + str(self.__nombre)