'''
Entry point file for game.
'''

import GameController
import GameModel
import GameView
import Material
import Rules

# FIXME Belongs in Game Rules
#GAME_MODE = 4
MAX_ATTEMPTS = 3

#book = 'John'
book = '3_John copy'
#book = 'Philemon' 

rules = Rules.Rules()
code = rules.choose_minigame()
model = GameModel.Playthrough(code, MAX_ATTEMPTS)
view = GameView.GameScreen(model)
material = Material.Book(book)
verses = material.verses()
controller = GameController.Game(model, view, verses)
controller.play(code)

