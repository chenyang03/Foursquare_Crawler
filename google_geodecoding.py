import urllib2
import time
import random
import json
from foursq_utils import *


def get_country(address):
    if len(address) == 0:
        return 'error'
    for i in range(0, 10):
        address = address.replace(str(i), '')
    url = '%20'.join((GEOCODING_URL + address + '&key=' + random.choice(Google_API_Keys)).split(' '))
    raw = get_raw_info(url)
    if raw == -1 or raw == -2:
        return 'error'
    try:
        ds = json.dumps(raw)
        de = json.loads(ds)
        data = eval(de)
    except:
        return 'error'
    try:
        for item in data['results'][0]['address_components']:
            if 'country' in item['types']:
                return item['short_name']
    except:
        return 'error'

