import unittest

from bmc import Minigame
from bmc import Verse


class TestMinigame(unittest.TestCase):
  def test_content(self):
    verse = Verse.Fake(
      section='Section',
      reference='Book 1:23',
      text='Verse verse verse',
    )
    minigame = Minigame.Minigame(verse=verse)
    self.assertEqual(verse.text(), minigame.content())


class TestBlankOneWord(unittest.TestCase):
  def _verse(self):
    return Verse.Fake(
      section='Section',
      reference='Book 1:23',
      text='Verse verse verse',
    )

  def _minigame(self, words_to_guess):
    verse = self._verse()
    return Minigame.BlankOneWord(
      verse=verse, n_words=words_to_guess, seed=1,
    )

  def test_word_is_blanked_on_game_start(self):
    minigame = self._minigame(words_to_guess=1)
    minigame.prepare_screen_for_play()
    self.assertEqual('_____ verse verse', minigame.content())

  def test_partial_reveal_when_hint_requested(self):
    minigame = self._minigame(words_to_guess=1)
    minigame.prepare_screen_for_play()
    minigame.on_hint()
    self.assertEqual('____e verse verse', minigame.content())

  def test_word_is_revealed_on_correct_guess(self):
    minigame = self._minigame(words_to_guess=1)
    minigame.prepare_screen_for_play()
    minigame.on_correct_guess()
    self.assertEqual('Verse verse verse', minigame.content())

  def test_new_word_is_blanked_on_correct_guess(self):
    minigame = self._minigame(words_to_guess=2)
    minigame.prepare_screen_for_play()
    start_state = minigame.content()

    minigame.on_correct_guess()
    new_state = minigame.content()

    self.assertEqual('Verse verse _____', new_state)
    self.assertNotEqual(start_state, new_state)

  def test_reveal_all_when_all_guessed_correctly(self):
    minigame = self._minigame(words_to_guess=2)
    minigame.prepare_screen_for_play()
    start_state = minigame.content()

    minigame.on_correct_guess()
    next_state = minigame.content()

    minigame.on_correct_guess()
    end_state = minigame.content()

    self.assertNotEqual(start_state, next_state)
    self.assertNotEqual(start_state, end_state)
    self.assertNotEqual(next_state, end_state)
    self.assertEqual('Verse verse verse', end_state)


class TestBlankMultipleWords(unittest.TestCase):
  def _verse(self):
    return Verse.Fake(
      section='Section',
      reference='Book 1:23',
      text='Verse verse verse',
    )

  def _minigame(self, words_to_guess):
    verse = self._verse()
    return Minigame.BlankMultipleWords(
      verse=verse, n_words=words_to_guess, seed=1,
    )

  def test_words_are_blanked_on_game_start(self):
    minigame = self._minigame(words_to_guess=2)
    minigame.prepare_screen_for_play()
    self.assertEqual('_____ verse _____', minigame.content())

  def test_partial_reveal_of_current_word_when_hint_requested(self):
    minigame = self._minigame(words_to_guess=2)
    minigame.prepare_screen_for_play()
    minigame.on_hint()
    self.assertEqual('____e verse _____', minigame.content())

  def test_first_word_is_revealed_on_correct_guess(self):
    minigame = self._minigame(words_to_guess=2)
    minigame.prepare_screen_for_play()
    minigame.on_correct_guess()
    self.assertEqual('Verse verse _____', minigame.content())

  def test_partial_reveal_of_new_word(self):
    minigame = self._minigame(words_to_guess=2)
    minigame.prepare_screen_for_play()
    minigame.on_correct_guess()
    self.assertEqual('Verse verse _____', minigame.content())

    minigame.on_hint()
    self.assertEqual('Verse verse ____e', minigame.content())

  def test_reveal_all_when_all_guessed_correctly(self):
    minigame = self._minigame(words_to_guess=2)
    minigame.prepare_screen_for_play()
    start_state = minigame.content()
    self.assertEqual('_____ verse _____', start_state)

    minigame.on_correct_guess()
    next_state = minigame.content()
    self.assertEqual('Verse verse _____', next_state)

    minigame.on_correct_guess()
    end_state = minigame.content()
    self.assertEqual('Verse verse verse', end_state)


class TestBlankPhrases(unittest.TestCase):
  def _verse(self):
    return Verse.Fake(
      section='Section',
      reference='Psalm 119:11',
      text='I have hidden your word in my heart that I might not sin against you.',
    )

  def _minigame(self, n_phrases, words_per_phrase, seed):
    verse = self._verse()
    return Minigame.BlankPhrases(
      verse=verse,
      n_phrases=n_phrases,
      words_per_phrase=words_per_phrase,
      seed=seed,
    )

  def test_2_phrases_of_3_words_are_blanked_on_game_start(self):
    minigame = self._minigame(
      n_phrases=2, words_per_phrase=3, seed=2
    )
    minigame.prepare_screen_for_play()
    expected = '_ ____ ______ your word in my heart that I might not ___ _______ ___.'
    actual = minigame.content()
    self.assertEqual(expected, actual)

  def test_3_phrases_of_2_words_are_blanked_on_game_start(self):
    minigame = self._minigame(
      n_phrases=3, words_per_phrase=2, seed=6
    )
    minigame.prepare_screen_for_play()
    expected = '_ ____ hidden your word in my heart ____ _ might not ___ _______ you.'
    actual = minigame.content()
    self.assertEqual(expected, actual)

  def test_first_word_is_revealed_on_correct_guess(self):
    minigame = self._minigame(
      n_phrases=2, words_per_phrase=3, seed=2
    )
    minigame.prepare_screen_for_play()
    expected = '_ ____ ______ your word in my heart that I might not ___ _______ ___.'
    actual = minigame.content()
    self.assertEqual(expected, actual)

    minigame.on_correct_guess()
    self.assertEqual('I ____ ______ your word in my heart that I might not ___ _______ ___.', minigame.content())

  def test_partial_reveal_of_new_word(self):
    minigame = self._minigame(
      n_phrases=2, words_per_phrase=3, seed=2
    )
    minigame.prepare_screen_for_play()
    expected = '_ ____ ______ your word in my heart that I might not ___ _______ ___.'
    actual = minigame.content()
    self.assertEqual(expected, actual)

    minigame.on_correct_guess()
    self.assertEqual('I ____ ______ your word in my heart that I might not ___ _______ ___.', minigame.content())

    minigame.on_hint()
    self.assertEqual('I ___e ______ your word in my heart that I might not ___ _______ ___.', minigame.content())

  def test_reveal_all_when_all_guessed_correctly(self):
    intermediate_states = []
    n_phrases = 2
    words_per_phrase = 3
    minigame = self._minigame(
      n_phrases=n_phrases,
      words_per_phrase=words_per_phrase,
      seed=2
    )
    minigame.prepare_screen_for_play()

    n_blanks = n_phrases * words_per_phrase
    for _ in range(n_blanks):
      state = minigame.content()
      intermediate_states.append(state)
      minigame.on_correct_guess()
    end_state = minigame.content()

    expected = 'I have hidden your word in my heart that I might not sin against you.'
    self.assertFalse(end_state in intermediate_states)
    self.assertEqual(expected, end_state) 


class TestBlankAllWords(unittest.TestCase):
  def _verse(self):
    return Verse.Fake(
      section='Section',
      reference='Book 1:23',
      text='Verse verse verse',
    )

  def _minigame(self):
    verse = self._verse()
    return Minigame.BlankAllWords(verse=verse)

  def test_all_words_are_blanked_on_game_start(self):
    minigame = self._minigame()
    minigame.prepare_screen_for_play()
    self.assertEqual('_____ _____ _____', minigame.content())

  def test_partial_reveal_when_hint_requested(self):
    minigame = self._minigame()
    minigame.prepare_screen_for_play()
    minigame.on_hint()
    self.assertEqual('____e _____ _____', minigame.content())

  def test_word_is_revealed_on_correct_guess(self):
    minigame = self._minigame()
    minigame.prepare_screen_for_play()
    minigame.on_correct_guess()
    self.assertEqual('Verse _____ _____', minigame.content())

  def test_reveal_all_when_all_guessed_correctly(self):
    intermediate_states = []
    n_words = 3
    minigame = self._minigame()
    minigame.prepare_screen_for_play()

    for _ in range(n_words):
      state = minigame.content()
      intermediate_states.append(state)
      minigame.on_correct_guess()
    end_state = minigame.content()

    expected = 'Verse verse verse'
    self.assertFalse(end_state in intermediate_states)
    self.assertEqual(expected, end_state) 
