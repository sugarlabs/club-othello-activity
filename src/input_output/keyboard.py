from io_object import IOObject
from pygame.locals import KEYDOWN,K_KP4,K_KP6,K_KP8,K_KP2,K_KP9,K_KP3,K_ESCAPE,K_KP1,K_KP7,K_NUMLOCK,K_g,K_p,K_e,K_t
from pygame import key
from main.constants import IZQUIERDA,DERECHA,ARRIBA,ABAJO,CONTINUAR,SALIR,MAS_INFO,TECLA_DESCONOCIDA, \
                           SELECCION,ATRAS,CONTAR_FICHAS,ATAJO_PERDER_JUEGO,ATAJO_EMPATAR_JUEGO,ATAJO_GANAR_JUEGO, \
                           ATAJO_PASAR_TUTORIAL
import logging

log = logging.getLogger( 'INPUT' )
log.setLevel( logging.DEBUG )

class Keyboard(IOObject):
    def __init__(self, engine=""):
        self.__teclas_permitidas = [K_KP4,K_KP6,K_KP8,K_KP2,K_KP9,K_KP3,K_ESCAPE,K_KP1,K_KP7,K_g,K_e,K_p,K_t]
        if engine == "":
            raise Exception("Engine no inicilizado")
        else:
            IOObject.__init__(self,engine)

    def new_event(self, event):
        if event.type == KEYDOWN:
            teclas_presionadas = self.__get_pressed_key()
            if not teclas_presionadas == []:
                self.__pressed_key(teclas_presionadas)
            #else:
            #    print "No se encuentra la tecla presionada (Class Keyboard)"

    #Para conocer que tecla o telcas se presionaron, debido a que puede ser una tecla individual o
    #una combinacion de dos teclas
    def __get_pressed_key(self):
        teclas_presionadas = []
        pressed_keys = key.get_pressed()
        for key_constant, pressed in enumerate(pressed_keys):
            if pressed:
                if self.__teclas_permitidas.count(key_constant) == 1:
                    teclas_presionadas.append(key_constant)
        return teclas_presionadas

    def __pressed_key(self,teclas):
        can_teclas_presionadas = len(teclas)
        if can_teclas_presionadas == 1:
            self.__single_key(teclas[0])
        elif can_teclas_presionadas == 2:
            self.__keys_combined(teclas)

    def __keys_combined(self, teclas):
        tecla_1, tecla_2 = teclas[0], teclas[1]
        if (tecla_1 == K_KP3 or tecla_1 == K_KP1) and (tecla_2 == K_KP3 or tecla_2 == K_KP1):
            self.engine.arrive_input(CONTAR_FICHAS)

    def __single_key(self, tecla):
        if tecla == K_KP4:
            #print "Se presiono la tecla izquierda con costante" + str(tecla)
            self.engine.arrive_input(IZQUIERDA)
        elif tecla == K_KP6:
            #print "Se presiono la tecla derecha"
            self.engine.arrive_input(DERECHA)
        elif tecla == K_KP8:
            #print "Se presiono la tecla arriba"
            self.engine.arrive_input(ARRIBA)
        elif tecla == K_KP2:
            #print "Se presiono la tecla abajo"
            self.engine.arrive_input(ABAJO)
        elif tecla == K_KP9:
            #print "Se presiono la tecla continuar"
            self.engine.arrive_input(CONTINUAR)
        elif tecla == K_KP3:
            self.engine.arrive_input(MAS_INFO)
        elif tecla == K_KP1:
            self.engine.arrive_input(SELECCION)
        elif tecla == K_KP7:
            self.engine.arrive_input(ATRAS)
        elif tecla == K_ESCAPE:
            self.engine.arrive_input(SALIR)
        elif tecla == K_p:
            self.engine.arrive_input(ATAJO_PERDER_JUEGO)
        elif tecla == K_e:
            self.engine.arrive_input(ATAJO_EMPATAR_JUEGO)
        elif tecla == K_g:
            self.engine.arrive_input(ATAJO_GANAR_JUEGO)
        elif tecla == K_t:
            self.engine.arrive_input(ATAJO_PASAR_TUTORIAL)
        else:
            self.engine.arrive_input(TECLA_DESCONOCIDA)
            log.warning("Se presiono un tecla sin funcion")