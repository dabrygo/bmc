'''
Created on Aug 12, 2017

@author: dabrygo
'''

import unittest

def words_from(text):
    words = []
    word = ""
    for character in text:
        if character.isalnum():
            word += character
        elif word:
            words.append(word)
            word = ""
    if word:
        words.append(word)
    return words


class TestWordsFrom(unittest.TestCase):
    def test_words_from_single_word(self):
        self.assertEqual(['abc'], words_from('abc'))
        
    def test_words_from_multiple_singly_spaced_words(self):
        self.assertEqual(['abc', 'def'], words_from('abc def'))


def blankify(text):
    return ["_" * len(word) for word in words_from(text)]


class TestBlankify(unittest.TestCase):
    def test_replace_a_letter_with_a_blank(self):
        self.assertEqual(["_"], blankify("a"))
        
    def test_do_not_replace_punctuation(self):
        self.assertEqual([], blankify(","))
        
    def test_replace_two_letters_with_blanks(self):
        self.assertEqual(["__"], blankify("ab"))
        
    def test_do_not_replace_whitespace(self):
        self.assertEqual(["_", "_"], blankify("a b"))
        
    def test_replace_digits(self):
        self.assertEqual(["__"], blankify("12"))
        
    def test_replace_characters_in_simple_sentence(self):
        self.assertEqual(["____", "__", "_______"], blankify("Call me Ishmael."))
        
    def test_do_not_replace_common_puncutation_marks(self):
        self.assertEqual(["__"], blankify("Hi,"), 'comma failed')
        self.assertEqual(["___"], blankify("man;"), 'semicolon failed')
        self.assertEqual(["__"], blankify("Eh?"), 'question mark failed')
        self.assertEqual(["__"], blankify("No!"), 'exclamation mark failed')
        self.assertEqual(["_"], blankify("I."), 'period failed')
        

def map_character_to_word(word):
    return word[0].lower()

def map_characters_to_words(words):
    return [map_character_to_word(word) for word in words]


class TestMapCharacterToWord(unittest.TestCase):
    def test_character_of_single_letter_word_is_that_letter(self):
        self.assertEqual('a', map_character_to_word('a'))
        
    def test_case_does_not_matter(self):
        self.assertEqual('a', map_character_to_word('A'))
        
    def test_character_of_multiletter_word_is_first_letter(self):
        self.assertEqual('a', map_character_to_word('ab'))
        
    def test_first_letters_of_multiple_words(self):
        self.assertEqual(['i', 'a', 'g'], map_characters_to_words(['I', 'am', 'Groot']))
        
        
def reveal_if_correct_guess(blanked, unblanked, guessed):
    assert len(guessed) == 1 
    should_guess = map_character_to_word(unblanked)
    if guessed == should_guess:
        return unblanked
    return blanked

        
class TestReveal(unittest.TestCase):
    def test_reveal_a_word_if_guess_right_letter(self):
        self.assertEqual('hi', reveal_if_correct_guess('__', 'hi', 'h'))
        
    def test_do_not_reveal_a_word_if_guess_wrong_letter(self):
        self.assertEqual('__', reveal_if_correct_guess('__', 'hi', 'g'))
        
    @unittest.expectedFailure
    def test_do_not_guess_more_than_one_letter(self):
        reveal_if_correct_guess('__', 'hi', 'hi')
        

def game(text):
    blanked_text = blankify(text)
    words = words_from(text)
    print(blanked_text)
    print(words)
    guess = input('>>>')
    print(guess)
    reveal = reveal_if_correct_guess("_________", words[0], guess)
    print(reveal)
    
game("Fourscore and seven years ago")

if __name__ == '__main__':
    unittest.main()