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

def run():
  """ Execute the commands parsed from the command line. """
  (err, value) = commando.parse('command [<address>|<user>|<password>] (toggle|verbose)', sys.argv[1:])

  if err:
    print(value)
    return

  value = _set_defaults(value)
  commands.dispatch(value)
