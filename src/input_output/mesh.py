from io_object import IOObject
import olpcgames, logging, pickle, os
from olpcgames import mesh
from othello.utils import Coordinate
from main.constants import ESPERANDO_OPONENTE, JUGANDO, ON, OFF, PLAY, LIST
import pygame.event as PEvent
from pyfestival import Festival

log = logging.getLogger( 'MESH' )
log.setLevel( logging.DEBUG )


class Mesh(IOObject):
    def __init__(self, write_path="", audio="", video=""):
        if write_path == "":
            raise Exception("Error!, mesh necesita el path al directorio de escritura de la aplicacion para funcionar (Class Mesh)")
        if audio == "":
            raise Exception("Error!, mesh necesita Audio para funcionar (Class Mesh)")
        if video == "":
            raise Exception("Error!, mesh necesita Video para funcionar (Class Mesh)")
        self.__write_path = write_path
        self.__audio = audio
        self.__video = video
        self._buddies = {}
        self.__contrarios = []
        self.__can_contrarios = 0
        self.__conf_men_juego = 0
        self.__estado = OFF
        self.__hay_oponente_esperando = False
        self.__festival = Festival()
        self.__tube_id = 0
        self.__oponente = ""
        self.__estados_activos = [ON, ESPERANDO_OPONENTE, JUGANDO]

    def set_engine(self, engine):
        self.__engine = engine

    def new_event(self, event):
        if self.__estado in self.__estados_activos:
            if event.type == olpcgames.CONNECT:
                self.__tube_id = event.id
                self.__audio.play_voice_sound("club","conexion exitosa")
                log.debug("Participantes: "  + str(mesh.get_participants()))
                self.__set_up()
            elif event.type == olpcgames.PARTICIPANT_ADD:
                # create a new participant display value...
                current = self._buddies.get( event.handle )
                if not current:
                    if current is False:
                        self.remove_buddy( current )
                    else:
                        def on_buddy( buddy, event=event ):
                            """Process update from the network telling us about a buddy
                            Note: this function runs in the wrapper's thread, *not* the Pygame thread!"""
                            log.info( '''Newly joined buddy: %s (%s)''', buddy.props.nick, event.handle )
                            self.add_buddy( event.handle, buddy )
                        mesh.lookup_buddy( event.handle, on_buddy )
            elif event.type == olpcgames.PARTICIPANT_REMOVE:
                if not self.remove_buddy( event.handle ):
                    # race condition, need to block new/upcoming elements...
                    self._buddies[ event.handle ] = False
            elif event.type == olpcgames.MESSAGE_UNI:
                self.__handle_message(event.handle, event.content)
            return False
        else:
            if event.type == olpcgames.MESSAGE_UNI and event.content == "HAY_ALGUIEN?":
                mesh.send_to(event.handle,"HAY_ALGUIEN?NO_ESTOY")
            return False

    def __set_up(self):
        envio_mensaje = False
        self.__can_contrarios = 0
        self.__conf_men_juego = 0
        for participante in mesh.get_participants():
            if mesh.my_handle() != participante:
                envio_mensaje = True
                mesh.send_to(participante, "HAY_ALGUIEN?")
                self.__can_contrarios += 1
        if not envio_mensaje:
            self.__audio.play_voice_sound("club","esperando oponente")
            self.__estado = ESPERANDO_OPONENTE


    def send_game_message(self):
        self.__can_contrarios = 0
        self.__contrarios = []
        for participante in mesh.get_participants():
            if mesh.my_handle() != participante:
                self.__contrarios.append(participante)
                mesh.send_to(participante, "JUEGO?")
        self.__can_contrarios = len(self.__contrarios)
        self.__conf_men_juego = 0

    def __send_waiting_message(self):
        for participante in mesh.get_participants():
            if mesh.my_handle() != participante:
                mesh.send_to(participante, "ESPERANDO_JUEGO_NUEVO")

    def add_buddy( self, handle, buddy ):
        """Add a new buddy to internal structures

        Note: this is called in the GObject thread!
        """
        try:
            current = self._buddies.get( handle )
            if current is False:
                self.remove_buddy( handle )
                return
            self._buddies[ handle ] = buddy
        except Exception, err:
            log.error( """Failure setting up buddy %s: %s""", buddy, get_traceback( err ) )

    def remove_buddy( self,handle ):
        """Remove this buddy from all internal structures"""
        current = self._buddies.get( handle )
        log.info("Removing %s", current.props.nick)
        try:
            del self._buddies[ handle ]
        except KeyError, err:
            pass
        return current

    def __handle_message(self, jugador, mensaje):
        if mensaje == "PARTIDA":
            log.info("Me llego el mensaje: " + mensaje)
            #Iniciar una partida de Othello, luego enviar un mensaje confirmando esto y adjuntar al mismo la configuracion de la partida
            self.__audio.play_voice_sound("club","comenzando partida")
            contrario = str(self._buddies[jugador].props.nick)
            #self.__festival.say(contrario)
            self.__engine.init_game(nombre="mesh")
            self.__video.init_game_elements(self.__engine.juego, self.__audio)
            mesh.send_to(jugador, "PARTIDA LISTA:" + self.__serialize_game_conf())
            log.info("Envie el mensaje PARTIDA LISTA")
            self.__estado = JUGANDO
            self.__oponente = jugador
        elif mensaje.startswith("PARTIDA LISTA:"):
            log.info("Me llego el mensaje: " + mensaje.split(':')[0])
            #Iniciar una partida de Othello y a continuacion enviar un mensaje para empezar a jugar
            conf_inicial = self.__unserialize_game_conf(mensaje.split(':')[1])
            self.__engine.setup_game(conf_inicial,nombre="mesh")
            self.__video.init_game_elements(self.__engine.juego, self.__audio)
            mesh.send_to(jugador, "LISTO PARA JUGAR")
            self.__estado = JUGANDO
        elif mensaje == "LISTO PARA JUGAR":
            log.info("Me llego el mensaje: " + mensaje)
            #Activa la bandera para empezar a jugar, realiza una jugada y envia a continuacion un mensaje con la jugada que se hizo
            self.__engine.on_play_mesh_game()
        elif mensaje.startswith("JUGADA:"):
            log.info("Me llego el mensaje: " + mensaje)
            #Mensaje JUGADA:(x,y)
            #Actualizar el tablero, realizar una jugada y enviar un mensaje con la jugada que se hizo
            x, y = map(lambda i: int(i.strip('()')), mensaje.split(':')[1].split(','))
            jugada = Coordinate(x,y)
            #if jugada.x != -1 and jugada.y != -1:
            #Si tanto x como y son iguales a -1 quiere decir que el contrario paso el turno porque no tenia jugadas posibles.
            self.__engine.juego.play(coord=jugada,audio=self.__engine.get_audio(),marcador=self.__engine.get_video().marcador,ventana=self.__engine.get_video().ventana)
            self.__engine.on_play_mesh_game()
        elif mensaje == "JUEGO?":
            log.info("Me llego el mensaje: " + mensaje)
            if self.__estado == ESPERANDO_OPONENTE:
                mesh.send_to(jugador, "JUEGO?_OK")
            else:
                mesh.send_to(jugador, "JUEGO?_NOPUEDO")
                log.info("En este momento no estoy disponible para comenzar una partida")
        elif mensaje.startswith("JUEGO?"):
            log.info("Me llego el mensaje: " + mensaje)
            rta = mensaje.split('_')[1]
            if jugador in self.__contrarios:
                self.__conf_men_juego += 1
                if rta == "NOPUEDO":
                    self.__contrarios.remove(jugador)
            if self.__conf_men_juego == self.__can_contrarios:
                if not self.__contrarios == []:
                    #Si ya llegaron las respuestas de todos los mensajes mostrar en una lista los oponentes disponibles
                    self.__video.create_selection_list(titulo="LISTA DE OPONENTES")
                    opciones = []
                    con = 1
                    for contrario in self.__contrarios:
                        if con <= 3:
                            opciones.append({"descripcion":str(self._buddies[contrario].props.nick),"id":contrario,"visible":True})
                        else:
                            opciones.append({"descripcion":str(self._buddies[contrario].props.nick),"id":contrario,"visible":False})
                        con += 1
                    self.__audio.wait_sound_end(tiempo=600)
                    self.__audio.play_voice_sound("club","seleccione oponente")
                    self.__video.selection_list.add_options(opciones)
                    self.__video.show_selection_list()
                    #self.__audio.wait_sound_end(tiempo=600)
                    #self.__video.selection_list.read_option(self.__audio)
                else:
                    self.__audio.play_voice_sound("club","no se encontraron oponentes")
                    self.__video.create_selection_list()
                    self.__video.selection_list.add_options([{"descripcion":"Salir","id":"salir","visible":True},{"descripcion":"Reintentar Busqueda", "id":"reintentar_busqueda","visible":True}])
                    self.__video.show_selection_list()
            else:
                log.debug("Todavia no me llegaron las respuestas de todos los oponentes. Men confirmados: %s. Can Contrarios: %s", self.__conf_men_juego, self.__can_contrarios)
        elif mensaje == "ESPERANDO_JUEGO_NUEVO":
            self.__hay_oponente_esperando = True
        elif mensaje == "SALGO":
            self.__video.dissapear_game_elements()
            self.__audio.play_voice_sound("club","oponente abandono la partida")
            self.__video.create_selection_list()
            self.__video.selection_list.add_options([{"descripcion":"Salir","id":"salir","visible":True},{"descripcion":"Volver a Jugar", "id":"volver_a_jugar","visible":True}])
            self.__video.show_selection_list()
            self.__engine.change_context(LIST)
            self.__estado = ON
        elif mensaje == "HAY_ALGUIEN?":
            mesh.send_to(jugador, "HAY_ALGUIEN?ESTOY")
        elif mensaje.startswith("HAY_ALGUIEN?"):
            rta = mensaje.split('?')[1]
            self.__conf_men_juego += 1
            if rta == "ESTOY":
                self.__audio.play_voice_sound("club","buscando oponentes")
                self.send_game_message()
            else:
                if self.__conf_men_juego == self.__can_contrarios:
                    self.__audio.play_voice_sound("club","esperando oponente")
                    self.__estado = ESPERANDO_OPONENTE
                    self.__engine.change_context(PLAY)
        else:
            log.debug("Mensaje Desconocido... %s", mensaje)

    def set_state(self, valor):
        self.__estado = valor

    def init_list_action(self, id_accion):
        if type(id_accion) == type(""):
            if id_accion == "reintentar_busqueda":
                self.send_game_message()
                self.__engine.change_context(LIST)
            elif id_accion == "volver_a_jugar":
                if self.__hay_oponente_esperando:
                    self.__hay_oponente_esperando = False
                    self.send_game_message()
                    self.__engine.change_context(LIST)
                else:
                    self.__audio.play_voice_sound("club","esperando oponente")
                    self.__estado = ESPERANDO_OPONENTE
                    self.__send_waiting_message()
                    self.__engine.change_context(PLAY)
        else:
            self.__engine.change_context(PLAY)
            mesh.send_to(id_accion, "PARTIDA")
            self.__oponente = id_accion

    def remove_me(self):
        if self.__estado == JUGANDO:
            mesh.send_to(self.__oponente, "SALGO")
        dbus_handle = mesh.my_handle()
        #mesh.instance(self.__tube_id).ordered_bus_names.remove(dbus_handle)
        PEvent.post(PEvent.Event(mesh.PARTICIPANT_REMOVE, handle=dbus_handle))

    def remove_all(self):
        #log.info( 'Antes de obtener el dbus_handle...')
        #dbus_handle = mesh.instance().tube.participants[self.__get_oponent_handle()]
        #log.info( 'Tengo el dbus_handle...')
        #mesh.instance().ordered_bus_names.remove(mesh.my_handle())
        #log.info( 'Hice el remove...')
        #PEvent.post(PEvent.Event(mesh.PARTICIPANT_REMOVE, handle=mesh.my_handle()))
        #log.info( 'Envie el evento PARTICIPANT_REMOVE...')
        mesh.instance().tube.close()
        #log.debug("Return type _getConn: " + str(type(mesh._getConn())))

    def __serialize_game_conf(self):
        conf_partida = {"jugadores":self.__engine.juego.get_players(),"tablero":self.__engine.juego.get_board_configuration()}
        f = open(os.path.abspath(self.__write_path + '/tmp/tmp.dat'),'w')
        pickle.dump(conf_partida, f)
        f.close()
        f = open(os.path.abspath(self.__write_path + '/tmp/tmp.dat'))
        str_conf = f.read()
        f.close()
        return str_conf

    def __unserialize_game_conf(self, str):
        f = open(os.path.abspath(self.__write_path + '/tmp/tmp.dat'),'w')
        f.write(str)
        f.close()
        f = open(os.path.abspath(self.__write_path + '/tmp/tmp.dat'))
        conf = pickle.load(f)
        f.close()
        return conf

    def __get_oponent_handle(self):
        for handle in self._buddies.keys():
            if mesh.my_handle() != handle:
                return handle

    def send_end_move_message(self):
        destinatario = self.__get_oponent_handle()
        jugada = self.__engine.juego.get_last_human_move()
        if jugada != "":
            mesh.send_to(destinatario, "JUGADA:" + jugada.to_string())
        else:
            #Si la jugada es igual a "" es porque no le quedaban jugadas posibles y tuvo que pasar el turno
            mesh.send_to(destinatario, "JUGADA:" + Coordinate(-1,-1).to_string())
        self.__engine.off_play_mesh_game()

    ###
    #Metodos que utilizo para que funcione el join programatico a una actividad compartida
    ###
    def __privacy_changed_cb(self, shared_activity, param_spec):
        if shared_activity.props.private:
            olpcgames.ACTIVITY._jobject.metadata['share-scope'] = "invite"
        else:
            olpcgames.ACTIVITY._jobject.metadata['share-scope'] = "public"

    def joined_cb(self, activity, success, err):
        """Callback when join has finished"""
        olpcgames.ACTIVITY.shared_activity.disconnect(olpcgames.ACTIVITY._join_id)
        olpcgames.ACTIVITY._join_id = None
        if not success:
            logging.debug("Failed to join activity: %s" % err)
            return

        olpcgames.ACTIVITY.present()
        olpcgames.ACTIVITY.emit('joined')
        self.__privacy_changed_cb(olpcgames.ACTIVITY.shared_activity, None)
