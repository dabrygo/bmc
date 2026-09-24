'''
Entry point file for game.
'''

import os.path

import Display
import Parser
import Reader


directory = 'rsc/books'
#book = 'John'
book = '3_John copy'
#book = 'Philemon' 
filename = book + '.txt'
path = os.path.join(directory, filename)
reader = Reader.File(path)
lines = reader.lines()
parser = Parser.Simple(lines)
verses = parser.parse()

screen = Display.GameScreen()
screen.run(verses)
