""" Represents the commands that can be sent to the Hitron router (cable CPE device). """

import datetime
import sys
import urllib.parse
import requests

class Router:
  """ The state and methods needed to communicate with the device. """

  def __init__(self, address, username, password, logger):
    self.username = username
    self.password = password
    self.address = address
    self.logger = logger
    self.model = None
    self.session = None
    self.csrf = None

  def _connect(self):
    if self.session is not None:
      return

    post_data = {
      "user": self.username,
      "pwd": self.password,
      "rememberMe": False,
      "pwdCookieFlag": False
    }

    # This doesn't throw, even failures return 200. We know we got a successful
    # login if the cookie has a userid.
    session = requests.Session()
    self.session = session
    req = session.post(f'http://{self.address}/goform/login', post_data)

    if 'userid' not in req.cookies:
      self.logger.log_failure(req.text)
      sys.exit(-1)

    userid = str(req.cookies['userid'])
    userid = f'{userid[:8]}...'
    self.logger.log_info('CONNECTED', f'userid: {userid}')

  def _data_request(self, name):
    if self.session is None:
      req = requests.get(f'http://{self.address}/data/{name}.asp')
    else:
      timestamp = datetime.datetime.now(datetime.timezone.utc)
      params = {'_': timestamp}
      req = self.session.get(f'http://{self.address}/data/{name}.asp',
                             params=params)

    data = req.json()
    return data

  def get_sys_model(self):
    """ System Model request; this one doesn't need authentication. """
    system_data = self._data_request('system_model')
    self.model = system_data['modelName']
    self.logger.log_info('SYSTEM_MODEL', system_data, filter_by=[])
    return system_data

  def get_sysinfo(self):
    """ Router System Info request. """
    self._connect()
    data = self._data_request('getSysInfo')
    self.logger.log_info('SYSINFO', data[0], filter_by=[])

    return data

  def get_wireless(self):
    """ Get basic and ssid info from all wireless bands and combine for updates. """
    self._connect()
    basic = self._data_request('wireless_basic')
    self.logger.log_info('WIRELESS_BASIC', basic, rows=True, filter_by=[])
    ssid = self._data_request('wireless_ssid')
    self.logger.log_info('WIRELESS_SSID', ssid, rows=True, filter_by=[])

    bands = {}

    for band in basic:
      bands[band['band']] = band

    for band in ssid:
      bands[band['band']].update(band)

    collect = list(bands.values())
    return collect

  def _get_csrf(self):
    """ The CSRF token is only needed on updates. """
    self._connect()
    if self.csrf is None:
      csrf = self._data_request('getCsrfToken')
      self.logger.log_info('CSRF', csrf, filter_by=['token'])
      self.csrf = csrf['token']
      return self.csrf

    return self.csrf


  def update_wireless(self, model):
    """ Send updates for the wireless data in the model.  """

    csrf = self._get_csrf()

    data = {
      'model': model,
      'csrf_token': csrf,
      '_method': 'PUT'
    }

    payload = urllib.parse.urlencode(data)
    url = f'http://{self.address}/goform/WirelessCollection'
    self.session.post(url,
                      headers={'X-HTTP-Method-Override': 'PUT',
                               'X-Requested-With': 'XMLHttpRequest'},
                      data=payload,
                      cookies={'isEdit': '0', 'isEdit1': '0', 'isEdit2': '0', 'isEdit3': '0'})
