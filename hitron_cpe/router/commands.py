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

def print_help(values, router, logger):
  print()
  print('Hitron Cable CPE (modem/router) tool')
  print()
  print('The following commands are supported. To get information about a specific command,')
  print('type the command with the --help option, eg "hitron probe --help"')
  print()
  print('To override defaults pass --address, --user, and/or --password.')
  print()

  commands = command_list.keys()
  for command in commands:
    message = [command, command_list[command]['doc']]
    logger.log_columns(message, [20])

  print()

def probe(values, router, logger):
  if values['help']:
    print()
    print('hitron probe [options]')
    logger.log_columns([' ', '--address', 'The IP address to reach your device. Defaults to 192.168.0.1.'],
                       [10, 15])
    print()
    return

  sys_model = router.get_sys_model()
  logger.log('PROBE', f'Success: Model {sys_model["modelName"]}')

def uptime(values, router, logger):
  if values['help']:
    print()
    print('hitron uptime [options]')
    logger.log_columns([' ', '--address', 'The IP address to reach your device. Defaults to 192.168.0.1.'],
                       [10, 15])
    logger.log_columns([' ', '--user', 'The user name to connect to the device. Defaults to "cusadmin".'],
                       [10, 15])
    logger.log_columns([' ', '--password', 'The password used to connect to the device. Defaults to "password".'],
                       [10, 15])


    print()
    return

  sys_info = (router.get_sysinfo())[0]
  logger.log('UPTIME', f'WAN: {sys_info["systemWanUptime"]} LAN: {sys_info["systemLanUptime"]}')

def ip(values, router, logger):
  if values['help']:
    print()
    print('hitron ip [options]')
    logger.log_columns([' ', '--address', 'The IP address to reach your device. Defaults to 192.168.0.1.'],
                       [10, 15])
    logger.log_columns([' ', '--user', 'The user name to connect to the device. Defaults to "cusadmin".'],
                       [10, 15])
    logger.log_columns([' ', '--password', 'The password used to connect to the device. Defaults to "password".'],
                       [10, 15])


    print()
    return

  sys_info = (router.get_sysinfo())[0]
  logger.log('IP', f'WAN (public) IP: {sys_info["wanIp"]}')

def wireless(values, router, logger):
  if values['help']:
    print()
    print('hitron wireless [options]')
    logger.log_columns([' ', '--address', 'The IP address to reach your device. Defaults to 192.168.0.1.'],
                       [10, 15])
    logger.log_columns([' ', '--user', 'The user name to connect to the device. Defaults to "cusadmin".'],
                       [10, 15])
    logger.log_columns([' ', '--password', 'The password used to connect to the device. Defaults to "password".'],
                       [10, 15])
    logger.log_columns([' ', '--toggle_ssid', 'The name of the WiFi network to toggle. If present the given network will be turned on or off.'],
                       [10, 15])



    print()
    return

  wireless = router.get_wireless()

  if 'toggle_ssid' in values:
    time.sleep(5)
    toggle_ssid = values['toggle_ssid']
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
  'help': {
    'cmd': print_help,
    'doc': 'Print this message.'
  },
  'probe': {
    'cmd': probe,
    'doc': 'Tries to connect to the device without authenticating, showing the model number if successful.'
  },
  'uptime': {
    'cmd': uptime,
    'doc': 'Authenticates to the device and shows the current running uptime for LAN and WAN.'
  },
  'ip': {
    'cmd': ip,
    'doc': 'Authenticates to the device and shows the current public IP address of the gateway.'
  },
  'wireless': {
    'cmd': wireless,
    'doc': 'Returns the state of the wireless networks, or with --toggle_ssid will turn them on or off.'
  }
}

def dispatch(value):
  if value['command'] not in command_list:
    print(f'Unknown command: {value["command"]}')
    print('Try "hitron help"')
    return

  logger = Logger(value['verbose'])
  router = Router(value['address'],
                  value['user'],
                  value['password'],
                  logger)

  command_list[value['command']]['cmd'](value, router, logger)
