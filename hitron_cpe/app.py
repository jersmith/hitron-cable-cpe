""" App runner for hitron router."""

import sys
from hitron_cpe.common import commando
from hitron_cpe.router import commands

def _set_defaults(value):
  address = '192.168.0.1'
  if 'address' not in value:
    value['address'] = address

  user = 'cusadmin'
  if 'user' not in value:
    value['user'] = user

  return value

def run():
  """ Execute the commands parsed from the command line. """
  (err, value) = commando.parse('command [<address>|<user>|password] (toggle|verbose)', sys.argv[1:])

  if err:
    print(value)
    return

  value = _set_defaults(value)
  print(f'value: {value}')
  commands.dispatch(value)


