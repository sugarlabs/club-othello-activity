from room import Room
from character import Character, ChPedroMadera, ChDonCano, ChPabloGris, ChSofiaDulce, ChProtasio
from _xml.parser import Parser
import os

class Club:
    def __init__(self, main_path):
        self.__characters = []
        self.__rooms = []
        self.__elevator = {"seleccionado" : False, "direccion" : ""}
        #Al comienzo no hay ninguna habitacion seleccionada
        self.__hab_seleccionada = {"habitacion" : "", "posicion" : ""}

        xml_info = self.__get_xml_info(os.path.abspath(main_path + "/data/club.xml"),"configuration")
        self.__init_characters(xml_info)
        self.__init_rooms(xml_info)
        #Recorro todas las habitaciones y cargo para cada una la habitaciones que le rodean
        xml_info = self.__get_xml_info(os.path.abspath(main_path + "/data/club.xml"),"navigation")
        self.__set_navegation(xml_info)

    def __init_characters(self, config_info):
        for p in config_info:
            if p.get_name() == 'character':
                if p.get_attribute('name') == "pedro madera":
                    self.__characters.append(ChPedroMadera(nombre=p.get_attribute('name'),id=p.get_attribute('id')))
                elif p.get_attribute('name') == "don cano":
                    self.__characters.append(ChDonCano(nombre=p.get_attribute('name'),id=p.get_attribute('id')))
                elif p.get_attribute('name') == "pablo gris":
                    self.__characters.append(ChPabloGris(nombre=p.get_attribute('name'),id=p.get_attribute('id')))
                elif p.get_attribute('name') == "sofia dulce":
                    self.__characters.append(ChSofiaDulce(nombre=p.get_attribute('name'),id=p.get_attribute('id')))
                elif p.get_attribute('name') == "protasio":
                    self.__characters.append(ChProtasio(nombre=p.get_attribute('name'),id=p.get_attribute('id')))
                else:
                    self.__characters.append(Character(nombre=p.get_attribute('name'),id=p.get_attribute('id')))

    def __init_rooms(self, config_info):
        for e in config_info:
            if e.get_name() == 'room':
                piso = False
                if e.get_attribute('floor') == 'yes':
                    piso = True
                personaje = ""
                if e.get_attribute('owner') != '':
                    personaje = self.__get_character(e.get_attribute('owner'))
                self.__rooms.append(Room(nombre=e.get_attribute('name'),especial=piso,duenho=personaje,id=e.get_attribute('id')))
            elif e.get_name() == 'alone_initial_room':
                self.__alone_initial_room = e.get_attribute('id')
            elif e.get_name() == 'shared_initial_room':
                self.__shared_initial_room = e.get_attribute('id')

    #Seteo las habitaciones que le rodean a cada habitacion
    def __set_navegation(self, nav_info):
        hab = ""
        for e in nav_info:
            if e.get_name() == 'room':
                hab = self.__get_room(e.get_attribute('id'))
            if e.get_name() == 'connection':
                if hab != "":
                    if e.get_attribute('up') != '':
                        aux_hab = self.__get_room(e.get_attribute('up'))
                        hab.set_up_room(aux_hab)
                    if e.get_attribute('down') != '':
                        aux_hab = self.__get_room(e.get_attribute('down'))
                        hab.set_down_room(aux_hab)
                    if e.get_attribute('left') != '':
                        aux_hab = self.__get_room(e.get_attribute('left'))
                        hab.set_left_room(aux_hab)
                    if e.get_attribute('right') != '':
                        aux_hab = self.__get_room(e.get_attribute('right'))
                        hab.set_right_room(aux_hab)
                    hab = ""

    def __get_character(self, id):
        for p in self.__characters:
            if p.get_id() == id:
                return p

    def get_character_by_name(self, nombre):
        for p in self.__characters:
            if p.get_name() == nombre:
                return p

    def __get_xml_info(self,archivo,etiqueta):
        f = open(archivo)
        p = Parser()
        return p.find_child_element(etiqueta,f)

    def __set_state(self,state_info):
        self.__set_rooms_state(state_info)
        self.__set_characters_state(state_info)

    def __set_characters_state(self, estado):
        for c in estado.get_characters_state().items():
            id = c[0]
            per = self.__get_character(id)
            per.set_available_to_play(c[1]['juego'])
            per.set_available_to_talk(c[1]['dialogo'])

    def __set_rooms_state(self,estado):
        for r in estado.get_rooms_state().items():
            id = r[0]
            hab = self.__get_room(id)
            hab.set_available(r[1]['habilitada'])

    def __get_room(self, id):
        for r in self.__rooms:
            if r.get_id() == id:
                return r

    def get_rooms(self):
        return self.__rooms

    def get_room_by_name(self, nombre):
        for r in self.__rooms:
            if r.get_name() == nombre:
                return r

    def get_alone_initial_room(self):
        return self.__get_room(self.__alone_initial_room)

    def get_shared_initial_room(self):
        return self.__get_room(self.__shared_initial_room)

    def set_current_state(self, estado_actual):
        self.__set_state(estado_actual)

    def select_room(self, hab, direccion):
        self.__hab_seleccionada["habitacion"] = hab
        self.__hab_seleccionada["posicion"] = direccion

    def room_selected(self):
        return self.__hab_seleccionada

    def select_elevator(self, direccion):
        self.__elevator["seleccionado"] = True
        self.__elevator["direccion"] = direccion

    def unselect_elevator(self):
        self.__elevator["seleccionado"] = False
        self.__elevator["direccion"] = ""

    def get_elevator(self):
        return self.__elevator
