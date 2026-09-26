'''
Entry point file for game.
'''

import Display
import Game
import GameData
import Material

# FIXME Belongs in Game Rules
GAME_MODE = 4
MAX_ATTEMPTS = 3

#book = 'John'
book = '3_John copy'
#book = 'Philemon' 

material = Material.Book(book)
verses = material.verses()
model = GameData.Session(GAME_MODE, MAX_ATTEMPTS)
view = Display.GameScreen(model)
controller = Game.Game(verses, GAME_MODE, model, view)
controller.play(GAME_MODE)
