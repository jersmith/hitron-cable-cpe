""" Explicit commands using the router api. """

from hitron_cpe.common import Logger
from hitron_cpe.router import Router


#  router.get_wireless()
#  router.toggle_wireless('berkeley')

def probe(values, router, logger):
  sys_model = router.get_sys_model()
  logger.log('PROBE', f'Success: Model {sys_model["modelName"]}')

def uptime(values, router, logger):
  sys_info = (router.get_sysinfo())[0]
  logger.log('UPTIME', f'WAN: {sys_info["systemWanUptime"]} LAN: {sys_info["systemLanUptime"]}')

command_list = {
  'probe': probe,
  'uptime': uptime
}

def dispatch(value):
  logger = Logger(value['verbose'])
  router = Router(value['address'],
                  value['user'],
                  value['password'],
                  logger)

  command_list[value['command']](value, router, logger)
