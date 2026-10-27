import csv
import os
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
    if sequence == 'custom':
      reordered_material = []
      sequence_file = 'rsc/sequence.csv'
      if not os.path.exists(sequence_file):
        raise FileNotFoundError(f"Custom sequence file not found: {sequence_file}")
      with open(sequence_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for i, row in enumerate(reader):
          is_header_row = i == 0
          if is_header_row:
            continue

          n_verses, type_, *verses = row

          n_verses = int(n_verses)
          if n_verses < 0:
            raise ValueError(f"Expected at least one verse but found {n_verses} in line {i}")
          if n_verses > 1:
            raise NotImplementedError(f"More than one verse ({n_verses} in line {i}) not yet supported")
 
          if type_ == 'consecutive':
            raise NotImplementedError(f"'consecutive' not yet supported (line {i})")
          elif type_ == 'reference':
            pass
          else:
            raise ValueError(f"Unknown type '{type_}' in line {i}")

          found = False
          for material_verse in material:
            verse, *_ = verses
            if material_verse.reference() == verse:
              reordered_material.append(material_verse)
              found = True
          if not found:
            raise ValueError(f"Could not find verse {verse}")
      return reordered_material
    elif sequence == 'sequential':
      return material
    elif sequence == 'reverse':
      return material[::-1]
    elif sequence == 'random':
      return random.sample(material, len(material))
    assert False, f"Unknown sequence code: {sequence}"

  def sequence(self):
    '''Choose order to present material to user'''
    supported_sequences = ['custom', 'sequential', 'reverse', 'random']
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



