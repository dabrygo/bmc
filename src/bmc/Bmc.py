'''
Entry point file for game.
'''

from bmc import Configuration
from bmc import Session

config = Configuration.Configuration.from_file()
session = Session.Session.from_config(config)
session.play_new_game()
session.handle_exit_end_screen()