""" App runner for toggle-wifi."""

import sys
from hitron_cpe.common import commando

import requests
import datetime

class Router:
  def __init__(self, address, username, password):
    self.username = username
    self.password = password
    self.address = address

    r = requests.get(f'http://{address}/data/system_model.asp')
    system_data = r.json()

    self.model = system_data['modelName']

    print(f'response: {r}')
    print(system_data)

    self._connect()

  def _connect(self):
    print(f'connecting user: {self.username}')

    post_data = {
      "user": self.username,
      "pwd": self.password,
      "rememberMe": False,
      "pwdCookieFlag": False
    }

    # This doesn't throw, even failures return 200. We know we got a successful
    # login if the cookie has a userid.
    r = requests.post(f'http://{self.address}/goform/login', post_data)
    print(f'Login: {r}')
    self.cookies = r.cookies

    if 'userid' not in self.cookies:
      print(r.text)

  def get_wireless(self):
    timestamp = datetime.datetime.now(datetime.timezone.utc)
    params = { '_': timestamp}
    r = requests.get(f'http://{self.address}/data/wireless_ssid.asp', cookies=self.cookies, params=params)
    data = r.json()

    return data



def run():
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

  router = Router(address, user, value['password'])
  print(f'Model: {router.model}')

  userid = router.cookies['userid']
  print(userid)

  wireless_data = router.get_wireless()
  print(wireless_data)

