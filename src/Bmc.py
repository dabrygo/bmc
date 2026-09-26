'''
Entry point file for game.
'''

import Display
import Material


#book = 'John'
book = '3_John copy'
#book = 'Philemon' 

screen = Display.GameScreen()
material = Material.Book(book)
verses = material.verses()
screen.run(verses)
