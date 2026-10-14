import random
import sys

import pygame

from bmc import GameView


class Rules:
  def __init__(self, sequence, seed=None):
    self._sequence = sequence
    if seed is not None:
      random.seed(seed)

  @classmethod
  def from_config(cls, config):
    return cls(config.sequence())

  def sequenced(self, material):
    '''Choose order to present material to user'''
    sequence = self.sequence()
    if sequence == 'sequential':
      return material
    elif sequence == 'reverse':
      return material[::-1]
    elif sequence == 'random':
      return random.sample(material, len(material))
    assert False, f"Unknown sequence code: {sequence}"

  def sequence(self):
    '''Choose order to present material to user'''
    supported_sequences = ['sequential', 'reverse', 'random']
    if self._sequence in supported_sequences:
      return self._sequence
    else:
      raise ValueError(f"Unknown sequence code: {self._sequence}")

  def choose_minigame(self):
    '''Allow the user to choose a minigame.'''
    selection_view = GameView.SelectMinigame()
    while True:
      selection_view.refresh_screen()

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          sys.exit()

        if event.type == pygame.KEYDOWN:
          pressed_keys = pygame.key.get_pressed()

          if pressed_keys[pygame.K_1]:
            return 1
          elif pressed_keys[pygame.K_2]:
            return 2
          elif pressed_keys[pygame.K_3]:
            return 3
          elif pressed_keys[pygame.K_4]:
            return 4



