'''
Entry point file for game.
'''

import GameController
import GameModel
import GameView
import Material
import Rules
import Session

# FIXME Belongs in Game Rules
#GAME_MODE = 4
MAX_ATTEMPTS = 3

#book = 'John'
book = '3_John copy'
#book = 'Philemon' 

session = Session.Session(MAX_ATTEMPTS, book)
session.play_new_game()
session.handle_exit_end_screen()