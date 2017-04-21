import time, pygame, logging

log = logging.getLogger( 'src.hyperhistory.events' )
log.setLevel( logging.DEBUG )

class Events:
    def __init__(self):
        self.__current_event = ""
        self.__type_current_event = ""
        self.__open_event = False

    def run_events(self, engine, eventos):
        #Iterar sobre los eventos y ejecutarlos
        for e in eventos:
            self.__run_event(engine, e)

    def run_event(self, engine, evento):
        if evento['nombre'] == "bienvenida":
            self.__current_event = evento['nombre']
            self.__type_current_event = evento["tipo"]
            self.__open_event = True
            pg = engine.get_club().get_character_by_name("pablo gris")
            pg.wellcome(engine)
            pg.set_current_event(evento)
            engine.set_action(metodo=pg.close_event,parametros=(engine))
            pygame.display.update()
            #self.__wait_event_end()
            #pg.close_action(("bienvenida",engine,evento))
        elif evento['nombre'] == "presentacion":
            self.__current_event = "presentacion"
            self.__type_current_event = evento["tipo"]
            self.__open_event = True
            sd = engine.get_club().get_character_by_name("sofia dulce")
            sd.presentation(engine)
            sd.set_current_event(evento)
            engine.set_action(metodo=sd.close_event,parametros=(engine))
            pygame.display.update()
        elif evento['nombre'] == "end_game":
            self.__current_event = "end_game"
            self.__type_current_event = evento["tipo"]
            self.__open_event = True
            pt = engine.get_club().get_character_by_name("protasio")
            pt.fin_juego(engine)
            pt.set_current_event(evento)
            engine.set_action(metodo=pt.close_event,parametros=(engine))
            pygame.display.update()
        else:
            log.debug("El evento no esta mapeado a ninguna funcion")

    def __wait_event_end(self):
        while self.__open_event:
            time.sleep(1.)

    def close_event(self):
        self.__open_event = False

    def is_an_open_event(self, tipo=""):
        if tipo == "":
            return self.__open_event
        else:
            if self.__type_current_event == tipo and self.__open_event:
                return True
            else:
                return False

