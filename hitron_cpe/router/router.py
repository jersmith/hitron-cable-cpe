import sys
import requests
import datetime

class Router:
  def __init__(self, address, username, password, logger):
    self.username = username
    self.password = password
    self.address = address
    self.logger = logger

    r = requests.get(f'http://{address}/data/system_model.asp')
    system_data = r.json()

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
    r = requests.post(f'http://{self.address}/goform/login', post_data)

    if 'userid' not in r.cookies:
      self.logger.log_failure(r.text)
      sys.exit(-1)

    self.cookies = r.cookies

    userid = str(r.cookies['userid'])
    userid = f'{userid[:8]}...'
    self.logger.log('CONNECTED', f'userid: {userid}')


  def get_wireless(self):
    timestamp = datetime.datetime.now(datetime.timezone.utc)
    params = { '_': timestamp}
    r = requests.get(f'http://{self.address}/data/wireless_ssid.asp', cookies=self.cookies, params=params)
    data = r.json()

    return data

