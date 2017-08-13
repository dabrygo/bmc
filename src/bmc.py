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


def blank(words):
    return ["_" * len(word) for word in words]

def blanks_for(text):
    return blank(words_from(text))


class TestBlanksFor(unittest.TestCase):
    def test_replace_a_letter_with_a_blank(self):
        self.assertEqual(["_"], blanks_for("a"))
        
    def test_do_not_replace_punctuation(self):
        self.assertEqual([], blanks_for(","))
        
    def test_replace_two_letters_with_blanks(self):
        self.assertEqual(["__"], blanks_for("ab"))
        
    def test_do_not_replace_whitespace(self):
        self.assertEqual(["_", "_"], blanks_for("a b"))
        
    def test_replace_digits(self):
        self.assertEqual(["__"], blanks_for("12"))
        
    def test_replace_characters_in_simple_sentence(self):
        self.assertEqual(["____", "__", "_______"], blanks_for("Call me Ishmael."))
        
    def test_do_not_replace_common_puncutation_marks(self):
        self.assertEqual(["__"], blanks_for("Hi,"), 'comma failed')
        self.assertEqual(["___"], blanks_for("man;"), 'semicolon failed')
        self.assertEqual(["__"], blanks_for("Eh?"), 'question mark failed')
        self.assertEqual(["__"], blanks_for("No!"), 'exclamation mark failed')
        self.assertEqual(["_"], blanks_for("I."), 'period failed')
        

def blankify(words_to_blank, text):
    words = words_to_blank
    blanks = blank(words)
    word = words[0]
    blanked_text = ""
    end = 0
    for i, word in enumerate(words):
        start = text.find(word)
        blanked_text += text[end:start]
        blanked_text += blanks[i]
        end = start + len(word)
    blanked_text += text[end:]
    return blanked_text
     

def blank_all_words_in(text):
    return blankify(words_from(text), text)


class TestHideWordsIn(unittest.TestCase):
    def test_blankify_one_word_sentence(self):
        self.assertEqual("__!", blank_all_words_in("No!"))
    
    def test_hide_words_in_simple_sentence(self):
        self.assertEqual("____ __ _______.", blank_all_words_in("Call me Ishmael."))
        
    def test_do_not_blank_first_word_in_simple_sentence(self):
        self.assertEqual("Call __ _______.", blankify(["me", "Ishmael"], "Call me Ishmael."))
        
    def test_blank_only_last_word_in_simple_sentence(self):
        self.assertEqual("Call me _______.", blankify(["Ishmael"], "Call me Ishmael."))
        

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
 

def get_character_from_stdin():
    import msvcrt # FIXME: Only works with Windows
    while msvcrt.kbhit():
        msvcrt.getch()
    guess_byte = msvcrt.getch()
    guess = guess_byte.decode('utf-8')
    return guess.lower()       


def game(text):
    blanks = blanks_for(text)
    words = words_from(text)
    while blanks:
        displayed_text = blankify(words, text)
        print(displayed_text)
        word = words.pop(0)
        blank = blanks.pop(0)
        guess = get_character_from_stdin()
        print(guess)
        if guess == 0:
            break
        reveal = reveal_if_correct_guess(blank, word, guess)
        if reveal == word:
            if words:
                blankify(words, text)
        else:
            words.insert(0, word)
            blanks.insert(0, blank)
    print(text)
    
game("Fourscore and seven years ago")
    
    
if __name__ == '__main__':
    unittest.main()