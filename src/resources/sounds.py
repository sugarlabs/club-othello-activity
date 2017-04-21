import os
from _xml.parser import Parser

class Sounds:
    def __init__(self, main_path):
        self.__main_path = main_path    
    
    def set_main_path(self, path):
        self.__main_path = path
    
    def get_sound_file_name(self, categoria="",tipo="",nombre=""):
        self.__f = open(os.path.abspath(self.__main_path + "/data/resources.xml"))
        self.__parser = Parser()
        attrs = {'type' : tipo, 'name' : nombre}
        elemento = self.__parser.find_element_attribute(categoria,attrs,self.__f)
        if elemento.is_empty():
            raise Exception("No se encontro el elemento en el archivo XML (Sounds Class)")
        self.__f.close()
        self.__parser.close()
        return os.path.abspath(self.__main_path+elemento.get_text('str'))
