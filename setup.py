#!/usr/bin/env python
try:
    from sugar.activity import bundlebuilder
    bundlebuilder.start()
except ImportError:
    import os
    os.system("find ./ | sed 's,^./,ClubOthello.activity/,g' > MANIFEST")
    os.chdir('..')
    os.system('zip -r ClubOthello.xo ClubOthello.activity')
    os.system('mv ClubOthello.xo ./ClubOthello.activity')
    os.chdir('ClubOthello.activity')