from main.constants import ARRIBA, ABAJO, DERECHA, IZQUIERDA

class Room:
    def __init__(self, nombre=-1, disponible=False, utilizada=False, duenho="", especial=False, id=""):
        self.__nombre = nombre
        self.__duenho = duenho
        self.__utilizada = utilizada
        self.__disponible = disponible
        self.__especial = especial
        self.__id = id
        self.__navegacion = {"arriba":"","abajo":"","izquierda":"","derecha":""}

    def used(self,value):
        self.__utilizada = value

    def is_used(self):
        return self.__utilizada

    def set_owner(self,duenho):
        self.__duenho = duenho

    def get_owner(self):
        return self.__duenho

    def is_available(self):
        return self.__disponible

    def set_available(self, valor):
        self.__disponible = valor

    def get_name(self):
        return self.__nombre

    def get_id(self):
        return self.__id

    def is_floor(self):
        return self.__especial

    def set_up_room(self, hab):
        self.__navegacion["arriba"] = hab

    def set_left_room(self, hab):
        self.__navegacion["izquierda"] = hab

    def set_right_room(self, hab):
        self.__navegacion["derecha"] = hab

    def set_down_room(self, hab):
        self.__navegacion["abajo"] = hab

    def get_up_room(self):
        return self.__navegacion["arriba"]

    def get_down_room(self):
        return self.__navegacion["abajo"]

    def get_left_room(self):
        return self.__navegacion["izquierda"]

    def get_right_room(self):
        return self.__navegacion["derecha"]

    def get_availables_rooms(self):
        hab_disponibles = {}
        hab = self.get_left_room()
        if hab != "":
            hab_disponibles[IZQUIERDA] = hab
        hab = self.get_right_room()
        if hab != "":
            hab_disponibles[DERECHA] = hab
        hab = self.get_up_room()
        if hab != "":
            hab_disponibles[ARRIBA] = hab
        hab = self.get_down_room()
        if hab != "":
            hab_disponibles[ABAJO] = hab
        return hab_disponibles

    def equal(self, other):
        if self.__id == other.get_id():
            return True
        else:
            return False

    def __str__(self):
        return "Pieza\nNombre: " + self.__nombre + ", disponible: " + str(self.__disponible)