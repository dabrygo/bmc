'''
Entry point file for game.
'''

import GameController
import GameModel
import GameView
import Material

# FIXME Belongs in Game Rules
GAME_MODE = 4
MAX_ATTEMPTS = 3

#book = 'John'
book = '3_John copy'
#book = 'Philemon' 

model = GameModel.Playthrough(GAME_MODE, MAX_ATTEMPTS)
view = GameView.GameScreen(model)
material = Material.Book(book)
verses = material.verses()
controller = GameController.Game(model, view, verses, GAME_MODE)
controller.play()
