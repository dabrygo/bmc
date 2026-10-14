'''Determines settings for a game based on a configuration file.'''

import configparser
import os


class Configuration:
  def __init__(self, settings):
   self._settings = settings

  @classmethod
  def from_file(cls, file='rsc/configs/default.config'):
    config = configparser.ConfigParser()
    if not os.path.exists(file):
      raise FileNotFoundError(f"Config file not found: {file}")
    config.read(file)
    return cls(config['DEFAULT'])

  def book(self):
    return self._settings['Book']

  def max_attempts(self):
    return int(self._settings['MaxAttempts'])
