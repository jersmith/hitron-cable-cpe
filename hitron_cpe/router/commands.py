""" Explicit commands using the router api. """

import json
import time
from hitron_cpe.common import Logger
from hitron_cpe.router import Router

def _strip_external_spaces(json_str):
  clean = ''

  in_quotes = False
  for letter in json_str:
    if letter == '"':
      in_quotes = not in_quotes

    if letter == ' ':
      if in_quotes == True:
        clean += letter
    else:
      clean += letter

  return clean


def probe(values, router, logger):
  sys_model = router.get_sys_model()
  logger.log('PROBE', f'Success: Model {sys_model["modelName"]}')

def uptime(values, router, logger):
  sys_info = (router.get_sysinfo())[0]
  logger.log('UPTIME', f'WAN: {sys_info["systemWanUptime"]} LAN: {sys_info["systemLanUptime"]}')

def ip(values, router, logger):
  sys_info = (router.get_sysinfo())[0]
  logger.log('IP', f'WAN (public) IP: {sys_info["wanIp"]}')

def wireless(value, router, logger):
  wireless = router.get_wireless()

  if 'toggle_ssid' in value:
    time.sleep(5)
    toggle_ssid = value['toggle_ssid']
    found = False
    for band in wireless:
      if band['ssidName'] == toggle_ssid:
        found = True
        band['active'] = True
        band['bandunsave'] = True
        band['unsave'] = False
        toggle_value = band['wlsEnable']
        if toggle_value == 'ON':
          band['enable'] = 'OFF'
          band['wlsEnable'] = 'OFF'
          band['wlsOnOff'] = 'OFF'
        else:
          band['enable'] = 'ON'
          band['wlsEnable'] = 'ON'
          band['wlsOnOff'] = 'ON'
      else:
        band['active'] = False
        band['bandunsave'] = False
        band['unsave'] = False

    if found == True:
      json_str = json.dumps(wireless)
      clean = _strip_external_spaces(json_str)
      router.update_wireless(clean)
      logger.log('WIRELESS', f'toggle_ssid: {toggle_ssid} success')

  else:
    logger.log('WIRELESS', wireless, rows=True, filter_by=['band', 'bandwidth', 'ssidName', 'wlsEnable'])

command_list = {
  'probe': probe,
  'uptime': uptime,
  'ip': ip,
  'wireless': wireless
}

def dispatch(value):
  logger = Logger(value['verbose'])
  router = Router(value['address'],
                  value['user'],
                  value['password'],
                  logger)

  command_list[value['command']](value, router, logger)
