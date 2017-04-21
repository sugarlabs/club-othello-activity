from olpcgames import activity
from gettext import gettext as _
import os, logging

class ClubOthelloActivity(activity.PyGameActivity):
    """Club de Othello"""

    game_title = _('Club de Othello XO')
    game_size = None
    game_name = "run"

