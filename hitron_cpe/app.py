""" App runner for hitron router."""

import sys
from hitron_cpe.common import commando
from hitron_cpe.router import commands

def _set_defaults(value):
  """ Reasonable defaults for these save some typing. """
  # should work unless you've gotten creative with your network
  address = '192.168.0.1'
  if 'address' not in value:
    value['address'] = address

  # not sure this can be changed
  user = 'cusadmin'
  if 'user' not in value:
    value['user'] = user

  # yes, some providers set this as a default.
  password = 'password'
  if 'password' not in value:
    value['password'] = password

  return value

def _load_config(value):
  if 'config' in value:
    config_file = value['config']
  else:
    config_file = '.hitronrc'

  try:
    with open(config_file) as config_file:
      lines = config_file.readlines()
      for line in lines:
        pair = line.split('=')

        if pair[0] in value:
          kval = pair[1].strip()
          if kval[0] == "'" or kval[0] == '"':
            kval = kval[1:-1]

          value[pair[0]] = kval

  except OSError:
    print(f'[+] {config_file} not found, using defaults')

  return value

def run():
  """ Execute the commands parsed from the command line. """
  (err, value) = commando.parse(
    'command [<address>|<user>|<password>|<toggle_ssid>|<config>] (verbose|help)',
    sys.argv[1:])

  if err:
    print('Invalid command, try: ./hitron help')
    return

  value = _set_defaults(value)
  value = _load_config(value)
  commands.dispatch(value)
