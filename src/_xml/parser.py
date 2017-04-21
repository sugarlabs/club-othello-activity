""" Modulo que contiene un wrapper de la clase expat del modulo xml de la
    libreria de python.
"""
from xml.parsers import expat
from element import Element

class Parser:
    """ Clase Parser

    Esta clase se utiliza para leer los archivos xml, tiene como base
    la clase expat del modulo xml de la libreria de python a la cual se le
    agregaron algunas funcionalidades
    """
    def __init__(self):
        """Constructor de la clase.

        Inicializa las propiedades privadas:
        -parser: la cual contiene el parser expat
        -buscando: propiedad que se utiliza en caso de que no se quiera leer
        todo el archivo xml y solo se necesita buscar un elemento en particular
        -nombre_buscar: se utiliza para almacenar el nombre del elemento a buscar
        en caso que no se quiera leer todo el archivo XML sino buscar un elemento
        en particular.
        -encontrado: se utiliza como bandera para indicar si ya fue o no encontrado
        un elemento en particular.
        -elemento: propiedad en la cual se almacena una instancia de la clase element.
        -vec_elementos: vector en el cual se almacenan los elementos que contiene el archivo XML.
        -attrs: dicccionario en el cual se almacenan los atributos del elemento actual que se
        esta leyendo.
        """
        self.__parser = expat.ParserCreate()
        self.__parser.StartElementHandler = self.__start_element
        self.__parser.EndElementHandler = self.__end_element
        self.__parser.CharacterDataHandler = self.__char_data
        self.__buscando = False
        self.__nombre_buscar = ""
        self.__encontrado = False
        self.__elemento = Element()
        self.__vec_elementos = []
        self.__attrs = {}

    def __start_element(self, name, attrs):
        """Wrapper del metodo del mismo nombre de la clase expat.

        La diferencia con el original es que permite dejar de leer el
        archivo una vez encontrado un elemento en particular.
        """
        if self.__buscando:
            if name == self.__nombre_buscar:
                self.__encontrado = True
                self.__elemento.set_name(repr(name))
                self.__elemento.set_attributes(attrs)
            elif self.__encontrado:
                self.__buscando = False

    def __end_element(self, name):
        """Wrapper del metodo del mismo nombre de la clase expat.

        La diferencia con el original es que permite dejar de leer el
        archivo una vez encontrado un elemento en particular.
        """
        if name == self.__nombre_buscar and self.__encontrado:
            self.__buscando = False

    def __char_data(self, data):
        """Wrapper del metodo del mismo nombre de la clase expat.

        La diferencia con el original es que permite dejar de leer el
        archivo una vez encontrado un elemento en particular.
        """
        if self.__buscando and self.__encontrado:
            self.__elemento.set_text(data)
            self.__buscando = False

    def __start_element_attributes(self, name, attrs):
        """ Metodo para buscar un elemento en particular teniendo en cuenta sus atributos.

        Si encuentra el elemento pedido almacena su nombre y sus atributos en
        las propiedades respectivas, luego setea la bandera encontrado a True.
        Si ya encontro el elemento, la siguiente vez que lea un elemento
        nuevo del archivo XML setea la bandera buscado a False para terminar
        con la busqueda.
        Parametros:
        -name: nombre del elemento a buscar.
        -attrs: atributos por los cuales buscar el elemento.
        """
        if self.__buscando:
            if name == self.__nombre_buscar and attrs == self.__attrs:
                self.__encontrado = True
                self.__elemento.set_name(repr(name))
                self.__elemento.set_attributes(attrs)
            elif self.__encontrado:
                self.__buscando = False

    def __start_element_childs(self, name, attrs):
        """ Metodo que se utiliza cuando se desea encontrar todos los hijos de un
        elemento en particular.

        Basicamente su funcionamiento consiste en buscar el elemento padre, una
        vez encontrado almacena todos sus elementos hijos en la propiedad vec_elementos.
        Paramentros:
        -name: nombre del elemento padre.
        -attrs: atributos del elemento padre (se utiliza solo a modo de compatibilidad con el parser expat)
        """
        if name == self.__nombre_buscar:
            self.__encontre_padre = True
        elif self.__encontre_padre:
            elem = Element()
            elem.set_name(name)
            elem.set_attributes(attrs)
            self.__vec_elementos.append(elem)

    def __char_data_childs(self, data):
        """ Metodo que se utiliza cuando se desea encontrar todos los hijos de un
        elemento en particular.

        Su funcionamiento consiste en guardar el texto entre etiquetas de
        cada uno de los hijos del elemento en particular.
        Parametros:
        -data: texto entre las etiquetas (el parse expat se encarga de proporcionar este parametro)
        """
        if not self.__vec_elementos == []:
            elem = self.__vec_elementos.pop()
            #Solamente si todavia no guarde el texto lo guardo
            if elem.get_text('str') == "":
                elem.set_text(data)
            self.__vec_elementos.append(elem)

    def __end_element_childs(self, name):
        """ Metodo que se utiliza cuando se desea encontrar todos los hijos de un
        elemento en particular.

        Su funcionalidad consiste en setear a False la bandera encontre_padre de forma tal
        para indicar al metodo start_element_childs que se cerro el elemento padre.
        """
        if name == self.__nombre_buscar:
            self.__encontre_padre = False

    def find_element(self, elemento, xml):
        """ Metodo que se utiliza para buscar un elemento en particular sin tener en cuenta sus atributos.

        Parametros:
        -elemento: elemento en particular a buscar.
        -xml: archivo o string xml donde debe buscarse el elemento.
        Retorno:
        Objeto de la clase Element
        """
        self.__buscando = True
        self.__nombre_buscar = elemento
        self.__encontrado = False
        self.__elemento.clear()
        self.parse(xml)
        #if self.__encontrado:
        #    print str(self.__elemento)
        return self.__elemento

    def find_element_attribute(self, elemento, attrs, xml):
        """ Metodo que utiliza para buscar un elemento teniendo en cuenta los atributos del mismo.

        Parametros:
        -elemento: elemento en particular a buscar.
        -attrs: atributos que debe contener el elemento a buscar.
        -xml: archivo o string xml donde debe buscarse el elemento.
        Retorno:
        Objeto de la clase Element
        """
        #print "AHORA VOY A BUSCAR " + str(elemento)
        self.__buscando = True
        self.__nombre_buscar = elemento
        self.__attrs = attrs
        self.__encontrado = False
        self.__elemento.clear()
        self.__parser.StartElementHandler = self.__start_element_attributes
        self.parse(xml)
        #if self.__encontrado:
        #    print str(self.__elemento)
        return self.__elemento

    def find_child_element(self, padre, xml):
        """ Metodo que se utiliza para buscar los hijos de un elemento en particular.

        Parametros:
        -padre: nombre del elemento padre.
        -xml: archivo o string xml donde debe realizarse la buscqueda.
        Retorno:
        Lista de objetos de la clase Element
        """
        self.__encontre_padre = False
        self.__nombre_buscar = padre
        #Cambio las funciones de parseo y utilizo unas especiales para buscar hijos de los elementos
        self.__parser.StartElementHandler = self.__start_element_childs
        self.__parser.EndElementHandler = self.__end_element_childs
        self.__parser.CharacterDataHandler = self.__char_data_childs
        self.parse(xml)
        #for e in self.__vec_elementos:
        #    print str(e)
        return self.__vec_elementos

    def xml_has_element(self, elemento, xml):
        """Metodo que se utiliza para conocer si un archivo xml determinado
        contiene un elemento en particular.

        Paramentros:
        -elemento: elemento a buscar.
        -xml: archivo o string xml sobre el cual se debe realizar la busqueda.
        Retorno:
        -True: si se encontro.
        -False: en caso de que no se encuentre.
        """
        self.__buscando = True
        self.__nombre_buscar = elemento
        self.__encontrado = False
        self.parse(xml)
        return self.__encontrado

    def parse(self, xml):
        """ Metodo que se utiliza antes de comenzar a parsear el xml.

        Su funcion consiste en transformar el parametro xml a string
        si es que el que se recibe no es de ese tipo.
        Paramentros:
        - xml: archivo o string xml.
        """
        if type(xml) == file:
            xml = xml.read()
        xml = unicode(xml,"latin-1").encode('iso-8859-1')
        try:
            self.__read_xml(xml)
        except Exception, e:
            print e

    def __read_xml(self, xml):
        """ Metodo que se utiliza para comenzar a leer el xml.

        Paramentros:
        -xml: string con el formato xml.
        """
        self.__parser.Parse(xml,0)

    def close(self):
        """ Metodo que se utiliza para cerrar el parser xml """
        self.__parser.Parse("", 1)
        del self.__parser

if __name__ == "__main__":
    v = []

    p = Parser()

    f = open("../../data/games.xml")

    v = p.find_child_element("games",f)

    p.close()

