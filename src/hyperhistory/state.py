from _xml.parser import Parser
from main.constants import INITIAL_STATE
import os

class State:
    def __init__(self):
        self.__habitaciones = {}
        self.__personajes = {}
        self.__precondiciones = []
        self.__acciones = []
        self.__eventos = []
        self.__teclas = {}
        self.__nombre = ""
        self.__nro_max_estados = 17

    def get_max_estados(self):
        return self.__nro_max_estados

    def get_name(self):
        return self.__nombre

    def is_initial_state(self):
        if self.__nombre == INITIAL_STATE:
            return True
        else:
            return False

    def save_state(self, state, main_path):
        f = open(os.path.abspath(main_path + "/data/hyperhistory.xml"))
        p = Parser()
        self.__nombre = state
        elementos = p.find_child_element(state,f)
        for e in elementos:
            if e.get_name() == 'character':
                if e.get_attribute('enable_play') == 'yes':
                    habilitado_juego = True
                else:
                    habilitado_juego = False
                if e.get_attribute('enable_dialogue') == 'yes':
                    habilitado_dialogo = True
                else:
                    habilitado_dialogo = False
                personaje = {}
                personaje['juego'] =  habilitado_juego
                personaje['dialogo'] = habilitado_dialogo
                self.__personajes[e.get_attribute('id')] = personaje.copy()
            elif e.get_name() == 'room':
                if e.get_attribute('enable') == 'yes':
                    habilitada = True
                else:
                    habilitada = False
                hab = {}
                hab['habilitada'] = habilitada
                self.__habitaciones[e.get_attribute('id')] = hab.copy()
            elif e.get_name() == 'key':
                if e.get_attribute('enable') == 'yes':
                    habilitada = True
                else:
                    habilitada = False
                hab = {}
                hab['habilitada'] = habilitada
                self.__teclas[e.get_attribute('id')] = hab.copy()
            elif e.get_name() == 'precondition':
                self.__precondiciones.append(e.get_attribute('name'))
            elif e.get_name() == 'action':
                accion = {}
                accion['nombre'] = e.get_attribute('name')
                accion['consecuencia'] = e.get_attribute('consequences')
                accion['nuevo_estado'] = e.get_attribute('new_state')
                self.__acciones.append(accion.copy())
            elif e.get_name() == 'event':
                event = {}
                event['nombre'] = e.get_attribute('name')
                event['tipo'] = e.get_attribute('type')
                event['consecuencia'] = e.get_attribute('consequences')
                event['nuevo_estado'] = e.get_attribute('new_state')
                self.__eventos.append(event.copy())

    def get_rooms_state(self):
        return self.__habitaciones

    def get_characters_state(self):
        return self.__personajes

    def get_keys_state(self):
        return self.__teclas

    def get_state_events(self):
        return self.__eventos

    def get_state_actions(self):
        return self.__acciones
