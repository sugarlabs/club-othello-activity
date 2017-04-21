import pygame
from olpcgames import pausescreen

class EventManager:
    def __init__(self):
        self.__id_objeto = 0
        self.__objetos = {}
        self.__escuchar_eventos = True

    def subscribe(self, objeto):
        objeto.set_id = self.__id_objeto
        self.__objetos[self.__id_objeto] = objeto
        self.__id_objeto += 1

    def unsubscribe(self, objeto):
        for o in self.__objetos.items():
            if o[1].get_id() == objeto.get_id():
                del self.__objetos[o[0]]

    def __warn(self, event):
        for o in self.__objetos.items():
            o[1].new_event(event)

    def listen_event(self, valor):
        self.__escuchar_eventos = valor

    def run(self):
        clock = pygame.time.Clock()
        while True:
            milliseconds = clock.tick(25) # maximum number of frames per second
            # Event-management loop with support for pausing after X seconds (20 here)
            events = pausescreen.get_events(sleep_timeout=60)
		    # Now the main event-processing loop
            if events:
                for event in events:
                    self.__warn(event)
            pygame.display.update()

	#while True:
            #for event in pygame.event.get():
        #while self.__escuchar_eventos:
            #event = pygame.event.wait()
            #self.__warn(event)
            #Refresco la pantalla
            #pygame.display.update()

