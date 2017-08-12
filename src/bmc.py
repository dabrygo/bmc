'''
Created on Aug 12, 2017

@author: dabrygo
'''

import unittest

def blankify(text):
    blanked = ""
    for character in text:
        if character.isalnum():
            blanked += '_'
        else:
            blanked += character
    return blanked

   
class TestBlankify(unittest.TestCase):
    def test_replace_a_letter_with_a_blank(self):
        self.assertEqual("_", blankify("a"))
        
    def test_do_not_replace_punctuation(self):
        self.assertEqual(",", blankify(","))
        
    def test_replace_two_letters_with_blanks(self):
        self.assertEqual("__", blankify("ab"))
        
    def test_do_not_replace_whitespace(self):
        self.assertEqual("_ _", blankify("a b"))
        
    def test_replace_digits(self):
        self.assertEqual("__", blankify("12"))
        
    def test_replace_characters_in_simple_sentence(self):
        self.assertEqual("____ __ _______.", blankify("Call me Ishmael."))
        
    def test_do_not_replace_common_puncutation_marks(self):
        self.assertEqual("__,", blankify("Hi,"), 'comma failed')
        self.assertEqual("___;", blankify("man;"), 'semicolon failed')
        self.assertEqual("__?", blankify("Eh?"), 'question mark failed')
        self.assertEqual("__!", blankify("No!"), 'exclamation mark failed')
        self.assertEqual("_.", blankify("I."), 'period failed')
        
        
if __name__ == '__main__':
    unittest.main()