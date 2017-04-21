from _xml.parser import Parser
from main.constants import DIAL, IZQUIERDA, ARRIBA, ABAJO, DERECHA, SELECCION, TUTORIAL1, CHALLENGE1, CHALLENGE2, WON3, TUTORIAL2, CONTINUAR, \
                           BRONZE, PLATA, ORO, CHALLENGE3, CHALLENGE4, NULL, CHALLENGES_COMPLETED, ORO
from othello.utils import Coordinate
from othello.referee import Referee
import thread, os, time, logging, pygame

#Dialog States
INICIO_DIALOGO = -900
ESPERANDO_ACCION = -901
ESPERANDO_CONTINUAR = -902
ESPERANDO_ACCION_ESPECIAL = -904
ACCION_DESAFIO = -905
TERMINO_DIALOGO = -903

log = logging.getLogger( 'src.hyperhistory.dialog' )
log.setLevel( logging.DEBUG )

class DialogueManager:
    def __init__(self, main_path="", write_path="", engine="", dialogue_file_name=""):
        if engine == "":
            raise Exception("Error!, dialogo necesita engine para funcionar")
        if main_path == "":
            raise Exception("Error!, dialogo necesita el path principal para funcionar")
        self.__textos = []
        #self.__main_path = main_path + "/resources/sounds/club/personajes"
        self.__hay_dialogo_abierto = False
        self.__club = engine.get_club()
        self.__audio = engine.get_audio()
        self.__video = engine.get_video()
        self.__keys = engine.get_keys()
        self.__navegacion = engine.get_navigation_manager()
        self.__usuario = engine.get_user()
        self.__engine = engine
        if dialogue_file_name == "":
            self.__nombre_archivo = os.path.abspath(main_path + "/data/scripts/es.xml")
        else:
            self.__nombre_archivo = dialogue_file_name
        self.__datos_dialogo = {}
        self.__datos_dialogo["etiqueta"] = {}
        self.__datos_dialogo["cantidad_grupos"] = 0
        self.__accion_entrada = {}
        self.__estado_dialogo = ""
        self.__textos_dialogo_error = ""
        self.__texto_a_mostrar = ""
        self.__last_sounds = []
        self.__nombre_dialogo = ""
        self.__error_desafio = False
        try:
            f = open(os.path.abspath(write_path + "/data/dialog.log"),'r')
            f.close()
            self.__log_file = open(os.path.abspath(write_path + "/data/dialog.log"),'a')
            print >> self.__log_file, '\nDIALOG LOG: ' + time.asctime()
        except:
            self.__log_file = open(os.path.abspath(write_path + "/data/dialog.log"),'w')
            print >> self.__log_file, 'DIALOG LOG: ' + time.asctime()

    def __del__(self):
        self.__log_file.close()

    def __get_label(self):
        if self.__nombre_dialogo == "pg_bienvenida":
            return self.__datos_dialogo["etiqueta"]["id"] + str(self.__datos_dialogo["etiqueta"]["grupo"])
        elif self.__nombre_dialogo == "pg_tutorial1" or \
             self.__nombre_dialogo == "pg_tutorial2":
            if self.__datos_dialogo["etiqueta"]["grupo"] < 10:
                return self.__datos_dialogo["etiqueta"]["id"] + "0" + str(self.__datos_dialogo["etiqueta"]["grupo"])
            else:
                return self.__datos_dialogo["etiqueta"]["id"] + str(self.__datos_dialogo["etiqueta"]["grupo"])
        else:
            return self.__datos_dialogo["etiqueta"]["id"][self.__datos_dialogo["etiqueta"]["grupo"]]

    def begin_dialogue(self, nombre, grupo_inicial=0):
        self.__datos_dialogo["cantidad_grupos"] = 0
        self.__datos_dialogo["etiqueta"]["grupo"] = grupo_inicial
        if nombre == "pg_bienvenida":
            self.__datos_dialogo["etiqueta"]["id"] = "INI0"
            self.__datos_dialogo["cantidad_grupos"] = 5
        elif nombre == "pg_tutorial1":
            self.__datos_dialogo["etiqueta"]["id"] = "TUT1"
            self.__datos_dialogo["cantidad_grupos"] = 26
        elif nombre == "pg_tutorial2":
            self.__datos_dialogo["etiqueta"]["id"] = "PG_TUT2_"
            self.__datos_dialogo["cantidad_grupos"] = 8
        elif nombre == "pm_bloqueo_acceso_piso2_1":
            self.__datos_dialogo["etiqueta"]["id"] = ["PM_BLOCK_VOCALS_MEET","PM_INTRO_VOCALS","PM_BLOCK_VOCALS_GO_TUT1"]
        elif nombre == "pm_bloqueo_acceso_piso2_2":
            self.__datos_dialogo["etiqueta"]["id"] = ["PM_BLOCK_VOCALS_GO_TUT1_AGAIN"]
        elif nombre == "dc_bienvenida_ir_tut":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_MEET","DC_GO_TUT1"]
        elif nombre == "dc_ir_tut":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_GO_TUT1_AGAIN"]
        elif nombre == "dc_bienvenida_comenzar_chal_1":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_MEET","DC_START_CHAL1","DC_CHAL1_EXPLAIN_GOAL","DC_A1_TIP"]
        elif nombre == "dc_saludo_comenzar_chal_1":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_HI","DC_START_CHAL1","DC_A1_TIP"]
        elif nombre == "dc_consejo_desafio_a1" or nombre == "dc_retake_chal_a1":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_A1_TIP"]
        elif nombre == "dc_ask_select_option_list":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_ASK_FOR_RETRY"]
        elif nombre == "dc_ok_challenge_check_answer":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_CHECK_ANSWER"]
        elif nombre == "dc_consejo_desafio_a2" or nombre == "dc_retake_chal_a2":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_A2_TIP"]
        elif nombre == "dc_continue_chal1":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_CONTINUE_CHAL1"]
        elif nombre == "dc_finalizar_chal1":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_FINALIZE_CHAL1","DC_BYE"]
        elif nombre == "dc_bye":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_BYE"]
        elif nombre == "dc_go_pm1":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_GO_PM1"]
        elif nombre == "dc_go_pm2":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_GO_PM2"]
        elif nombre == "dc_go_pm3":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_GO_PM3"]
        elif nombre == "dc_chal_retake":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_CHAL_RETAKE"]
        elif nombre == "dc_saludo_comenzar_chal_2":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_HI","DC_START_CHAL2","DC_A3_TIP"]
        elif nombre == "dc_consejo_desafio_a3" or nombre == "dc_retake_chal_a3":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_A3_TIP"]
        elif nombre == "dc_continue_chal2":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_CONTINUE_CHAL2"]
        elif nombre == "dc_consejo_desafio_a4" or nombre == "dc_retake_chal_a4":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_A4_TIP"]
        elif nombre == "dc_consejo_desafio_a5" or nombre == "dc_retake_chal_a5":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_A5_TIP"]
        elif nombre == "dc_finalizar_chal2":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_FINALIZE_CHAL2","DC_BYE"]
        elif nombre == "dc_saludo_comenzar_chal_3":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_HI","DC_START_CHAL3","DC_B1_TIP"]
        elif nombre == "dc_consejo_desafio_b1" or nombre == "dc_retake_chal_b1":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_B1_TIP"]
        elif nombre == "dc_retake_chal_b2":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_B2_TIP"]
        elif nombre == "dc_retake_chal_b3":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_B3_TIP"]
        elif nombre == "dc_retake_chal_b4":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_B4_TIP"]
        elif nombre == "dc_retake_chal_b5":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_B5_TIP"]
        elif nombre == "dc_go_tut2":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_GO_TUT2"]
        elif nombre == "dc_give_retro_medals":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_GIVE_RETRO_MEDALS"]
        elif nombre == "dc_explain_medals_finalizar_chal_3":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_EXPLAIN_MEDALS","DC_BYE"]
        elif nombre == "dc_go_sd1":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_GO_SD"]
        elif nombre == "dc_give_gold":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_GIVE_GOLD"]
        elif nombre == "dc_give_silver":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_GIVE_SILVER"]
        elif nombre == "dc_give_bronze":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_GIVE_BRONZE"]
        elif nombre == "dc_saludo_comenzar_chal_4":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_HI","DC_START_CHAL4","DC_C1_TIP"]
        elif nombre == "dc_finalizar_chal4":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_FINALIZE_CHAL4","DC_BYE"]
        elif nombre == "dc_retake_chal_c1":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_C1_TIP"]
        elif nombre == "dc_retake_chal_c2":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_C2_TIP"]
        elif nombre == "dc_retake_chal_c3":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_C3_TIP"]
        elif nombre == "dc_retake_chal_c4":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_C4_TIP"]
        elif nombre == "dc_retake_chal_c5":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_C5_TIP"]
        elif nombre == "dc_go_pt1":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_GO_PT"]
        elif nombre == "dc_go_pt2":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_HI","DC_GO_PT2"]
        elif nombre == "dc_get_medals":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_GET_MEDALS"]
        elif nombre == "dc_pt_defeated":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_PT_DEFEATED"]
        elif nombre == "dc_chals_clear":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_CHALS_CLEAR"]
        elif nombre ==  "dc_chals_completed":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_CHALS_COMPLETED"]
        elif nombre ==  "dc_all_clear":
            self.__datos_dialogo["etiqueta"]["id"] = ["DC_ALL_CLEAR"]
        elif nombre == "pg_go_pm1":
            self.__datos_dialogo["etiqueta"]["id"] = ["PG_GO_PM1"]
        elif nombre == "pg_go_pm2":
            self.__datos_dialogo["etiqueta"]["id"] = ["PG_GO_PM2"]
        elif nombre == "pg_go_pm3":
            self.__datos_dialogo["etiqueta"]["id"] = ["PG_GO_PM3"]
        elif nombre == "pg_go_sd":
            self.__datos_dialogo["etiqueta"]["id"] = ["PG_GO_SD"]
        elif nombre == "pg_go_pt1":
            self.__datos_dialogo["etiqueta"]["id"] = ["PG_GO_PT"]
        elif nombre == "pg_go_pt2":
            self.__datos_dialogo["etiqueta"]["id"] = ["PG_GO_PT2"]
        elif nombre == "pg_chal1":
            self.__datos_dialogo["etiqueta"]["id"] = ["PG_GO_CHAL1"]
        elif nombre == "pg_go_chal2":
            self.__datos_dialogo["etiqueta"]["id"] = ["PG_GO_CHAL2"]
        elif nombre == "pg_go_chal3":
            self.__datos_dialogo["etiqueta"]["id"] = ["PG_GO_CHAL3"]
        elif nombre == "pg_go_chal4":
            self.__datos_dialogo["etiqueta"]["id"] = ["PG_GO_CHAL4"]
        elif nombre == "pg_retake":
            self.__datos_dialogo["etiqueta"]["id"] = ["TUT_RETAKE"]
        elif nombre == "pg_intro_retake_leason":
            self.__datos_dialogo["etiqueta"]["id"] = ["TUT_RETAKE1"]
        elif nombre == "pg_get_medals":
            self.__datos_dialogo["etiqueta"]["id"] = ["PG_GET_MEDALS"]
        elif nombre == "pg_pt_defeated":
            self.__datos_dialogo["etiqueta"]["id"] = ["PG_PT_DEFEATED"]
        elif nombre == "pg_all_clear":
            self.__datos_dialogo["etiqueta"]["id"] = ["PG_ALL_CLEAR"]
        elif nombre == "pm_first_meet_go_chal1":
            self.__datos_dialogo["etiqueta"]["id"] = ["PM_MEET_SHOW_ROOM","PM_INTRO_VOCALS","PM_GO_CHAL1"]
        elif nombre == "pm_intro_room_go_chal1":
            self.__datos_dialogo["etiqueta"]["id"] = ["PM_SHOW_ROOM","PM_GO_CHAL1"]
        elif nombre == "pm_intro_room_go_chal1_again":
            self.__datos_dialogo["etiqueta"]["id"] = ["PM_GO_CHAL1_AGAIN"]
        elif nombre == "pm_first_meet_first_game":
            self.__datos_dialogo["etiqueta"]["id"] = ["PM_MEET_SHOW_ROOM","PM_INTRO_VOCALS","PM_MATCH1_NMET","PM_MATCH1","PM_PREMATCH_PHRASE"]
        elif nombre == "pm_intro_room_first_game":
            self.__datos_dialogo["etiqueta"]["id"] = ["PM_SHOW_ROOM","PM_MATCH1_MET","PM_MATCH1","PM_PREMATCH_PHRASE"]
        elif nombre == "pm_init_first_game":
            self.__datos_dialogo["etiqueta"]["id"] = ["PM_HI","PM_MATCH1_MET","PM_MATCH1","PM_PREMATCH_PHRASE"]
        elif nombre == "pm_prematch_phrase":
            self.__datos_dialogo["etiqueta"]["id"] = ["PM_PREMATCH_PHRASE"]
        elif nombre == "pm_hi_go_chal2":
            self.__datos_dialogo["etiqueta"]["id"] = ["PM_HI","PM_GO_CHAL2"]
        elif nombre == "pm_init_second_game":
            self.__datos_dialogo["etiqueta"]["id"] = ["PM_MATCH2","PM_PREMATCH_PHRASE"]
        elif nombre == "pm_init_third_game":
            self.__datos_dialogo["etiqueta"]["id"] = ["PM_MATCH3","PM_PREMATCH_PHRASE"]
        elif nombre == "pm_gano_juego":
            self.__datos_dialogo["etiqueta"]["id"] = ["PM_MATCH_WIN"]
        elif nombre == "pm_perdio_juego1":
            self.__datos_dialogo["etiqueta"]["id"] = ["PM_MATCH1_LOSE"]
        elif nombre == "pm_perdio_juego2":
            self.__datos_dialogo["etiqueta"]["id"] = ["PM_MATCH2_LOSE"]
        elif nombre == "pm_perdio_juego3":
            self.__datos_dialogo["etiqueta"]["id"] = ["PM_MATCH3_LOSE"]
        elif nombre == "pm_bye":
            self.__datos_dialogo["etiqueta"]["id"] = ["PM_MATCH3_GIVE_MEDAL"]
        elif nombre == "pm_empato_juego":
            self.__datos_dialogo["etiqueta"]["id"] = ["PM_MATCH_DRAW"]
        elif nombre == "pm_go_tut2":
            self.__datos_dialogo["etiqueta"]["id"] = ["PM_GO_TUT2","PM_PREREMATCH"]
        elif nombre == "pm_go_chal3":
            self.__datos_dialogo["etiqueta"]["id"] = ["PM_GO_CHAL3","PM_PREREMATCH"]
        elif nombre == "pm_prerematch":
            self.__datos_dialogo["etiqueta"]["id"] = ["PM_PREREMATCH"]
        elif nombre == "pm_rematch":
            self.__datos_dialogo["etiqueta"]["id"] = ["PM_REMATCH"]
        elif nombre == "pm_perdio_revancha":
            self.__datos_dialogo["etiqueta"]["id"] = ["PM_REMATCH_LOSE"]
        elif nombre == "pm_gano_revancha":
            self.__datos_dialogo["etiqueta"]["id"] = ["PM_REMATCH_WIN"]
        elif nombre == "pm_go_sd":
            self.__datos_dialogo["etiqueta"]["id"] = ["PM_GO_SD","PM_PREREMATCH"]
        elif nombre == "pm_go_pt1":
            self.__datos_dialogo["etiqueta"]["id"] = ["PM_GO_PT","PM_PREREMATCH"]
        elif nombre == "pm_go_chal4":
            self.__datos_dialogo["etiqueta"]["id"] = ["PM_GO_CHAL4","PM_PREREMATCH"]
        elif nombre == "pm_go_pt2":
            self.__datos_dialogo["etiqueta"]["id"] = ["PM_GO_PT2","PM_PREREMATCH"]
        elif nombre == "pm_get_medals":
            self.__datos_dialogo["etiqueta"]["id"] = ["PM_GET_MEDALS","PM_PREREMATCH"]
        elif nombre == "pm_pt_defeated":
            self.__datos_dialogo["etiqueta"]["id"] = ["PM_PT_DEFEATED","PM_PREREMATCH"]
        elif nombre == "pm_all_clear":
            self.__datos_dialogo["etiqueta"]["id"] = ["PM_ALL_CLEAR","PM_PREREMATCH"]
        elif nombre == "sd_presentation":
            self.__datos_dialogo["etiqueta"]["id"] = ["SD_INTRO"]
        elif nombre == "sd_go_tut2":
            self.__datos_dialogo["etiqueta"]["id"] = ["SD_GO_TUT2"]
        elif nombre == "sd_go_chal3":
            self.__datos_dialogo["etiqueta"]["id"] = ["SD_GO_CHAL3"]
        elif nombre == "sd_go_chal4":
            self.__datos_dialogo["etiqueta"]["id"] = ["SD_GO_CHAL4","SD_PREREMATCH"]
        elif nombre == "sd_go_pt2":
            self.__datos_dialogo["etiqueta"]["id"] = ["SD_GO_PT2","SD_PREREMATCH"]
        elif nombre == "sd_init_first_game":
            self.__datos_dialogo["etiqueta"]["id"] = ["SD_MATCH1","SD_PREMATCH_PHRASE"]
        elif nombre == "sd_init_second_game":
            self.__datos_dialogo["etiqueta"]["id"] = ["SD_MATCH2","SD_PREMATCH_PHRASE"]
        elif nombre == "sd_init_third_game":
            self.__datos_dialogo["etiqueta"]["id"] = ["SD_MATCH3","SD_PREMATCH_PHRASE"]
        elif nombre == "sd_prematch_phrase":
            self.__datos_dialogo["etiqueta"]["id"] = ["SD_PREMATCH_PHRASE"]
        elif nombre == "sd_rematch_game":
            self.__datos_dialogo["etiqueta"]["id"] = ["SD_REMATCH"]
        elif nombre == "sd_perdio_juego1":
            self.__datos_dialogo["etiqueta"]["id"] = ["SD_MATCH1_LOSE"]
        elif nombre == "sd_perdio_juego2":
            self.__datos_dialogo["etiqueta"]["id"] = ["SD_MATCH2_LOSE"]
        elif nombre == "sd_perdio_juego3":
            self.__datos_dialogo["etiqueta"]["id"] = ["SD_MATCH3_LOSE"]
        elif nombre == "sd_perdio_revancha":
            self.__datos_dialogo["etiqueta"]["id"] = ["SD_REMATCH_LOSE"]
        elif nombre == "sd_empato_juego":
            self.__datos_dialogo["etiqueta"]["id"] = ["SD_MATCH_DRAW"]
        elif nombre == "sd_gano_juego":
            self.__datos_dialogo["etiqueta"]["id"] = ["SD_MATCH_WIN"]
        elif nombre == "sd_give_medal1":
            self.__datos_dialogo["etiqueta"]["id"] = ["SD_MATCH1_GIVE_MEDAL"]
        elif nombre == "sd_give_medal2":
            self.__datos_dialogo["etiqueta"]["id"] = ["SD_MATCH2_GIVE_MEDAL"]
        elif nombre == "sd_give_medal3":
            self.__datos_dialogo["etiqueta"]["id"] = ["SD_MATCH3_GIVE_MEDAL"]
        elif nombre == "sd_get_medals":
            self.__datos_dialogo["etiqueta"]["id"] = ["SD_GET_MEDALS","SD_PREREMATCH"]
        elif nombre == "sd_pt_defeated":
            self.__datos_dialogo["etiqueta"]["id"] = ["SD_PT_DEFEATED","SD_PREREMATCH"]
        elif nombre == "sd_all_clear":
            self.__datos_dialogo["etiqueta"]["id"] = ["SD_ALL_CLEAR","SD_PREREMATCH"]
        elif nombre == "pt_intro_infection_go_sd":
            self.__datos_dialogo["etiqueta"]["id"] = ["PT_INTRO","PT_INFECTION","PT_INFECTION2","PT_GO_SD"]
        elif nombre == "pt_intro_go_chal4":
            self.__datos_dialogo["etiqueta"]["id"] = ["PT_INTRO","PT_INFECTION","PT_INFECTION2","PT_GO_CHAL4"]
        elif nombre == "pt_go_chal4":
            self.__datos_dialogo["etiqueta"]["id"] = ["PT_GO_CHAL4"]
        elif nombre == "pt_go_sd":
            self.__datos_dialogo["etiqueta"]["id"] = ["PT_GO_SD"]
        elif nombre == "pt_init_first_game":
            self.__datos_dialogo["etiqueta"]["id"] = ["PT_MATCH1","PT_PREMATCH_PHRASE"]
        elif nombre == "pt_init_second_game":
            self.__datos_dialogo["etiqueta"]["id"] = ["PT_MATCH2","PT_PREMATCH_PHRASE"]
        elif nombre == "pt_init_third_game":
            self.__datos_dialogo["etiqueta"]["id"] = ["PT_MATCH3","PT_PREMATCH_PHRASE"]
        elif nombre == "pt_rematch_game":
            self.__datos_dialogo["etiqueta"]["id"] = ["PT_REMATCH"]
        elif nombre == "pt_prematch_phrase":
            self.__datos_dialogo["etiqueta"]["id"] = ["PT_PREMATCH_PHRASE"]
        elif nombre == "pt_perdio_juego1":
            self.__datos_dialogo["etiqueta"]["id"] = ["PT_MATCH1_LOSE"]
        elif nombre == "pt_perdio_juego2":
            self.__datos_dialogo["etiqueta"]["id"] = ["PT_MATCH2_LOSE"]
        elif nombre == "pt_perdio_juego3":
            self.__datos_dialogo["etiqueta"]["id"] = ["PT_MATCH3_LOSE"]
        elif nombre == "pt_perdio_revancha":
            self.__datos_dialogo["etiqueta"]["id"] = ["PT_REMATCH_LOSE"]
        elif nombre == "pt_empato_juego":
            self.__datos_dialogo["etiqueta"]["id"] = ["PT_MATCH_DRAW"]
        elif nombre == "pt_gano_juego":
            self.__datos_dialogo["etiqueta"]["id"] = ["PT_MATCH_WIN"]
        elif nombre == "pt_pt_defeated":
            self.__datos_dialogo["etiqueta"]["id"] = ["PT_PT_DEFEATED","PT_PREREMATCH"]
        elif nombre == "pt_all_clear":
            self.__datos_dialogo["etiqueta"]["id"] = ["PT_ALL_CLEAR","PT_PREREMATCH"]
        elif nombre == "pt_match2_more_medals":
            self.__datos_dialogo["etiqueta"]["id"] = ["PT_MATCH2_MORE_MEDALS"]
        elif nombre == "pt_match3_more_medals":
            self.__datos_dialogo["etiqueta"]["id"] = ["PT_MATCH3_MORE_MEDALS"]
        elif nombre == "pt_go_sd2":
            self.__datos_dialogo["etiqueta"]["id"] = ["PT_MATCH3_GO_SD"]
        elif nombre == "pt_give_trophy":
            self.__datos_dialogo["etiqueta"]["id"] = ["PT_MATCH3_GIVE_TROPHY"]
        elif nombre == "pt_match3_lose_cont":
            self.__datos_dialogo["etiqueta"]["id"] = ["PT_MATCH3_LOSE_CONT"]
        elif nombre == "pt_best_player":
            self.__datos_dialogo["etiqueta"]["id"] = ["PT_MATCH3_LOSE_CONT"]
        elif nombre == "end_game":
            self.__datos_dialogo["etiqueta"]["id"] = ["PT_END1","PG_END1","DC_END1","PM_END1","SD_END1","PT_END2","PG_END2","DC_END2","PM_END2","SD_END2"]
        else:
            log.info("No existe un dialogo asociado al nombre " + nombre)
        if self.__datos_dialogo["cantidad_grupos"] == 0:
            self.__datos_dialogo["cantidad_grupos"] = len(self.__datos_dialogo["etiqueta"]["id"]) - 1
        self.__nombre_dialogo = nombre
        self.__hay_dialogo_abierto = True
        self.__error_desafio = False
        self.__get_dialogue_from_file(self.__get_label())
        self.__estado_dialogo = INICIO_DIALOGO
        self.__textos_dialogo_error = ""
        self.manage_dialogue()

    def get_dialogue_name(self):
        return self.__nombre_dialogo

    def __get_dialogue_from_file(self, etiqueta):
        f = open(self.__nombre_archivo)
        p = Parser()
        self.__textos = p.find_child_element(etiqueta,f)
        if self.__textos == "":
            raise Exception("Error!, No se encontro la etiqueta de dialogo requerida (DialogueManager Class)")
        f.close()
        p.close()

    def __are_texts_in_group(self):
        if len(self.__textos) > 0:
            return True
        else:
            return False

    def __wait_special_input(self, elemento):
        if 'input' in elemento.get_attributes():
            self.__accion_entrada["tipo"] = "simple"
            self.__accion_entrada["entrada_esperada"] = int(elemento.get_attribute('constant_key'))
            return True
        elif 'special_input' in elemento.get_attributes():
            self.__accion_entrada["tipo"] = "especial"
            self.__accion_entrada["entrada_esperada"] = int(elemento.get_attribute('constant_key'))
            self.__accion_entrada["nombre_accion_especial"] = elemento.get_attribute('id')
            self.__accion_entrada["teclas_permitidas_accion"] = [IZQUIERDA,DERECHA,ARRIBA,ABAJO,SELECCION]
            return True
        else:
            return False

    def __read_next_texts_group(self, etiqueta_extra="", etiqueta_error_desafio=""):
        if etiqueta_error_desafio == "":
            if self.__textos_dialogo_error == "":
                self.__datos_dialogo["etiqueta"]["grupo"] += 1
            self.__get_dialogue_from_file(self.__get_label()+etiqueta_extra)
        else:
            self.__get_dialogue_from_file(etiqueta_error_desafio)

    def __save_last_text(self, ultimo_texto):
        self.__last_text = ultimo_texto

    def __end_dialogue(self):
        if self.__datos_dialogo["etiqueta"]["grupo"] < self.__datos_dialogo["cantidad_grupos"]:
            return False
        if self.__datos_dialogo["etiqueta"]["grupo"] == self.__datos_dialogo["cantidad_grupos"]:
            if self.__textos_dialogo_error != "":
                #Si estaba en el dialogo de error del ultimo grupo
                return False
            else:
                if not self.__are_texts_in_group():
                    #Si ya no quedan textos en el ultimo grupo de dialogo y no estoy viniendo de dialogo de error
                    return True
                else:
                    #Si quedan todavia textos en el grupo de dialogo
                    return False
        else:
            return True

    def __advance_dialogue(self):
        if not self.__end_dialogue():
            if not self.__are_texts_in_group():
                self.__read_next_texts_group()
            self.show_dialogue()
        else:
            self.__estado_dialogo = TERMINO_DIALOGO

    def __go_to_error_dialogue(self):
        if self.__textos_dialogo_error == "":
            self.__read_next_texts_group(etiqueta_extra="_NO")
            self.__textos_dialogo_error = list(self.__textos)
        else:
            self.__textos = self.__textos_dialogo_error
        self.__show_error_dialogue()

    def challenge_error(self):
        return self.__error_desafio

    def __play_in_possible_move(self):
        coord_actual = self.__video.board.get_coord_selected_cell()
        for coord_jp in self.__jugadas_posibles_desafio:
            if coord_jp.equal(coord_actual):
                return True
        return False

    #Creo esta funcion porque la manera de manejar los errores en los desafios es totalmente distinta a los tutoriales
    def __go_to_challenge_error_dialogue(self):
        self.__error_desafio = True
        coord_actual = self.__video.board.get_coord_selected_cell()
        self.__engine.juego.play(coord_actual,self.__audio,self.__video.marcador, self.__video.ventana,{"play_turn_sound":False,"change_score_color":False})
        if self.__accion_entrada["nombre_accion_especial"] == "desafio_a1" or \
           self.__accion_entrada["nombre_accion_especial"] == "desafio_a2" or \
           self.__accion_entrada["nombre_accion_especial"] == "desafio_a3" or \
           self.__accion_entrada["nombre_accion_especial"] == "desafio_a4":
            self.__read_next_texts_group(etiqueta_error_desafio="DC_WRONG_ANSWER_MAXIMIZE")
        self.show_dialogue()
        self.__audio.play_fx_sound("otros","more_text",{'loop':True})
        self.__keys.disable_keys(self.__accion_entrada["teclas_permitidas_accion"],DIAL)
        self.__accion_entrada.clear()
        self.__video.text_box.delete_text()


    def repeat_dialogue(self):
        self.__video.text_box.show_text(self.__video.ventana,self.__last_text)
        for s in self.__last_sounds:
            self.__audio.play_character_voice(s["character"],s["sonido"])
        self.__audio.play_fx_sound("otros","more_text",{'loop':True})

    def ended_dialogue(self):
        if self.__estado_dialogo == TERMINO_DIALOGO:
            return True
        else:
            return False

    def __ok_waited_input(self, entrada):
        if self.__accion_entrada["tipo"] == "simple":
            if entrada == self.__accion_entrada["entrada_esperada"]:
                return True
            else:
                return False
        elif self.__accion_entrada["tipo"] == "especial":
            if self.__accion_entrada["nombre_accion_especial"] == "jugada_4_3":
                coord = self.__video.board.graphic_coord_to_logic_coord(Coordinate(3,4))
                if self.__video.board.get_coord_selected_cell().equal(coord):
                    self.__engine.juego.play(coord,self.__audio,self.__video.marcador, self.__video.ventana,{"play_turn_sound":False})
                    self.__video.text_box.refresh_text_box(self.__video.ventana)
                    return True
                else:
                    return False
            elif self.__accion_entrada["nombre_accion_especial"] == "jugada_2_1":
                coord = self.__video.board.graphic_coord_to_logic_coord(Coordinate(1,2))
                if self.__video.board.get_coord_selected_cell().equal(coord):
                    self.__engine.juego.play(coord,self.__audio,self.__video.marcador, self.__video.ventana, {"play_turn_sound":False})
                    self.__video.text_box.refresh_text_box(self.__video.ventana)
                    return True
                else:
                    return False
            elif self.__accion_entrada["nombre_accion_especial"] == "jugada_1_6":
                coord = self.__video.board.graphic_coord_to_logic_coord(Coordinate(6,1))
                if self.__video.board.get_coord_selected_cell().equal(coord):
                    self.__engine.juego.play(coord,self.__audio,self.__video.marcador, self.__video.ventana, {"play_turn_sound":False})
                    self.__video.text_box.refresh_text_box(self.__video.ventana)
                    return True
                else:
                    return False
            elif self.__accion_entrada["nombre_accion_especial"] == "movimiento_4_1":
                coord = self.__video.board.graphic_coord_to_logic_coord(Coordinate(1,4))
                if self.__video.board.get_coord_selected_cell().equal(coord):
                    return True
                else:
                    return False
            elif self.__accion_entrada["nombre_accion_especial"] == "desafio_a1":
                coord = self.__video.board.graphic_coord_to_logic_coord(Coordinate(4,4))
                if self.__video.board.get_coord_selected_cell().equal(coord):
                    self.__engine.juego.play(coord,self.__audio,self.__video.marcador, self.__video.ventana, {"play_turn_sound":False,"change_score_color":False})
                    #self.__video.text_box.refresh_text_box(self.__video.ventana)
                    self.__error_desafio = False
                    return True
                else:
                    return False
            elif self.__accion_entrada["nombre_accion_especial"] == "desafio_a2":
                coord = self.__video.board.graphic_coord_to_logic_coord(Coordinate(2,3))
                if self.__video.board.get_coord_selected_cell().equal(coord):
                    self.__engine.juego.play(coord,self.__audio,self.__video.marcador, self.__video.ventana, {"play_turn_sound":False,"change_score_color":False})
                    #self.__video.text_box.refresh_text_box(self.__video.ventana)
                    self.__error_desafio = False
                    return True
                else:
                    return False
            elif self.__accion_entrada["nombre_accion_especial"] == "desafio_a3":
                coord = self.__video.board.graphic_coord_to_logic_coord(Coordinate(1,6))
                if self.__video.board.get_coord_selected_cell().equal(coord):
                    self.__engine.juego.play(coord,self.__audio,self.__video.marcador, self.__video.ventana, {"play_turn_sound":False,"change_score_color":False})
                    self.__error_desafio = False
                    return True
                else:
                    return False
            elif self.__accion_entrada["nombre_accion_especial"] == "desafio_a4":
                coord = self.__video.board.graphic_coord_to_logic_coord(Coordinate(2,3))
                if self.__video.board.get_coord_selected_cell().equal(coord):
                    self.__engine.juego.play(coord,self.__audio,self.__video.marcador, self.__video.ventana, {"play_turn_sound":False,"change_score_color":False})
                    self.__error_desafio = False
                    return True
                else:
                    return False
            elif self.__accion_entrada["nombre_accion_especial"] == "desafio_a5":
                coord = self.__video.board.graphic_coord_to_logic_coord(Coordinate(3,4))
                if self.__video.board.get_coord_selected_cell().equal(coord):
                    self.__engine.juego.play(coord,self.__audio,self.__video.marcador, self.__video.ventana, {"play_turn_sound":False,"change_score_color":False})
                    self.__error_desafio = False
                    return True
                else:
                    return False
            elif self.__accion_entrada["nombre_accion_especial"] == "desafio_b1":
                coord = self.__video.board.graphic_coord_to_logic_coord(Coordinate(1,6))
                if self.__video.board.get_coord_selected_cell().equal(coord):
                    self.__engine.juego.play(coord,self.__audio,self.__video.marcador, self.__video.ventana, {"play_turn_sound":False})
                    self.__error_desafio = False
                    return True
                else:
                    return False
            elif self.__accion_entrada["nombre_accion_especial"] == "desafio_b2":
                coord = self.__video.board.graphic_coord_to_logic_coord(Coordinate(3,1))
                if self.__video.board.get_coord_selected_cell().equal(coord):
                    self.__engine.juego.play(coord,self.__audio,self.__video.marcador, self.__video.ventana, {"play_turn_sound":False})
                    self.__error_desafio = False
                    return True
                else:
                    return False
            elif self.__accion_entrada["nombre_accion_especial"] == "desafio_b3":
                coord = self.__video.board.graphic_coord_to_logic_coord(Coordinate(6,6))
                if self.__video.board.get_coord_selected_cell().equal(coord):
                    self.__engine.juego.play(coord,self.__audio,self.__video.marcador, self.__video.ventana, {"play_turn_sound":False})
                    self.__error_desafio = False
                    return True
                else:
                    return False
            elif self.__accion_entrada["nombre_accion_especial"] == "desafio_b4":
                coord = self.__video.board.graphic_coord_to_logic_coord(Coordinate(3,1))
                if self.__video.board.get_coord_selected_cell().equal(coord):
                    self.__engine.juego.play(coord,self.__audio,self.__video.marcador, self.__video.ventana, {"play_turn_sound":False})
                    self.__error_desafio = False
                    return True
                else:
                    return False
            elif self.__accion_entrada["nombre_accion_especial"] == "desafio_b5":
                coord = self.__video.board.graphic_coord_to_logic_coord(Coordinate(1,1))
                if self.__video.board.get_coord_selected_cell().equal(coord):
                    self.__engine.juego.play(coord,self.__audio,self.__video.marcador, self.__video.ventana, {"play_turn_sound":False})
                    self.__error_desafio = False
                    return True
                else:
                    return False
            elif self.__accion_entrada["nombre_accion_especial"] == "desafio_c1":
                coord = self.__video.board.graphic_coord_to_logic_coord(Coordinate(4,4))
                if self.__video.board.get_coord_selected_cell().equal(coord):
                    self.__engine.juego.play(coord,self.__audio,self.__video.marcador, self.__video.ventana, {"play_turn_sound":False})
                    self.__error_desafio = False
                    return True
                else:
                    return False
            elif self.__accion_entrada["nombre_accion_especial"] == "desafio_c2":
                coord = self.__video.board.graphic_coord_to_logic_coord(Coordinate(2,4))
                if self.__video.board.get_coord_selected_cell().equal(coord):
                    self.__engine.juego.play(coord,self.__audio,self.__video.marcador, self.__video.ventana, {"play_turn_sound":False})
                    self.__error_desafio = False
                    return True
                else:
                    return False
            elif self.__accion_entrada["nombre_accion_especial"] == "desafio_c3":
                coord = self.__video.board.graphic_coord_to_logic_coord(Coordinate(4,4))
                if self.__video.board.get_coord_selected_cell().equal(coord):
                    self.__engine.juego.play(coord,self.__audio,self.__video.marcador, self.__video.ventana, {"play_turn_sound":False})
                    self.__error_desafio = False
                    return True
                else:
                    return False
            elif self.__accion_entrada["nombre_accion_especial"] == "desafio_c4":
                coord = self.__video.board.graphic_coord_to_logic_coord(Coordinate(2,2))
                if self.__video.board.get_coord_selected_cell().equal(coord):
                    self.__engine.juego.play(coord,self.__audio,self.__video.marcador, self.__video.ventana, {"play_turn_sound":False})
                    self.__error_desafio = False
                    return True
                else:
                    return False
            elif self.__accion_entrada["nombre_accion_especial"] == "desafio_c5":
                coord = self.__video.board.graphic_coord_to_logic_coord(Coordinate(6,6))
                if self.__video.board.get_coord_selected_cell().equal(coord):
                    self.__engine.juego.play(coord,self.__audio,self.__video.marcador, self.__video.ventana, {"play_turn_sound":False})
                    self.__error_desafio = False
                    return True
                else:
                    return False
            elif self.__accion_entrada["nombre_accion_especial"] == "recorrer_tablero":
                return True


    def __print_log(self, mensaje):
        try:
            print >> self.__log_file, mensaje
        except:
            print mensaje

    def manage_dialogue(self, datos_adicionales=""):
        if self.__estado_dialogo == ESPERANDO_ACCION:
            if self.__ok_waited_input(datos_adicionales):
                self.__keys.disable_key(self.__accion_entrada["entrada_esperada"],DIAL)
                self.__accion_entrada.clear()
                self.__advance_dialogue()
                if self.__estado_dialogo == ESPERANDO_CONTINUAR:
                    self.__audio.play_fx_sound("otros","more_text",{'loop':True})
            else:
                tecla_esperada = self.__keys.get_key_by_constant(self.__accion_entrada["entrada_esperada"]).get_name()
                tecla_recibida = self.__keys.get_key_by_constant(datos_adicionales).get_name()
                self.__print_log("Error se esperaba tecla: " + tecla_esperada + " se recibio: " + tecla_recibida)
                self.__go_to_error_dialogue()
        elif self.__estado_dialogo == ESPERANDO_ACCION_ESPECIAL:
            self.__video.text_box.disappear(self.__video.ventana)
            self.__video.marcador.refresh(self.__video.ventana)
            if datos_adicionales == self.__accion_entrada["entrada_esperada"]:
                if self.__ok_waited_input(datos_adicionales):
                    #Respondio correctamente
                    if self.__accion_entrada["nombre_accion_especial"] == "desafio_b1" or \
                       self.__accion_entrada["nombre_accion_especial"] == "desafio_b2" or \
                       self.__accion_entrada["nombre_accion_especial"] == "desafio_b3" or \
                       self.__accion_entrada["nombre_accion_especial"] == "desafio_b4" or \
                       self.__accion_entrada["nombre_accion_especial"] == "desafio_b5":
                        #Si es un DESAFIO B
                        self.__audio.play_init_turn_sounds(self.__video.board,self.__engine.juego,leer_turno_nro=False)
                        self.__jugada_usuario = self.__video.board.get_coord_selected_cell()
                        self.__estado_dialogo = ACCION_DESAFIO
                    else:
                        self.__keys.disable_keys(self.__accion_entrada["teclas_permitidas_accion"],DIAL)
                        self.__accion_entrada.clear()
                        self.__advance_dialogue()
                        if self.__estado_dialogo == ESPERANDO_CONTINUAR:
                            self.__audio.play_fx_sound("otros","more_text",{'loop':True})
                else:
                    #No respondio correctamente
                    coord_sel = self.__video.board.get_coord_selected_cell()
                    self.__print_log("Se esperaba: " + self.__accion_entrada["nombre_accion_especial"] + " se recibio jugada en: " + str(coord_sel))
                    if self.__accion_entrada["nombre_accion_especial"].find("desafio") == 0:
                        #Si es un DESAFIO
                        if self.__play_in_possible_move():
                            #Si jugo en una jugada posible
                            if self.__accion_entrada["nombre_accion_especial"] == "desafio_b1" or \
                               self.__accion_entrada["nombre_accion_especial"] == "desafio_b2" or \
                               self.__accion_entrada["nombre_accion_especial"] == "desafio_b3" or \
                               self.__accion_entrada["nombre_accion_especial"] == "desafio_b4" or \
                               self.__accion_entrada["nombre_accion_especial"] == "desafio_b5":
                                self.__engine.juego.play(coord_sel,self.__audio,self.__video.marcador, self.__video.ventana,{"play_turn_sound":False})
                                self.__audio.play_init_turn_sounds(self.__video.board,self.__engine.juego,leer_turno_nro=False)
                                self.__jugada_usuario = coord_sel
                                self.__estado_dialogo = ACCION_DESAFIO
                                self.__error_desafio = True
                            else:
                                self.__go_to_challenge_error_dialogue()
                        else:
                            #Dar error DC_WRONG_ANSWER_NOT_PLAYABLE y continua intentando
                            self.__audio.play_fx_sound("board","mal_mov")
                            if self.__accion_entrada["nombre_accion_especial"].find("c") == -1:
                                self.__read_next_texts_group(etiqueta_error_desafio="DC_WRONG_ANSWER_NOT_PLAYABLE")
                            else:
                                self.__read_next_texts_group(etiqueta_error_desafio="DC_CHALLENGE_C_NOT_PLAYABLE")
                            self.__show_challenge_error_dialogue()
                    else:
                        self.__go_to_error_dialogue()
            else:
                if not datos_adicionales == SELECCION:
                    self.__video.board.do_move(datos_adicionales, self.__audio)
                else:
                    self.__do_audio_action("cell_info")
        elif self.__estado_dialogo == ESPERANDO_CONTINUAR or self.__estado_dialogo == INICIO_DIALOGO:
            self.__advance_dialogue()
            if self.__estado_dialogo == ESPERANDO_CONTINUAR:
                #Pregunto de nuevo si el estado es igual a ESPERANDO_CONTINUAR porque pudo haber cambiado despues de pasar por advance_dialog
                self.__audio.play_fx_sound("otros","more_text",{'loop':True})
        elif self.__estado_dialogo == ACCION_DESAFIO:
            self.__video.text_box.disappear(self.__video.ventana)
            if datos_adicionales == CONTINUAR:
                if not self.__jugada_usuario == "":
                    if self.__accion_entrada["nombre_accion_especial"] == "desafio_b1":
                        if self.__jugada_usuario.equal_xy(5,2) or self.__jugada_usuario.equal_xy(5,3):
                            self.__engine.juego.play(Coordinate(4,2),self.__audio,self.__video.marcador, self.__video.ventana,{"play_turn_sound":False,"update_possibles_moves":False})
                        else:
                            self.__engine.juego.play(Coordinate(2,3),self.__audio,self.__video.marcador, self.__video.ventana,{"play_turn_sound":False,"update_possibles_moves":False})
                    elif self.__accion_entrada["nombre_accion_especial"] == "desafio_b2":
                        if self.__jugada_usuario.equal_xy(1,1) or self.__jugada_usuario.equal_xy(3,0):
                            self.__engine.juego.play(Coordinate(2,0),self.__audio,self.__video.marcador, self.__video.ventana,{"play_turn_sound":False,"update_possibles_moves":False})
                        elif self.__jugada_usuario.equal_xy(5,1):
                            self.__engine.juego.play(Coordinate(5,2),self.__audio,self.__video.marcador, self.__video.ventana,{"play_turn_sound":False,"update_possibles_moves":False})
                        elif self.__jugada_usuario.equal_xy(4,1):
                            self.__engine.juego.play(Coordinate(4,0),self.__audio,self.__video.marcador, self.__video.ventana,{"play_turn_sound":False,"update_possibles_moves":False})
                        elif self.__jugada_usuario.equal_xy(4,3):
                            self.__engine.juego.play(Coordinate(5,3),self.__audio,self.__video.marcador, self.__video.ventana,{"play_turn_sound":False,"update_possibles_moves":False})
                        elif self.__jugada_usuario.equal_xy(1,3):
                            self.__engine.juego.play(Coordinate(2,4),self.__audio,self.__video.marcador, self.__video.ventana,{"play_turn_sound":False,"update_possibles_moves":False})
                        elif self.__jugada_usuario.equal_xy(2,4):
                            self.__engine.juego.play(Coordinate(1,5),self.__audio,self.__video.marcador, self.__video.ventana,{"play_turn_sound":False,"update_possibles_moves":False})
                    elif self.__accion_entrada["nombre_accion_especial"] == "desafio_b3":
                        if self.__jugada_usuario.equal_xy(0,5):
                            #Respuesta correcta
                            self.__engine.juego.play(Coordinate(3,3),self.__audio,self.__video.marcador, self.__video.ventana,{"play_turn_sound":False,"update_possibles_moves":False})
                        elif self.__jugada_usuario.equal_xy(1,5):
                            self.__engine.juego.play(Coordinate(2,2),self.__audio,self.__video.marcador, self.__video.ventana,{"play_turn_sound":False,"update_possibles_moves":False})
                        elif self.__jugada_usuario.equal_xy(0,3):
                            self.__engine.juego.play(Coordinate(3,2),self.__audio,self.__video.marcador, self.__video.ventana,{"play_turn_sound":False,"update_possibles_moves":False})
                        elif self.__jugada_usuario.equal_xy(0,1):
                            self.__engine.juego.play(Coordinate(1,0),self.__audio,self.__video.marcador, self.__video.ventana,{"play_turn_sound":False,"update_possibles_moves":False})
                    elif self.__accion_entrada["nombre_accion_especial"] == "desafio_b4":
                        if self.__jugada_usuario.equal_xy(3,0) or self.__jugada_usuario.equal_xy(4,5):
                            self.__engine.juego.play(Coordinate(4,1),self.__audio,self.__video.marcador, self.__video.ventana,{"play_turn_sound":False,"update_possibles_moves":False})
                        elif self.__jugada_usuario.equal_xy(2,0) or self.__jugada_usuario.equal_xy(1,1) or self.__jugada_usuario.equal_xy(1,2) or \
                             self.__jugada_usuario.equal_xy(1,3) or self.__jugada_usuario.equal_xy(1,4) or self.__jugada_usuario.equal_xy(1,5) or \
                             self.__jugada_usuario.equal_xy(2,0):
                            self.__engine.juego.play(Coordinate(3,0),self.__audio,self.__video.marcador, self.__video.ventana,{"play_turn_sound":False,"update_possibles_moves":False})
                    elif self.__accion_entrada["nombre_accion_especial"] == "desafio_b5":
                        if self.__jugada_usuario.equal_xy(0,1) or self.__jugada_usuario.equal_xy(0,3):
                            self.__engine.juego.play(Coordinate(0,2),self.__audio,self.__video.marcador, self.__video.ventana,{"play_turn_sound":False,"update_possibles_moves":False})
                        elif self.__jugada_usuario.equal_xy(2,5) or self.__jugada_usuario.equal_xy(4,5):
                            self.__engine.juego.play(Coordinate(3,5),self.__audio,self.__video.marcador, self.__video.ventana,{"play_turn_sound":False,"update_possibles_moves":False})
                        elif self.__jugada_usuario.equal_xy(3,0):
                            self.__engine.juego.play(Coordinate(2,0),self.__audio,self.__video.marcador, self.__video.ventana,{"play_turn_sound":False,"update_possibles_moves":False})
                        elif self.__jugada_usuario.equal_xy(2,0):
                            self.__engine.juego.play(Coordinate(1,0),self.__audio,self.__video.marcador, self.__video.ventana,{"play_turn_sound":False,"update_possibles_moves":False})
                        elif self.__jugada_usuario.equal_xy(1,0):
                            self.__engine.juego.play(Coordinate(3,0),self.__audio,self.__video.marcador, self.__video.ventana,{"play_turn_sound":False,"update_possibles_moves":False})
                        elif self.__jugada_usuario.equal_xy(0,2):
                            self.__engine.juego.play(Coordinate(0,1),self.__audio,self.__video.marcador, self.__video.ventana,{"play_turn_sound":False,"update_possibles_moves":False})
                        elif self.__jugada_usuario.equal_xy(0,5):
                            self.__engine.juego.play(Coordinate(1,5),self.__audio,self.__video.marcador, self.__video.ventana,{"play_turn_sound":False,"update_possibles_moves":False})
                        elif self.__jugada_usuario.equal_xy(3,5):
                            self.__engine.juego.play(Coordinate(4,5),self.__audio,self.__video.marcador, self.__video.ventana,{"play_turn_sound":False,"update_possibles_moves":False})
                        elif self.__jugada_usuario.equal_xy(5,2):
                            self.__engine.juego.play(Coordinate(5,3),self.__audio,self.__video.marcador, self.__video.ventana,{"play_turn_sound":False,"update_possibles_moves":False})
                        elif self.__jugada_usuario.equal_xy(5,3):
                            self.__engine.juego.play(Coordinate(5,4),self.__audio,self.__video.marcador, self.__video.ventana,{"play_turn_sound":False,"update_possibles_moves":False})
                        elif self.__jugada_usuario.equal_xy(5,4):
                            self.__engine.juego.play(Coordinate(5,2),self.__audio,self.__video.marcador, self.__video.ventana,{"play_turn_sound":False,"update_possibles_moves":False})
                        elif self.__jugada_usuario.equal_xy(5,0):
                            #Respuesta correcta
                            self.__audio.play_voice_sound("game", "pasa_el_turno")
                            self.__audio.wait_sound_end()
                            self.__engine.juego.change_turn()
                            self.__video.marcador.render_all(self.__engine.juego.get_board(),self.__engine.juego.get_turn().get_color(),self.__video.ventana)
                    self.__jugada_usuario = ""
                    self.__get_dialogue_from_file("DC_CHECK_ANSWER")
                    self.show_dialogue()
                    self.__estado_dialogo = ACCION_DESAFIO
                else:
                    self.__video.board.lista_jugadas = Referee.possibles_moves(self.__engine.juego.get_turn().get_color(),self.__engine.juego.get_board())
                    self.__video.board.render_list_possible_moves(self.__video.ventana)
                    self.__video.refresh_window()
                    self.__audio.play_init_turn_sounds(self.__video.board,self.__engine.juego,leer_turno_nro=False,leer_turno=False)
                    self.__audio.wait_sound_end(tiempo=600)
                    if self.__error_desafio:
                        self.__read_next_texts_group(etiqueta_error_desafio="DC_WRONG_ANSWER_BORDER")
                        self.show_dialogue()
                        self.__audio.play_fx_sound("otros","more_text",{'loop':True})
                        self.__keys.disable_keys(self.__accion_entrada["teclas_permitidas_accion"],DIAL)
                        self.__video.text_box.delete_text()
                    else:
                        self.__keys.disable_keys(self.__accion_entrada["teclas_permitidas_accion"],DIAL)
                        self.__accion_entrada.clear()
                        self.__advance_dialogue()
            else:
                if not datos_adicionales == SELECCION:
                    self.__video.board.do_move(datos_adicionales, self.__audio)
                else:
                    self.__do_audio_action("cell_info")

    def __show_error_dialogue(self):
        texto_final = ""
        aux_textos = list(self.__textos)
        while aux_textos != []:
            texto = aux_textos.pop(0).get_text('str')
            self.__get_dialogue_from_file(texto)
            e_texto = self.__textos.pop(0)
            texto_final += e_texto.get_text('str')
            texto_final += '\n'
            self.__audio.play_character_voice(e_texto.get_attribute('character'),e_texto.get_attribute('sound'))
        self.__video.text_box.show_text(self.__video.ventana,texto_final)
        self.__save_last_text(texto_final)
        self.__audio.play_fx_sound("otros","wait_input")

    def __show_challenge_error_dialogue(self):
        texto_final = ""
        while self.__textos != []:
            e_texto = self.__textos.pop(0)
            texto_final += e_texto.get_text('str')
            texto_final += '\n'
            self.__audio.play_character_voice(e_texto.get_attribute('character'),e_texto.get_attribute('sound'))
        self.__video.text_box.show_text(self.__video.ventana,texto_final)
        self.__save_last_text(texto_final)
        self.__audio.play_fx_sound("otros","wait_input")

    def __set_state(self, elemento):
        if self.__wait_special_input(elemento):
            if 'input' in elemento.get_attributes():
                self.__keys.enable_key(self.__accion_entrada["entrada_esperada"])
                self.__estado_dialogo = ESPERANDO_ACCION
                self.__audio.play_fx_sound("otros","wait_input")
            elif 'special_input' in elemento.get_attributes():
                self.__keys.enable_move_keys()
                self.__estado_dialogo = ESPERANDO_ACCION_ESPECIAL
                self.__audio.play_fx_sound("otros","wait_input")
        else:
            self.__estado_dialogo = ESPERANDO_CONTINUAR
        self.__textos_dialogo_error = ""

    def show_dialogue(self):
        self.__texto_a_mostrar = ""
        self.__last_sounds = []
        self.__pre_show_dialogue()

    def __pre_show_dialogue(self):
        e_texto = self.__textos[0]
        self.__do_show_dialogue(e_texto)
        self.__video.text_box.show_text(self.__video.ventana,self.__texto_a_mostrar)
        if e_texto.has_attribute('after_video_action'):
            self.__do_video_action(e_texto.get_attribute('after_video_action'))
        if e_texto.has_attribute('after_audio_action'):
            self.__do_audio_action(e_texto.get_attribute('after_audio_action'))
        self.__save_last_text(self.__texto_a_mostrar)

    def __do_show_dialogue(self,e_texto):
        if e_texto.get_name() == 'text' and e_texto.has_attribute('join'):
            self.__show_join_dialogue(e_texto)
        elif e_texto.get_name() == 'exec_ref':
            self.__show_ref_dialogue(e_texto)
        elif e_texto.get_name() == 'text':
            self.__show_normal_dialogue(e_texto)
        else:
            raise Exception("Etiqueta desconocida! (Dialog Class)")

    def __do_video_action(self, accion):
        if accion == "select_class_room":
            self.__video.text_box.disappear(self.__video.ventana)
            self.__video.text_box.delete_text()
            hab_actual = self.__usuario.get_current_room().get_left_room()
            extra = [self.__video.text_box]
            #func = {'nombre':.is_up,'parametros':""}
            #extra.append(func)
            #func = {'nombre':self.__video.text_box.get_final_position,'parametros':""}
            #extra.append(func)
            self.__navegacion.select_room(hab_actual,IZQUIERDA)
            self.__audio.wait_sound_end(tiempo=600)
            self.__video.club.pause_door_animation()
            self.__video.text_box.show(self.__video.ventana)
            self.__video.club.launch_door_animation(extra)
        elif accion == "go_to_second_floor":
            #self.__video.text_box.disappear(self.__video.ventana)
            self.__video.text_box.delete_text()
            self.__video.club.end_door_animation()
            self.__navegacion.go_to_floor()
            personaje = self.__club.get_character_by_name("pablo gris")
            self.__video.club.show_character(personaje)
            self.__audio.wait_sound_end(tiempo=600)
            self.__video.text_box.show(self.__video.ventana)
        elif accion == "select_elevator_up":
            self.__video.club.end_door_animation()
            self.__video.text_box.disappear(self.__video.ventana)
            self.__video.text_box.delete_text()
            self.__navegacion.select_elevator(ARRIBA)
            self.__audio.wait_sound_end(tiempo=600)
            self.__video.club.pause_door_animation()
            self.__video.text_box.show(self.__video.ventana)
            #extra = []
            #func = {'nombre':self.__video.text_box.refresh_text_box,'parametros':(self.__video.ventana)}
            #extra.append(func)
            extra = [self.__video.text_box]
            self.__video.club.launch_door_animation(extra)
        elif accion == "class_room_more_info":
            self.__navegacion.selection_more_info()
            self.__video.club.pause_door_animation()
            self.__video.text_box.disappear(self.__video.ventana)
            self.__video.text_box.delete_text()
            #extra = []
            #func = {'nombre':self.__video.text_box.refresh_text_box,'parametros':(self.__video.ventana)}
            #extra.append(func)
            extra = [self.__video.text_box]
            self.__video.club.launch_door_animation()
            self.__audio.wait_sound_end(tiempo=600)
            self.__video.club.pause_door_animation()
            self.__video.text_box.show(self.__video.ventana)
            self.__video.club.launch_door_animation(extra)
        elif accion == "floor_more_info":
            self.__navegacion.more_info()
            self.__video.text_box.disappear(self.__video.ventana)
            self.__video.text_box.delete_text()
            self.__audio.wait_sound_end(tiempo=600)
            self.__video.text_box.show(self.__video.ventana)
        elif accion == "show_board":
            self.__video.text_box.disappear(self.__video.ventana)
            self.__video.text_box.delete_text()
            self.__engine.init_game("tutorial1")
            self.__video.show_board()
            #self.__video.show_scores()
            self.__video.board.set_coord_selected_cell(Coordinate(1,1))
            thread.start_new_thread(self.__video.board.render_animation_cell,(self.__video.ventana,))
            self.__video.text_box.show(self.__video.ventana)
        elif accion == "init_chal_a1" or accion == "init_chal_a2" or \
             accion == "init_chal_a3" or accion == "init_chal_a4" or \
             accion == "init_chal_b1" or accion == "init_chal_a5" or \
             accion == "init_chal_b2" or accion == "init_chal_b3" or \
             accion == "init_chal_b4" or accion == "init_chal_b5" or \
             accion == "init_chal_c1" or accion == "init_chal_c2" or \
             accion == "init_chal_c3" or accion == "init_chal_c4" or \
             accion == "init_chal_c5":
            self.__set_up_challenge(accion)
        elif accion == "to_left_cell":
            self.__video.board.do_move(IZQUIERDA, self.__audio)
            self.__audio.wait_sound_end(tiempo=600)
        elif accion == "to_up_cell":
            self.__video.board.do_move(ARRIBA, self.__audio)
            self.__audio.wait_sound_end(tiempo=600)
        elif accion == "show_pieces":
            self.__video.text_box.disappear(self.__video.ventana)
            self.__video.text_box.delete_text()
            #Mostrar las fichas
            self.__video.board.get_logical_board().set_up()
            self.__video.board.render_configuration(self.__video.ventana)
            self.__video.board.lista_jugadas = Referee.possibles_moves(self.__engine.juego.get_turn().get_color(),self.__video.board.get_logical_board())
            self.__video.board.render_list_possible_moves(self.__video.ventana)
            self.__engine.juego.update_possible_moves()
            self.__video.show_scores()
            self.__audio.play_voice_sound("game", "inicio")
            self.__audio.play_voice_sound("board", "tablero4x4")
            self.__audio.wait_sound_end(tiempo=600)
            self.__video.text_box.show(self.__video.ventana)
        elif accion == "play_4_2":
            self.__make_a_play((Coordinate(2,4)))
        elif accion == "pg_show_selection_list":
            self.__video.create_selection_list()
            relacion_pg = self.__usuario.get_character_relation("pablo gris")
            if relacion_pg == TUTORIAL1:
                self.__video.selection_list.add_options([{"descripcion":"Salir","id":"salir","visible":True},{"descripcion":"1a Clase", "id":"tutorial1","visible":True}])
            if relacion_pg == TUTORIAL2:
                self.__video.selection_list.add_options([{"descripcion":"Salir","id":"salir","visible":True},{"descripcion":"1a Clase", "id":"tutorial1","visible":True},{"descripcion":"2a Clase", "id":"tutorial2","visible":True}])
            else:
                log.debug("Faltan agregar opciones para otros tipos de relacion, lista Pablo Gris")
            self.__video.show_selection_list()
        elif accion == "pm_show_selection_list":
            relacion_dc = self.__usuario.get_character_relation("don cano")
            if relacion_dc == CHALLENGE4 or relacion_dc == CHALLENGES_COMPLETED:
                self.__video.create_selection_list(tipo="sin_jugadas_posibles")
                self.__video.selection_list.add_options([{"descripcion":"Jugar sin marcar jugadas posibles","id":"jugar_sin_jugadas_posibles","visible":True},{"descripcion":"Salir","id":"salir","visible":True},{"descripcion":"Jugar", "id":"jugar","visible":True}])
            else:
                self.__video.create_selection_list()
                self.__video.selection_list.add_options([{"descripcion":"Salir","id":"salir","visible":True},{"descripcion":"Jugar", "id":"jugar","visible":True}])
            self.__video.show_selection_list()
        elif accion == "pt_show_selection_list":
            self.__video.create_selection_list()
            relacion_pt = self.__usuario.get_character_relation("protasio")
            if relacion_pt == WON3:
                self.__video.selection_list.add_options([{"descripcion":"Salir","id":"salir","visible":True},{"descripcion":"Jugar", "id":"jugar","visible":True}])
            else:
                log.debug("Faltan agregar opciones para otros tipos de relacion, lista Protasio")
            self.__video.show_selection_list()
        elif accion == "sd_show_selection_list":
            relacion_sd = self.__usuario.get_character_relation("sofia dulce")
            relacion_dc = self.__usuario.get_character_relation("don cano")
            if relacion_sd == WON3:
                if relacion_dc == CHALLENGE4 or relacion_dc == CHALLENGES_COMPLETED:
                    self.__video.create_selection_list(tipo="sin_jugadas_posibles")
                    self.__video.selection_list.add_options([{"descripcion":"Jugar sin marcar jugadas posibles","id":"jugar_sin_jugadas_posibles","visible":True},{"descripcion":"Salir","id":"salir","visible":True},{"descripcion":"Jugar", "id":"jugar","visible":True}])
                else:
                    self.__video.create_selection_list()
                    self.__video.selection_list.add_options([{"descripcion":"Salir","id":"salir","visible":True},{"descripcion":"Jugar", "id":"jugar_con_jp","visible":True}])
            else:
                log.debug("Faltan agregar opciones para otros tipos de relacion, lista Sofia Dulce")
            self.__video.show_selection_list()
        #Lista de seleccion que aparece si es que se responde mal a los desafios, las opciones no llevan id para diferenciar del resto
        elif accion == "dc_show_selection_list":
            self.__video.create_selection_list()
            self.__video.selection_list.add_options([{"descripcion":"Reintentar","id":"reintentar","visible":True},{"descripcion":"Salir al pasillo","id":"salir_pasillo","visible":True}])
            self.__video.show_selection_list()
        elif accion == "dc_show_retake_list":
            self.__video.create_selection_list()
            relacion_dc = self.__usuario.get_character_relation("don cano")
            don_cano = self.__engine.get_club().get_character_by_name("don cano")
            if relacion_dc == CHALLENGE1:
                self.__video.selection_list.add_options([{"descripcion":"Salir","id":"salir","visible":True}, \
                                                         {"descripcion":"Tomar desafio A1","id":"retake_chal_a1","visible":True,"medalla":""}, \
                                                         {"descripcion":"Tomar desafio A2","id":"retake_chal_a2","visible":True,"medalla":""}])
            elif relacion_dc == CHALLENGE2:
                self.__video.selection_list.add_options([{"descripcion":"Tomar desafio A4","id":"retake_chal_a4","visible":True,"medalla":""}, \
                                                         {"descripcion":"Salir","id":"salir","visible":True}, \
                                                         {"descripcion":"Tomar desafio A1","id":"retake_chal_a1","visible":True,"medalla":""}, \
                                                         {"descripcion":"Tomar desafio A2","id":"retake_chal_a2","visible":False,"medalla":""}, \
                                                         {"descripcion":"Tomar desafio A3","id":"retake_chal_a3","visible":False,"medalla":""}])
            elif relacion_dc == CHALLENGE3:
                self.__video.selection_list.add_options([{"descripcion":don_cano.get_challenge_title(self.__usuario,"b5"),"id":"retake_chal_b5","visible":True,"medalla":self.__usuario.get_challenge_medal("b5")}, \
                                                         {"descripcion":"Salir","id":"salir","visible":True}, \
                                                         {"descripcion":don_cano.get_challenge_title(self.__usuario,"a1"),"id":"retake_chal_a1","visible":True,"medalla":self.__usuario.get_challenge_medal("a1")}, \
                                                         {"descripcion":don_cano.get_challenge_title(self.__usuario,"a2"),"id":"retake_chal_a2","visible":False,"medalla":self.__usuario.get_challenge_medal("a2")}, \
                                                         {"descripcion":don_cano.get_challenge_title(self.__usuario,"a3"),"id":"retake_chal_a3","visible":False,"medalla":self.__usuario.get_challenge_medal("a3")}, \
                                                         {"descripcion":don_cano.get_challenge_title(self.__usuario,"a4"),"id":"retake_chal_a4","visible":False,"medalla":self.__usuario.get_challenge_medal("a4")}, \
                                                         {"descripcion":don_cano.get_challenge_title(self.__usuario,"a5"),"id":"retake_chal_a5","visible":False,"medalla":self.__usuario.get_challenge_medal("a5")}, \
                                                         {"descripcion":don_cano.get_challenge_title(self.__usuario,"b1"),"id":"retake_chal_b1","visible":False,"medalla":self.__usuario.get_challenge_medal("b1")}, \
                                                         {"descripcion":don_cano.get_challenge_title(self.__usuario,"b2"),"id":"retake_chal_b2","visible":False,"medalla":self.__usuario.get_challenge_medal("b2")}, \
                                                         {"descripcion":don_cano.get_challenge_title(self.__usuario,"b3"),"id":"retake_chal_b3","visible":False,"medalla":self.__usuario.get_challenge_medal("b3")}, \
                                                         {"descripcion":don_cano.get_challenge_title(self.__usuario,"b4"),"id":"retake_chal_b4","visible":False,"medalla":self.__usuario.get_challenge_medal("b4")}])
            elif relacion_dc == CHALLENGE4 or relacion_dc == CHALLENGES_COMPLETED:
                self.__video.selection_list.add_options([{"descripcion":don_cano.get_challenge_title(self.__usuario,"c5"),"id":"retake_chal_c5","visible":True,"medalla":self.__usuario.get_challenge_medal("c5")}, \
                                                         {"descripcion":"Salir","id":"salir","visible":True}, \
                                                         {"descripcion":don_cano.get_challenge_title(self.__usuario,"a1"),"id":"retake_chal_a1","visible":True,"medalla":self.__usuario.get_challenge_medal("a1")}, \
                                                         {"descripcion":don_cano.get_challenge_title(self.__usuario,"a2"),"id":"retake_chal_a2","visible":False,"medalla":self.__usuario.get_challenge_medal("a2")}, \
                                                         {"descripcion":don_cano.get_challenge_title(self.__usuario,"a3"),"id":"retake_chal_a3","visible":False,"medalla":self.__usuario.get_challenge_medal("a3")}, \
                                                         {"descripcion":don_cano.get_challenge_title(self.__usuario,"a4"),"id":"retake_chal_a4","visible":False,"medalla":self.__usuario.get_challenge_medal("a4")}, \
                                                         {"descripcion":don_cano.get_challenge_title(self.__usuario,"a5"),"id":"retake_chal_a5","visible":False,"medalla":self.__usuario.get_challenge_medal("a5")}, \
                                                         {"descripcion":don_cano.get_challenge_title(self.__usuario,"b1"),"id":"retake_chal_b1","visible":False,"medalla":self.__usuario.get_challenge_medal("b1")}, \
                                                         {"descripcion":don_cano.get_challenge_title(self.__usuario,"b2"),"id":"retake_chal_b2","visible":False,"medalla":self.__usuario.get_challenge_medal("b2")}, \
                                                         {"descripcion":don_cano.get_challenge_title(self.__usuario,"b3"),"id":"retake_chal_b3","visible":False,"medalla":self.__usuario.get_challenge_medal("b3")}, \
                                                         {"descripcion":don_cano.get_challenge_title(self.__usuario,"b4"),"id":"retake_chal_b4","visible":False,"medalla":self.__usuario.get_challenge_medal("b4")}, \
                                                         {"descripcion":don_cano.get_challenge_title(self.__usuario,"b5"),"id":"retake_chal_b5","visible":False,"medalla":self.__usuario.get_challenge_medal("b5")}, \
                                                         {"descripcion":don_cano.get_challenge_title(self.__usuario,"c1"),"id":"retake_chal_c1","visible":False,"medalla":self.__usuario.get_challenge_medal("c1")}, \
                                                         {"descripcion":don_cano.get_challenge_title(self.__usuario,"c2"),"id":"retake_chal_c2","visible":False,"medalla":self.__usuario.get_challenge_medal("c2")}, \
                                                         {"descripcion":don_cano.get_challenge_title(self.__usuario,"c3"),"id":"retake_chal_c3","visible":False,"medalla":self.__usuario.get_challenge_medal("c3")}, \
                                                         {"descripcion":don_cano.get_challenge_title(self.__usuario,"c4"),"id":"retake_chal_c4","visible":False,"medalla":self.__usuario.get_challenge_medal("c4")}])
            self.__video.show_selection_list()
        elif accion == "init_tut2":
            self.__video.text_box.disappear(self.__video.ventana)
            self.__video.text_box.delete_text()
            self.__engine.init_game("tutorial2")
            self.__video.init_leason_elements(self.__engine.juego, self.__engine.get_audio())
            self.__audio.wait_sound_end(tiempo=600)
            self.__video.text_box.show(self.__video.ventana)
        elif accion == "play_3_1":
            self.__make_a_play(Coordinate(1,3))
        elif accion == "play_5_4":
            self.__make_a_play(Coordinate(4,5))
        elif accion == "dissapear_game_elements":
            self.__video.text_box.disappear(self.__video.ventana)
            self.__video.dissapear_game_elements()
            self.__video.text_box.show(self.__video.ventana)
        elif accion == "show_gold_trophy":
            self.__video.text_box.disappear(self.__video.ventana)
            self.__engine.get_audio().play_fx_sound("otros","trofeo_oro")
            self.__video.show_trophy(ORO)
            pygame.time.wait(800)
            self.__video.dissapear_trophy(ORO)
            self.__video.text_box.show(self.__video.ventana)
        else:
            raise Exception("Accion desconocida (Dialog Class)")

    def __set_up_challenge(self, nombre_desafio):
        subnombres = nombre_desafio.split("_")
        self.__video.text_box.disappear(self.__video.ventana)
        self.__video.text_box.delete_text()
        if subnombres[2].find("c") == -1:
            self.__engine.init_game("desafio_" + subnombres[2])
        else:
            self.__engine.init_game("desafio_" + subnombres[2],con_jugadas_posibles=False)
        self.__video.init_challenge_elements(subnombres[1] + "_" + subnombres[2], self.__engine.juego, self.__engine.get_audio())
        self.__jugadas_posibles_desafio = Referee.possibles_moves(self.__engine.juego.get_turn().get_color(),self.__engine.juego.get_board())
        self.__audio.wait_sound_end(tiempo=600)
        self.__video.text_box.show(self.__video.ventana)

    def __make_a_play(self, coord_juego):
        coord = self.__video.board.graphic_coord_to_logic_coord(coord_juego)
        self.__video.text_box.disappear(self.__video.ventana)
        self.__video.marcador.refresh(self.__video.ventana)
        self.__engine.juego.play(coord,self.__audio,self.__video.marcador, self.__video.ventana,{"play_turn_sound":False})
        self.__video.text_box.show(self.__video.ventana)

    def __do_audio_action(self, accion):
        if accion == "cell_info":
            self.__video.board.play_box_info_sound(self.__audio)
            self.__audio.wait_sound_end(tiempo=600)
        elif accion == "read_possible_moves":
            self.__video.board.play_possible_moves_sound(self.__audio)
            self.__audio.wait_sound_end(tiempo=600)
        elif accion == "count_pieces":
            self.__video.board.play_count_pieces_sound(self.__audio,self.__engine.juego)
            self.__audio.wait_sound_end(tiempo=600)
            self.__video.dissapear_scores()
            self.__video.dissapear_board()
        elif accion == "virus":
            self.__audio.play_fx_sound("club","infeccion")
            self.__audio.wait_sound_end(tiempo=600)

    def __show_join_dialogue(self,e_texto):
        self.__show_normal_dialogue(e_texto)
        self.__pre_show_dialogue()

    def __show_normal_dialogue(self,e_texto):
        #Veo si tiene una accion que ejecutar
        if e_texto.has_attribute('video_action'):
            self.__do_video_action(e_texto.get_attribute('video_action'))
        if e_texto.has_attribute('audio_action'):
            self.__do_audio_action(e_texto.get_attribute('audio_action'))
        texto = e_texto.get_text('str')
        self.__texto_a_mostrar += texto + " "
        #SONIDO DEL DIALOGO
        last_sound = {}
        last_sound["character"] = e_texto.get_attribute('character')
        last_sound["sonido"] = e_texto.get_attribute('sound')
        self.__audio.play_character_voice(last_sound["character"],last_sound["sonido"])
        self.__last_sounds.append(last_sound)
        self.__textos.pop(0)
        self.__set_state(e_texto)

    def __show_ref_dialogue(self,e_ref):
        self.__get_dialogue_from_file(e_ref.get_text('str'))
        self.__pre_show_dialogue()