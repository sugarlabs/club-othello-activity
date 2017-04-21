from main.constants import F_MEET_BLOCK_VOCALS, S_MEET_BLOCK_VOCALS, NULL, MEET, MEET_GO_TUT, MEET_GO_TUT_AGAIN, \
                           DERECHA, WELCOME, TUTORIAL1, LIST, NAVE, DIAL, PLAY, GANAR, EMPATAR, IZQUIERDA, \
                           PERDER, WON1, DRAW1, LOSE1, BRONZE, MEET_GO_CHAL1, MEET_GO_CHAL1_AGAIN, CHALLENGE1, \
                           WON2, DRAW2, LOSE2, PLATA, CHALLENGE2, DRAW3, LOSE3, WON3, ORO, TUTORIAL2, CHALLENGE3, MEET_GO_CHAL4, CHALLENGE4, \
                           CHALLENGES_COMPLETED, ALL_CLEAR, CLEAR_GAMES, CLEAR_CHALLENGES, MARFIL, MADERA
from othello.player import PC
from othello.ai import Ai
import logging, pygame

log = logging.getLogger( 'src.hyperhistory.character' )
log.setLevel( logging.DEBUG )

class Character:
    def __init__(self, nombre=-1, partida=False, dialogo=False, id=""):
        self.__nombre = nombre
        self.__disponible_partida = partida
        self.__disponible_dialogo = dialogo
        self.__id = id

    def is_available_to_play(self):
        return self.__disponible_partida

    def is_available_to_talk(self):
        return self.__disponible_dialogo

    def __str__(self):
        return "Nombre: " + self.__nombre + "\nPartida: " + str(self.__disponible_partida) + "\nDialogo: " + str(self.__disponible_dialogo)

    def get_name(self):
        log.debug("obteniendo el nombre del personaje")
        return self.__nombre

    def get_id(self):
        return self.__id

    def set_available_to_play(self, valor):
        self.__disponible_partida = valor

    def set_available_to_talk(self, valor):
        self.__disponible_dialogo = valor

class ChPabloGris(Character):
    def __init__(self, nombre=-1, partida=False, dialogo=False, id=""):
        Character.__init__(self, nombre, partida, dialogo, id)
        self.__accion = {}
        self.__evento = {}
        self.__leccion_retomada = ""

    def set_current_action(self, accion):
        self.__accion = accion

    def set_current_event(self, evento):
        self.__evento = evento

    def do_action(self, nombre):
        if nombre == "bienvenida":
            pass
        else:
            pass

    def __find_action(self, acciones, nombre_accion):
        for a in acciones:
            if a['nombre'] == nombre_accion:
                return a

    def init_room_action(self, engine):
        usuario = engine.get_user()
        estado = usuario.get_state()
        acciones = estado.get_state_actions()
        state_problem = False
        character_relation_problem = False
        if estado.get_name() == "state1":
            if usuario.get_character_relation("pablo gris") == WELCOME:
                self.__tutorial1(engine)
                self.set_current_action(self.__find_action(acciones, "tutorial1"))
            else:
                character_relation_problem = True
        elif estado.get_name() == "state2":
            if usuario.get_character_relation("pablo gris") == TUTORIAL1:
                self.__go_another_place("go_chal1",engine)
                self.set_current_action({"nombre":"go_chal1"})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state3":
            if usuario.get_character_relation("pablo gris") == TUTORIAL1:
                self.__go_another_place("go_hab_pm1",engine)
                self.set_current_action({"nombre":"go_hab_pm1"})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state4":
            if usuario.get_character_relation("pablo gris") == TUTORIAL1:
                self.__go_another_place("go_hab_pm2",engine)
                self.set_current_action({"nombre":"go_hab_pm2"})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state5":
            if usuario.get_character_relation("pablo gris") == TUTORIAL1:
                self.__go_another_place("go_chal2",engine)
                self.set_current_action({"nombre":"go_chal2"})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state6":
            if usuario.get_character_relation("pablo gris") == TUTORIAL1:
                self.__go_another_place("go_hab_pm3",engine)
                self.set_current_action({"nombre":"go_hab_pm3"})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state8":
            if usuario.get_character_relation("pablo gris") == TUTORIAL1:
                self.__tutorial2(engine)
                self.set_current_action(self.__find_action(acciones, "tutorial2"))
            else:
                character_relation_problem = True
        elif estado.get_name() == "state9":
            if usuario.get_character_relation("pablo gris") == TUTORIAL2:
                self.__go_another_place("go_chal3",engine)
                self.set_current_action({"nombre":"go_chal3"})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state10":
            if usuario.get_character_relation("pablo gris") == TUTORIAL2:
                self.__go_another_place("go_hab_sd",engine)
                self.set_current_action({"nombre":"go_hab_sd"})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state11":
            if usuario.get_character_relation("pablo gris") == TUTORIAL2:
                if usuario.get_character_relation("protasio") == NULL:
                    self.__go_another_place("go_hab_pt1",engine)
                    self.set_current_action({"nombre":"go_hab_pt1"})
                else:
                    self.__go_another_place("go_chal4",engine)
                    self.set_current_action({"nombre":"go_chal4"})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state12":
            if usuario.get_character_relation("pablo gris") == TUTORIAL2:
                self.__go_another_place("go_hab_pt2",engine)
                self.set_current_action({"nombre":"go_hab_pt2"})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state13":
            if usuario.get_character_relation("pablo gris") == TUTORIAL2:
                engine.get_dialog_manager().begin_dialogue("pg_get_medals")
                self.set_current_action({"nombre":"get_medals"})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state14":
            if usuario.get_character_relation("pablo gris") == TUTORIAL2:
                engine.get_dialog_manager().begin_dialogue("pg_get_medals")
                self.set_current_action({"nombre":"get_medals"})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state15":
            if usuario.get_character_relation("pablo gris") == TUTORIAL2:
                engine.get_dialog_manager().begin_dialogue("pg_pt_defeated")
                self.set_current_action({"nombre":"pt_defeated"})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state17":
            if usuario.get_character_relation("pablo gris") == TUTORIAL2:
                engine.get_dialog_manager().begin_dialogue("pg_all_clear")
                self.set_current_action({"nombre":"all_clear"})
            else:
                character_relation_problem = True
        else:
            state_problem = True
        if state_problem:
            log.error("Estado invalido! (Class: ChPabloGris, Method: init_room_action)")
        if character_relation_problem:
            log.debug("No hay accion asociada a la relacion con Pablo Gris en el %s (Method: init_room_action)", estado.get_name())

    def __go_another_place(self,accion,engine):
        video = engine.get_video()
        video.text_box.show(video.ventana)
        if accion == "go_hab_pm1":
            engine.get_dialog_manager().begin_dialogue("pg_go_pm1")
        elif accion == "go_hab_pm2":
            engine.get_dialog_manager().begin_dialogue("pg_go_pm2")
        elif accion == "go_hab_pm3":
            engine.get_dialog_manager().begin_dialogue("pg_go_pm3")
        elif accion == "go_chal1":
            engine.get_dialog_manager().begin_dialogue("pg_chal1")
        elif accion == "go_chal2":
            engine.get_dialog_manager().begin_dialogue("pg_go_chal2")
        elif accion == "go_chal3":
            engine.get_dialog_manager().begin_dialogue("pg_go_chal3")
        elif accion == "go_chal4":
            engine.get_dialog_manager().begin_dialogue("pg_go_chal4")
        elif accion == "go_hab_sd":
            engine.get_dialog_manager().begin_dialogue("pg_go_sd")
        elif accion == "go_hab_pt1":
            engine.get_dialog_manager().begin_dialogue("pg_go_pt1")
        elif accion == "go_hab_pt2":
            engine.get_dialog_manager().begin_dialogue("pg_go_pt2")

    def __tutorial1(self, engine):
        video = engine.get_video()
        video.text_box.show(video.ventana)
        engine.get_dialog_manager().begin_dialogue("pg_tutorial1")

    def __tutorial2(self, engine):
        video = engine.get_video()
        video.text_box.show(video.ventana)
        engine.get_dialog_manager().begin_dialogue("pg_tutorial2")

    def init_list_action(self, id_leason, engine):
        engine.change_context(DIAL)
        engine.get_dialog_manager().begin_dialogue("pg_intro_retake_leason")
        self.set_current_action({"nombre":"intro_retake_leason"})
        if id_leason ==  "tutorial1":
            self.__leccion_retomada = "tutorial1"
        elif id_leason == "tutorial2":
            self.__leccion_retomada = "tutorial2"

    def wellcome(self, engine):
        engine.get_audio().stop_sound()
        video = engine.get_video()
        video.text_box.show(video.ventana)
        engine.get_dialog_manager().begin_dialogue("pg_bienvenida")

    def demo_end(self, engine):
        video = engine.get_video()
        video.text_box.show(video.ventana)
        self.set_current_action({"nombre":"demo_end"})
        engine.set_action(self.close_action,engine)
        pg = engine.get_club().get_character_by_name("pablo gris")
        video.club.show_character(pg)
        engine.get_dialog_manager().begin_dialogue("pg_demo_end")

    def close_action(self,param):
        engine = param
        usuario = engine.get_user()
        contexto_pos_dialogo = ""
        if self.__accion['nombre'] == "tutorial1":
            usuario.set_character_relation(self.get_name(),TUTORIAL1)
            if 'consecuencia' in self.__accion and  self.__accion['consecuencia'] == "change_state":
                engine.change_state(self.__accion['nuevo_estado'])
            engine.get_navigation_manager().leave_room()
            contexto_pos_dialogo = NAVE
            usuario.set_skill_level(TUTORIAL1)
        elif self.__accion['nombre'] == "go_hab_pm1" or \
             self.__accion['nombre'] == "go_chal1" or \
             self.__accion['nombre'] == "go_hab_pm2" or \
             self.__accion['nombre'] == "go_chal2" or \
             self.__accion['nombre'] == "go_hab_pm3" or \
             self.__accion['nombre'] == "go_chal3" or \
             self.__accion['nombre'] == "go_hab_sd" or \
             self.__accion['nombre'] == "go_hab_pt1" or \
             self.__accion['nombre'] == "go_chal4" or \
             self.__accion['nombre'] == "go_hab_pt2" or \
             self.__accion['nombre'] == "get_medals" or \
             self.__accion['nombre'] == "pt_defeated" or \
             self.__accion['nombre'] == "all_clear":
            engine.get_dialog_manager().begin_dialogue("pg_retake")
            contexto_pos_dialogo = LIST
        elif self.__accion['nombre'] == "intro_retake_leason":
            if self.__leccion_retomada == "tutorial1":
                engine.get_dialog_manager().begin_dialogue("pg_tutorial1",grupo_inicial=1)
            elif self.__leccion_retomada == "tutorial2":
                engine.get_dialog_manager().begin_dialogue("pg_tutorial2",grupo_inicial=1)
            self.set_current_action({"nombre":"retake_leason"})
            contexto_pos_dialogo = DIAL
        elif self.__accion['nombre'] == "retake_leason":
            engine.get_navigation_manager().leave_room()
            contexto_pos_dialogo = NAVE
        elif self.__accion['nombre'] == "demo_end":
            engine.get_audio().play_voice_sound("otros","salida_club")
            engine.get_audio().wait_sound_end()
            engine.get_navigation_manager().exit_club()
        elif self.__accion['nombre'] == "tutorial2":
            usuario.set_character_relation(self.get_name(),TUTORIAL2)
            if 'consecuencia' in self.__accion and  self.__accion['consecuencia'] == "change_state":
                engine.change_state(self.__accion['nuevo_estado'])
            engine.get_navigation_manager().leave_room()
            contexto_pos_dialogo = NAVE
            usuario.set_skill_level(TUTORIAL2)
        return contexto_pos_dialogo

    def close_event(self, param):
        engine = param
        usuario = engine.get_user()
        video = engine.get_video()
        contexto_pos_dialogo = ""
        if self.__evento['nombre'] == "bienvenida":
            usuario.set_character_relation(self.get_name(),WELCOME)
            if self.__evento['consecuencia'] == "change_state":
                engine.change_state(self.__evento['nuevo_estado'])
            video.club.show_room(usuario.get_current_room())
            self.__evento.clear()
            contexto_pos_dialogo = NAVE
        return contexto_pos_dialogo


class ChPedroMadera(Character):
    def __init__(self, nombre=-1, partida=False, dialogo=False, id=""):
        Character.__init__(self, nombre, partida, dialogo, id)
        self.__accion = {}
        self.__evento = {}
        self.__juego = {}
        self.__medalla = ""

    def set_current_action(self, accion):
        self.__accion = accion

    def set_current_event(self, evento):
        self.__evento = evento

    def set_current_game(self, juego):
        self.__juego = juego

    def do_action(self, nombre_accion, engine):
        video = engine.get_video()
        video.club.show_character(self)
        video.text_box.show(video.ventana)
        if nombre_accion == "bloqueo_acceso_piso2_1":
            engine.get_dialog_manager().begin_dialogue("pm_bloqueo_acceso_piso2_1")
        elif nombre_accion == "bloqueo_acceso_piso2_2":
            engine.get_dialog_manager().begin_dialogue("pm_bloqueo_acceso_piso2_2")
        else:
            raise Exception("Accion desconocida, (ChPedroMadera Class, do_action method)")

    def __find_action(self, acciones, nombre_accion):
        for a in acciones:
            if a['nombre'] == nombre_accion:
                return a

    def init_room_action(self, engine):
        usuario = engine.get_user()
        estado = usuario.get_state()
        #acciones = estado.get_state_actions()
        video = engine.get_video()
        video.text_box.show(video.ventana)
        state_problem = False
        character_relation_problem = False
        if estado.get_name() == "state2":
            if usuario.get_character_relation(self.get_name()) == NULL:
                engine.get_dialog_manager().begin_dialogue("pm_first_meet_go_chal1")
                self.set_current_action({"nombre":"first_meet_go_chal1","continua_con_dialogo":False})
            elif usuario.get_character_relation(self.get_name()) == F_MEET_BLOCK_VOCALS or \
                 usuario.get_character_relation(self.get_name()) == S_MEET_BLOCK_VOCALS:
                engine.get_dialog_manager().begin_dialogue("pm_intro_room_go_chal1")
                self.set_current_action({"nombre":"intro_room_go_chal1","continua_con_dialogo":False})
            elif usuario.get_character_relation(self.get_name()) == MEET_GO_CHAL1 or \
                 usuario.get_character_relation(self.get_name()) == MEET_GO_CHAL1_AGAIN:
                engine.get_dialog_manager().begin_dialogue("pm_intro_room_go_chal1_again")
                self.set_current_action({"nombre":"intro_room_go_chal1_again","continua_con_dialogo":False})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state3":
            if usuario.get_character_relation(self.get_name()) == NULL:
                engine.get_dialog_manager().begin_dialogue("pm_first_meet_first_game")
                self.set_current_action({"nombre":"first_meet_first_game","continua_con_dialogo":False})
            elif usuario.get_character_relation(self.get_name()) == F_MEET_BLOCK_VOCALS or \
                 usuario.get_character_relation(self.get_name()) == S_MEET_BLOCK_VOCALS:
                engine.get_dialog_manager().begin_dialogue("pm_intro_room_first_game")
                self.set_current_action({"nombre":"intro_room_first_game","continua_con_dialogo":False})
            elif usuario.get_character_relation(self.get_name()) == MEET_GO_CHAL1 or \
                 usuario.get_character_relation(self.get_name()) == MEET_GO_CHAL1_AGAIN:
                engine.get_dialog_manager().begin_dialogue("pm_init_first_game")
                self.set_current_action({"nombre":"init_first_game","continua_con_dialogo":False})
            elif usuario.get_character_relation(self.get_name()) == DRAW1 or \
                 usuario.get_character_relation(self.get_name()) == LOSE1:
                engine.get_dialog_manager().begin_dialogue("pm_init_first_game")
                self.set_current_action({"nombre":"init_first_game","continua_con_dialogo":False})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state4":
            if usuario.get_character_relation(self.get_name()) == WON1 or \
                usuario.get_character_relation(self.get_name()) == DRAW2 or \
                usuario.get_character_relation(self.get_name()) == LOSE2:
                engine.get_dialog_manager().begin_dialogue("pm_init_second_game")
                self.set_current_action({"nombre":"init_second_game","continua_con_dialogo":False})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state5":
            if usuario.get_character_relation(self.get_name()) == WON2:
                engine.get_dialog_manager().begin_dialogue("pm_hi_go_chal2")
                self.set_current_action({"nombre":"hi_go_chal2","continua_con_dialogo":False})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state6":
            if usuario.get_character_relation(self.get_name()) == WON2 or \
               usuario.get_character_relation(self.get_name()) == DRAW3 or \
               usuario.get_character_relation(self.get_name()) == LOSE3:
                engine.get_dialog_manager().begin_dialogue("pm_init_third_game")
                self.set_current_action({"nombre":"init_third_game","continua_con_dialogo":False})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state8":
            if usuario.get_character_relation(self.get_name()) == WON3:
                engine.get_dialog_manager().begin_dialogue("pm_go_tut2")
                self.set_current_action({"nombre":"go_tut2","continua_con_dialogo":True})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state9":
            if usuario.get_character_relation(self.get_name()) == WON3:
                engine.get_dialog_manager().begin_dialogue("pm_go_chal3")
                self.set_current_action({"nombre":"go_chal3","continua_con_dialogo":True})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state10":
            if usuario.get_character_relation(self.get_name()) == WON3:
                engine.get_dialog_manager().begin_dialogue("pm_go_sd")
                self.set_current_action({"nombre":"go_sd","continua_con_dialogo":True})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state11":
            if usuario.get_character_relation(self.get_name()) == WON3:
                if usuario.get_character_relation("protasio") == NULL:
                    engine.get_dialog_manager().begin_dialogue("pm_go_pt1")
                    self.set_current_action({"nombre":"go_pt1","continua_con_dialogo":True})
                else:
                    engine.get_dialog_manager().begin_dialogue("pm_go_chal4")
                    self.set_current_action({"nombre":"go_chal4","continua_con_dialogo":True})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state12":
            if usuario.get_character_relation(self.get_name()) == WON3:
                engine.get_dialog_manager().begin_dialogue("pm_go_pt2")
                self.set_current_action({"nombre":"go_pt2","continua_con_dialogo":True})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state13":
            if usuario.get_character_relation(self.get_name()) == WON3:
                engine.get_dialog_manager().begin_dialogue("pm_get_medals")
                self.set_current_action({"nombre":"get_medals","continua_con_dialogo":True})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state14":
            if usuario.get_character_relation(self.get_name()) == WON3:
                engine.get_dialog_manager().begin_dialogue("pm_get_medals")
                self.set_current_action({"nombre":"get_medals","continua_con_dialogo":True})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state15":
            if usuario.get_character_relation(self.get_name()) == WON3:
                engine.get_dialog_manager().begin_dialogue("pm_pt_defeated")
                self.set_current_action({"nombre":"pt_defeated","continua_con_dialogo":True})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state17":
            if usuario.get_character_relation(self.get_name()) == WON3:
                engine.get_dialog_manager().begin_dialogue("pm_all_clear")
                self.set_current_action({"nombre":"all_clear","continua_con_dialogo":True})
            else:
                character_relation_problem = True
        else:
            state_problem = True
        if state_problem:
            log.error("Estado invalido! (Class: ChPedroMadera, Method: init_room_action)")
        if character_relation_problem:
            log.debug("No hay accion asociada a la relacion con Pedro Madera en el %s (Method: init_room_action)", estado.get_name())

    def block_third_floor_access(self, engine):
        usuario = engine.get_user()
        video = engine.get_video()
        video.club.show_character(self)
        video.text_box.show(video.ventana)
        estado = usuario.get_state()
        if estado.get_name() == "state1":
            if usuario.get_character_relation(self.get_name()) == NULL:
                engine.get_dialog_manager().begin_dialogue("pm_bloqueo_acceso_piso2_1")
                self.set_current_action({"nombre":"bloqueo_acceso_piso2_1","continua_con_dialogo":False})
            elif usuario.get_character_relation(self.get_name()) == F_MEET_BLOCK_VOCALS:
                engine.get_dialog_manager().begin_dialogue("pm_bloqueo_acceso_piso2_2")
                self.set_current_action({"nombre":"bloqueo_acceso_piso2_2","continua_con_dialogo":False})
            else:
                log.debug("Relacion con Pedro Madera incorrecta!. Class: ChPedroMadera, Method: block_third_floor_access")
        else:
            log.debug("Estado de la aplicacion incorrecto!. Class: ChPedroMadera, Method: block_third_floor_access")

    def init_list_action(self, id_action, engine):
        engine.change_context(DIAL)
        if id_action == "jugar_sin_jugadas_posibles":
            juego_con_jp = False
        else:
            juego_con_jp = True
        engine.init_game("revancha_pm",juego_con_jp)
        self.__juego = {"nombre":"revancha","objeto":engine.juego}
        engine.get_dialog_manager().begin_dialogue("pm_prematch_phrase")
        self.set_current_action({"nombre":"prematch_phrase","continua_con_dialogo":False})

    def close_action(self, param):
        engine = param
        usuario = engine.get_user()
        video = engine.get_video()
        contexto_pos_dialogo = ""
        if not self.__accion['continua_con_dialogo']:
            video.text_box.disappear(video.ventana)
        if self.__accion['nombre'] == "bloqueo_acceso_piso2_1":
            usuario.set_character_relation(self.get_name(),F_MEET_BLOCK_VOCALS)
            contexto_pos_dialogo = NAVE
        elif self.__accion['nombre'] == "bloqueo_acceso_piso2_2":
            usuario.set_character_relation(self.get_name(),S_MEET_BLOCK_VOCALS)
            contexto_pos_dialogo = NAVE
        elif self.__accion['nombre'] == "first_meet_go_chal1" or \
             self.__accion['nombre'] == "intro_room_go_chal1":
            usuario.set_character_relation(self.get_name(),MEET_GO_CHAL1)
            contexto_pos_dialogo = NAVE
            engine.get_navigation_manager().leave_room()
        elif self.__accion['nombre'] == "intro_room_go_chal1_again":
            usuario.set_character_relation(self.get_name(), MEET_GO_CHAL1_AGAIN)
            contexto_pos_dialogo = NAVE
            engine.get_navigation_manager().leave_room()
        elif self.__accion['nombre'] == "hi_go_chal2":
            contexto_pos_dialogo = NAVE
            engine.get_navigation_manager().leave_room()
        elif self.__accion['nombre'] == "first_meet_first_game" or \
             self.__accion['nombre'] == "intro_room_first_game" or \
             self.__accion['nombre'] == "init_first_game":
            contexto_pos_dialogo = PLAY
            engine.init_game("partida1_pm")
            self.__juego = {"nombre":"partida1"}
            video.init_game_elements(engine.juego, engine.get_audio())
        elif self.__accion['nombre'] == "init_second_game":
            contexto_pos_dialogo = PLAY
            engine.init_game("partida2_pm")
            self.__juego = {"nombre":"partida2"}
            video.init_game_elements(engine.juego, engine.get_audio())
        elif self.__accion['nombre'] == "init_third_game":
            contexto_pos_dialogo = PLAY
            engine.init_game("partida3_pm")
            self.__juego = {"nombre":"partida3"}
            video.init_game_elements(engine.juego, engine.get_audio())
        elif self.__accion['nombre'] == "prematch_phrase":
            contexto_pos_dialogo = PLAY
            video.text_box.disappear(video.ventana)
            video.init_game_elements(self.__juego["objeto"], engine.get_audio())
        elif self.__accion['nombre'] == "dial_dp_juego_perdido":
            usuario = engine.get_user()
            contexto_pos_dialogo = DIAL
            if usuario.get_character_relation(self.get_name()) == WON1:
                engine.get_audio().play_fx_sound("otros","medalla_bronce")
                video.show_medal(BRONZE)
                usuario.save_medal("bronce")
                self.__medalla = BRONZE
            if usuario.get_character_relation(self.get_name()) == WON2:
                engine.get_audio().play_fx_sound("otros","medalla_plata")
                video.show_medal(PLATA)
                usuario.delete_medal("bronce")
                usuario.save_medal("plata")
                self.__medalla = PLATA
            if usuario.get_character_relation(self.get_name()) == WON3:
                engine.get_audio().play_fx_sound("otros","medalla_oro")
                video.show_medal(ORO)
                usuario.delete_medal("plata")
                usuario.save_medal("oro")
                self.__medalla = ORO
            engine.get_audio().wait_sound_end(tiempo=600)
            engine.get_dialog_manager().begin_dialogue("pm_bye")
            self.set_current_action({"nombre":"bye","continua_con_dialogo":False})
        elif self.__accion['nombre'] == "bye":
            if self.__medalla != "":
                video.dissapear_medal(self.__medalla)
                self.__medalla = ""
            accion = self.__find_action(usuario.get_state().get_state_actions(), "won_game")
            if accion['nuevo_estado'] == "state7":
                contexto_pos_dialogo = DIAL
                nueva_hab = usuario.get_current_room().get_right_room()
                video.club.move_to_another_room(nueva_hab,DERECHA,extra="presentacion_sofia")
                usuario.set_current_room(nueva_hab)
            else:
                contexto_pos_dialogo = NAVE
                engine.get_navigation_manager().leave_room()
            engine.change_state(accion['nuevo_estado'])
        elif self.__accion['nombre'] == "go_tut2" or \
             self.__accion['nombre'] == "go_chal3" or \
             self.__accion['nombre'] == "go_sd" or \
             self.__accion['nombre'] == "go_pt1" or \
             self.__accion['nombre'] == "go_chal4" or \
             self.__accion['nombre'] == "go_pt2" or \
             self.__accion['nombre'] == "get_medals" or \
             self.__accion['nombre'] == "pt_defeated" or \
             self.__accion['nombre'] == "all_clear":
            engine.get_dialog_manager().begin_dialogue("pm_rematch")
            self.set_current_action({"nombre":"rematch","continua_con_dialogo":False})
            contexto_pos_dialogo = LIST
        elif self.__accion['nombre'] == "dp_revancha" or \
             self.__accion['nombre'] == "dp_juego_empatado_o_ganado":
            contexto_pos_dialogo = NAVE
            engine.get_navigation_manager().leave_room()
        else:
            raise Exception("Accion desconocida, (Class: ChPedroMadera, Method: close_action)")
        return contexto_pos_dialogo

    def close_game(self, engine):
        ganador = engine.juego.get_final_result()
        resultado = ""
        video = engine.get_video()
        video.dissapear_scores()
        video.dissapear_board()
        if ganador != "":
            if ganador.get_name() == PC:
                resultado = GANAR
            else:
                resultado = PERDER
        else:
            resultado = EMPATAR
        if resultado == PERDER:
            if self.__juego['nombre'] == "partida1":
                engine.get_dialog_manager().begin_dialogue("pm_perdio_juego1")
                engine.get_user().set_character_relation(self.get_name(),WON1)
            elif self.__juego['nombre'] == "partida2":
                engine.get_dialog_manager().begin_dialogue("pm_perdio_juego2")
                engine.get_user().set_character_relation(self.get_name(),WON2)
            elif self.__juego['nombre'] == "partida3":
                engine.get_dialog_manager().begin_dialogue("pm_perdio_juego3")
                engine.get_user().set_character_relation(self.get_name(),WON3)
            elif self.__juego['nombre'] == "revancha":
                engine.get_dialog_manager().begin_dialogue("pm_perdio_revancha")
        else:
            if resultado == EMPATAR:
                engine.get_dialog_manager().begin_dialogue("pm_empato_juego")
                if self.__juego['nombre'] == "partida1":
                    engine.get_user().set_character_relation(self.get_name(),DRAW1)
                elif self.__juego['nombre'] == "partida2":
                    engine.get_user().set_character_relation(self.get_name(),DRAW2)
                elif self.__juego['nombre'] == "partida3":
                    engine.get_user().set_character_relation(self.get_name(),DRAW3)
            elif resultado == GANAR:
                if self.__juego['nombre'] == "partida1":
                    engine.get_dialog_manager().begin_dialogue("pm_gano_juego")
                    engine.get_user().set_character_relation(self.get_name(),LOSE1)
                elif self.__juego['nombre'] == "partida2":
                    engine.get_dialog_manager().begin_dialogue("pm_gano_juego")
                    engine.get_user().set_character_relation(self.get_name(),LOSE2)
                elif self.__juego['nombre'] == "partida3":
                    engine.get_dialog_manager().begin_dialogue("pm_gano_juego")
                    engine.get_user().set_character_relation(self.get_name(),LOSE3)
                elif self.__juego['nombre'] == "revancha":
                    engine.get_dialog_manager().begin_dialogue("pm_gano_revancha")
        contexto_pos_juego = DIAL
        if self.__juego['nombre'] == "revancha":
            self.set_current_action({"nombre":"dp_revancha","continua_con_dialogo":False})
        else:
            if resultado == PERDER:
                self.set_current_action({"nombre":"dial_dp_juego_perdido","continua_con_dialogo":True})
            else:
                self.set_current_action({"nombre":"dp_juego_empatado_o_ganado","continua_con_dialogo":False})
        return contexto_pos_juego


class ChDonCano(Character):
    def __init__(self, nombre=-1, partida=False, dialogo=False, id=""):
        Character.__init__(self, nombre, partida, dialogo, id)
        self.__accion = {}
        self.__desafio = ""
        self.__retomar_leccion = False
        self.__nro_intentos = 0
        self.__medalla = ""
        self.__trofeo = ""

    def set_current_action(self, accion):
        self.__accion = accion

    def set_current_challenge(self, desafio):
        self.__desafio = desafio

    def get_challenge_title(self, usuario, desafio):
        if usuario.get_challenge_medal(desafio) == BRONZE:
            return "Tomar desafio " + desafio.upper() + " (BRONCE)"
        elif usuario.get_challenge_medal(desafio) == PLATA:
            return "Tomar desafio " + desafio.upper() + " (PLATA)"
        elif usuario.get_challenge_medal(desafio) == ORO:
            return "Tomar desafio " + desafio.upper() + " (ORO)"
        else:
            return "Tomar desafio " + desafio.upper()

    def __find_action(self, acciones, nombre_accion):
        for a in acciones:
            if a['nombre'] == nombre_accion:
                return a

    def __update_user_medals(self, usuario, desafio):
        if usuario.get_challenge_medal(desafio) == PLATA:
            usuario.delete_medal("plata")
        elif usuario.get_challenge_medal(desafio) == BRONZE:
            usuario.delete_medal("bronce")

    def init_room_action(self, engine):
        log.debug("Ingresando al metodo que manejo las acciones de la habitacion")
        usuario = engine.get_user()
        video = engine.get_video()
        video.text_box.show(video.ventana)
        estado = usuario.get_state()
        character_relation_problem = False
        state_problem = False
        if estado.get_name() == "state1":
            #Todavia no paso por el Tutorial de aprendizaje de Othello
            if usuario.get_character_relation(self.get_name()) == NULL:
                #Nunca antes se encontro con Don Cano
                engine.get_dialog_manager().begin_dialogue("dc_bienvenida_ir_tut")
                self.set_current_action({"nombre":"bienvenida_ir_tut","continua_con_dialogo":False})
            else:
                engine.get_dialog_manager().begin_dialogue("dc_ir_tut")
                self.set_current_action({"nombre":"ir_tut","continua_con_dialogo":False})
        elif estado.get_name() == "state2":
            #Ya tomo el tutorial de aprendizaje de Othello
            log.debug("Despues de verificar el estado...")
            if usuario.get_character_relation(self.get_name()) == NULL:
                #Nunca se encontro con Don Cano
                engine.get_dialog_manager().begin_dialogue("dc_bienvenida_comenzar_chal_1")
                self.set_current_action({"nombre":"bienvenida_comenzar_chal_1","continua_con_dialogo":False})
                self.set_current_challenge("chal_a1")
                self.__nro_intentos = 1
            else:
                #Si ya se encontro con Don Cano
                engine.get_dialog_manager().begin_dialogue("dc_saludo_comenzar_chal_1")
                self.set_current_action({"nombre":"saludo_comenzar_chal_1","continua_con_dialogo":False})
                self.set_current_challenge("chal_a1")
                self.__nro_intentos = 1
        elif estado.get_name() == "state3":
            #Ya paso los dos primeros desafios
            if usuario.get_character_relation(self.get_name()) == CHALLENGE1:
                engine.get_dialog_manager().begin_dialogue("dc_go_pm1")
                self.set_current_action({"nombre":"go_pm1","continua_con_dialogo":True})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state4":
            #Ya paso los dos primeros desafios
            if usuario.get_character_relation(self.get_name()) == CHALLENGE1:
                engine.get_dialog_manager().begin_dialogue("dc_go_pm2")
                self.set_current_action({"nombre":"go_pm2","continua_con_dialogo":True})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state5":
            #Ya paso los dos primeros desafios y las dos primeras partidas contra pedro madera
            if usuario.get_character_relation(self.get_name()) == CHALLENGE1:
                engine.get_dialog_manager().begin_dialogue("dc_saludo_comenzar_chal_2")
                self.set_current_action({"nombre":"saludo_comenzar_chal_2","continua_con_dialogo":False})
                self.set_current_challenge("chal_a3")
                self.__nro_intentos = 1
            else:
                log.error("El estado 5 y la relacion con el personaje no coinciden. (Method: init_room_action)")
        elif estado.get_name() == "state6":
            #Ya paso los desafios a1, a2, a3, a4 y las dos primeras partidas contra pedro madera
            if usuario.get_character_relation(self.get_name()) == CHALLENGE2:
                engine.get_dialog_manager().begin_dialogue("dc_go_pm3")
                self.set_current_action({"nombre":"go_pm3","continua_con_dialogo":True})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state8":
            #Ya paso los desafios a1, a2, a3, a4 y las tres partidas contra pedro madera
            if usuario.get_character_relation(self.get_name()) == CHALLENGE2:
                engine.get_dialog_manager().begin_dialogue("dc_go_tut2")
                self.set_current_action({"nombre":"go_tut2","continua_con_dialogo":False})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state9":
            #Ya paso el segundo tutorial con Pablo Gris
            if usuario.get_character_relation(self.get_name()) == CHALLENGE2:
                engine.get_dialog_manager().begin_dialogue("dc_saludo_comenzar_chal_3")
                self.set_current_action({"nombre":"saludo_comenzar_chal_3","continua_con_dialogo":False})
                self.set_current_challenge("chal_b1")
                self.__nro_intentos = 1
            else:
                character_relation_problem = True
        elif estado.get_name() == "state10":
            #Ya paso el desafio por 5 medallas de bronce
            if usuario.get_character_relation(self.get_name()) == CHALLENGE3:
                engine.get_dialog_manager().begin_dialogue("dc_go_sd1")
                self.set_current_action({"nombre":"go_sd1","continua_con_dialogo":True})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state11":
            if usuario.get_character_relation("protasio") == NULL:
                engine.get_dialog_manager().begin_dialogue("dc_go_pt1")
                self.set_current_action({"nombre":"go_pt1","continua_con_dialogo":True})
            else:
                engine.get_dialog_manager().begin_dialogue("dc_saludo_comenzar_chal_4")
                self.set_current_action({"nombre":"saludo_comenzar_chal_4","continua_con_dialogo":False})
                self.set_current_challenge("chal_c1")
                self.__nro_intentos = 1
        elif estado.get_name() == "state12":
            #Ya paso el desafio sin jugadas posibles marcadas
            if usuario.get_character_relation(self.get_name()) == CHALLENGE4:
                engine.get_dialog_manager().begin_dialogue("dc_go_pt2")
                self.set_current_action({"nombre":"go_pt2","continua_con_dialogo":True})
            elif usuario.get_character_relation(self.get_name()) == CHALLENGES_COMPLETED:
                engine.get_dialog_manager().begin_dialogue("dc_chals_completed")
                self.set_current_action({"nombre":"chals_completed","continua_con_dialogo":True})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state13":
            if usuario.get_character_relation(self.get_name()) == CHALLENGE4:
                engine.get_dialog_manager().begin_dialogue("dc_get_medals")
                self.set_current_action({"nombre":"get_medals","continua_con_dialogo":True})
            elif usuario.get_character_relation(self.get_name()) == CHALLENGES_COMPLETED:
                engine.get_dialog_manager().begin_dialogue("dc_chals_completed")
                self.set_current_action({"nombre":"chals_completed","continua_con_dialogo":True})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state14":
            if usuario.get_character_relation(self.get_name()) == CHALLENGE4:
                engine.get_dialog_manager().begin_dialogue("dc_get_medals")
                self.set_current_action({"nombre":"get_medals","continua_con_dialogo":True})
            elif usuario.get_character_relation(self.get_name()) == CHALLENGES_COMPLETED:
                engine.get_dialog_manager().begin_dialogue("dc_chals_completed")
                self.set_current_action({"nombre":"chals_completed","continua_con_dialogo":True})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state15":
            if usuario.get_character_relation(self.get_name()) == CHALLENGE4:
                engine.get_dialog_manager().begin_dialogue("dc_pt_defeated")
                self.set_current_action({"nombre":"pt_defeated","continua_con_dialogo":True})
            elif usuario.get_character_relation(self.get_name()) == CHALLENGES_COMPLETED:
                engine.get_dialog_manager().begin_dialogue("dc_chals_completed")
                self.set_current_action({"nombre":"chals_completed","continua_con_dialogo":True})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state17":
            if usuario.get_character_relation(self.get_name()) == CHALLENGES_COMPLETED:
                engine.get_dialog_manager().begin_dialogue("dc_all_clear")
                self.set_current_action({"nombre":"all_clear","continua_con_dialogo":True})
            else:
                character_relation_problem = True
        else:
            state_problem = True
        if state_problem:
            log.error("Estado invalido! (Class: ChDonCano, Method: init_room_action)")
        if character_relation_problem:
            log.debug("No hay accion asociada a la relacion con Don Cano en el %s (Method: init_room_action)", estado.get_name())

    def init_list_action(self, id_leason, engine):
        engine.change_context(DIAL)
        if not id_leason == "reintentar":
            self.__retomar_leccion = True
            if id_leason == "retake_chal_a1":
                self.__desafio = "chal_a1"
            elif id_leason == "retake_chal_a2":
                self.__desafio = "chal_a2"
            elif id_leason == "retake_chal_a3":
                self.__desafio = "chal_a3"
            elif id_leason == "retake_chal_a4":
                self.__desafio = "chal_a4"
            elif id_leason == "retake_chal_a5":
                self.__desafio = "chal_a5"
            elif id_leason == "retake_chal_b1":
                self.__desafio = "chal_b1"
            elif id_leason == "retake_chal_b2":
                self.__desafio = "chal_b2"
            elif id_leason == "retake_chal_b3":
                self.__desafio = "chal_b3"
            elif id_leason == "retake_chal_b4":
                self.__desafio = "chal_b4"
            elif id_leason == "retake_chal_b5":
                self.__desafio = "chal_b5"
            elif id_leason == "retake_chal_c1":
                self.__desafio = "chal_c1"
            elif id_leason == "retake_chal_c2":
                self.__desafio = "chal_c2"
            elif id_leason == "retake_chal_c3":
                self.__desafio = "chal_c3"
            elif id_leason == "retake_chal_c4":
                self.__desafio = "chal_c4"
            elif id_leason == "retake_chal_c5":
                self.__desafio = "chal_c5"
            self.__nro_intentos = 1
        else:
            self.__nro_intentos += 1
            self.__retomar_leccion = False
        if self.__desafio == "chal_a1":
            engine.get_dialog_manager().begin_dialogue("dc_retake_chal_a1")
            self.set_current_action({"nombre":"retake_chal_a1","continua_con_dialogo":False})
        elif self.__desafio == "chal_a2":
            engine.get_dialog_manager().begin_dialogue("dc_retake_chal_a2")
            self.set_current_action({"nombre":"retake_chal_a2","continua_con_dialogo":False})
        elif self.__desafio == "chal_a3":
            engine.get_dialog_manager().begin_dialogue("dc_retake_chal_a3")
            self.set_current_action({"nombre":"retake_chal_a3","continua_con_dialogo":False})
        elif self.__desafio == "chal_a4":
            engine.get_dialog_manager().begin_dialogue("dc_retake_chal_a4")
            self.set_current_action({"nombre":"retake_chal_a4","continua_con_dialogo":False})
        elif self.__desafio == "chal_a5":
            engine.get_dialog_manager().begin_dialogue("dc_retake_chal_a5")
            self.set_current_action({"nombre":"retake_chal_a5","continua_con_dialogo":False})
        elif self.__desafio == "chal_b1":
            engine.get_dialog_manager().begin_dialogue("dc_retake_chal_b1")
            self.set_current_action({"nombre":"retake_chal_b1","continua_con_dialogo":False})
        elif self.__desafio == "chal_b2":
            engine.get_dialog_manager().begin_dialogue("dc_retake_chal_b2")
            self.set_current_action({"nombre":"retake_chal_b2","continua_con_dialogo":False})
        elif self.__desafio == "chal_b3":
            engine.get_dialog_manager().begin_dialogue("dc_retake_chal_b3")
            self.set_current_action({"nombre":"retake_chal_b3","continua_con_dialogo":False})
        elif self.__desafio == "chal_b4":
            engine.get_dialog_manager().begin_dialogue("dc_retake_chal_b4")
            self.set_current_action({"nombre":"retake_chal_b4","continua_con_dialogo":False})
        elif self.__desafio == "chal_b5":
            engine.get_dialog_manager().begin_dialogue("dc_retake_chal_b5")
            self.set_current_action({"nombre":"retake_chal_b5","continua_con_dialogo":False})
        elif self.__desafio == "chal_c1":
            engine.get_dialog_manager().begin_dialogue("dc_retake_chal_c1")
            self.set_current_action({"nombre":"retake_chal_c1","continua_con_dialogo":False})
        elif self.__desafio == "chal_c2":
            engine.get_dialog_manager().begin_dialogue("dc_retake_chal_c2")
            self.set_current_action({"nombre":"retake_chal_c2","continua_con_dialogo":False})
        elif self.__desafio == "chal_c3":
            engine.get_dialog_manager().begin_dialogue("dc_retake_chal_c3")
            self.set_current_action({"nombre":"retake_chal_c3","continua_con_dialogo":False})
        elif self.__desafio == "chal_c4":
            engine.get_dialog_manager().begin_dialogue("dc_retake_chal_c4")
            self.set_current_action({"nombre":"retake_chal_c4","continua_con_dialogo":False})
        elif self.__desafio == "chal_c5":
            engine.get_dialog_manager().begin_dialogue("dc_retake_chal_c5")
            self.set_current_action({"nombre":"retake_chal_c5","continua_con_dialogo":False})

    def close_action(self, param):
        engine = param
        usuario = engine.get_user()
        video = engine.get_video()
        contexto_pos_dialogo = ""
        if not self.__accion['continua_con_dialogo']:
            video.text_box.disappear(video.ventana)
        if self.__accion['nombre'] == "bienvenida_ir_tut":
            usuario.set_character_relation(self.get_name(),MEET_GO_TUT)
            engine.get_navigation_manager().leave_room()
            contexto_pos_dialogo = NAVE
        elif self.__accion['nombre'] == "ir_tut":
            usuario.set_character_relation(self.get_name(),MEET_GO_TUT_AGAIN)
            engine.get_navigation_manager().leave_room()
            contexto_pos_dialogo = NAVE
        elif self.__accion['nombre'] == "bienvenida_comenzar_chal_1" or \
             self.__accion['nombre'] == "saludo_comenzar_chal_1" or \
             self.__accion['nombre'] == "retake_chal_a1" or \
             self.__accion['nombre'] == "consejo_desafio_a2" or \
             self.__accion['nombre'] == "retake_chal_a2" or \
             self.__accion['nombre'] == "saludo_comenzar_chal_2" or \
             self.__accion['nombre'] == "retake_chal_a3" or \
             self.__accion['nombre'] == "consejo_desafio_a4" or \
             self.__accion['nombre'] == "retake_chal_a4" or \
             self.__accion['nombre'] == "saludo_comenzar_chal_3" or \
             self.__accion['nombre'] == "retake_chal_b1" or \
             self.__accion['nombre'] == "retake_chal_a5"or \
             self.__accion['nombre'] == "retake_chal_b2" or \
             self.__accion['nombre'] == "retake_chal_b3" or \
             self.__accion['nombre'] == "retake_chal_b4" or \
             self.__accion['nombre'] == "retake_chal_b5" or \
             self.__accion['nombre'] == "saludo_comenzar_chal_4" or \
             self.__accion['nombre'] == "retake_chal_c1" or \
             self.__accion['nombre'] == "retake_chal_c2" or \
             self.__accion['nombre'] == "retake_chal_c3" or \
             self.__accion['nombre'] == "retake_chal_c4" or \
             self.__accion['nombre'] == "retake_chal_c5":
            contexto_pos_dialogo = self.__end_challenge(engine, video)
        elif self.__accion['nombre'] == "ok_challenge_check_answer":
            video.dissapear_game_elements()
            video.text_box.show(video.ventana)
            if not self.__retomar_leccion:
                if self.__desafio == "chal_a1":
                    engine.get_dialog_manager().begin_dialogue("dc_continue_chal1")
                    self.set_current_action({"nombre":"continue_chal1","continua_con_dialogo":False})
                elif self.__desafio == "chal_a2":
                    engine.get_dialog_manager().begin_dialogue("dc_finalizar_chal1")
                    self.set_current_action({"nombre":"finalizar_chal1","continua_con_dialogo":False})
                elif self.__desafio == "chal_a3":
                    engine.get_dialog_manager().begin_dialogue("dc_continue_chal2")
                    self.set_current_action({"nombre":"continue_chal2","continua_con_dialogo":False})
                elif self.__desafio == "chal_a4":
                    engine.get_dialog_manager().begin_dialogue("dc_finalizar_chal2")
                    self.set_current_action({"nombre":"finalizar_chal2","continua_con_dialogo":False})
                elif self.__desafio == "chal_c1":
                    self.__give_challenge_medal(engine, usuario)
            else:
                self.__give_challenge_medal(engine, usuario)
            contexto_pos_dialogo = DIAL
        elif self.__accion['nombre'] == "give_gold" or \
             self.__accion['nombre'] == "give_silver" or \
             self.__accion['nombre'] == "give_bronze":
            medalla_a_entregar =  self.__accion['nombre'].split('_')[1]
            desafio = self.__desafio.split("_")[1]
            if medalla_a_entregar == "gold":
                usuario.save_challenge_medal(desafio, ORO)
                usuario.save_medal("oro")
                self.__medalla = ORO
                video.show_medal(ORO)
                engine.get_audio().play_fx_sound("otros","medalla_oro")
            elif medalla_a_entregar == "silver":
                usuario.save_challenge_medal(desafio, PLATA)
                usuario.save_medal("plata")
                self.__medalla = PLATA
                video.show_medal(PLATA)
                engine.get_audio().play_fx_sound("otros","medalla_plata")
            elif medalla_a_entregar == "bronze":
                usuario.save_challenge_medal(desafio, BRONZE)
                usuario.save_medal("bronce")
                self.__medalla = BRONZE
                video.show_medal(BRONZE)
                engine.get_audio().play_fx_sound("otros","medalla_bronce")
            else:
                log.warning("Medalla desconocida. (Method: close_action)")
            if not self.__medals_clear(usuario):
                if self.__desafio == "chal_c1":
                    engine.get_dialog_manager().begin_dialogue("dc_finalizar_chal4")
                    self.set_current_action({"nombre":"finalizar_chal4","continua_con_dialogo":False})
                else:
                    engine.get_dialog_manager().begin_dialogue("dc_bye")
                    self.set_current_action({"nombre":"bye","continua_con_dialogo":False})
            else:
                engine.get_dialog_manager().begin_dialogue("dc_chals_clear")
                self.set_current_action({"nombre":"chals_clear","continua_con_dialogo":True})
        #TODO: Si no sirve eliminar
        elif self.__accion['nombre'] == "ok_retake_challenge_check_answer":
            engine.get_navigation_manager().leave_room()
            contexto_pos_dialogo = NAVE
        elif self.__accion['nombre'] == "give_retro_medals":
            for _ in xrange(1,6):
                engine.get_audio().play_fx_sound("otros","medalla_bronce")
                video.show_medal(BRONZE)
                usuario.save_medal("bronce")
                engine.get_audio().wait_sound_end(tiempo=600)
            usuario.save_challenge_medal("a1", BRONZE)
            usuario.save_challenge_medal("a2", BRONZE)
            usuario.save_challenge_medal("a3", BRONZE)
            usuario.save_challenge_medal("a4", BRONZE)
            usuario.save_challenge_medal("b1", BRONZE)
            video.dissapear_medal(BRONZE)
            engine.get_dialog_manager().begin_dialogue("dc_explain_medals_finalizar_chal_3")
            self.set_current_action({"nombre":"explain_medals_finalizar_chal_3","continua_con_dialogo":False})
        elif self.__accion['nombre'] == "explain_medals_finalizar_chal_3":
            usuario.set_character_relation(self.get_name(),CHALLENGE3)
            engine.get_navigation_manager().leave_room()
            contexto_pos_dialogo = NAVE
            accion = self.__find_action(usuario.get_state().get_state_actions(), "complete_chal_3")
            engine.change_state(accion['nuevo_estado'])
            usuario.set_skill_level(CHALLENGE3)
        elif self.__accion['nombre'] == "continue_chal1":
            engine.get_dialog_manager().begin_dialogue("dc_consejo_desafio_a2")
            self.set_current_action({"nombre":"consejo_desafio_a2","continua_con_dialogo":False})
            self.set_current_challenge("chal_a2")
            contexto_pos_dialogo = ""
        elif self.__accion['nombre'] == "continue_chal2":
            engine.get_dialog_manager().begin_dialogue("dc_consejo_desafio_a4")
            self.set_current_action({"nombre":"consejo_desafio_a4","continua_con_dialogo":False})
            self.set_current_challenge("chal_a4")
            contexto_pos_dialogo = ""
        elif self.__accion['nombre'] == "finalizar_chal1":
            usuario.set_character_relation(self.get_name(),CHALLENGE1)
            engine.get_navigation_manager().leave_room()
            contexto_pos_dialogo = NAVE
            accion = self.__find_action(usuario.get_state().get_state_actions(), "complete_chal_1")
            engine.change_state(accion['nuevo_estado'])
            usuario.set_skill_level(CHALLENGE1)
        elif self.__accion['nombre'] == "finalizar_chal2":
            usuario.set_character_relation(self.get_name(),CHALLENGE2)
            engine.get_navigation_manager().leave_room()
            contexto_pos_dialogo = NAVE
            accion = self.__find_action(usuario.get_state().get_state_actions(), "complete_chal_2")
            engine.change_state(accion['nuevo_estado'])
            usuario.set_skill_level(CHALLENGE2)
        elif self.__accion['nombre'] == "finalizar_chal4":
            if self.__medalla != "":
                video.dissapear_medal(self.__medalla)
                self.__medalla = ""
            usuario.set_character_relation(self.get_name(),CHALLENGE4)
            engine.get_navigation_manager().leave_room()
            contexto_pos_dialogo = NAVE
            accion = self.__find_action(usuario.get_state().get_state_actions(), "complete_chal_4")
            engine.change_state(accion['nuevo_estado'])
            usuario.set_skill_level(CHALLENGE4)
        elif self.__accion['nombre'] == "chals_clear":
            if self.__medalla != "":
                video.dissapear_medal(self.__medalla)
                self.__medalla = ""
            engine.get_audio().play_fx_sound("otros","trofeo_marfil")
            video.show_trophy(MARFIL)
            self.__trofeo = MARFIL
            usuario.set_character_relation(self.get_name(),CHALLENGES_COMPLETED)
            if usuario.get_state().get_name() == "state15":
                usuario.set_skill_level(ALL_CLEAR)
            else:
                usuario.set_skill_level(CLEAR_CHALLENGES)
            engine.get_dialog_manager().begin_dialogue("dc_bye")
            self.set_current_action({"nombre":"bye","continua_con_dialogo":False})
        elif self.__accion['nombre'] == "go_pm1" or \
             self.__accion['nombre'] == "go_pm2" or \
             self.__accion['nombre'] == "go_pm3" or \
             self.__accion['nombre'] == "go_sd1" or \
             self.__accion['nombre'] == "go_pt1" or \
             self.__accion['nombre'] == "go_pt2" or \
             self.__accion['nombre'] == "get_medals" or \
             self.__accion['nombre'] == "pt_defeated" or \
             self.__accion['nombre'] == "chals_completed" or \
             self.__accion['nombre'] == "all_clear":
            engine.get_dialog_manager().begin_dialogue("dc_chal_retake")
            contexto_pos_dialogo = LIST
        elif self.__accion['nombre'] == "go_tut2":
            engine.get_navigation_manager().leave_room()
            contexto_pos_dialogo = NAVE
        elif self.__accion['nombre'] == "bye":
            if self.__medalla != "":
                video.dissapear_medal(self.__medalla)
                self.__medalla = ""
            if self.__trofeo != "":
                video.dissapear_trophy(self.__trofeo)
                self.__trofeo = ""
            if usuario.get_skill_level() == ALL_CLEAR:
                contexto_pos_dialogo = DIAL
                nueva_hab = usuario.get_current_room().get_right_room()
                video.club.move_to_another_room(nueva_hab,DERECHA,extra="final_juego")
                usuario.set_current_room(nueva_hab)
                accion = self.__find_action(usuario.get_state().get_state_actions(), "challenges_completed")
                engine.change_state(accion['nuevo_estado'])
            else:
                engine.get_navigation_manager().leave_room()
                contexto_pos_dialogo = NAVE
        return contexto_pos_dialogo

    def __medals_clear(self, usuario):
        medallas =  usuario.get_challenge_medals()
        for medalla in medallas.values():
            if not medalla == ORO:
                return False
        return True

    def __give_challenge_medal(self, engine, usuario):
        desafio = self.__desafio.split("_")[1]
        if (usuario.get_character_relation(self.get_name()) == CHALLENGE3 or usuario.get_character_relation(self.get_name()) == CHALLENGE4) and \
            not usuario.get_challenge_medal(desafio) == ORO:
            self.__update_user_medals(usuario, desafio)
            if self.__nro_intentos == 1:
                engine.get_dialog_manager().begin_dialogue("dc_give_gold")
                self.set_current_action({"nombre":"give_gold","continua_con_dialogo":True})
            elif self.__nro_intentos == 2:
                engine.get_dialog_manager().begin_dialogue("dc_give_silver")
                self.set_current_action({"nombre":"give_silver","continua_con_dialogo":True})
            elif self.__nro_intentos > 2:
                engine.get_dialog_manager().begin_dialogue("dc_give_bronze")
                self.set_current_action({"nombre":"give_bronze","continua_con_dialogo":True})
            else:
                log.debug("Nro. de intetos desconocidos. (Method: close_action)")
        else:
            engine.get_dialog_manager().begin_dialogue("dc_bye")
            self.set_current_action({"nombre":"bye","continua_con_dialogo":False})

    def __end_challenge(self, engine, video):
        if engine.get_dialog_manager().challenge_error():
            engine.get_dialog_manager().begin_dialogue("dc_ask_select_option_list")
            contexto = LIST
        else:
            self.__ok_challenge(engine, video)
            contexto = ""
        return contexto

    def __ok_challenge(self, engine, video):
        engine.get_audio().play_voice_sound("game","ok_"+self.__desafio)
        engine.get_audio().wait_sound_end(tiempo=600)
        nombre_personaje = self.get_name()
        relacion_con_personaje = engine.get_user().get_character_relation(nombre_personaje)
        if (relacion_con_personaje != CHALLENGE3 or relacion_con_personaje != CHALLENGE4):
            if not self.__desafio  == "chal_b1" and not self.__desafio  == "chal_b2" and not self.__desafio  == "chal_b3" and \
               not self.__desafio  == "chal_b4" and not self.__desafio  == "chal_b5":
                video.text_box.show(video.ventana)
                engine.get_dialog_manager().begin_dialogue("dc_ok_challenge_check_answer")
                self.set_current_action({"nombre":"ok_challenge_check_answer","continua_con_dialogo":True})
                engine.get_audio().play_fx_sound("otros","wait_input")
            else:
                video.dissapear_game_elements()
                video.text_box.show(video.ventana)
                if self.__desafio  == "chal_b1" and not self.__accion['nombre'] == "retake_chal_b1":
                    engine.get_dialog_manager().begin_dialogue("dc_give_retro_medals")
                    self.set_current_action({"nombre":"give_retro_medals","continua_con_dialogo":True})
                else:
                    self.__give_challenge_medal(engine, engine.get_user())
        else:
            self.__give_challenge_medal(engine, engine.get_user())

class ChSofiaDulce(Character):
    def __init__(self, nombre=-1, partida=False, dialogo=False, id=""):
        Character.__init__(self, nombre, partida, dialogo, id)
        self.__accion = {}
        self.__evento = {}
        self.__juego = {}
        self.__medalla = ""

    def set_current_action(self, accion):
        self.__accion = accion

    def set_current_event(self, evento):
        self.__evento = evento

    def set_current_game(self, juego):
        self.__juego = juego

    def __find_action(self, acciones, nombre_accion):
        for a in acciones:
            if a['nombre'] == nombre_accion:
                return a

    def init_room_action(self, engine):
        usuario = engine.get_user()
        video = engine.get_video()
        video.text_box.show(video.ventana)
        estado = usuario.get_state()
        state_problem = False
        character_relation_problem = False
        if estado.get_name() == "state8":
            if usuario.get_character_relation(self.get_name()) == MEET:
                engine.get_dialog_manager().begin_dialogue("sd_go_tut2")
                self.set_current_action({"nombre":"go_tut2","continua_con_dialogo":False})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state9":
            if usuario.get_character_relation(self.get_name()) == MEET:
                engine.get_dialog_manager().begin_dialogue("sd_go_chal3")
                self.set_current_action({"nombre":"go_chal3","continua_con_dialogo":False})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state10":
            if usuario.get_character_relation(self.get_name()) == MEET or \
               usuario.get_character_relation(self.get_name()) == DRAW1 or \
               usuario.get_character_relation(self.get_name()) == LOSE1:
                engine.get_dialog_manager().begin_dialogue("sd_init_first_game")
                self.set_current_action({"nombre":"init_first_game","continua_con_dialogo":False})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state11":
            if usuario.get_character_relation(self.get_name()) == MEET or \
               usuario.get_character_relation(self.get_name()) == DRAW1 or \
               usuario.get_character_relation(self.get_name()) == LOSE1:
                engine.get_dialog_manager().begin_dialogue("sd_init_first_game")
                self.set_current_action({"nombre":"init_first_game","continua_con_dialogo":False})
            elif usuario.get_character_relation(self.get_name()) == WON1 or \
               usuario.get_character_relation(self.get_name()) == DRAW2 or \
               usuario.get_character_relation(self.get_name()) == LOSE2:
                engine.get_dialog_manager().begin_dialogue("sd_init_second_game")
                self.set_current_action({"nombre":"init_second_game","continua_con_dialogo":False})
            elif usuario.get_character_relation(self.get_name()) == WON2 or \
                 usuario.get_character_relation(self.get_name()) == DRAW3 or \
                 usuario.get_character_relation(self.get_name()) == LOSE3:
                engine.get_dialog_manager().begin_dialogue("sd_init_third_game")
                self.set_current_action({"nombre":"init_third_game","continua_con_dialogo":False})
            elif usuario.get_character_relation(self.get_name()) == WON3:
                engine.get_dialog_manager().begin_dialogue("sd_go_chal4")
                self.set_current_action({"nombre":"go_chal4","continua_con_dialogo":True})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state12":
            if usuario.get_character_relation(self.get_name()) == MEET or \
               usuario.get_character_relation(self.get_name()) == DRAW1 or \
               usuario.get_character_relation(self.get_name()) == LOSE1:
                engine.get_dialog_manager().begin_dialogue("sd_init_first_game")
                self.set_current_action({"nombre":"init_first_game","continua_con_dialogo":False})
            elif usuario.get_character_relation(self.get_name()) == WON1 or \
               usuario.get_character_relation(self.get_name()) == DRAW2 or \
               usuario.get_character_relation(self.get_name()) == LOSE2:
                engine.get_dialog_manager().begin_dialogue("sd_init_second_game")
                self.set_current_action({"nombre":"init_second_game","continua_con_dialogo":False})
            elif usuario.get_character_relation(self.get_name()) == WON2 or \
                 usuario.get_character_relation(self.get_name()) == DRAW3 or \
                 usuario.get_character_relation(self.get_name()) == LOSE3:
                engine.get_dialog_manager().begin_dialogue("sd_init_third_game")
                self.set_current_action({"nombre":"init_third_game","continua_con_dialogo":False})
            elif usuario.get_character_relation(self.get_name()) == WON3:
                engine.get_dialog_manager().begin_dialogue("sd_go_pt2")
                self.set_current_action({"nombre":"go_pt2","continua_con_dialogo":True})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state13":
            if usuario.get_character_relation(self.get_name()) == MEET or \
               usuario.get_character_relation(self.get_name()) == DRAW1 or \
               usuario.get_character_relation(self.get_name()) == LOSE1:
                engine.get_dialog_manager().begin_dialogue("sd_init_first_game")
                self.set_current_action({"nombre":"init_first_game","continua_con_dialogo":False})
            elif usuario.get_character_relation(self.get_name()) == WON1 or \
               usuario.get_character_relation(self.get_name()) == DRAW2 or \
               usuario.get_character_relation(self.get_name()) == LOSE2:
                engine.get_dialog_manager().begin_dialogue("sd_init_second_game")
                self.set_current_action({"nombre":"init_second_game","continua_con_dialogo":False})
            elif usuario.get_character_relation(self.get_name()) == WON2 or \
                 usuario.get_character_relation(self.get_name()) == DRAW3 or \
                 usuario.get_character_relation(self.get_name()) == LOSE3:
                engine.get_dialog_manager().begin_dialogue("sd_init_third_game")
                self.set_current_action({"nombre":"init_third_game","continua_con_dialogo":False})
            elif usuario.get_character_relation(self.get_name()) == WON3:
               engine.get_dialog_manager().begin_dialogue("sd_get_medals")
               self.set_current_action({"nombre":"get_medals","continua_con_dialogo":True})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state14":
            if usuario.get_character_relation(self.get_name()) == MEET or \
               usuario.get_character_relation(self.get_name()) == DRAW1 or \
               usuario.get_character_relation(self.get_name()) == LOSE1:
                engine.get_dialog_manager().begin_dialogue("sd_init_first_game")
                self.set_current_action({"nombre":"init_first_game","continua_con_dialogo":False})
            elif usuario.get_character_relation(self.get_name()) == WON1 or \
               usuario.get_character_relation(self.get_name()) == DRAW2 or \
               usuario.get_character_relation(self.get_name()) == LOSE2:
                engine.get_dialog_manager().begin_dialogue("sd_init_second_game")
                self.set_current_action({"nombre":"init_second_game","continua_con_dialogo":False})
            elif usuario.get_character_relation(self.get_name()) == WON2 or \
                 usuario.get_character_relation(self.get_name()) == DRAW3 or \
                 usuario.get_character_relation(self.get_name()) == LOSE3:
                engine.get_dialog_manager().begin_dialogue("sd_init_third_game")
                self.set_current_action({"nombre":"init_third_game","continua_con_dialogo":False})
            elif usuario.get_character_relation(self.get_name()) == WON3:
                engine.get_dialog_manager().begin_dialogue("sd_get_medals")
                self.set_current_action({"nombre":"get_medals","continua_con_dialogo":True})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state15":
            if usuario.get_character_relation(self.get_name()) == WON1 or \
               usuario.get_character_relation(self.get_name()) == DRAW2 or \
               usuario.get_character_relation(self.get_name()) == LOSE2:
                engine.get_dialog_manager().begin_dialogue("sd_init_second_game")
                self.set_current_action({"nombre":"init_second_game","continua_con_dialogo":False})
            elif usuario.get_character_relation(self.get_name()) == WON2 or \
                 usuario.get_character_relation(self.get_name()) == DRAW3 or \
                 usuario.get_character_relation(self.get_name()) == LOSE3:
                engine.get_dialog_manager().begin_dialogue("sd_init_third_game")
                self.set_current_action({"nombre":"init_third_game","continua_con_dialogo":False})
            elif usuario.get_character_relation(self.get_name()) == WON3:
                engine.get_dialog_manager().begin_dialogue("sd_pt_defeated")
                self.set_current_action({"nombre":"pt_defeated","continua_con_dialogo":True})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state17":
            if usuario.get_character_relation(self.get_name()) == WON3:
                engine.get_dialog_manager().begin_dialogue("sd_all_clear")
                self.set_current_action({"nombre":"all_clear","continua_con_dialogo":True})
            else:
                character_relation_problem = True
        else:
            state_problem = True
        if state_problem:
            log.error("Estado invalido! (Class: ChSofiaDulce, Method: init_room_action)")
        if character_relation_problem:
            log.debug("No hay accion asociada a la relacion con Sofia Dulce en el %s (Method: init_room_action)", estado.get_name())

    def init_list_action(self, id_action, engine):
        engine.change_context(DIAL)
        #video = engine.get_video()
        #usuario = engine.get_user()
        #video.text_box.disappear(video.ventana)
        if id_action == "jugar_sin_jugadas_posibles":
            juego_con_jp = False
        else:
            juego_con_jp = True
        #if usuario.get_character_relation(self.get_name()) == WON1 or \
        #    usuario.get_character_relation(self.get_name()) == DRAW2 or \
        #    usuario.get_character_relation(self.get_name()) == LOSE2:
        #    engine.init_game("partida2_sd",juego_con_jp)
        #    self.set_current_game({"nombre":"partida2"})
        #elif usuario.get_character_relation(self.get_name()) == WON2 or \
        #     usuario.get_character_relation(self.get_name()) == DRAW3 or \
        #     usuario.get_character_relation(self.get_name()) == LOSE3:
        #     engine.init_game("partida3_sd",juego_con_jp)
        #     self.set_current_game({"nombre":"partida3"})
        #elif usuario.get_character_relation(self.get_name()) == WON3:
        engine.init_game("revancha_sd", juego_con_jp, nivel=Ai.MEDIO)
        self.__juego = {"nombre":"revancha","objeto":engine.juego}
        engine.get_dialog_manager().begin_dialogue("sd_prematch_phrase")
        self.set_current_action({"nombre":"prematch_phrase","continua_con_dialogo":False})
        #video.init_game_elements(engine.juego, engine.get_audio())

    def close_action(self, param):
        engine = param
        usuario = engine.get_user()
        video = engine.get_video()
        contexto_pos_dialogo = ""
        if not self.__accion['continua_con_dialogo']:
            video.text_box.disappear(video.ventana)
        if self.__accion['nombre'] == "go_tut2":
            engine.get_navigation_manager().leave_room()
            contexto_pos_dialogo = NAVE
        elif self.__accion['nombre'] == "go_chal3":
            engine.get_navigation_manager().leave_room()
            contexto_pos_dialogo = NAVE
        elif self.__accion['nombre'] == "go_chal4" or \
             self.__accion['nombre'] == "get_medals" or \
             self.__accion['nombre'] == "pt_defeated" or \
             self.__accion['nombre'] == "all_clear" or \
             self.__accion['nombre'] == "go_pt2":
            engine.get_dialog_manager().begin_dialogue("sd_rematch_game")
            self.set_current_action({"nombre":"rematch_game","continua_con_dialogo":False})
            contexto_pos_dialogo = LIST
        elif self.__accion['nombre'] == "init_first_game":
            contexto_pos_dialogo = PLAY
            engine.init_game("partida1_sd", nivel=Ai.MEDIO)
            self.__juego = {"nombre":"partida1"}
            video.init_game_elements(engine.juego, engine.get_audio())
        elif self.__accion['nombre'] == "init_second_game":
            contexto_pos_dialogo = PLAY
            engine.init_game("partida2_sd", nivel=Ai.MEDIO)
            self.__juego = {"nombre":"partida2"}
            video.init_game_elements(engine.juego, engine.get_audio())
        elif self.__accion['nombre'] == "init_third_game":
            contexto_pos_dialogo = PLAY
            engine.init_game("partida3_sd", nivel=Ai.MEDIO)
            self.__juego = {"nombre":"partida3"}
            video.init_game_elements(engine.juego, engine.get_audio())
        elif self.__accion['nombre'] == "prematch_phrase":
            contexto_pos_dialogo = PLAY
            video.text_box.disappear(video.ventana)
            video.init_game_elements(self.__juego["objeto"], engine.get_audio())
        elif self.__accion['nombre'] == "dp_revancha" or \
             self.__accion['nombre'] == "dp_juego_empatado_o_ganado":
            contexto_pos_dialogo = NAVE
            engine.get_navigation_manager().leave_room()
        elif self.__accion['nombre'] == "dial_dp_juego_perdido":
            usuario = engine.get_user()
            contexto_pos_dialogo = DIAL
            if usuario.get_character_relation(self.get_name()) == WON1:
                engine.get_audio().play_fx_sound("otros","medalla_bronce")
                video.show_medal(BRONZE)
                usuario.save_medal("bronce")
                self.__medalla = BRONZE
            if usuario.get_character_relation(self.get_name()) == WON2:
                engine.get_audio().play_fx_sound("otros","medalla_plata")
                video.show_medal(PLATA)
                usuario.delete_medal("bronce")
                usuario.save_medal("plata")
                self.__medalla = PLATA
            if usuario.get_character_relation(self.get_name()) == WON3:
                engine.get_audio().play_fx_sound("otros","medalla_oro")
                video.show_medal(ORO)
                usuario.delete_medal("plata")
                usuario.save_medal("oro")
                self.__medalla = ORO
            engine.get_audio().wait_sound_end(tiempo=600)
            if self.__juego['nombre'] == "partida1":
                engine.get_dialog_manager().begin_dialogue("sd_give_medal1")
            elif self.__juego['nombre'] == "partida2":
                engine.get_dialog_manager().begin_dialogue("sd_give_medal2")
            elif self.__juego['nombre'] == "partida3":
                engine.get_dialog_manager().begin_dialogue("sd_give_medal3")
            self.set_current_action({"nombre":"dp_entregar_medalla","continua_con_dialogo":False})
        elif self.__accion['nombre'] == "dp_entregar_medalla":
            if self.__medalla != "":
                video.dissapear_medal(self.__medalla)
                self.__medalla = ""
            if usuario.get_state().get_name() == "state10":
                accion = self.__find_action(usuario.get_state().get_state_actions(), "won_game")
                engine.change_state(accion['nuevo_estado'])
            contexto_pos_dialogo = NAVE
            engine.get_navigation_manager().leave_room()
        return contexto_pos_dialogo

    def presentation(self, engine):
        engine.get_audio().stop_sound()
        video = engine.get_video()
        video.text_box.show(video.ventana)
        engine.get_dialog_manager().begin_dialogue("sd_presentation")

    def close_event(self, param):
        engine = param
        usuario = engine.get_user()
        video = engine.get_video()
        contexto_pos_dialogo = ""
        if video.text_box.is_up():
            video.text_box.disappear(video.ventana)
        if self.__evento['nombre'] == "presentacion":
            usuario.set_character_relation(self.get_name(), MEET)
            if self.__evento['consecuencia'] == "change_state":
                engine.change_state(self.__evento['nuevo_estado'])
            self.__evento.clear()
            hab = engine.get_club().get_room_by_name("tercer piso")
            video.club.show_room(hab)
            contexto_pos_dialogo = NAVE
        return contexto_pos_dialogo

    def close_game(self, engine):
        ganador = engine.juego.get_final_result()
        resultado = ""
        video = engine.get_video()
        video.dissapear_scores()
        video.dissapear_board()
        if ganador != "":
            if ganador.get_name() == PC:
                resultado = GANAR
            else:
                resultado = PERDER
        else:
            resultado = EMPATAR
        if resultado == PERDER:
            if self.__juego['nombre'] == "partida1":
                engine.get_dialog_manager().begin_dialogue("sd_perdio_juego1")
                engine.get_user().set_character_relation(self.get_name(),WON1)
            elif self.__juego['nombre'] == "partida2":
                engine.get_dialog_manager().begin_dialogue("sd_perdio_juego2")
                engine.get_user().set_character_relation(self.get_name(),WON2)
            elif self.__juego['nombre'] == "partida3":
                engine.get_dialog_manager().begin_dialogue("sd_perdio_juego3")
                engine.get_user().set_character_relation(self.get_name(),WON3)
            elif self.__juego['nombre'] == "revancha":
                engine.get_dialog_manager().begin_dialogue("sd_perdio_revancha")
        else:
            if resultado == EMPATAR:
                engine.get_dialog_manager().begin_dialogue("sd_empato_juego")
                if self.__juego['nombre'] == "partida1":
                    engine.get_user().set_character_relation(self.get_name(),DRAW1)
                elif self.__juego['nombre'] == "partida2":
                    engine.get_user().set_character_relation(self.get_name(),DRAW2)
                elif self.__juego['nombre'] == "partida3":
                    engine.get_user().set_character_relation(self.get_name(),DRAW3)
            elif resultado == GANAR:
                engine.get_dialog_manager().begin_dialogue("sd_gano_juego")
                if self.__juego['nombre'] == "partida1":
                    engine.get_user().set_character_relation(self.get_name(),LOSE1)
                elif self.__juego['nombre'] == "partida2":
                    engine.get_user().set_character_relation(self.get_name(),LOSE2)
                elif self.__juego['nombre'] == "partida3":
                    engine.get_user().set_character_relation(self.get_name(),LOSE3)
        contexto_pos_juego = DIAL
        if self.__juego['nombre'] == "revancha":
            self.set_current_action({"nombre":"dp_revancha","continua_con_dialogo":False})
        else:
            if resultado == PERDER:
                self.set_current_action({"nombre":"dial_dp_juego_perdido","continua_con_dialogo":True})
            else:
                self.set_current_action({"nombre":"dp_juego_empatado_o_ganado","continua_con_dialogo":False})
        return contexto_pos_juego

class ChProtasio(Character):
    def __init__(self, nombre=-1, partida=False, dialogo=False, id=""):
        Character.__init__(self, nombre, partida, dialogo, id)
        self.__accion = {}
        self.__evento = {}
        self.__juego = {}
        self.__medalla = ""

    def set_current_action(self, accion):
        self.__accion = accion

    def set_current_event(self, evento):
        self.__evento = evento

    def __find_action(self, acciones, nombre_accion):
        for a in acciones:
            if a['nombre'] == nombre_accion:
                return a

    def fin_juego(self, engine):
        engine.get_audio().stop_sound()
        video = engine.get_video()
        video.text_box.show(video.ventana)
        engine.get_dialog_manager().begin_dialogue("end_game")

    def close_event(self, param):
        engine = param
        usuario = engine.get_user()
        video = engine.get_video()
        contexto_pos_dialogo = ""
        video.text_box.disappear(video.ventana)
        if self.__evento['nombre'] == "end_game":
            self.__evento.clear()
            hab = usuario.get_current_room()
            video.club.show_room(hab)
            contexto_pos_dialogo = NAVE
            accion = self.__find_action(usuario.get_state().get_state_actions(), "after_end")
            engine.change_state(accion['nuevo_estado'])
        return contexto_pos_dialogo

    def init_room_action(self, engine):
        usuario = engine.get_user()
        video = engine.get_video()
        video.text_box.show(video.ventana)
        estado = usuario.get_state()
        state_problem = False
        character_relation_problem = False
        if estado.get_name() == "state10":
            if usuario.get_character_relation(self.get_name()) == NULL:
                engine.get_dialog_manager().begin_dialogue("pt_intro_infection_go_sd")
                self.set_current_action({"nombre":"intro_infection_go_sd","continua_con_dialogo":False})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state11":
            if usuario.get_character_relation(self.get_name()) == NULL:
                engine.get_dialog_manager().begin_dialogue("pt_intro_go_chal4")
                self.set_current_action({"nombre":"intro_go_chal4","continua_con_dialogo":False})
            elif usuario.get_character_relation(self.get_name()) == MEET:
                engine.get_dialog_manager().begin_dialogue("pt_go_chal4")
                self.set_current_action({"nombre":"go_chal4","continua_con_dialogo":False})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state12":
            if usuario.get_character_relation(self.get_name()) == MEET or \
               usuario.get_character_relation(self.get_name()) == DRAW1 or \
               usuario.get_character_relation(self.get_name()) == LOSE1:
                if usuario.get_character_relation('sofia dulce') == WON1 or \
                   usuario.get_character_relation('sofia dulce') == WON2 or \
                   usuario.get_character_relation('sofia dulce') == WON3:
                    engine.get_dialog_manager().begin_dialogue("pt_init_first_game")
                    self.set_current_action({"nombre":"init_first_game","continua_con_dialogo":False})
                else:
                    engine.get_dialog_manager().begin_dialogue("pt_go_sd")
                    self.set_current_action({"nombre":"go_sd","continua_con_dialogo":False})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state13":
            if usuario.get_character_relation(self.get_name()) == WON1 or \
               usuario.get_character_relation(self.get_name()) == DRAW2 or \
               usuario.get_character_relation(self.get_name()) == LOSE2:
                hash_medallas = usuario.get_medals()
                total_medallas = hash_medallas["bronce"] + hash_medallas["plata"] + hash_medallas["oro"]
                if total_medallas >= 12 and hash_medallas["oro"] >= 2:
                    engine.get_dialog_manager().begin_dialogue("pt_init_second_game")
                    self.set_current_action({"nombre":"init_second_game","continua_con_dialogo":False})
                else:
                    engine.get_dialog_manager().begin_dialogue("pt_match2_more_medals")
                    self.set_current_action({"nombre":"match2_more_medals","continua_con_dialogo":False})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state14":
            if usuario.get_character_relation(self.get_name()) == WON2 or \
               usuario.get_character_relation(self.get_name()) == DRAW3 or \
               usuario.get_character_relation(self.get_name()) == LOSE3:
                hash_medallas = usuario.get_medals()
                total_medallas = hash_medallas["bronce"] + hash_medallas["plata"] + hash_medallas["oro"]
                if total_medallas >= 18 and hash_medallas["oro"] >= 4:
                    if usuario.get_character_relation('sofia dulce') == WON3:
                        engine.get_dialog_manager().begin_dialogue("pt_init_third_game")
                        self.set_current_action({"nombre":"init_third_game","continua_con_dialogo":False})
                    else:
                        engine.get_dialog_manager().begin_dialogue("pt_go_sd2")
                        self.set_current_action({"nombre":"go_sd2","continua_con_dialogo":False})
                else:
                    engine.get_dialog_manager().begin_dialogue("pt_match3_more_medals")
                    self.set_current_action({"nombre":"match3_more_medals","continua_con_dialogo":False})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state15":
            if usuario.get_character_relation(self.get_name()) == WON3:
                engine.get_dialog_manager().begin_dialogue("pt_pt_defeated")
                self.set_current_action({"nombre":"pt_defeated","continua_con_dialogo":True})
            else:
                character_relation_problem = True
        elif estado.get_name() == "state17":
            if usuario.get_character_relation(self.get_name()) == WON3:
                engine.get_dialog_manager().begin_dialogue("pt_all_clear")
                self.set_current_action({"nombre":"all_clear","continua_con_dialogo":True})
            else:
                character_relation_problem = True
        else:
            state_problem = True
        if state_problem:
            log.error("Estado invalido! (Class: ChProtasio, Method: init_room_action)")
        if character_relation_problem:
            log.debug("No hay accion asociada a la relacion con Protasio en el %s (Method: init_room_action)", estado.get_name())

    def init_list_action(self, id_action, engine):
        engine.change_context(DIAL)
        #video = engine.get_video()
        #video.text_box.disappear(video.ventana)
        engine.init_game("revancha_pt", con_jugadas_posibles=False, nivel=Ai.DIFICIL)
        self.__juego = {"nombre":"revancha", "objeto":engine.juego}
        engine.get_dialog_manager().begin_dialogue("pt_prematch_phrase")
        self.set_current_action({"nombre":"prematch_phrase","continua_con_dialogo":False})
        #video.init_game_elements(engine.juego, engine.get_audio())

    def close_action(self, param):
        engine = param
        usuario = engine.get_user()
        video = engine.get_video()
        contexto_pos_dialogo = ""
        if not self.__accion['continua_con_dialogo']:
            video.text_box.disappear(video.ventana)
        if self.__accion['nombre'] == "intro_infection_go_sd":
            engine.get_user().set_character_relation(self.get_name(),MEET)
            accion = self.__find_action(usuario.get_state().get_state_actions(), "infection_club")
            engine.change_state(accion['nuevo_estado'])
            engine.get_navigation_manager().leave_room()
            contexto_pos_dialogo = NAVE
        elif self.__accion['nombre'] == "intro_go_chal4":
            engine.get_user().set_character_relation(self.get_name(),MEET)
            engine.get_navigation_manager().leave_room()
            contexto_pos_dialogo = NAVE
        elif self.__accion['nombre'] == "go_chal4" or \
             self.__accion['nombre'] == "match2_more_medals" or \
             self.__accion['nombre'] == "go_sd2" or \
             self.__accion['nombre'] == "go_sd" or \
             self.__accion['nombre'] == "match3_more_medals":
            engine.get_navigation_manager().leave_room()
            contexto_pos_dialogo = NAVE
        elif self.__accion['nombre'] == "pt_defeated" or \
             self.__accion['nombre'] == "all_clear":
            engine.get_dialog_manager().begin_dialogue("pt_rematch_game")
            self.set_current_action({"nombre":"rematch_game","continua_con_dialogo":False})
            contexto_pos_dialogo = LIST
        elif self.__accion['nombre'] == "init_first_game":
            contexto_pos_dialogo = PLAY
            engine.init_game("partida1_pt",con_jugadas_posibles=False,nivel=Ai.DIFICIL)
            self.__juego = {"nombre":"partida1"}
            video.init_game_elements(engine.juego, engine.get_audio())
        elif self.__accion['nombre'] == "init_second_game":
            contexto_pos_dialogo = PLAY
            engine.init_game("partida2_pt",con_jugadas_posibles=False,nivel=Ai.DIFICIL)
            self.__juego = {"nombre":"partida2"}
            video.init_game_elements(engine.juego, engine.get_audio())
        elif self.__accion['nombre'] == "init_third_game":
            contexto_pos_dialogo = PLAY
            engine.init_game("partida3_pt",con_jugadas_posibles=False,nivel=Ai.DIFICIL)
            self.__juego = {"nombre":"partida3"}
            video.init_game_elements(engine.juego, engine.get_audio())
        elif self.__accion['nombre'] == "prematch_phrase":
            contexto_pos_dialogo = PLAY
            video.text_box.disappear(video.ventana)
            video.init_game_elements(self.__juego["objeto"], engine.get_audio())
        elif self.__accion['nombre'] == "dp_revancha" or \
             self.__accion['nombre'] == "dp_juego_empatado_o_ganado":
            contexto_pos_dialogo = NAVE
            engine.get_navigation_manager().leave_room()
        elif self.__accion['nombre'] == "dial_dp_juego_perdido":
            usuario = engine.get_user()
            contexto_pos_dialogo = DIAL
            if usuario.get_character_relation(self.get_name()) == WON1:
                engine.get_audio().play_fx_sound("otros","medalla_bronce")
                video.show_medal(BRONZE)
                usuario.save_medal("bronce")
                self.__medalla = BRONZE
            if usuario.get_character_relation(self.get_name()) == WON2:
                engine.get_audio().play_fx_sound("otros","medalla_plata")
                video.show_medal(PLATA)
                usuario.delete_medal("bronce")
                usuario.save_medal("plata")
                self.__medalla = PLATA
            if usuario.get_character_relation(self.get_name()) == WON3:
                engine.get_audio().play_fx_sound("otros","medalla_oro")
                video.show_medal(ORO)
                usuario.delete_medal("plata")
                usuario.save_medal("oro")
                self.__medalla = ORO
            engine.get_audio().wait_sound_end(tiempo=600)
            if usuario.get_character_relation(self.get_name()) == WON3:
                self.set_current_action({"nombre":"dp_entregar_medalla","continua_con_dialogo":True})
            else:
                self.set_current_action({"nombre":"dp_entregar_medalla","continua_con_dialogo":False})
        elif self.__accion['nombre'] == "dp_entregar_medalla":
            if self.__medalla != "":
                video.dissapear_medal(self.__medalla)
                self.__medalla = ""
            if usuario.get_character_relation('protasio') == WON3:
                contexto_pos_dialogo = DIAL
                engine.get_dialog_manager().begin_dialogue("pt_give_trophy")
                self.set_current_action({"nombre":"give_trophy","continua_con_dialogo":True})
            else:
                accion = self.__find_action(usuario.get_state().get_state_actions(), "won_game")
                contexto_pos_dialogo = NAVE
                engine.get_navigation_manager().leave_room()
                engine.change_state(accion['nuevo_estado'])
        elif self.__accion['nombre'] == "give_trophy":
            engine.get_audio().play_fx_sound("otros","trofeo_madera")
            video.show_trophy(MADERA)
            pygame.time.wait(800)
            video.dissapear_trophy(MADERA)
            engine.get_dialog_manager().begin_dialogue("pt_match3_lose_cont")
            self.set_current_action({"nombre":"match3_lose_cont","continua_con_dialogo":False})
        elif self.__accion['nombre'] == "match3_lose_cont":
            if usuario.get_character_relation('don cano') == CHALLENGES_COMPLETED:
                accion = self.__find_action(usuario.get_state().get_state_actions(), "won_game_and_challenges_completed")
                usuario.set_skill_level(ALL_CLEAR)
                contexto_pos_dialogo = DIAL
                nueva_hab = usuario.get_current_room().get_left_room()
                video.club.move_to_another_room(nueva_hab,IZQUIERDA,extra="final_juego")
                usuario.set_current_room(nueva_hab)
            else:
                accion = self.__find_action(usuario.get_state().get_state_actions(), "won_game")
                usuario.set_skill_level(CLEAR_GAMES)
                contexto_pos_dialogo = NAVE
                engine.get_navigation_manager().leave_room()
            engine.change_state(accion['nuevo_estado'])
        return contexto_pos_dialogo

    def close_game(self, engine):
        ganador = engine.juego.get_final_result()
        resultado = ""
        video = engine.get_video()
        video.dissapear_scores()
        video.dissapear_board()
        if ganador != "":
            if ganador.get_name() == PC:
                resultado = GANAR
            else:
                resultado = PERDER
        else:
            resultado = EMPATAR
        if resultado == PERDER:
            if self.__juego['nombre'] == "partida1":
                engine.get_dialog_manager().begin_dialogue("pt_perdio_juego1")
                engine.get_user().set_character_relation(self.get_name(),WON1)
            elif self.__juego['nombre'] == "partida2":
                engine.get_dialog_manager().begin_dialogue("pt_perdio_juego2")
                engine.get_user().set_character_relation(self.get_name(),WON2)
            elif self.__juego['nombre'] == "partida3":
                engine.get_dialog_manager().begin_dialogue("pt_perdio_juego3")
                engine.get_user().set_character_relation(self.get_name(),WON3)
            elif self.__juego['nombre'] == "revancha":
                engine.get_dialog_manager().begin_dialogue("pt_perdio_revancha")
        else:
            if resultado == EMPATAR:
                engine.get_dialog_manager().begin_dialogue("pt_empato_juego")
                if self.__juego['nombre'] == "partida1":
                    engine.get_user().set_character_relation(self.get_name(),DRAW1)
                elif self.__juego['nombre'] == "partida2":
                    engine.get_user().set_character_relation(self.get_name(),DRAW2)
                elif self.__juego['nombre'] == "partida3":
                    engine.get_user().set_character_relation(self.get_name(),DRAW3)
            elif resultado == GANAR:
                engine.get_dialog_manager().begin_dialogue("pt_gano_juego")
                if self.__juego['nombre'] == "partida1":
                    engine.get_user().set_character_relation(self.get_name(),LOSE1)
                elif self.__juego['nombre'] == "partida2":
                    engine.get_user().set_character_relation(self.get_name(),LOSE2)
                elif self.__juego['nombre'] == "partida3":
                    engine.get_user().set_character_relation(self.get_name(),LOSE3)
        contexto_pos_juego = DIAL
        if self.__juego['nombre'] == "revancha":
            self.set_current_action({"nombre":"dp_revancha","continua_con_dialogo":False})
        else:
            if resultado == PERDER:
                self.set_current_action({"nombre":"dial_dp_juego_perdido","continua_con_dialogo":True})
            else:
                self.set_current_action({"nombre":"dp_juego_empatado_o_ganado","continua_con_dialogo":False})
        return contexto_pos_juego
