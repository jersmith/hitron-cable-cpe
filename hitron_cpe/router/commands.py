""" Explicit commands using the router api. """

from hitron_cpe.common import Logger
from hitron_cpe.router import Router


#  router.get_sysinfo()
#  router.get_wireless()
#  router.toggle_wireless('berkeley')

def probe(values, router, logger):
  router.get_sys_model()

def list_wireless(values, router, logger):
  print(f'list_wireless password: {values["password"]}')

command_list = {
  'probe': probe,
  'list_wireless': list_wireless
}

def dispatch(value):
  logger = Logger(value['verbose'])
  router = Router(value['address'],
                  value['user'],
                  value['password'],
                  logger)

  command_list[value['command']](value, router, logger)
