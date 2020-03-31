""" App runner for hitron router."""

import sys
from hitron_cpe.common import commando
from hitron_cpe.common import Logger
from hitron_cpe.router import Router

def run():
  """ Connect to the router and execute the commands parsed from the command line. """
  (err, value) = commando.parse('[<address>|<user>|password] (toggle|verbose)', sys.argv[1:])

  if err:
    print(value)
    return

  address = '192.168.0.1'
  if 'address' in value:
    address = value['address']

  user = 'cusadmin'
  if 'user' in value:
    user = value['user']

  logger = Logger(value['verbose'])
  router = Router(address, user, value['password'], logger)

  wireless_data = router.get_wireless()
  print(wireless_data)

