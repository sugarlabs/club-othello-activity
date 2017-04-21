from pygame import mixer, time
from pygame.locals import USEREVENT
from main.constants import IZQUIERDA, DERECHA, ARRIBA, ABAJO, MAS_INFO, SELECCION, CONTAR_FICHAS, \
                           ATRAS
from othello.player import HUMANO, PC, VIRTUAL
from othello.board import BLANCO
from resources.sounds import Sounds
from othello.utils import get_number_word
import thread, sys, pygame, logging

log = logging.getLogger( 'AUDIO' )
log.setLevel( logging.DEBUG )

class Channel():
    def __init__(self):
        try:
            #Inicilializo el modulo para ejecutar sonidos
            if sys.platform.find('win') != -1:
                mixer.pre_init(44100,16,1,4096)
            else:
                mixer.pre_init(44100)
            mixer.init()
            self.__canal = mixer.find_channel()
            self.__cola = []
            self.__ejecutando_sonidos = False
            self.__end_sound_event = False
            self.__new_sound_event = False
            self.__escuchar = True
            self.__sonido_actual = ""
            self.SILENCE_CHANNEL = USEREVENT + 4
            self.nombre_grupo_sonido = ""
        except pygame.error, e:
            raise Exception("ERROR!: " + str(e) + ", al inicilizar el video. La aplicacion se cerrara")

    def new_event(self, event):
        if event.type == self.SILENCE_CHANNEL:
            if self.silence():
                pass
            else:
                event.post(event.Event(self.SILENCE_CHANNEL))

    def get_end_sound_event(self):
        return self.__end_sound_event

    def get_new_sound_event(self):
        return self.__new_sound_event

    def queue(self,sonido):
        self.__cola.append(sonido)

    def get_queue(self):
        return self.__cola

    def play(self, obj_sonido):
        sonido = mixer.Sound(obj_sonido["path_archivo"])
        if obj_sonido["nombre"] != "":
            self.__sonido_actual = obj_sonido["nombre"]
        if obj_sonido["caracteristicas"] != "":
            if "loop" in obj_sonido["caracteristicas"]:
                self.__canal.play(sonido,-1)
            elif "volumen" in obj_sonido["caracteristicas"]:
                derecha = obj_sonido["caracteristicas"]["volumen"]["derecha"]
                izquierda = obj_sonido["caracteristicas"]["volumen"]["izquierda"]
                self.__canal.set_volume(izquierda,derecha)
                self.__canal.play(sonido)
            elif "grupo_sonido" in obj_sonido["caracteristicas"]:
                self.nombre_grupo_sonido = obj_sonido["caracteristicas"]["grupo_sonido"]
                self.__canal.play(sonido)
                if self.__sonido_actual == "wait_input":
                    self.nombre_grupo_sonido = ""
            else:
                log.warn("Faltan acciones para las demas caracteristicas")
        else:
            self.__canal.play(sonido)
        while self.__canal.get_busy():
            time.wait(100)
        self.__end_sound_event = True

    def empty_queue(self):
        if len(self.__cola) > 0:
            return False
        else:
            return True

    def play_next_sound(self):
        if not self.empty_queue():
            sonido = self.__cola.pop(0)
            self.play(sonido)
            self.__ejecutando_sonidos = True
            return True
        else:
            self.__ejecutando_sonidos = False
            return False

    def play_new_sound(self):
        if self.__ejecutando_sonidos:
            return False
        else:
            self.play_next_sound()
            return True

    def start(self):
        self.__escuchar = True

    def stop(self):
        self.__canal.stop()
        self.__cola = []

    def end(self):
        self.__escuchar = False

    def send_new_sound_event(self):
        self.__new_sound_event = True

    def silence(self):
        if self.__canal.get_busy() == 1:
            return False
        else:
            if self.empty_queue():
                return True
            else:
                return False

    def play_sounds_queue(self):
        while not self.empty_queue():
            sonido = self.__cola.pop(0)
            self.play(sonido)

    def listen(self):
        while self.__escuchar:
            if self.__end_sound_event:
                self.__end_sound_event = False
                self.play_next_sound()
            if self.__new_sound_event:
                self.__new_sound_event = False
                self.play_new_sound()

    def get_current_sound_name(self):
        return self.__sonido_actual

class Audio():
    def __init__(self, main_path=""):
        self.__canal = Channel()
        self.__sounds_files = Sounds(main_path)

    def on_channel(self):
        try:
            self.__canal.start()
            thread.start_new_thread(self.__canal.listen,())
        except:
            raise Exception ("Ocurrio un problema en el hilo del canal de Audio")

    def off_channel(self):
        self.__canal.end()
        time.wait(200)

    def stop_sound(self):
        self.__canal.stop()

    def pause_channel(self):
        self.__canal.play_sounds_queue()
        self.__canal.end()

    def restart_channel(self):
        self.on_channel()
        if not self.__canal.empty_queue():
            self.__canal.send_new_sound_event()

    def silence_channel(self):
        return self.__canal.silence()

    def get_sound_name(self):
        return self.__canal.get_current_sound_name()

    def get_sound_group_name(self):
        return self.__canal.nombre_grupo_sonido

    def wait_sound_end(self, tiempo=""):
        if tiempo == "":
            tiempo = 150
        while not self.__canal.silence():
            time.wait(tiempo)

    def play_sound(self, sonido, nombre_sonido="", extra=""):
        obj_sonido = {"path_archivo":sonido,"nombre":nombre_sonido,"caracteristicas":extra}
        self.__canal.queue(obj_sonido)
        self.__canal.send_new_sound_event()

    def play_key_sound(self, key):
        self.__canal.stop()
        self.play_fx_sound("otros", "select")
        if key == IZQUIERDA:
            self.play_voice_sound("otros", "izquierda")
        elif key == DERECHA:
            self.play_voice_sound("otros", "derecha")
        elif key == ARRIBA:
            self.play_voice_sound("otros", "arriba")
        elif key == ABAJO:
            self.play_voice_sound("otros", "abajo")
        elif key == MAS_INFO:
            self.play_voice_sound("otros", "mas_info")
        elif key == SELECCION:
            self.play_voice_sound("otros", "seleccion")
        elif key == CONTAR_FICHAS:
            self.play_voice_sound("otros", "contar_fichas")
        elif key == ATRAS:
            self.play_voice_sound("otros", "atras")
            self.play_fx_sound("otros", "atras")
        else:
            pass

    def play_disabled_key_sound(self):
        canal_aux = mixer.find_channel()
        #self.__canal.stop()
        sonido = mixer.Sound(self.__sounds_files.get_sound_file_name("otros","fx","disabled_key"))
        canal_aux.play(sonido)

    def play_fx_sound(self, nombre, clave, extra=""):
        try:
            sonido = self.__sounds_files.get_sound_file_name(nombre,"fx",clave)
        except:
            raise Exception("Error!, no se encontro el sonido " + str(sonido))
        self.play_sound(sonido,nombre_sonido=clave,extra=extra)

    def play_voice_sound(self, nombre, clave, extra=""):
        try:
            sonido = self.__sounds_files.get_sound_file_name(nombre,"voz",clave)
        except:
            raise Exception("Error!, no se encontro el archivo de sonido")
        self.play_sound(sonido,nombre_sonido=clave,extra=extra)

    def play_character_voice(self, nombre_personaje, clave):
        try:
            sonido = self.__sounds_files.get_sound_file_name("personaje",nombre_personaje,clave)
        except:
            raise Exception("Error!, no se encontro el archivo de sonido")
        self.play_sound(sonido,nombre_sonido=clave)

    def play_init_turn_sounds(self, tablero_g, juego, leer_turno_nro=True, leer_configuracion=True, leer_turno=True):
        hay_jugadas_posibles = False
        if leer_turno_nro:
            self.play_voice_sound("game", "turno_numero", {'grupo_sonido':'inicio_turno'})
            self.play_voice_sound("numero",get_number_word(juego.get_turn_number(),turno=True),{'grupo_sonido':'inicio_turno'})
        if leer_configuracion:
            hay_jugadas_posibles = tablero_g.play_count_pieces_sound(self,juego)
        if hay_jugadas_posibles and leer_turno:
            jugador_de_turno = juego.get_turn()
            if jugador_de_turno.get_name() == HUMANO:
                if jugador_de_turno.get_color() == BLANCO:
                    self.play_voice_sound("game", "jugador_blanco",{'grupo_sonido':'inicio_turno'})
                else:
                    self.play_voice_sound("game", "jugador_negro",{'grupo_sonido':'inicio_turno'})
                self.play_voice_sound("game", "es_su_turno",{'grupo_sonido':'inicio_turno'})
                self.play_voice_sound("game", "seleccione_jugada",{'grupo_sonido':'inicio_turno'})
            elif jugador_de_turno.get_name() == PC:
                if jugador_de_turno.get_color() == BLANCO:
                    self.play_voice_sound("game", "jugador_negro",{'grupo_sonido':'inicio_turno'})
                else:
                    self.play_voice_sound("game", "jugador_blanco",{'grupo_sonido':'inicio_turno'})
                self.play_voice_sound("game", "no_es_su_turno",{'grupo_sonido':'inicio_turno'})
                self.play_voice_sound("game", "examine_tablero",{'grupo_sonido':'inicio_turno'})
            elif jugador_de_turno.get_name() == VIRTUAL:
                if jugador_de_turno.get_color() == BLANCO:
                    self.play_voice_sound("game", "jugador_negro",{'grupo_sonido':'inicio_turno'})
                else:
                    self.play_voice_sound("game", "jugador_blanco",{'grupo_sonido':'inicio_turno'})
                self.play_voice_sound("game", "no_es_su_turno",{'grupo_sonido':'inicio_turno'})
                self.play_voice_sound("game", "espere jugada oponente",{'grupo_sonido':'inicio_turno'})
            if not jugador_de_turno.get_name() == VIRTUAL:
                self.play_fx_sound("otros","wait_input",{'grupo_sonido':'inicio_turno'})

    def play_board_configuration(self, tablero_g, juego):
        tablero_g.play_count_pieces_sound(self,juego)

    def play_end_game_sounds(self, tablero_g, juego):
        self.play_voice_sound("game", "fin_partida")
        tablero_g.play_count_pieces_sound(self,juego)
        ganador = juego.get_final_result()
        if ganador != '':
            self.play_voice_sound("game", "el_jugador")
            if ganador.get_color() == BLANCO:
                self.play_voice_sound("game", "blanco")
            else:
                self.play_voice_sound("game", "negro")
            self.play_voice_sound("game", "gana_la_partida")
        else:
            self.play_voice_sound("game", "es_un_empate")
        self.play_fx_sound("otros","wait_input")
        self.wait_sound_end()

    def play_board_size_sound(self, dim_tablero):
        if dim_tablero == 4:
            self.play_voice_sound("board", "tablero4x4")
        elif dim_tablero == 6:
            self.play_voice_sound("board", "tablero6x6")
        elif dim_tablero == 8:
            self.play_voice_sound("board", "tablero8x8")