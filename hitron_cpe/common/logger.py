""" A simple log formatter. """

import datetime

class Logger:
  def __init__(self, verbose):
    self.verbose = verbose

  def log(self, command, message ):
    if self.verbose:
      timestamp = datetime.datetime.now()
      timestring = timestamp.strftime('%a %d %b %r')
      print(f'{timestring}: [{command}] -- {message}')

  def log_failure(self, raw_string):
    print(raw_string)
