import os

class Fonts:
    #Variables de clase
    __file_names = {}
    
    #Nombre de los archivos de fuentes
    __file_names['fuente1'] = 'resources/fonts/font.ttf'
    
    @staticmethod
    def get_fonts_file_names():
        return Fonts.__file_names