import os, logging
from _xml.parser import Parser
from main.constants import TECLA_DESCONOCIDA

log = logging.getLogger( 'src.main.keys' )
log.setLevel( logging.DEBUG )

class Key:
    def __init__(self, nombre="", id=-1, habilitada=False, constante=""):
        self.__nombre = nombre
        self.__id = id
        self.__habilitada = habilitada
        self.__constante = int(constante)

    def get_name(self):
        return self.__nombre

    def set_name(self, nombre):
        self.__nombre = nombre

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def enable(self):
        return self.__habilitada

    def set_enable(self, habilitada):
        self.__habilitada = habilitada

    def set_constant(self, constante):
        self.__constante = constante

    def get_constant(self):
        return self.__constante

class Keys:
    def __init__(self, main_path=""):
        self.__keys = []
        self.__main_path = main_path
        try:
            xml_info = self.__get_xml_info(os.path.abspath(self.__main_path+"/data/keys.xml"),"configuration")
            self.__init_keys(xml_info)
        except Exception, e:
            print e
            raise Exception("Problemas al inicializar las teclas (Keys Class)")


    def __get_xml_info(self,archivo,etiqueta):
        f = open(archivo)
        p = Parser()
        elementos = p.find_child_element(etiqueta,f)
        p.close()
        f.close()
        return elementos

    def __init_keys(self, config_info):
        for k in config_info:
            if k.get_name() == 'key':
                self.__keys.append(Key(nombre=k.get_attribute('name'),id=k.get_attribute('id'),constante=k.get_attribute('constant')))

    def __get_key_by_id(self, id):
        for k in self.__keys:
            if k.get_id() == id:
                return k

    def get_key_by_constant(self, constant):
        for k in self.__keys:
            if k.get_constant() == constant:
                return k

    def __get_key_by_name(self, nombre):
        for k in self.__keys:
            if k.get_name() == nombre:
                return k

    def set_current_state(self, estado_actual):
        for k in estado_actual.get_keys_state().items():
            id = k[0]
            key = self.__get_key_by_id(id)
            key.set_enable(k[1]['habilitada'])

    def enable_keys(self, contexto):
        etiqueta = 'context_' + str(contexto)
        xml_info = self.__get_xml_info(os.path.abspath(self.__main_path+"/data/keys.xml"),etiqueta)
        for k in xml_info:
            key = self.__get_key_by_id(k.get_attribute('id'))
            if k.get_attribute('enable') == 'yes':
                key.set_enable(True)
            else:
                key.set_enable(False)

    def enable_key(self, key_constant):
        key = self.get_key_by_constant(key_constant)
        key.set_enable(True)

    def enable_move_keys(self):
        tecla = self.__get_key_by_name("izquierda")
        tecla.set_enable(True)
        tecla = self.__get_key_by_name("derecha")
        tecla.set_enable(True)
        tecla = self.__get_key_by_name("arriba")
        tecla.set_enable(True)
        tecla = self.__get_key_by_name("abajo")
        tecla.set_enable(True)
        tecla = self.__get_key_by_name("seleccion")
        tecla.set_enable(True)

    #def enable_keys(self, keys):
    #    pass

    def disable_keys(self, teclas, contexto):
        for t in teclas:
            self.disable_key(t, contexto)

    def disable_key(self, key_constant, contexto):
        etiqueta = 'context_' + str(contexto)
        xml_info = self.__get_xml_info(os.path.abspath(self.__main_path+"/data/keys.xml"),etiqueta)
        for k in xml_info:
            key = self.__get_key_by_id(k.get_attribute('id'))
            if key.get_constant() == key_constant:
                if k.get_attribute('enable') == 'no':
                    key.set_enable(False)

    #key como constante
    def is_enable(self, key_constant):
        for k in self.__keys:
            if k.get_constant() == key_constant:
                return k.enable()
        if key_constant == TECLA_DESCONOCIDA:
            return False

    def __str__(self):
        cad = "\n"
        for k in self.__keys:
            if k.enable():
                cad += "Tecla: " + str(k.get_name()) + " habilitada\n"
            else:
                cad += "Tecla: " + str(k.get_name()) + " deshabilitada\n"
        return cad
