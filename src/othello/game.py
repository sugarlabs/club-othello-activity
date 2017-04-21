from referee import Referee
from ai import Ai
from player import PC, HUMANO, VIRTUAL
import pygame, os, time, board, logging
from sugar.activity.activity import get_activity_root

log = logging.getLogger( 'src.othello.game' )
log.setLevel( logging.DEBUG )

class Game:
    def __init__(self,tablero,jugador1,jugador2,con_jugadas_posibles=True,nivel=Ai.FACIL, write_path=""):
        #self.__gui = Gui()
        #self.__tablero = self.__gui.init_board().get_board()
        self.__tablero_g = tablero
        self.__tablero = tablero.get_logical_board()
        #Iniciliazo la inteligencia para la PC
        self.__pc = Ai(nivel)
        #Inicializo un vector de jugadores
        self.__jugadores = [jugador1,jugador2]
        self.__ganador = ""
        self.__nro_turno = 0
        self.__termino_juego = False
        self.__juego_mesh = False
        self.__con_jugadas_posibles = con_jugadas_posibles
        self.__lista_jugadas_posibles = []
        if write_path != "":
            #Imprimo en el log la configuracion del juego que se inicia
            try:
                f = open(os.path.abspath(write_path + "/data/game.log"),'r')
                f.close()
                self.__log_file = open(os.path.abspath(write_path + "/data/game.log"),'a')
                print >> self.__log_file, '\nGAME LOG: ' + time.asctime()
            except:
                self.__log_file = open(os.path.abspath(write_path + "/data/game.log"),'w')
                print >> self.__log_file, 'GAME LOG: ' + time.asctime()
            print >> self.__log_file, 'Tablero: ' + str(self.__tablero.get_dimension()) + 'x' + str(self.__tablero.get_dimension())
            if jugador1.get_color() == board.BLANCO and jugador1.get_name() == PC:
                print >> self.__log_file, 'PC: Blanco'
                print >> self.__log_file, 'Jugador: Negro'
            elif jugador1.get_name() == HUMANO and jugador2.get_name() == HUMANO:
                if jugador1.get_color() == board.BLANCO:
                    print >> self.__log_file, 'Jugador1: Blanco'
                    print >> self.__log_file, 'Jugador2: Negro'
                else:
                    print >> self.__log_file, 'Jugador1: Negro'
                    print >> self.__log_file, 'Jugador2: Blanco'
            else:
                print >> self.__log_file, 'PC: Negro'
                print >> self.__log_file, 'Jugador: Blanco'

    def __del__(self):
        try:
            self.__log_file.close()
        except:
            log.debug("Problemas al cerrar el descriptor de archivo. (Game Class)")

    def get_game_log_file(self):
        return self.__log_file

    def get_turn(self):
        return self.__jugadores[self.__turno]

    def set_turn(self,jugador):
        if jugador.equal(self.__jugadores[0]):
            self.__turno = 0
        elif jugador.equal(self.__jugadores[1]):
            self.__turno = 1
        else:
            raise Exception("No se pudo asignar el turno, el jugador no existe! (Game Class)")
        self.update_possible_moves()

    def update_possible_moves(self):
        self.__lista_jugadas_posibles = Referee.possibles_moves(self.get_turn().get_color(),self.__tablero)

    def increase_turn_number(self):
        self.__nro_turno += 1

    def get_turn_number(self):
        return self.__nro_turno

    def __next_turn(self):
        color = self.__jugadores[self.__turno].get_color()
        #Veo si hay jugada posible para el turno siguiente, es decir si era Blanco para el Negro
        if Referee.is_at_least_one_move(color*-1, self.__tablero):
            return True
        else:
            return False

    def with_possibles_moves(self):
        return self.__con_jugadas_posibles

    def change_turn(self):
        #if self.__next_turn():
        self.__turno = (self.__turno - 1) * -1
        self.increase_turn_number()
        #    return True
        #else:
        #    return False

    def is_over(self):
        if Referee.is_at_least_one_move(board.BLANCO, self.__tablero):
            return False
        elif Referee.is_at_least_one_move(board.NEGRO, self.__tablero):
            return False
        else:
            return True

    def init_next_turn(self):
        pass

    def __print_log(self, mensaje):
        try:
            print >> self.__log_file, mensaje
        except:
            print mensaje

    def get_mesh_game(self):
        return self.__juego_mesh

    def set_mesh_game(self, valor):
        self.__juego_mesh = valor

    def play(self, coord="", audio="", marcador="", ventana="", extra=""):
        pc_manual = False
        if not self.is_over():
            jugadas_posibles_real = len(self.__lista_jugadas_posibles)
            self.__ultima_jugada_humano = ""
            if jugadas_posibles_real > 0:
                nombre_de_turno = self.get_turn().get_name()
                color_de_turno =  self.get_turn().get_color()
                if nombre_de_turno == HUMANO or nombre_de_turno == VIRTUAL:
                    if coord == "":
                        coord = self.__tablero_g.get_coord_selected_cell()
                    if color_de_turno == board.BLANCO:
                        pudo_jugar = self.__tablero_g.set_piece(coord,color_de_turno,"blanco",audio, ventana)
                        sonido_voltear = "voltear_negro"
                    else:
                        pudo_jugar = self.__tablero_g.set_piece(coord,color_de_turno,"negro",audio, ventana)
                        sonido_voltear = "voltear_blanco"
                    if pudo_jugar:
                        marcador.render_numbers(self.__tablero,self.get_turn().get_color(),ventana)
                        self.__ultima_jugada_humano = coord
                        self.__print_log("JUGADOR jugo en: " + str(self.__ultima_jugada_humano))
                        if nombre_de_turno == VIRTUAL:
                            self.__tablero_g.set_coord_selected_cell(coord)
                elif nombre_de_turno == PC:
                    if coord == "":
                        pudo_jugar = self.play_pc()
                    else:
                        pudo_jugar = self.__tablero_g.set_piece(coord,color_de_turno,"blanco",audio, ventana)
                        sonido_voltear = "voltear_negro"
                        pc_manual = True
                    if pudo_jugar:
                        if coord == "":
                            coord = self.get_last_pc_move()
                        self.__tablero_g.set_coord_selected_cell(coord)
                        if not pc_manual:
                            if color_de_turno == board.BLANCO:
                                pudo_jugar = self.__tablero_g.set_piece(coord,color_de_turno,"blanco",audio, ventana)
                                sonido_voltear = "voltear_negro"
                            else:
                                pudo_jugar = self.__tablero_g.set_piece(coord,color_de_turno,"negro",audio, ventana)
                                sonido_voltear = "voltear_blanco"
                        marcador.render_numbers(self.__tablero,self.get_turn().get_color(),ventana)
                        self.__print_log("PC jugo en: " + str(coord))
                if pudo_jugar:
                    audio.wait_sound_end()
                    self.__tablero_g.do_line_animation(coord, color_de_turno, sonido_voltear, audio, marcador, ventana)
            else:
                pudo_jugar = True
                audio.play_voice_sound("game", "pasa_el_turno")
                audio.wait_sound_end()
                #extra = {"play_turn_sound":False}
            if pudo_jugar:                
                if not self.is_over():
                    self.change_turn()
                    self.update_possible_moves()
                    if self.__con_jugadas_posibles:
                        if extra == "" or (not extra == "" and not "update_possibles_moves" in extra):
                            self.__tablero_g.lista_jugadas = self.__lista_jugadas_posibles                            
                    if not extra == "":
                        if not "change_score_color" in extra:
                            marcador.render_all(self.__tablero,self.get_turn().get_color(),ventana)
                        if not "play_turn_sound" in extra:
                            audio.play_init_turn_sounds(self.__tablero_g,self)
                    else:
                        audio.play_init_turn_sounds(self.__tablero_g,self)
                        marcador.render_all(self.__tablero,self.get_turn().get_color(),ventana)
                    if self.__con_jugadas_posibles:
                        self.__tablero_g.render_list_possible_moves(ventana)
                    pygame.display.update()
                else:
                    self.__lista_jugadas_posibles = []
                    if extra == "":
                        self.__termino_juego = True
                        marcador.render_all(self.__tablero,self.get_turn().get_color(),ventana)
                        pygame.display.update()
                        audio.play_end_game_sounds(self.__tablero_g,self)
        else:
            audio.play_end_game_sounds(self.__tablero_g,self)
            self.__termino_juego = True

        return pudo_jugar

    def game_ended(self):
        return self.__termino_juego

    def play_pc(self):
        return self.__make_a_move()

    def __make_a_move(self):
        if self.__pc.play(self.__tablero,self.__jugadores[self.__turno].get_color()):
            self.__ultima_jugada_pc = self.__pc.get_last_move()
            return True
        else:
            return False

    def get_player_by_color(self, color=board.BLANCO):
        for jugador in self.__jugadores:
            if jugador.get_color() == color:
                return jugador

    def get_player_by_name(self, nombre=PC):
        for jugador in self.__jugadores:
            if jugador.get_name() == nombre:
                return jugador

    def get_final_result(self):
        if self.__tablero.get_can_fichas_blancas() > self.__tablero.get_can_fichas_negras():
            return self.get_player_by_color(board.BLANCO)
        elif self.__tablero.get_can_fichas_blancas() < self.__tablero.get_can_fichas_negras():
            return self.get_player_by_color(board.NEGRO)
        else:
            return ''

    def get_last_pc_move(self):
        return self.__ultima_jugada_pc

    def get_last_human_move(self):
        return self.__ultima_jugada_humano

    def get_players(self):
        """ Retorna un vector con los datos de los jugadores."""

        jugador1 = self.__jugadores[0]
        jugador2 = self.__jugadores[1]
        return [{'nombre':jugador1.get_name(),'color':jugador1.get_color()},{'nombre':jugador2.get_name(),'color':jugador2.get_color()}]

    def get_board_configuration(self):
        """ Retorna un diccionario con la configuracion actual del tablero."""

        return {'dimension':self.__tablero.get_dimension(),'configuracion':self.__tablero.get_casillas()}

    def get_board(self):
        return self.__tablero

    def shorcut_lose_game(self):
        jug_humano = self.get_player_by_name(HUMANO)
        if jug_humano.get_color() == board.BLANCO:
            self.__tablero.set_can_fichas_blancas(0)
            self.__tablero.set_can_fichas_negras(1)
        else:
            self.__tablero.set_can_fichas_blancas(1)
            self.__tablero.set_can_fichas_negras(0)

    def shorcut_win_game(self):
        jug_humano = self.get_player_by_name(HUMANO)
        if jug_humano.get_color() == board.BLANCO:
            self.__tablero.set_can_fichas_blancas(1)
            self.__tablero.set_can_fichas_negras(0)
        else:
            self.__tablero.set_can_fichas_blancas(0)
            self.__tablero.set_can_fichas_negras(1)

    def shorcut_draw_game(self):
        self.__tablero.set_can_fichas_blancas(1)
        self.__tablero.set_can_fichas_negras(1)

    def get_list_possible_moves(self):
        return self.__lista_jugadas_posibles