import sys

import pygame

import GameController
import GameModel
import GameView
import Material
import Rules


class Session:
  def __init__(self, n_attempts, book):
    self._n_attempts = n_attempts
    self._rules = Rules.Rules()
    self._material = Material.Book(book)

  def play_new_game(self):
    minigame_code = self._rules.choose_minigame()
    model = GameModel.Playthrough(minigame_code, self._n_attempts)
    view = GameView.GameScreen(model)
    verses = self._material.verses()
    controller = GameController.Game(model, view, verses)
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


