from main.constants import ARRIBA, ABAJO, DERECHA, IZQUIERDA, ALL_CLEAR
import os, time, olpcgames

class NavigationManager:
    def __init__(self, engine="", write_path=""):
        if engine == "":
            raise Exception("Error!, navegacion necesita engine para funcionar")
        self.__audio = engine.get_audio()
        self.__video = engine.get_video()
        self.__usuario = engine.get_user()
        self.__club = engine.get_club()
        self.__log_file = ""
        if write_path != "":
            try:
                f = open(os.path.abspath(write_path + "/data/navigation.log"),'r')
                f.close()
                self.__log_file = open(os.path.abspath(write_path + "/data/navigation.log"),'a')
                print >> self.__log_file, '\nNAVIGATION LOG: ' + time.asctime()
            except:
                self.__log_file = open(os.path.abspath(write_path + "/data/navigation.log"),'w')
                print >> self.__log_file, 'NAVIGATION LOG: ' + time.asctime()

    def __del__(self):
        if self.__log_file != "":
            self.__log_file.close()

    def __print_log(self, mensaje):
        try:
            print >> self.__log_file, mensaje
        except:
            print mensaje

    def enter_room(self, hab, pos_hab="", animacion_y_sonido=True):
        self.__usuario.set_current_room(hab)
        if animacion_y_sonido:
            self.__video.club.end_door_animation()
            self.__audio.play_fx_sound("club","puerta")
            self.__video.club.move_to_another_room(hab,pos_hab)
            self.__audio.stop_sound()
        self.__print_log("Entro a " + str(self.__usuario.get_current_room().get_name()))
        self.__audio.play_voice_sound("club",hab.get_name())
        #if not hab.is_floor():
        self.__audio.wait_sound_end(tiempo=500)

    def leave_room(self):
        nueva_hab = self.__usuario.get_current_room().get_right_room()
        if nueva_hab != "":
            self.enter_room(nueva_hab,DERECHA)
        else:
            nueva_hab = self.__usuario.get_current_room().get_left_room()
            self.enter_room(nueva_hab,IZQUIERDA)

    def go_to_floor(self):
        self.__video.club.end_door_animation()
        asc_dir = self.__club.get_elevator()["direccion"]
        if asc_dir == ARRIBA:
            hab = self.__usuario.get_current_room().get_up_room()
            name = "ascensor_arriba"
        elif asc_dir == ABAJO:
            hab = self.__usuario.get_current_room().get_down_room()
            name = "ascensor_abajo"
        else:
            raise Exception("Error!, el ascensor tiene una direccion desconocida (Class Engine)")
        if hab.is_available():
            self.__usuario.set_current_room(hab)
            self.__audio.play_fx_sound("club",name)
            self.__video.club.move_to_another_floor(hab,asc_dir)
            self.__print_log("Fue al " + str(self.__usuario.get_current_room().get_name()))
            #Si baje al ala entrada salgo del club
            if hab.equal(self.__club.get_alone_initial_room()):
                self.exit_club()
            else:
                self.__audio.play_voice_sound("club",hab.get_name())
                self.__club.unselect_elevator()
            return True
        else:
            self.__print_log("Intento acceder a un piso no disponible")
            self.__club.unselect_elevator()
            return False

    def select_room(self, hab, hab_pos):
        self.__club.unselect_elevator()
        self.__club.select_room(hab,hab_pos)
        self.__audio.play_voice_sound("club",hab.get_name()+" sel")
        if not hab.is_floor():
            obj_ani = {'tipo' : 'habitacion', 'habitacion' : hab}
            self.__video.club.select_animation(obj_ani)
        self.__print_log("Selecciono " + str(self.__club.room_selected()["habitacion"].get_name()))

    def select_elevator(self, dir):
        hab_actual = self.__usuario.get_current_room()
        if dir == ARRIBA:
            hab_nueva = self.__usuario.get_current_room().get_up_room()
        elif dir == ABAJO:
            hab_nueva = self.__usuario.get_current_room().get_down_room()
        if hab_actual.is_floor():
            if hab_nueva != "":
                self.__club.select_room("","")
                self.__club.select_elevator(dir)
                self.__audio.play_voice_sound("club",hab_nueva.get_name() + " sel")
                obj_ani = {'tipo' : 'ascensor', 'direccion' : dir}
                self.__video.club.select_animation(obj_ani)
                self.__print_log("Selecciono el ascensor")
            else:
                print "Estoy del cual ya no se puede pasar a otro"

    def more_info(self):
        self.__audio.play_voice_sound("club",self.__usuario.get_current_room().get_name() + " info")

    def selection_more_info(self):
        hab_seleccionada = self.__club.room_selected()["habitacion"]
        if hab_seleccionada != "":
            self.__audio.play_voice_sound("club",hab_seleccionada.get_name()+" sel")
            self.__audio.play_voice_sound("club",hab_seleccionada.get_name() + " sel info")
        elif self.__club.get_elevator()["seleccionado"]:
            if self.__club.get_elevator()["direccion"] == ARRIBA:
                self.__audio.play_voice_sound("club",self.__usuario.get_current_room().get_up_room().get_name() + " sel info")
            else:
                self.__audio.play_voice_sound("club",self.__usuario.get_current_room().get_down_room().get_name() + " sel info")
        else:
            self.__audio.play_voice_sound("club","no habitacion sel")

    def exit_club(self):
        self.__audio.off_channel()
        self.__video.club.end_door_animation()
        self.__usuario.save_user_data()
        olpcgames.ACTIVITY.close(skip_save=True)
        exit()

    def exit_mettings_room(self):
        hab_disponibles = self.__usuario.get_current_room().get_availables_rooms()
        for pos_hab, nueva_hab in hab_disponibles.items():
            if nueva_hab.is_floor():
                break
        self.enter_room(nueva_hab, pos_hab)