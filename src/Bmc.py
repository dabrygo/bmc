'''
Entry point file for game.
'''

import os.path

import Display
import Parser
import Reader

GAME_MODE = 4

screen = Display.GameScreen()

directory = 'rsc/books'
#book = 'John'
book = '3_John'
#book = 'Philemon' 
filename = book + '.txt'
path = os.path.join(directory, filename)
reader = Reader.File(path)
lines = reader.lines()
parser = Parser.Simple(lines)
verses = parser.parse()

screen.init_screen()
screen.run(verses, GAME_MODE)
