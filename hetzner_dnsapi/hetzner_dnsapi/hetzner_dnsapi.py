#!/usr/bin/python3

import requests
import time  #voor testen
import configparser
import os

#DOCS: https://dns.hetzner.com/api-docs
class HetznerDNSAPI:
  def __init__(self, apikey):
    self.apikey = apikey
    self.sess   = requests.Session()

  def make_request(self, url, method='GET', data=None, params=None):
    headers = {'Content-Type':  'application/json; charset=utf-8',
               'Auth-API-Token': self.apikey
              }
    if method == 'GET':
      if params:
        res = self.sess.get(url, headers=headers, params=params)
      else:
        res = self.sess.get(url, headers=headers)
    elif method == 'PUT':
      res = self.sess.put(url, headers=headers, json=data)
    elif method == 'POST':
      res = self.sess.post(url, headers=headers, json=data)
    return res.json()

  def zones_get(self):
    return self.make_request('https://dns.hetzner.com/api/v1/zones')

  def zone_get(self, zone_id=None):
    if zone_id is None:
      return None
    return self.make_request('https://dns.hetzner.com/api/v1/zones/%s'%(zone_id))

  def zone_records_get(self, zone_id=None, record_id=None):
    if zone_id is None:
      return None
    params = {'zone_id': zone_id}

    all_records = self.make_request('https://dns.hetzner.com/api/v1/records', params=params)
    if record_id is None:
      return all_records
    else:
      for record in all_records['records']:
        if record['id'] == record_id:
          return {'records':[record]}
    return None

  def zone_record_update(self, zone_id=None, record_id=None, data=None):
    if zone_id is None or record_id is None or data is None:
      return None

    records = self.zone_records_get(zone_id=zone_id, record_id=record_id)
    current_data = {
            'name':    records['records'][0]['name'],
            'ttl':     records['records'][0]['ttl'],
            'type':    records['records'][0]['type'],
            'value':   records['records'][0]['value'],
            'zone_id': records['records'][0]['zone_id'],
    }
    for key in data:
      if key in current_data:
        current_data[key] = data[key]
    
    url = 'https://dns.hetzner.com/api/v1/records/%s'%(record_id)
    #print(url)
    #print(current_data)
    return self.make_request(url, method='PUT', data=current_data)



  def find_zone_id_for_name(self, name):
    zones = self.zones_get()
    for zone in zones['zones']:
      if zone['name'] == name:
        return zone['id']
    return None

  def find_record_id_for_name(self, zone_name=None, record_name=None):
    zone_id = self.find_zone_id_for_name(zone_name)
    if not zone_id:
      return None
    records = self.zone_records_get(zone_id=zone_id)
    for record in records['records']:
      if record['name'] == record_name:
        return record['id']
    return None

if __name__ == "__main__":
  hetzner = HetznerDNSAPI()

  zone_id   = hetzner.find_zone_id_for_name('domain.com')
  record_id = hetzner.find_record_id_for_name(zone_name='domain.com', record_name='_sip._udp.sip')
  print(record_id)
  print( hetzner.zone_record_update(zone_id=zone_id, record_id=record_id, data={'value': '10 50 5060 sip02.domain.com'}) )
  
  time.sleep(10)
  print( hetzner.zone_records_get(zone_id=zone_id) )

