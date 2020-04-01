""" A simple log formatter. """

import datetime

def _rpad(value, width):
  if len(value) > width:
    value = value[:width]

  pad = width - len(value)

  if pad > 0:
    for i in range(0, pad):
      value += ' '

  return value

def _pretty_print_data(data):
  for key, value in data.items():
    print(f'      >   {_rpad(key, 20)}:  {value}')

class Logger:
  """ Simple logger for formatting and handling verbose/failure logging. """
  def __init__(self, verbose):
    self.verbose = verbose

  def log(self, command, message, rows=False, filter_by=None):
    """ Log a formatted message, only if in verbose-mode, otherwise skip. """
    if self.verbose:
      timestamp = datetime.datetime.now()
      timestring = timestamp.strftime('%a %d %b %r')
      if filter_by is None:
        print(f'{timestring}: [{command}] -- {message}')
      else:
        print(f'{timestring}: [{command}]')
        if rows == True:
          for row in message:
            data = { your_key: row[your_key] for your_key in filter_by }
            _pretty_print_data(data)
            print('      --------------------')
        else:
          data = { your_key: message[your_key] for your_key in filter_by }
          _pretty_print_data(data)

  def log_failure(self, raw_string):
    """ Log a failure message, formatted if in verbose-mode, skinny otherwise. """
    if self.verbose:
      timestamp = datetime.datetime.now()
      timestring = timestamp.strftime('%a %d %b %r')
      print(f'{timestring}: [FAIL] -- {raw_string}')
    else:
      print(f'*** Failure: {raw_string}')
