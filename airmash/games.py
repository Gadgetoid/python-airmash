from .types import *

try:
    from urllib.request import Request, urlopen
except ImportError:
    from urllib2 import Request, urlopen

import json
import time

REQUEST_RATE = 5

last_data = None
cached_data = None

def build_host(host='', room=''):
    return GAME_ADDR.format(host=host, room=room)

def get_region(region='eu'):
    data = get_data()
    return data['regions'][region]

def get_game(region='eu', room='ffa1'):
    data = get_data()
    return data['regions'][region]['games'][room]

def get_url(region='eu', room='ffa1'):
    data = get_game(region, room)
    return data['url']

def get_protocol():
    data = get_data()
    return data['protocol']

def get_data():
    global cached_data, last_data
    if last_data is not None and time.time() - last_data < REQUEST_RATE:
        print("Sending cached data...")
        return cached_data

    request = Request(GAMES_ADDR)
    request.add_header('Referer', 'https://airma.sh')
    request.add_header('User-Agent', 'Mozilla/5.0')
    url = urlopen(request)
    data = json.loads(url.read().decode())
    src_regions = json.loads(data['data'])
    
    regions = {}

    for region in src_regions:
        games = {}
        for game in region['games']:
            games[game['id']] = {
                'type': game['type'],
                'id': game['id'],
                'name': game['name'],
                'nameShort': game['nameShort'],
                'host': game['host'],
                'players': game['players'],
                'url': build_host(game['host'], game['id'])
            }
        regions[region['id']] = {
            'name': region['name'],
            'games': games
        }

    cached_data =  {
        'protocol': data['protocol'],
        'regions': regions
    }

    last_data = time.time()
    return cached_data


