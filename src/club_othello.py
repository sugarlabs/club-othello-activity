from main.engine import Engine
from main.event_manager import EventManager
from input_output.keyboard import Keyboard
from input_output.video import Video
from input_output.audio import Audio
from input_output.mesh import Mesh
import olpcgames
from sugar.activity.activity import get_bundle_path, get_activity_root
import os, logging

log = logging.getLogger( 'ClubOthello run' )
log.setLevel( logging.DEBUG )

def init_game():
    logging.basicConfig()
    main_path = os.environ["SUGAR_BUNDLE_PATH"] #get_bundle_path()
    write_path =  os.environ["SUGAR_ACTIVITY_ROOT"] #get_activity_root()
    engine = ""
    try:
        audio = Audio(main_path)
        video = Video()
        if olpcgames.ACTIVITY._shared_activity:
            actividad_compartida = True
        else:
            actividad_compartida = False
        malla = Mesh(write_path,audio,video)
        manejador_eventos = EventManager()
        engine = Engine(main_path,write_path,video,audio,malla,actividad_compartida)
        malla.set_engine(engine)
        teclado = Keyboard(engine)
        manejador_eventos.subscribe(teclado)
        manejador_eventos.subscribe(malla)
        manejador_eventos.run()
    except Exception, e:
        if engine != "":
            engine.get_navigation_manager().exit_club()
        log.debug( "ERROR!!: " + str(olpcgames.util.get_traceback(e)) )
        exit()

if __name__ == "__main__":
    init_game()
