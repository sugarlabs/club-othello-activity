""" Modulo que contiene la defincion de la Clase Element
"""
class Element:
    """La Clase Element se utiliza para almacenar los datos de un
    elemento XML.
    """
    def __init__(self):
        """Constructor de la clase, inicializa las propiedas privadas:
           nombre: almacena el nombre del elemento
           atributos: almacena el o los atributos que contiene el elemento
           texto: diccionario que almacena el texto contenido entre las etiquetas
           de inicio y fin de un elemento. El diccionario contiene dos valores,
           repr para guardar el texto con su codificacion original y str para guardar
           el texto para guardar el texto convertido a string.
        """
        self.__nombre = ""
        self.__atributos = {}
        self.__texto = {'repr':'','str':''}

    def clear(self):
        """ Metodo que se utiliza para cerar las propiedades privadas de la
        clase
        """
        self.__nombre = ""
        self.__texto['repr'] = ''
        self.__texto['str'] = ''

    def set_name(self, nombre):
        """Setter de la propiedad privada nombre"""
        self.__nombre = nombre

    def set_text(self, texto):
        """Setter de la propiedad privada texto"""
        self.__texto['repr'] = repr(texto)
        texto = texto.encode('iso-8859-1')
        self.__texto['str'] = str(texto)

    def get_text(self, key):
        """Getter de la propiedad privada texto"""
        return self.__texto[key]

    def get_name(self):
        """Getter de la propiedad privada nombre"""
        return self.__nombre

    def get_attributes(self):
        """Getter de la propiedad privada atributos, el cual devuelve todos
        los atributos del elemento
        """
        return self.__atributos

    def get_attribute(self, atributo):
        """Getter de la propiedad privada atributos, el cual devuelve solo
        el atributo requerido en el parametro
        """
        return self.__atributos[atributo]

    def set_attributes(self, atributos):
        """Setter de la propiedad privada atributos, recibe un diccionario
        de atributos y los copia a la propiedad atributos de la clase
        """
        self.__atributos = atributos.copy()

    def has_attribute(self, atributo):
        """Metodo que se utiliza para conocer si un elemento tiene un atributo
        determinado pasado como parametro. Retorna True o False dependiendo de
        si contiene o no el atributo pasado como parametro.
        """
        return atributo in self.__atributos

    def is_empty(self):
        """Metodo que se utiliza conocer si un elemento en particular esta vacio,
        para ello se evalua la propiedad nombre y dependiendo de esto se retorna
        True o False.
        """
        if self.__nombre == "":
            return True
        else:
            return False

    def __str__(self):
        """Metodo que se utiliza cuando se desea imprimir como string
        una instancia de la clase element
        """
        return "Nombre: " + self.__nombre + "\nAtributos: " + str(self.__atributos) + "\nTexto: " + self.__texto['str']
