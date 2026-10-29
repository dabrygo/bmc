import sys

import pygame

from bmc import GameController
from bmc import GameModel
from bmc import GameView
from bmc import Material
from bmc import Rules


class Session:
  def __init__(self, n_attempts, material, rules):
    self._n_attempts = n_attempts
    self._material = material
    self._rules = rules

  @classmethod
  def from_config(cls, config):
    n_attempts = config.max_attempts()
    book_name = config.book()
    book = Material.Book.from_name(book_name)
    rules = Rules.Rules.from_config(config)
    return cls(n_attempts, book, rules)

  def play_new_game(self):
    minigame_code = self._rules.choose_minigame()
    verses = self._material.parse()
    sequence_name = self._rules.sequence()
    model = GameModel.Playthrough(
      mode_code=minigame_code, 
      sequence=sequence_name,
      max_attempts=self._n_attempts,
    )
    view = GameView.GameScreen(model)
    start_time = model.start_time()
    sequenced = self._rules.sequenced(verses, start_time)
    controller = GameController.Game(model, view, sequenced)
    controller.play(minigame_code)

  def handle_exit_end_screen(self):
    '''Handle exiting the end screen.'''
    user_exit = False
    while not user_exit:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          sys.exit()

        if event.type == pygame.KEYDOWN:
          pressed_keys = pygame.key.get_pressed()

          if pressed_keys[pygame.K_ESCAPE]:
            user_exit = True
          else:
            self.play_new_game()


