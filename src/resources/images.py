from main.constants import RESOLUTION1, RESOLUTION2

class Images:
    #Variables de clase
    __file_names_r1= {}
    __file_names_r2 = {}

    #Nombre de los archivos de imagenes para la resolucion de 800x600
    __file_names_r1['medallas'] = {'oro':{'archivo' : 'resources/images/medals/800x600/medal_gold_00.png', 'pos_xy' : (210,66)},
                                   'plata': {'archivo' : 'resources/images/medals/800x600/medal_silver_00.png', 'pos_xy' : (210,66)},
                                   'bronze': {'archivo' : 'resources/images/medals/800x600/medal_bronze_00.png', 'pos_xy' : (210,66)}}
    __file_names_r1['trofeos'] = {'oro':{'archivo' : 'resources/images/trophies/800x600/trophy_gold_00.png', 'pos_xy' : (210,40)},
                                   'marfil': {'archivo' : 'resources/images/trophies/800x600/trophy_ivory_00.png', 'pos_xy' : (210,40)},
                                   'madera': {'archivo' : 'resources/images/trophies/800x600/trophy_wood_00.png', 'pos_xy' : (210,40)}}
    __file_names_r1['tablero'] = {'celda_vacia' : 'resources/images/board/800x600/cell_inside_00.png',
                                         'borde_horizontal' : 'resources/images/board/800x600/board_hframe_00.png',
                                         'borde_vertical' : 'resources/images/board/800x600/board_vframe_00.png',
                                         'marca' : 'resources/images/board/800x600/mark_00.png'}
    __file_names_r1['animacion_celda'] = {'chica' : 'resources/images/board/800x600/cell_inside_01.png',
                                                 'mediana' : 'resources/images/board/800x600/cell_inside_02.png',
                                                 'grande' : 'resources/images/board/800x600/cell_inside_03.png'}
    __file_names_r1['piezas'] = {'negra' : 'resources/images/pieces/800x600/token_black_00.png',
                                        'blanca' : 'resources/images/pieces/800x600/token_white_00.png'}
    __file_names_r1['etc'] = {'caja_texto' : 'resources/images/etc/800x600/textbox_00.png',
                              'asc_botones' : {'archivo' : 'resources/images/etc/800x600/elevbutton_00.png', 'pos_xy' : (213,166)},
                              'asc_botones_sel' : {'archivo' : 'resources/images/etc/800x600/elevbutton_01.png' , 'pos_xy' : (213,166)},
                              'logo' : {'archivo' : 'resources/images/etc/800x600/logo.png' , 'pos_xy' : (213,166)}}
    __file_names_r1['marcador'] = {'barra_negra' : 'resources/images/etc/800x600/player_bar_01.png',
                                          'barra_amarilla' : 'resources/images/etc/800x600/player_bar_00.png',
                                          'bandera_negra' : 'resources/images/etc/800x600/flag_black_00.png',
                                          'bandera_blanca' : 'resources/images/etc/800x600/flag_white_00.png'}
    __file_names_r1['habitaciones'] = {'entrada' : 'resources/images/backgrounds/800x600/room_outdoors_00.png',
                                       'primer piso' : 'resources/images/backgrounds/800x600/room_floor0_00.png',
                                       'salon de clases' : 'resources/images/backgrounds/800x600/room_class_00.png',
                                       'secretaria' : 'resources/images/backgrounds/800x600/room_office_00.png',
                                       'segundo piso' : 'resources/images/backgrounds/800x600/room_floor1_00.png',
                                       'salon de desafios' : 'resources/images/backgrounds/800x600/room_challenge_00.png',
                                       'salon de encuentros' : 'resources/images/backgrounds/800x600/room_versus_00.png',
                                       'tercer piso' : 'resources/images/backgrounds/800x600/room_floor2_00.png',
                                       'habitacion pedro madera' : 'resources/images/backgrounds/800x600/room_pm_00.png',
                                       'habitacion sofia dulce' : 'resources/images/backgrounds/800x600/room_sd_00.png',
                                       'cuarto piso' : 'resources/images/backgrounds/800x600/room_floor3_00.png',
                                       'habitacion presidente' : 'resources/images/backgrounds/800x600/room_pt_00.png'}
    __file_names_r1['puertas'] = {'ascensor' : {'archivo' : 'resources/images/etc/800x600/elevator_00.png', 'pos_xy' : (298,60)},
                                  'asc_subida' : {'archivo' : 'resources/images/etc/800x600/elevator_01.png', 'pos_xy' : (298,60)},
                                  'asc_bajada' : {'archivo' : 'resources/images/etc/800x600/elevator_02.png', 'pos_xy' : (298,60)},
                                  'salon de clases' : {'archivo' : 'resources/images/doors/800x600/door_class_00.png','pos_xy' : (18,26)},
                                  'salon de clases sel' : {'archivo' : 'resources/images/doors/800x600/door_class_01.png', 'pos_xy' : (18,26)},
                                  'secretaria' : {'archivo' : 'resources/images/doors/800x600/door_office_00.png', 'pos_xy' : (710,26)},
                                  'secretaria sel' : {'archivo' : 'resources/images/doors/800x600/door_office_01.png', 'pos_xy' : (710,26)},
                                  'salon de desafios' : {'archivo' : 'resources/images/doors/800x600/door_challenge_00.png', 'pos_xy' : (18,26)},
                                  'salon de desafios sel' : {'archivo' : 'resources/images/doors/800x600/door_challenge_01.png', 'pos_xy': (18,26)},
                                  'salon de encuentros' : {'archivo' : 'resources/images/doors/800x600/door_versus_00.png', 'pos_xy' : (710,26)},
                                  'salon de encuentros sel' : {'archivo' : 'resources/images/doors/800x600/door_versus_01.png', 'pos_xy' : (710,26)},
                                  'habitacion pedro madera' : {'archivo' : 'resources/images/doors/800x600/door_pm_00.png', 'pos_xy' : (18,26)},
                                  'habitacion pedro madera sel' : {'archivo' : 'resources/images/doors/800x600/door_pm_01.png', 'pos_xy' : (18,26)},
                                  'habitacion sofia dulce' : {'archivo' : 'resources/images/doors/800x600/door_sd_00.png', 'pos_xy' : (710,26)},
                                  'habitacion sofia dulce sel' : {'archivo' : 'resources/images/doors/800x600/door_sd_01.png', 'pos_xy' : (710,26)},
                                  'habitacion presidente' : {'archivo' : 'resources/images/doors/800x600/door_pt_00.png', 'pos_xy' : (710,26)},
                                  'habitacion presidente sel' : {'archivo' : 'resources/images/doors/800x600/door_pt_01.png', 'pos_xy' : (710,26)}}
    __file_names_r1['personajes'] = {'pablo gris' : {'archivo' : 'resources/images/characters/800x600/char_pg_00.png', 'pos_xy' : (79,33), 'pos_xy_f' : (453,34), 'pos_xy_end':(120,50)},
                                     'don cano' : {'archivo' : 'resources/images/characters/800x600/char_dc_00.png', 'pos_xy' : (26,36), 'pos_xy_end':(26,36)},
                                     'pedro madera' : {'archivo' : 'resources/images/characters/800x600/char_pm_00.png', 'pos_xy' : (473,110), 'pos_xy_f' : (500,96), 'pos_xy_end':(500,36)},
                                     'sofia dulce' : {'archivo' : 'resources/images/characters/800x600/char_sd_00.png', 'pos_xy' : (523,56), 'pos_xy_f' : (470,70), 'pos_xy_end':(370,36)},
                                     'protasio' : {'archivo' : 'resources/images/characters/800x600/char_pt_00.png', 'pos_xy' : (546,100), 'pos_xy_end':(220,36)}}
    #Nombre de los archivos de imagenes para la resolucion de 1200x900
    __file_names_r2['medallas'] = {'oro':{'archivo' : 'resources/images/medals/1200x900/medal_gold_00.png', 'pos_xy' : (300,100)},
                                   'plata':{'archivo' : 'resources/images/medals/1200x900/medal_silver_00.png', 'pos_xy' : (300,100)},
                                   'bronze': {'archivo' : 'resources/images/medals/1200x900/medal_bronze_00.png', 'pos_xy' : (300,100)}}
    __file_names_r2['trofeos'] = {'oro':{'archivo' : 'resources/images/trophies/1200x900/trophy_gold_00.png', 'pos_xy' : (300,60)},
                                   'marfil': {'archivo' : 'resources/images/trophies/1200x900/trophy_ivory_00.png', 'pos_xy' : (300,60)},
                                   'madera': {'archivo' : 'resources/images/trophies/1200x900/trophy_wood_00.png', 'pos_xy' : (300,60)}}
    __file_names_r2['tablero'] = {'celda_vacia' : 'resources/images/board/1200x900/cell_inside_00.png',
                                         'borde_horizontal' : 'resources/images/board/1200x900/board_hframe_00.png',
                                         'borde_vertical' : 'resources/images/board/1200x900/board_vframe_00.png',
                                         'marca' : 'resources/images/board/1200x900/mark_00.png'}
    __file_names_r2['animacion_celda'] = {'chica' : 'resources/images/board/1200x900/cell_inside_01.png',
                                                 'mediana' : 'resources/images/board/1200x900/cell_inside_02.png',
                                                 'grande' : 'resources/images/board/1200x900/cell_inside_03.png'}
    __file_names_r2['piezas'] = {'negra' : 'resources/images/pieces/1200x900/token_black_00.png',
                                 'blanca' : 'resources/images/pieces/1200x900/token_white_00.png'}
    __file_names_r2['etc'] = {'caja_texto' : 'resources/images/etc/1200x900/textbox_00.png',
                              'asc_botones' : {'archivo' : 'resources/images/etc/1200x900/elevbutton_00.png', 'pos_xy' : (320,250)},
                              'asc_botones_sel' : {'archivo' : 'resources/images/etc/1200x900/elevbutton_01.png' , 'pos_xy' : (320,250)},
                              'logo' : {'archivo' : 'resources/images/etc/1200x900/logo.png' , 'pos_xy' : (320,250)}}
    __file_names_r2['marcador'] = {'barra_negra' : 'resources/images/etc/1200x900/player_bar_01.png',
                                          'barra_amarilla' : 'resources/images/etc/1200x900/player_bar_00.png',
                                          'bandera_negra' : 'resources/images/etc/1200x900/flag_black_00.png',
                                          'bandera_blanca' : 'resources/images/etc/1200x900/flag_white_00.png'}
    __file_names_r2['habitaciones'] = {'entrada' : 'resources/images/backgrounds/1200x900/room_outdoors_00.png',
                                       'primer piso' : 'resources/images/backgrounds/1200x900/room_floor0_00.png',
                                       'salon de clases' : 'resources/images/backgrounds/1200x900/room_class_00.png',
                                       'secretaria' : 'resources/images/backgrounds/1200x900/room_office_00.png',
                                       'segundo piso' : 'resources/images/backgrounds/1200x900/room_floor1_00.png',
                                       'salon de desafios' : 'resources/images/backgrounds/1200x900/room_challenge_00.png',
                                       'salon de encuentros' : 'resources/images/backgrounds/1200x900/room_versus_00.png',
                                       'tercer piso' : 'resources/images/backgrounds/1200x900/room_floor2_00.png',
                                       'habitacion pedro madera' : 'resources/images/backgrounds/1200x900/room_pm_00.png',
                                       'habitacion sofia dulce' : 'resources/images/backgrounds/1200x900/room_sd_00.png',
                                       'cuarto piso' : 'resources/images/backgrounds/1200x900/room_floor3_00.png',
                                       'habitacion presidente' : 'resources/images/backgrounds/1200x900/room_pt_00.png'}
    __file_names_r2['puertas'] = {'ascensor' : {'archivo' : 'resources/images/etc/1200x900/elevator_00.png', 'pos_xy' : (447,90)},
                                  'asc_subida' : {'archivo' : 'resources/images/etc/1200x900/elevator_01.png', 'pos_xy' : (447,90)},
                                  'asc_bajada' : {'archivo' : 'resources/images/etc/1200x900/elevator_02.png', 'pos_xy' : (447,90)},
                                  'salon de clases' : {'archivo' : 'resources/images/doors/1200x900/door_class_00.png','pos_xy' : (27,40)},
                                  'salon de clases sel' : {'archivo' : 'resources/images/doors/1200x900/door_class_01.png', 'pos_xy' : (27,40)},
                                  'secretaria' : {'archivo' : 'resources/images/doors/1200x900/door_office_00.png', 'pos_xy' : (1060,40)},
                                  'secretaria sel' : {'archivo' : 'resources/images/doors/1200x900/door_office_01.png', 'pos_xy' : (1060,40)},
                                  'salon de desafios' : {'archivo' : 'resources/images/doors/1200x900/door_challenge_00.png', 'pos_xy' : (27,40)},
                                  'salon de desafios sel' : {'archivo' : 'resources/images/doors/1200x900/door_challenge_01.png', 'pos_xy': (27,40)},
                                  'salon de encuentros' : {'archivo' : 'resources/images/doors/1200x900/door_versus_00.png', 'pos_xy' : (1060,40)},
                                  'salon de encuentros sel' : {'archivo' : 'resources/images/doors/1200x900/door_versus_01.png', 'pos_xy' : (1060,40)},
                                  'habitacion pedro madera' : {'archivo' : 'resources/images/doors/1200x900/door_pm_00.png', 'pos_xy' : (27,40)},
                                  'habitacion pedro madera sel' : {'archivo' : 'resources/images/doors/1200x900/door_pm_01.png', 'pos_xy' : (27,40)},
                                  'habitacion sofia dulce' : {'archivo' : 'resources/images/doors/1200x900/door_sd_00.png', 'pos_xy' : (1060,40)},
                                  'habitacion sofia dulce sel' : {'archivo' : 'resources/images/doors/1200x900/door_sd_01.png', 'pos_xy' : (1060,40)},
                                  'habitacion presidente' : {'archivo' : 'resources/images/doors/1200x900/door_pt_00.png', 'pos_xy' : (1060,40)},
                                  'habitacion presidente sel' : {'archivo' : 'resources/images/doors/1200x900/door_pt_01.png', 'pos_xy' : (1060,40)}}
    __file_names_r2['personajes'] = {'pablo gris' : {'archivo' : 'resources/images/characters/1200x900/char_pg_00.png', 'pos_xy' : (110,50), 'pos_xy_f' : (680,52), 'pos_xy_end':(180,75)},
                                     'don cano' : {'archivo' : 'resources/images/characters/1200x900/char_dc_00.png', 'pos_xy' : (40,55), 'pos_xy_end':(40,55)},
                                     'pedro madera' : {'archivo' : 'resources/images/characters/1200x900/char_pm_00.png', 'pos_xy' : (770,165), 'pos_xy_f' : (750,145), 'pos_xy_end':(750,55)},
                                     'sofia dulce' : {'archivo' : 'resources/images/characters/1200x900/char_sd_00.png', 'pos_xy' : (785,85), 'pos_xy_f' : (705,105), 'pos_xy_end':(555,55)},
                                     'protasio' : {'archivo' : 'resources/images/characters/1200x900/char_pt_00.png', 'pos_xy' : (820,150), 'pos_xy_end':(330,55)}}

    @staticmethod
    def get_images_file_names(resolucion=(800,600),tipo_imagen=""):
        try:
            if resolucion == RESOLUTION1:
                if tipo_imagen != "":
                    return Images.__file_names_r1[tipo_imagen]
                else:
                    return Images.__file_names_r1
            elif resolucion == RESOLUTION2:
                if tipo_imagen != "":
                    return Images.__file_names_r2[tipo_imagen]
                else:
                    return Images.__file_names_r2
            else:
                raise Exception("Resolucion desconocida (Images Class)")
        except:
            raise Exception("Problemas al retornar imagen (Images Class)")

