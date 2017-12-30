from airmash import games

url = games.get_url('eu', 'ffa1')
print("Game URL: {}".format(url))

data = games.get_data()
for region_id in data['regions']:
    region = data['regions'][region_id]
    print('\nRegion: {} ({})'.format(region['name'], region_id))
    for game_id in region['games']:
        game = region['games'][game_id]
        print('{}, {} players - URL: {}'.format(game['name'], game['players'], game['url']))
    print('')