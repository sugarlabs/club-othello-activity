from constants import NULL, ENTR, WELCOME, TUTORIAL1, F_MEET_BLOCK_VOCALS, MEET, BRONZE
from hyperhistory.state import State
import os, logging
from _xml.parser import Parser

log = logging.getLogger( 'src.main.user' )
log.setLevel( logging.DEBUG )

class User:
    def __init__(self, main_path="", write_path="", lugar_inicial = ""):
        self.__write_path = write_path
        self.__main_path = main_path
        self.__nombre = ""
        self.__open_user_data_file()
        self.__pieza_actual = lugar_inicial
#        self.set_state()

    def __open_user_data_file(self):
        try:
            self.__user_data_file = open(os.path.abspath(self.__write_path + "/data/user_data.xml"),'r')
            self.__load_user_data()
            self.__user_data_file.close()
        except:
            self.__create_user_data()

    def __create_user_data(self):
        self.__nivel_de_habilidad = NULL
        self.__init_character_relations()
        self.__load_config_settings()
        self.__init_medals()
        self.__init_trophies()
        self.__init_challenge_medals()

    def __load_user_data(self):
        parser = Parser()
        elementos_usuario = parser.find_child_element("user_data",self.__user_data_file)
        character_relations = {}
        for e in elementos_usuario:
            if e.get_name() == "state":
                self.set_state(e.get_attribute('name'))
            elif e.get_name() == "skill_level":
                self.__nivel_de_habilidad = int(e.get_attribute('constant'))
            elif e.get_name() == "character_relation":
                character_relations[e.get_attribute('name')] = int(e.get_attribute('relation_constant'))
            elif e.get_name() == "medals":
                self.__init_medals(e.get_attributes())
            elif e.get_name() == "trophies":
                self.__init_trophies(e.get_attributes())
            elif e.get_name() == "challenges_medals":
                self.__init_challenge_medals(e.get_attributes())
        self.__init_character_relations(character_relations)
        self.__load_config_settings(nuevo_usuario=False)
        parser.close()

    def __init_trophies(self, trofeos={}):
        self.__trofeos = {}
        if trofeos != {}:
            self.__trofeos["madera"] = int(trofeos["wood"])
            self.__trofeos["marfil"] = int(trofeos["ivory"])
            self.__trofeos["oro"] = int(trofeos["gold"])
        else:
            self.__trofeos = {"madera":0, "marfil":0, "oro":0}

    def __init_medals(self, medallas={}):
        self.__medallas = {}
        if medallas != {}:
            self.__medallas["bronce"] = int(medallas["bronze"])
            self.__medallas["plata"] = int(medallas["silver"])
            self.__medallas["oro"] = int(medallas["gold"])
        else:
            self.__medallas = {"bronce":0, "plata":0, "oro":0}

    def __init_challenge_medals(self, medallas_desafios={}):
        self.__medallas_desafios = {}
        if medallas_desafios != {}:
            self.__medallas_desafios["a1"] = int(medallas_desafios["a1"]) if medallas_desafios["a1"] != "" else medallas_desafios["a1"]
            self.__medallas_desafios["a2"] = int(medallas_desafios["a2"]) if medallas_desafios["a2"] != "" else medallas_desafios["a2"]
            self.__medallas_desafios["a3"] = int(medallas_desafios["a3"]) if medallas_desafios["a3"] != "" else medallas_desafios["a3"]
            self.__medallas_desafios["a4"] = int(medallas_desafios["a4"]) if medallas_desafios["a4"] != "" else medallas_desafios["a4"]
            self.__medallas_desafios["a5"] = int(medallas_desafios["a5"]) if medallas_desafios["a5"] != "" else medallas_desafios["a5"]
            self.__medallas_desafios["b1"] = int(medallas_desafios["b1"]) if medallas_desafios["b1"] != "" else medallas_desafios["b1"]
            self.__medallas_desafios["b2"] = int(medallas_desafios["b2"]) if medallas_desafios["b2"] != "" else medallas_desafios["b2"]
            self.__medallas_desafios["b3"] = int(medallas_desafios["b3"]) if medallas_desafios["b3"] != "" else medallas_desafios["b3"]
            self.__medallas_desafios["b4"] = int(medallas_desafios["b4"]) if medallas_desafios["b4"] != "" else medallas_desafios["b4"]
            self.__medallas_desafios["b5"] = int(medallas_desafios["b5"]) if medallas_desafios["b5"] != "" else medallas_desafios["b5"]
            self.__medallas_desafios["c1"] = int(medallas_desafios["c1"]) if medallas_desafios["c1"] != "" else medallas_desafios["c1"]
            self.__medallas_desafios["c2"] = int(medallas_desafios["c2"]) if medallas_desafios["c2"] != "" else medallas_desafios["c2"]
            self.__medallas_desafios["c3"] = int(medallas_desafios["c3"]) if medallas_desafios["c3"] != "" else medallas_desafios["c3"]
            self.__medallas_desafios["c4"] = int(medallas_desafios["c4"]) if medallas_desafios["c4"] != "" else medallas_desafios["c4"]
            self.__medallas_desafios["c5"] = int(medallas_desafios["c5"]) if medallas_desafios["c5"] != "" else medallas_desafios["c5"]
        else:
            self.__medallas_desafios = {"a1":BRONZE,"a2":BRONZE,"a3":BRONZE,"a4":BRONZE,"a5":"","b1":BRONZE,"b2":"","b3":"","b4":"","b5":"","c1":"","c2":"","c3":"","c4":"","c5":""}


    def __load_config_settings(self, nuevo_usuario=True):
        settings_file = open(os.path.abspath(self.__main_path + "/data/config_settings.xml"))
        parser = Parser()
        elementos_configuracion = parser.find_child_element("configuration_settings",settings_file)
        for e in elementos_configuracion:
            if e.get_name() == "dialogues":
                if e.get_attribute('interrupt') == 'yes':
                    self.__interrumpir_dialogos = True
                else:
                    self.__interrumpir_dialogos = False
            elif e.get_name() == "sounds":
                if e.get_attribute('interrupt') == 'yes':
                    self.__interrumpir_sonidos_entre_turnos = True
                else:
                    self.__interrumpir_sonidos_entre_turnos = False
            elif e.get_name() == "initial_state" and nuevo_usuario:
                self.set_state(e.get_attribute('name'))
            elif e.get_name() == "initial_context":
                self.__contexto = e.get_attribute('constant')
            elif e.get_name() == "shorcuts":
                if e.get_attribute('games') == 'yes':
                    self.__atajos_juegos = True
                else:
                    self.__atajos_juegos = False
                if e.get_attribute('tutorials') == 'yes':
                    self.__atajos_tutoriales = True
                else:
                    self.__atajos_tutoriales = False
        settings_file.close()
        parser.close()

    def save_user_data(self):
        self.__user_data_file = open(os.path.abspath(self.__write_path + "/data/user_data.xml"),'w')
        self.__user_data_file.write('<?xml version="1.0"?>\n')
        self.__user_data_file.write('<user_data>\n')
        self.__user_data_file.write('\t<state name="'+self.__estado.get_name()+'"></state>\n')
        self.__user_data_file.write('\t<skill_level constant="'+str(self.__nivel_de_habilidad)+'"></skill_level>\n')
        self.__user_data_file.write('\t<character_relation name="pablo gris" relation_constant="'+str(self.__character_relations['pablo gris'])+'"></character_relation>\n')
        self.__user_data_file.write('\t<character_relation name="pedro madera" relation_constant="'+str(self.__character_relations['pedro madera'])+'"></character_relation>\n')
        self.__user_data_file.write('\t<character_relation name="don cano" relation_constant="'+str(self.__character_relations['don cano'])+'"></character_relation>\n')
        self.__user_data_file.write('\t<character_relation name="sofia dulce" relation_constant="'+str(self.__character_relations['sofia dulce'])+'"></character_relation>\n')
        self.__user_data_file.write('\t<character_relation name="protasio" relation_constant="'+str(self.__character_relations['protasio'])+'"></character_relation>\n')
        self.__user_data_file.write('\t<medals bronze="'+str(self.__medallas['bronce'])+'" silver="'+str(self.__medallas['plata'])+'" gold="'+str(self.__medallas['oro'])+'"></medals>\n')
        self.__user_data_file.write('\t<trophies wood="'+str(self.__trofeos['madera'])+'" ivory="'+str(self.__trofeos['marfil'])+'" gold="'+str(self.__trofeos['oro'])+'"></trophies>\n')
        self.__user_data_file.write('\t<challenges_medals a1="'+str(self.__medallas_desafios['a1'])+'" a2="'+str(self.__medallas_desafios['a2'])+'" a3="'+str(self.__medallas_desafios['a3'])+ \
                                    '" a4="'+str(self.__medallas_desafios['a4'])+'" a5="'+str(self.__medallas_desafios['a5'])+'" b1="'+str(self.__medallas_desafios['b1'])+ \
                                    '" b2="'+str(self.__medallas_desafios['b2'])+'" b3="'+str(self.__medallas_desafios['b3'])+'" b4="'+str(self.__medallas_desafios['b4'])+ \
                                    '" b5="'+str(self.__medallas_desafios['b5'])+'" c1="'+str(self.__medallas_desafios['c1'])+'" c2="'+str(self.__medallas_desafios['c2'])+ \
                                    '" c3="'+str(self.__medallas_desafios['c3'])+'" c4="'+str(self.__medallas_desafios['c4'])+'" c5="'+str(self.__medallas_desafios['c5'])+ '"></challenges_medals>\n')
        self.__user_data_file.write('</user_data>')
        self.__user_data_file.close()

    def get_name(self):
        return self.__nombre

    def get_current_room(self):
        return self.__pieza_actual

    def set_current_room(self, nueva_pieza):
        self.__pieza_actual = nueva_pieza

    def get_skill_level(self):
        return self.__nivel_de_habilidad

    def set_skill_level(self, nuevo_nivel):
        self.__nivel_de_habilidad = nuevo_nivel

    def __init_character_relations(self, relaciones={}):
        self.__character_relations = {}
        if relaciones == {}:
            self.__character_relations["pablo gris"] = NULL #TUTORIAL1
            self.__character_relations["pedro madera"] = NULL #F_MEET_BLOCK_VOCALS
            self.__character_relations["sofia dulce"] = NULL
            self.__character_relations["don cano"] = NULL
            self.__character_relations["protasio"] = NULL
        else:
            self.__character_relations["pablo gris"] = relaciones["pablo gris"]
            self.__character_relations["pedro madera"] = relaciones["pedro madera"]
            self.__character_relations["sofia dulce"] = relaciones["sofia dulce"]
            self.__character_relations["don cano"] = relaciones["don cano"]
            self.__character_relations["protasio"] = relaciones["protasio"]

    def set_character_relation(self, nombre_personaje, relacion):
        self.__character_relations[nombre_personaje] = relacion

    def get_character_relation(self, nombre_personaje):        
        return self.__character_relations[nombre_personaje]

    def get_context(self):
        return self.__contexto

    def set_context(self, valor):
        self.__contexto = valor

    def set_state(self, estado="state2"):
        self.__estado = State()
        self.__estado.save_state(estado,self.__main_path)

    def get_state(self):
        return self.__estado

    def set_player(self, jugador):
        self.__jugador = jugador

    def get_player(self):
        return self.__jugador

    def interrupt_dialogue(self):
        return self.__interrumpir_dialogos

    def interrupt_sounds(self):
        return self.__interrumpir_sonidos_entre_turnos

    def enable_games_shorcuts(self):
        return self.__atajos_juegos

    def enable_tutorials_shorcuts(self):
        return self.__atajos_tutoriales

    def get_challenge_medals(self):
        return self.__medallas_desafios

    def get_challenge_medal(self, desafio):
        return self.__medallas_desafios[desafio]

    def save_challenge_medal(self, desafio, medalla):
        self.__medallas_desafios[desafio] = medalla

    def save_medal(self, tipo):
        self.__medallas[tipo] += 1

    def delete_medal(self, tipo):
        if self.__medallas[tipo] > 0:
            self.__medallas[tipo] -= 1
        else:
            log.debug("No se puede borrar la medalla, cantidad igual a cero. (Class: User, Method: delete_medal)")

    def save_trophie(self, tipo):
        self.__trofeos[tipo] += 1

    def delete_trophie(self, tipo):
        if self.__trofeos[tipo] > 0:
            self.__trofeos[tipo] -= 1
        else:
            log.debug("No se puede borrar el trofeo, cantidad igual a cero. (Class: User, Method: delete_trophie)")

    def get_medal(self, tipo):
        return self.__medallas[tipo]

    def get_medals(self):
        return self.__medallas

    def get_game_progress(self):
        nro_estado = int(self.__estado.get_name().split("state")[1])
        progreso_real = (100*nro_estado)/self.__estado.get_max_estados()
        modulo_progreso = progreso_real % 5
        if modulo_progreso != 0:
            intervalo = self.__get_interval(progreso_real)
            nro1 = abs(intervalo[0]-progreso_real)
            nro2 = abs(intervalo[1]-progreso_real)
            progreso_multiplo_5 = 0
            if nro1 == modulo_progreso:
                progreso_multiplo_5 =  intervalo[0]
            elif nro2 == modulo_progreso:
                progreso_multiplo_5 =  intervalo[1]
            else:
                log.debug("El nro. de progreso no corresponde al intervalo. (User Class)")
            return progreso_multiplo_5
        else:
            return progreso_real

    #Retorna el intervalo multiplo de 5 en el cual se encuentra contenido el numero dado
    def __get_interval(self, numero):
        if numero > 0 and numero <= 5:
            return (1,5)
        elif numero > 5 and numero <= 10:
            return (5,10)
        elif numero > 10 and numero <= 15:
            return (10,15)
        elif numero > 15 and numero <= 20:
            return (15,20)
        elif numero > 20 and numero <= 25:
            return (20,25)
        elif numero > 25 and numero <= 30:
            return (25,30)
        elif numero > 30 and numero <= 35:
            return (30,35)
        elif numero > 35 and numero <= 40:
            return (35,40)
        elif numero > 40 and numero <= 45:
            return (40,45)
        elif numero > 45 and numero <= 50:
            return (45,50)
        elif numero > 50 and numero <= 55:
            return (50,55)
        elif numero > 55 and numero <= 60:
            return (55,60)
        elif numero > 60 and numero <= 65:
            return (60,65)
        elif numero > 65 and numero <= 70:
            return (65,70)
        elif numero > 70 and numero <= 75:
            return (70,75)
        elif numero > 75 and numero <= 80:
            return (75,80)
        elif numero > 80 and numero <= 85:
            return (80,85)
        elif numero > 85 and numero <= 90:
            return (85,90)
        elif numero > 90 and numero <= 95:
            return (90,95)
        elif numero > 95 and numero <= 100:
            return (95,100)
        else:
            log.debug("No se encuentra el intervalo del numero de estado pasado. (User Class)")