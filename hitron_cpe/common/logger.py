""" A simple log formatter. """

import datetime

class Logger:
  """ Simple logger for formatting and handling verbose/failure logging. """
  def __init__(self, verbose):
    self.verbose = verbose

  def log(self, command, message):
    """ Log a formatted message, only if in verbose-mode, otherwise skip. """
    if self.verbose:
      timestamp = datetime.datetime.now()
      timestring = timestamp.strftime('%a %d %b %r')
      print(f'{timestring}: [{command}] -- {message}')

  def log_failure(self, raw_string):
    """ Log a failure message, formatted if in verbose-mode, skinny otherwise. """
    if self.verbose:
      timestamp = datetime.datetime.now()
      timestring = timestamp.strftime('%a %d %b %r')
      print(f'{timestring}: [FAIL] -- {raw_string}')
    else:
      print(f'*** Failure: {raw_string}')
