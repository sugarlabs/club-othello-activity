#import olpcgames, pygame, logging
import os, sys
sys.path.append(os.getcwd()+'/src')
sys.path.append(os.getcwd()+'/lib')
# Algo de esto habria que agregar para que el club de othello utilice el festival que acompana el paquete
#env = dict(os.environ)
#env['LD_LIBRARY_PATH'] = tse_dir

import club_othello

def main():
    club_othello.init_game()

if __name__ == "__main__":
    main()
