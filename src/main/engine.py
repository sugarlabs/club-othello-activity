from hyperhistory.club import Club
from user import User
from constants import IZQUIERDA,DERECHA,ARRIBA,ABAJO,CONTINUAR,SALIR,NAVE,DIAL,PLAY,LIST,MAS_INFO, \
                      ATRAS,SELECCION,CONTAR_FICHAS,ON,OFF,ATAJO_GANAR_JUEGO,ATAJO_PERDER_JUEGO,ATAJO_EMPATAR_JUEGO, ATAJO_PASAR_TUTORIAL
from keys import Keys
from hyperhistory.events import Events
from hyperhistory.dialog import DialogueManager
from hyperhistory.navigation import NavigationManager
from othello.game import Game
from othello.player import *
from othello.board import Board, BLANCO, NEGRO
from othello.gui import GraphicBoard
from othello.ai import Ai
from _xml.parser import Parser
import os, thread, logging
import olpcgames

log = logging.getLogger( 'src.main.engine' )
log.setLevel( logging.DEBUG )

class Engine():
    def __init__(self, main_path="", write_path="", video="", audio="", malla="", actividad_compartida=False):
        if main_path == "":
            raise Exception("Error!, engine necesita el path al directorio principal de la aplicacion para funcionar (Class Engine)")
        if video == "" or audio == "" or malla == "":
            raise Exception("Error!, engine necesita Audio, Video y Malla para funcionar (Class Engine)")
        self.__main_path = main_path
        self.__write_path = write_path
        #Iniciliazo el Audio y Video
        self.__video = video
        self.__audio = audio
        self.__malla = malla
        self.__actividad_compartida = actividad_compartida
        self.__audio.on_channel()
        #Inicializo las teclas
        self.__keys = Keys(main_path)
        #Iniciliazo el club (habitaciones)
        self.__club = Club(main_path)
        #Inicializo el usuario
        if self.__actividad_compartida:
            self.__usuario = User(main_path,write_path,lugar_inicial=self.__club.get_shared_initial_room())
            self.__paso_introduccion = True
            self.change_context(PLAY)
        else:
            self.__usuario = User(main_path,write_path,lugar_inicial=self.__club.get_alone_initial_room())
            self.__paso_introduccion = False
        #Seteo la configuracion del club a los valores del estado actual del usuario
        self.__estado_actual = self.__usuario.get_state()
        self.__club.set_current_state(self.__estado_actual)
        self.__keys.enable_keys(self.__usuario.get_context())
        #Iniciliazo el administrador de navegacion
        self.__navegacion_manager = NavigationManager(self, write_path)
        #Iniciliazo el administrador de dialogos
        self.__dialogo_manager = DialogueManager(engine=self,main_path=main_path,write_path=write_path)
        self.__events = Events()
        self.__accion = {}
        self.__path_archivo_juegos = main_path+"/data/games.xml"
        self.__show_club_introduction()
        self.__juego_mesh = False

    def get_user(self):
        return self.__usuario

    def get_audio(self):
        return self.__audio

    def get_video(self):
        return self.__video

    def get_club(self):
        return self.__club

    def get_keys(self):
        return self.__keys

    def get_dialog_manager(self):
        return self.__dialogo_manager

    def get_navigation_manager(self):
        return self.__navegacion_manager

    def set_action(self, metodo, parametros=""):
        self.__accion = {"metodo":metodo,"parametros":parametros}

    def on_play_mesh_game(self):
        self.__juego_mesh = True

    def off_play_mesh_game(self):
        self.__juego_mesh = False

    def init_game(self, nombre, con_jugadas_posibles=True, nivel=Ai.FACIL):
        parser = Parser()
        archivo_juegos = open(os.path.abspath(self.__path_archivo_juegos))
        elementos = parser.find_child_element("game_"+str(nombre),archivo_juegos)
        fichas_iniciales = []
        if len(elementos) <= 0 :
            raise Exception("No se encontraron elementos para el juego: " + nombre + " en el archivo xml: " + self.__path_archivo_juegos)
        for e in elementos:
            if e.get_name() == 'features':
                board_dim = int(e.get_attribute('board'))
                if e.get_attribute('oponent') == "virtual":
                    #Es un juego de mesh contra Humano
                    jugador1 = Player(BLANCO,HUMANO)
                    jugador2 = Player(NEGRO,VIRTUAL)
                else:
                    #Es un juego contra la PC
                    if e.get_attribute('white') == "user":
                        jugador1 = Player(BLANCO,HUMANO)
                        jugador2 = Player(NEGRO,PC)
                    else:
                        jugador1 = Player(BLANCO,PC)
                        jugador2 = Player(NEGRO,HUMANO)
                if e.get_attribute('initiator') == "white":
                    comienza = BLANCO
                else:
                    comienza = NEGRO
            elif e.get_name() == 'piece':
                ficha = {}
                if e.get_attribute('color') == "black":
                    ficha["color"] = NEGRO
                else:
                    ficha["color"] = BLANCO
                ficha["posicion"] = (int(e.get_attribute('pos_f')),int(e.get_attribute('pos_c')))
                fichas_iniciales.append(ficha)
        tablero_logico = Board(board_dim)
        if nombre == "tutorial1":
            tablero_logico.save_initial_configuration(fichas_iniciales)
        else:
            tablero_logico.set_up(fichas_iniciales)
        self.__video.create_graphic_board(tablero_logico)
        self.juego = Game(self.__video.board,jugador1,jugador2,con_jugadas_posibles,nivel,write_path=self.__write_path)
        if comienza == BLANCO:
            self.juego.set_turn(jugador1)
        else:
            self.juego.set_turn(jugador2)
        self.juego.increase_turn_number()
        if nombre == "mesh":
            self.juego.set_mesh_game(True)
            self.__usuario.set_player(jugador1)
        parser.close()
        archivo_juegos.close()

    def setup_game(self, config, nombre=""):
        tablero_logico = Board(config["tablero"]["dimension"])
        tablero_logico.set_casillas(config["tablero"]["configuracion"])
        tablero_logico.update_pieces_counters()
        self.__video.create_graphic_board(tablero_logico)
        jugador1 = Player(config["jugadores"][0]["color"],VIRTUAL)
        jugador2 = Player(config["jugadores"][1]["color"],HUMANO)
        self.juego = Game(self.__video.board,jugador1,jugador2,write_path=self.__write_path)
        self.juego.set_turn(jugador1)
        self.juego.increase_turn_number()
        if nombre == "mesh":
            self.juego.set_mesh_game(True)
            self.__usuario.set_player(jugador2)

    def __show_club_introduction(self):
        self.__video.club.show_room(self.__usuario.get_current_room())
        if not self.__actividad_compartida:
            self.__audio.play_voice_sound("club","voz_inicio")

    def __join_the_club(self):
        self.__audio.play_fx_sound("club","pasos")
        nueva_hab = self.__usuario.get_current_room().get_up_room()
        self.__paso_introduccion = True
        self.__usuario.set_current_room(nueva_hab)
        if self.__usuario.get_state().is_initial_state():
            self.__video.club.move_to_another_floor(nueva_hab,ARRIBA,extra="introduccion")
            self.change_context(DIAL)
        else:
            self.__video.club.move_to_another_floor(nueva_hab,ARRIBA)
            self.change_context(NAVE)
        self.__begin_game()

    def change_context(self, nuevo_contexto):
        self.__usuario.set_context(nuevo_contexto)
        self.__keys.enable_keys(nuevo_contexto)

    def __begin_game(self):
        self.__run_state_events()

    def __run_state_events(self):
        #Verificar si existe algun evento para el estado actual y ejecutarlo
        eventos_iniciales = self.__estado_actual.get_state_events()
        for evento in eventos_iniciales:
            #thread.start_new_thread(self.__events.run_events,(self, eventos_iniciales))
            self.__events.run_event(self, evento)

    def change_state(self, nuevo_estado):
        self.__usuario.set_state(nuevo_estado)
        self.__estado_actual = self.__usuario.get_state()
        self.__club.set_current_state(self.__estado_actual)
        self.__run_state_events()


    def arrive_input(self, accion):
        if not self.__keys.is_enable(accion):
            self.__audio.play_disabled_key_sound()
        else:
            if accion == SALIR:
                if self.__actividad_compartida:
                    self.__actividad_compartida = False
                    self.__malla.remove_me()
                self.__navegacion_manager.exit_club()
            else:
                if self.__paso_introduccion:
                    if self.__usuario.get_context() == NAVE:
                        self.__audio.play_key_sound(accion)
                        self.__make_nav_action(accion)
                    elif self.__usuario.get_context() == DIAL:
                        if not self.__usuario.interrupt_dialogue():
                            if self.__audio.get_sound_name() == "more_text":
                                self.__audio.play_key_sound(accion)
                                self.__make_dialog_action(accion)
                            else:
                                self.__audio.play_disabled_key_sound()
                        else:
                            self.__audio.play_key_sound(accion)
                            self.__make_dialog_action(accion)
                    elif self.__usuario.get_context() == PLAY:
                        if not self.__usuario.interrupt_sounds() and self.__audio.get_sound_group_name() == "inicio_turno":
                            self.__audio.play_disabled_key_sound()
                        else:
                            self.__audio.play_key_sound(accion)
                            self.__make_play_action(accion)
                    elif self.__usuario.get_context() == LIST:
                        self.__audio.play_key_sound(accion)
                        self.__make_list_action(accion)
                else:
                    self.__audio.play_key_sound(accion)
                    if accion == CONTINUAR:
                        self.__join_the_club()

    def __make_nav_action(self, accion):
        if accion == CONTINUAR:
            hab_sel = self.__club.room_selected()["habitacion"]
            pos_hab_sel = self.__club.room_selected()["posicion"]
            if hab_sel != "":
                if hab_sel.is_available():
                    self.__navegacion_manager.enter_room(hab_sel, pos_hab_sel)
                    if not hab_sel.is_floor():
                    #Es una habitacion
                        if hab_sel.get_name() != "salon de encuentros" and hab_sel.get_name() != "secretaria":
                            self.change_context(DIAL)
                            per_duenho = hab_sel.get_owner()
                            per_duenho.init_room_action(self)
                            self.__accion = {"metodo":per_duenho.close_action,"parametros":(self)}
                        else:
                            if hab_sel.get_name() == "salon de encuentros":
                                try:
                                    ps = olpcgames.ACTIVITY._pservice
                                    self.__audio.play_voice_sound("club","ingresando a la red")
                                    ps.get_activities_async(reply_handler=self._share_join_activity_cb)
                                except Exception, e:
                                    log.debug('Error: ' + str(e) + '. Al intentar usar el presence service (Engine Class)')
                                    self.__audio.play_voice_sound("club","error de conexion")
                                    self.__audio.play_voice_sound("club","saliendo salon desafios")
                                    self.__navegacion_manager.leave_room()
                            elif hab_sel.get_name() == "secretaria":
                                self.change_context(LIST)
                                self.__video.create_selection_list(titulo="OPCIONES DE SECRETARIA",tipo="secretaria")
                                progreso = self.__usuario.get_game_progress()
                                hash_medallas = self.__usuario.get_medals()
                                total_medallas = hash_medallas["bronce"] + hash_medallas["plata"] + hash_medallas["oro"]
                                str_medallas = str(hash_medallas["bronce"])+" BR  "+str(hash_medallas["plata"])+" PL  "+str(hash_medallas["oro"])+" OR  "+str(total_medallas)+" TOT"
                                self.__video.selection_list.add_options([{"descripcion":"Progreso del Juego: "+str(progreso)+"%","id":"progreso_juego-"+str(progreso),"visible":True},{"descripcion":"Medallas: "+str_medallas, "id":"medallas_obtenidas-"+str(hash_medallas["bronce"])+"."+str(hash_medallas["plata"])+"."+str(hash_medallas["oro"]),"visible":True}])
                                self.__video.show_selection_list()
                                self.__audio.play_voice_sound("club","secretaria intro")
                                self.__audio.play_voice_sound("club","secretaria desc")
                                self.__audio.play_voice_sound("club","secretaria info")
                                self.__audio.play_fx_sound("otros","wait_input")
                                self.__video.selection_list.read_option(self.__audio)
                            else:
                                log.error("Nombre de habitacion desconocido! (Engine Class)")
                else:
                    if not hab_sel.is_floor():
                        if hab_sel.get_owner() != "":
                            self.__audio.play_voice_sound("club","bloqueo_acceso_pieza_vocal")
                        else:
                            if hab_sel.get_name() == "salon de encuentros":
                                self.__audio.play_voice_sound("club","bloqueo_acceso_salon_encuentros")
                            else:
                                self.__audio.play_voice_sound("club","bloqueo_acceso_pieza_gral")
                        self.__audio.wait_sound_end()
                        self.__video.club.end_door_animation()
                self.__club.select_room("","")
            elif self.__club.get_elevator()["seleccionado"]:
                if not self.__navegacion_manager.go_to_floor():
                    if self.__usuario.get_state().get_name() == "state1" and self.__usuario.get_current_room().get_name() == "segundo piso":
                        pm = self.__club.get_character_by_name("pedro madera")
                        self.change_context(DIAL)
                        pm.block_third_floor_access(self)
                        self.__accion = {"metodo":pm.close_action,"parametros":(self)}
                    elif self.__usuario.get_current_room().get_name() == "tercer piso":
                        hash_medallas = self.__usuario.get_medals()
                        total_medallas = hash_medallas["bronce"] + hash_medallas["plata"] + hash_medallas["oro"]
                        if int(total_medallas) >= 7 and int(hash_medallas["oro"]) > 0:
                            pass
                        else:
                            self.__audio.play_voice_sound("club","bloqueo_acceso_piso_4")
            else:
                self.__audio.play_voice_sound("club","no habitacion sel")
        elif accion == IZQUIERDA:
            hab_izq = self.__usuario.get_current_room().get_left_room()
            if hab_izq != "":
                self.__navegacion_manager.select_room(hab_izq,accion)
            else:
                print "Desde la habitacion actual no se puede acceder a una habitacion a la izquierda"
        elif accion == DERECHA:
            hab_der = self.__usuario.get_current_room().get_right_room()
            if hab_der != "":
                self.__navegacion_manager.select_room(hab_der, accion)
            else:
                print "Desde la habitacion actual no se puede acceder a una habitacion a la derecha"
        elif accion == ARRIBA:
            self.__navegacion_manager.select_elevator(ARRIBA)
        elif accion == ABAJO:
            self.__navegacion_manager.select_elevator(ABAJO)
        elif accion == MAS_INFO:
            self.__navegacion_manager.more_info()
        elif accion == SELECCION:
            self.__navegacion_manager.selection_more_info()
        elif accion == ATRAS:
            self.__navegacion_manager.leave_room()
            self.change_context(NAVE)
        else:
            #Que pasa si presiono una tecla que no tenga nada que ver con el contexto
            pass

    def _share_join_activity_cb(self, activity_list):
        actividades_compartidas = activity_list
        bundle_club_othello = olpcgames.ACTIVITY.get_bundle_id()
        co_compartido = False
        self.__obj_actividad_compartida = ""
        for self.__obj_actividad_compartida in actividades_compartidas:
            if bundle_club_othello == self.__obj_actividad_compartida.get_property("type"):
                co_compartido = True
                break
        if not co_compartido:
            #Comparto
            try:
                olpcgames.ACTIVITY.share()
                self.__actividad_compartida = True
                self.__malla.set_state(ON)
                self.change_context(PLAY)
                log.info('Comparti Club de Othello en el vecindario, esperando que alguien se una para jugar...')
            except Exception, e:
                log.debug(str(e) +', al intentar compartir una actividad compartida (Engine Class).')
                self.__audio.play_voice_sound("club","error de conexion")
                self.__audio.play_voice_sound("club","saliendo salon desafios")
                self.__navegacion_manager.leave_room()
        else:
            #Me uno
            try:
                olpcgames.ACTIVITY.shared_activity = self.__obj_actividad_compartida
                olpcgames.ACTIVITY._shared_activity = self.__obj_actividad_compartida
                olpcgames.ACTIVITY._join_id = olpcgames.ACTIVITY.shared_activity.connect("joined", self.__malla.joined_cb)
                olpcgames.ACTIVITY.shared_activity.join()
                self.__actividad_compartida = True
                self.__malla.set_state(ON)
                self.change_context(LIST)
                log.info('Me uni a una actividad Club de Othello compartida en el vecindario, listo para jugar...')
            except Exception, e:
                log.debug(str(e) +', al intentar unirme a una actividad compartida (Engine Class).')
                self.__audio.play_voice_sound("club","error de conexion")
                self.__audio.play_voice_sound("club","saliendo salon desafios")
                self.__navegacion_manager.leave_room()

    def __close_dialog_action(self):
        #Cerrar la accion abierta anteriormente
        if self.__accion["parametros"] != "":
            nuevo_contexto = self.__accion["metodo"](self.__accion["parametros"])
        else:
            nuevo_contexto = self.__accion["metodo"]()
        #self.__accion.clear()
        return nuevo_contexto

    def __there_is_action_to_close(self):
        if self.__accion != {}:
            return True
        else:
            return False

    def __make_dialog_action(self, accion):
        if accion == ATRAS:
            self.__dialogo_manager.repeat_dialogue()
        elif accion == ATAJO_PASAR_TUTORIAL:
            if self.__usuario.enable_tutorials_shorcuts():
                if self.__dialogo_manager.get_dialogue_name().find("tutorial") != -1 or self.__dialogo_manager.get_dialogue_name().find("bienvenida") != -1:
                    if self.__there_is_action_to_close():
                        nuevo_contexto = self.__close_dialog_action()
                        #Si el nuevo contexto es igual a vacio significa que no se debe cambiar el contexto porque al cambiar el contexto
                        #se alteran la habitacion/deshabilitacion de las teclas
                        if not nuevo_contexto == "":
                            self.change_context(nuevo_contexto)
        else:
            self.__dialogo_manager.manage_dialogue(accion)
            if self.__dialogo_manager.ended_dialogue():
                if self.__there_is_action_to_close():
                    nuevo_contexto = self.__close_dialog_action()
                    #Si el nuevo contexto es igual a vacio significa que no se debe cambiar el contexto porque al cambiar el contexto
                    #se alteran la habitacion/deshabilitacion de las teclas
                    if not nuevo_contexto == "":
                        self.change_context(nuevo_contexto)

    def __make_play_action(self, accion):
        if accion == CONTINUAR:
            if not self.juego.game_ended():
                if self.__actividad_compartida:
                    if self.__juego_mesh:
                        hizo_jugada = self.juego.play(audio=self.__audio,marcador=self.__video.marcador,ventana=self.__video.ventana)
                        if hizo_jugada:
                            self.__malla.send_end_move_message()
                    else:
                        log.warn("No puede realizar aun una jugada!. Debe esperar a que el otro jugador finalize su jugada")
                else:
                    hizo_jugada = self.juego.play(audio=self.__audio,marcador=self.__video.marcador,ventana=self.__video.ventana)
            else:
                if self.__usuario.get_current_room().get_name() == "habitacion pedro madera" or \
                   self.__usuario.get_current_room().get_name() == "habitacion sofia dulce" or \
                   self.__usuario.get_current_room().get_name() == "habitacion presidente":
                    per_duenho = self.__usuario.get_current_room().get_owner()
                    nuevo_contexto = per_duenho.close_game(self)
                    self.change_context(nuevo_contexto)
                else:
                    #Es el salon de encuentros
                    self.__video.dissapear_game_elements()
                    self.change_context(LIST)
                    self.__audio.play_voice_sound("club","seleccione opcion")
                    self.__video.create_selection_list()
                    self.__video.selection_list.add_options([{"descripcion":"Salir","id":"salir","visible":True},{"descripcion":"Volver a Jugar", "id":"volver_a_jugar","visible":True}])
                    self.__video.show_selection_list()
                    self.__malla.set_state(ON)
        elif accion == IZQUIERDA or accion == DERECHA or accion == ARRIBA or accion == ABAJO:
            self.__video.board.do_move(accion, self.__audio,self.juego.get_game_log_file())
        elif accion == SELECCION:
            self.__video.board.play_box_info_sound(self.__audio)
        elif accion == MAS_INFO:
            self.__video.board.play_possible_moves_sound(self.__audio)
        elif accion == CONTAR_FICHAS:
            self.__video.board.play_count_pieces_sound(self.__audio,self.juego)
        elif accion == ATRAS:
            self.__video.dissapear_game_elements()
            if self.__actividad_compartida:
                self.__actividad_compartida = False
                self.__malla.remove_me()
                self.__malla.set_state(OFF)
            self.__navegacion_manager.leave_room()
            self.change_context(NAVE)
        else:
            if self.__usuario.enable_games_shorcuts():
                if accion == ATAJO_GANAR_JUEGO:
                    self.juego.shorcut_win_game()
                elif accion == ATAJO_PERDER_JUEGO:
                    self.juego.shorcut_lose_game()
                elif accion == ATAJO_EMPATAR_JUEGO:
                    self.juego.shorcut_draw_game()
                per_duenho = self.__usuario.get_current_room().get_owner()
                nuevo_contexto = per_duenho.close_game(self)
                self.change_context(nuevo_contexto)

    def __make_list_action(self, accion):
        if accion == CONTINUAR:
            if not self.__usuario.get_current_room().get_name() == "secretaria":
                self.__video.selection_list.read_option(self.__audio)
                while not self.__audio.silence_channel():
                    self.__video.selection_list.blink_option()
                opcion = self.__video.selection_list.get_selected_option()
                self.__video.remove_selection_list()
                if opcion["id"] == "salir" or opcion["id"] == "salir_pasillo":
                    if not self.__actividad_compartida:
                        self.__video.text_box.disappear(self.__video.ventana)
                        self.__video.dissapear_game_elements()
                    else:
                        if not self.__obj_actividad_compartida == "":
                            self.__malla.remove_me()
                        else:
                            self.__malla.remove_me()
                        self.__malla.set_state(OFF)
                    self.__navegacion_manager.leave_room()
                    self.change_context(NAVE)
                else:
                    if not self.__actividad_compartida:
                        per_duenho = self.__usuario.get_current_room().get_owner()
                        per_duenho.init_list_action(opcion["id"],self)
                        self.__accion = {"metodo":per_duenho.close_action,"parametros":(self)}
                    else:
                        self.__malla.init_list_action(opcion["id"])
        elif accion == ARRIBA or accion == ABAJO:
            self.__video.selection_list.change_selection_options(accion,self.__audio)
        elif accion == SELECCION:
            self.__video.selection_list.option_more_info(self.__audio)
        elif accion == ATRAS:
            if self.__usuario.get_current_room().get_name() == "salon de encuentros":
                if not self.__obj_actividad_compartida == "":
                    #log.debug('Voy a desconectarme de una actividad a la cual me uni')
                    self.__malla.remove_me()
                else:
                    #log.debug('Voy a descompartir una actividad que habia compartido en el vecindario')
                    self.__malla.remove_me()
                self.__malla.set_state(OFF)
            else:
                self.__video.text_box.disappear(self.__video.ventana)
            self.__video.remove_selection_list()
            self.__navegacion_manager.leave_room()
            self.change_context(NAVE)
        else:
            pass

