""" Represents the commands that can be sent to the Hitron router (cable CPE device). """

import sys
import datetime
import requests

class Router:
  """ The state and methods needed to communicate with the device. """

  def __init__(self, address, username, password, logger):
    self.username = username
    self.password = password
    self.address = address
    self.logger = logger
    self.cookies = None
    self.csrf = None

    system_data = self._data_request('system_model')

    self.model = system_data['modelName']
    self.logger.log('PROBE', f'Hitron Cable CPE {self.model}')
    self._connect()

  def _connect(self):
    post_data = {
      "user": self.username,
      "pwd": self.password,
      "rememberMe": False,
      "pwdCookieFlag": False
    }

    # This doesn't throw, even failures return 200. We know we got a successful
    # login if the cookie has a userid.
    req = requests.post(f'http://{self.address}/goform/login', post_data)

    if 'userid' not in req.cookies:
      self.logger.log_failure(req.text)
      sys.exit(-1)

    self.cookies = req.cookies

    userid = str(req.cookies['userid'])
    userid = f'{userid[:8]}...'
    self.logger.log('CONNECTED', f'userid: {userid}')

  def _data_request(self, name):
    if self.cookies is None:
      req = requests.get(f'http://{self.address}/data/{name}.asp')
    else:
      timestamp = datetime.datetime.now(datetime.timezone.utc)
      params = {'_': timestamp}
      req = requests.get(f'http://{self.address}/data/{name}.asp',
                         cookies=self.cookies,
                         params=params)

    data = req.json()
    return data


  def get_sysinfo(self):
    """ Router System Info request. """
    data = self._data_request('getSysInfo')
    #self.logger.log('SYSINFO', data)
    self.logger.log('SYSINFO', data[0], filter_by=['hwVersion', 'swVersion', 'serialNumber'])

    return data

  def get_wireless(self):
    """ Get basic and ssid info from all wireless bands and combine for updates. """
    basic = self._data_request('wireless_basic')
    ssid = self._data_request('wireless_ssid')

    bands = {}

    for band in basic:
      bands[band['band']] = band

    for band in ssid:
      bands[band['band']].update(band)

    collect = list(bands.values())

    #self.logger.log('WIRELESS', collect)
    self.logger.log('WIRELESS', collect, rows=True, filter_by=['band', 'bandwidth', 'ssidName', 'enable'])

    return collect

  def _get_csrf(self):
    """ The CSRF token is only needed on updates. """
    # GET http://192.168.0.1/data/getCsrfToken.asp
    print('not implemented')

  def toggle_wireless(self, ssid):
    """ Toggle the wireless band for ssid on or off. """
    # POST http://192.168.0.1/goform/WirelessCollection
    print('not implemented')
