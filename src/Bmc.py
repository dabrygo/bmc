'''
Entry point file for game.
'''

import Display
import Game
import GameData
import Material

# FIXME Belongs in Game Rules
GAME_MODE = 1
MAX_ATTEMPTS = 3

#book = 'John'
book = '3_John copy'
#book = 'Philemon' 

model = GameData.Session(GAME_MODE, MAX_ATTEMPTS)
view = Display.GameScreen(model)
material = Material.Book(book)
verses = material.verses()
controller = Game.Game(model, view, verses, GAME_MODE)
controller.play()
