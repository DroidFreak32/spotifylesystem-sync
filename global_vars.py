import yaml
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="327d9a61415f4e98b36a8964485e7f41",
                                               client_secret="2909fdb6d8a148bd950fcf4298e0f30e",
                                               redirect_uri="http://127.0.0.1:9090",
                                               scope="user-library-read"))

# playlist_list = sp.current_user_playlists()

playlist_list = {
    'href': 'https://api.spotify.com/v1/users/rushabshah32/playlists?offset=0&limit=50', 'items': [
        {'collaborative': False, 'description': '',
         'external_urls': {'spotify': 'https://open.spotify.com/playlist/3wxUTHoNAT60QsyXfCJRaG'},
         'href': 'https://api.spotify.com/v1/playlists/3wxUTHoNAT60QsyXfCJRaG', 'id': '3wxUTHoNAT60QsyXfCJRaG',
         'images': [
             {'height': 640, 'url': 'https://i.scdn.co/image/ab67616d0000b273593b46ea89cf97dc62152757', 'width': 640}],
         'name': 'My Shazam Tracks', 'owner': {'display_name': 'Rushab Shah', 'external_urls': {
            'spotify': 'https://open.spotify.com/user/rushabshah32'},
                                               'href': 'https://api.spotify.com/v1/users/rushabshah32',
                                               'id': 'rushabshah32', 'type': 'user',
                                               'uri': 'spotify:user:rushabshah32'}, 'primary_color': None,
         'public': True, 'snapshot_id': 'Miw1MTA0OTE5ZTNhOGIxZjhhZWY5NWM2YTdhODRmYzczZjkyZTYxZGM1',
         'tracks': {'href': 'https://api.spotify.com/v1/playlists/3wxUTHoNAT60QsyXfCJRaG/tracks', 'total': 1},
         'type': 'playlist', 'uri': 'spotify:playlist:3wxUTHoNAT60QsyXfCJRaG'},
        {'collaborative': False, 'description': '',
         'external_urls': {'spotify': 'https://open.spotify.com/playlist/03m0iBzmmSFmoEuKcQLDZz'},
         'href': 'https://api.spotify.com/v1/playlists/03m0iBzmmSFmoEuKcQLDZz', 'id': '03m0iBzmmSFmoEuKcQLDZz',
         'images': [{'height': 640,
                     'url': 'https://mosaic.scdn.co/640/ab67616d0000b27338d5b2e2c465d4743acc7b37ab67616d0000b27339522c242d7f10c0b80eb9b9ab67616d0000b273be43a3cafaca1c258ec23730ab67616d0000b273c6e4471284adb80e9dd45f8f',
                     'width': 640}, {'height': 300,
                                     'url': 'https://mosaic.scdn.co/300/ab67616d0000b27338d5b2e2c465d4743acc7b37ab67616d0000b27339522c242d7f10c0b80eb9b9ab67616d0000b273be43a3cafaca1c258ec23730ab67616d0000b273c6e4471284adb80e9dd45f8f',
                                     'width': 300}, {'height': 60,
                                                     'url': 'https://mosaic.scdn.co/60/ab67616d0000b27338d5b2e2c465d4743acc7b37ab67616d0000b27339522c242d7f10c0b80eb9b9ab67616d0000b273be43a3cafaca1c258ec23730ab67616d0000b273c6e4471284adb80e9dd45f8f',
                                                     'width': 60}], 'name': 'Post Rock',
         'owner': {'display_name': 'Rushab Shah',
                   'external_urls': {'spotify': 'https://open.spotify.com/user/rushabshah32'},
                   'href': 'https://api.spotify.com/v1/users/rushabshah32', 'id': 'rushabshah32', 'type': 'user',
                   'uri': 'spotify:user:rushabshah32'}, 'primary_color': None, 'public': True,
         'snapshot_id': 'MTEsZGE1ZTA4YzIwMTFmNjM0NWQyZTNlNDkyNTAxODQ4MzNkZDFhYmIwNw==',
         'tracks': {'href': 'https://api.spotify.com/v1/playlists/03m0iBzmmSFmoEuKcQLDZz/tracks', 'total': 8},
         'type': 'playlist', 'uri': 'spotify:playlist:03m0iBzmmSFmoEuKcQLDZz'}, {'collaborative': False,
                                                                                 'description': 'I ain&#x27;t no doctor but if I could fix others&#x27; hearts I&#x27;d make them listen to this without changing the order of the tracks :)',
                                                                                 'external_urls': {
                                                                                     'spotify': 'https://open.spotify.com/playlist/18n6rIA0rAkk20PQdgcA6j'},
                                                                                 'href': 'https://api.spotify.com/v1/playlists/18n6rIA0rAkk20PQdgcA6j',
                                                                                 'id': '18n6rIA0rAkk20PQdgcA6j',
                                                                                 'images': [{'height': 640,
                                                                                             'url': 'https://mosaic.scdn.co/640/ab67616d0000b2734ae1c4c5c45aabe565499163ab67616d0000b2736b3fa88bdd4af566fbbf2bbfab67616d0000b273b1f8da74f225fa1225cdfaceab67616d0000b273fc5f23d71de7ad824565f94c',
                                                                                             'width': 640},
                                                                                            {'height': 300,
                                                                                             'url': 'https://mosaic.scdn.co/300/ab67616d0000b2734ae1c4c5c45aabe565499163ab67616d0000b2736b3fa88bdd4af566fbbf2bbfab67616d0000b273b1f8da74f225fa1225cdfaceab67616d0000b273fc5f23d71de7ad824565f94c',
                                                                                             'width': 300},
                                                                                            {'height': 60,
                                                                                             'url': 'https://mosaic.scdn.co/60/ab67616d0000b2734ae1c4c5c45aabe565499163ab67616d0000b2736b3fa88bdd4af566fbbf2bbfab67616d0000b273b1f8da74f225fa1225cdfaceab67616d0000b273fc5f23d71de7ad824565f94c',
                                                                                             'width': 60}],
                                                                                 'name': 'Arctic Monkeys being a cardiologist',
                                                                                 'owner': {
                                                                                     'display_name': 'Rushab Shah',
                                                                                     'external_urls': {
                                                                                         'spotify': 'https://open.spotify.com/user/rushabshah32'},
                                                                                     'href': 'https://api.spotify.com/v1/users/rushabshah32',
                                                                                     'id': 'rushabshah32',
                                                                                     'type': 'user',
                                                                                     'uri': 'spotify:user:rushabshah32'},
                                                                                 'primary_color': None, 'public': True,
                                                                                 'snapshot_id': 'MzYsZjgwZTJiMDBjOWZkODk2MGE3MTYyMzkxNGZiNDFhZjRmNzE4MWFiNA==',
                                                                                 'tracks': {
                                                                                     'href': 'https://api.spotify.com/v1/playlists/18n6rIA0rAkk20PQdgcA6j/tracks',
                                                                                     'total': 22}, 'type': 'playlist',
                                                                                 'uri': 'spotify:playlist:18n6rIA0rAkk20PQdgcA6j'},
        {'collaborative': False, 'description': 'Fantasy land for the virgins',
         'external_urls': {'spotify': 'https://open.spotify.com/playlist/62V0MssVsUYGcmWp75D833'},
         'href': 'https://api.spotify.com/v1/playlists/62V0MssVsUYGcmWp75D833', 'id': '62V0MssVsUYGcmWp75D833',
         'images': [{'height': 640,
                     'url': 'https://mosaic.scdn.co/640/ab67616d0000b2734ae1c4c5c45aabe565499163ab67616d0000b273b1f8da74f225fa1225cdfaceab67616d0000b273f65d720a5d70dbb93e96d528ab67616d0000b273f7017fd086b1f27d90993175',
                     'width': 640}, {'height': 300,
                                     'url': 'https://mosaic.scdn.co/300/ab67616d0000b2734ae1c4c5c45aabe565499163ab67616d0000b273b1f8da74f225fa1225cdfaceab67616d0000b273f65d720a5d70dbb93e96d528ab67616d0000b273f7017fd086b1f27d90993175',
                                     'width': 300}, {'height': 60,
                                                     'url': 'https://mosaic.scdn.co/60/ab67616d0000b2734ae1c4c5c45aabe565499163ab67616d0000b273b1f8da74f225fa1225cdfaceab67616d0000b273f65d720a5d70dbb93e96d528ab67616d0000b273f7017fd086b1f27d90993175',
                                                     'width': 60}], 'name': 'Hot stuff',
         'owner': {'display_name': 'Rushab Shah',
                   'external_urls': {'spotify': 'https://open.spotify.com/user/rushabshah32'},
                   'href': 'https://api.spotify.com/v1/users/rushabshah32', 'id': 'rushabshah32', 'type': 'user',
                   'uri': 'spotify:user:rushabshah32'}, 'primary_color': None, 'public': True,
         'snapshot_id': 'MjYsZGY5ZWQzZjRhZDlkYmZmMzY4YjRmZjQ5MzBhMDYxZWExYzQxMTk5Nw==',
         'tracks': {'href': 'https://api.spotify.com/v1/playlists/62V0MssVsUYGcmWp75D833/tracks', 'total': 24},
         'type': 'playlist', 'uri': 'spotify:playlist:62V0MssVsUYGcmWp75D833'},
        {'collaborative': False, 'description': '',
         'external_urls': {'spotify': 'https://open.spotify.com/playlist/0K8Z3rRTTON1V348WDQz8Z'},
         'href': 'https://api.spotify.com/v1/playlists/0K8Z3rRTTON1V348WDQz8Z', 'id': '0K8Z3rRTTON1V348WDQz8Z',
         'images': [{'height': 640,
                     'url': 'https://mosaic.scdn.co/640/ab67616d0000b2732c30fdeffd0d99638a98416dab67616d0000b2733395f3e809dfbc2b1101d464ab67616d0000b2734fe83775017dd8af28079187ab67616d0000b273ee0d0dce888c6c8a70db6e8b',
                     'width': 640}, {'height': 300,
                                     'url': 'https://mosaic.scdn.co/300/ab67616d0000b2732c30fdeffd0d99638a98416dab67616d0000b2733395f3e809dfbc2b1101d464ab67616d0000b2734fe83775017dd8af28079187ab67616d0000b273ee0d0dce888c6c8a70db6e8b',
                                     'width': 300}, {'height': 60,
                                                     'url': 'https://mosaic.scdn.co/60/ab67616d0000b2732c30fdeffd0d99638a98416dab67616d0000b2733395f3e809dfbc2b1101d464ab67616d0000b2734fe83775017dd8af28079187ab67616d0000b273ee0d0dce888c6c8a70db6e8b',
                                                     'width': 60}], 'name': 'Something different',
         'owner': {'display_name': 'Rushab Shah',
                   'external_urls': {'spotify': 'https://open.spotify.com/user/rushabshah32'},
                   'href': 'https://api.spotify.com/v1/users/rushabshah32', 'id': 'rushabshah32', 'type': 'user',
                   'uri': 'spotify:user:rushabshah32'}, 'primary_color': None, 'public': True,
         'snapshot_id': 'MjEsNzQ5Y2RkNTA2OWM2MDhlNzJhNTA5YTg2MDU1MmI3NmYwZTFlNDJiNg==',
         'tracks': {'href': 'https://api.spotify.com/v1/playlists/0K8Z3rRTTON1V348WDQz8Z/tracks', 'total': 18},
         'type': 'playlist', 'uri': 'spotify:playlist:0K8Z3rRTTON1V348WDQz8Z'},
        {'collaborative': False, 'description': '',
         'external_urls': {'spotify': 'https://open.spotify.com/playlist/6ro7JwspABtrlTErGYO53a'},
         'href': 'https://api.spotify.com/v1/playlists/6ro7JwspABtrlTErGYO53a', 'id': '6ro7JwspABtrlTErGYO53a',
         'images': [{'height': 640,
                     'url': 'https://mosaic.scdn.co/640/ab67616d0000b27314d5029214f9f8e0ce2a9e3bab67616d0000b2733e653df72e6eb1ccb89576b3ab67616d0000b273cd3b5853d5cc9f9fdbaa7640ab67616d0000b273d9126888f214ca8521d83d2a',
                     'width': 640}, {'height': 300,
                                     'url': 'https://mosaic.scdn.co/300/ab67616d0000b27314d5029214f9f8e0ce2a9e3bab67616d0000b2733e653df72e6eb1ccb89576b3ab67616d0000b273cd3b5853d5cc9f9fdbaa7640ab67616d0000b273d9126888f214ca8521d83d2a',
                                     'width': 300}, {'height': 60,
                                                     'url': 'https://mosaic.scdn.co/60/ab67616d0000b27314d5029214f9f8e0ce2a9e3bab67616d0000b2733e653df72e6eb1ccb89576b3ab67616d0000b273cd3b5853d5cc9f9fdbaa7640ab67616d0000b273d9126888f214ca8521d83d2a',
                                                     'width': 60}], 'name': 'Modern Instrumentals',
         'owner': {'display_name': 'Rushab Shah',
                   'external_urls': {'spotify': 'https://open.spotify.com/user/rushabshah32'},
                   'href': 'https://api.spotify.com/v1/users/rushabshah32', 'id': 'rushabshah32', 'type': 'user',
                   'uri': 'spotify:user:rushabshah32'}, 'primary_color': None, 'public': True,
         'snapshot_id': 'OCwyZmRiYjliZmQwYmZkZjI5YTE5OTJkMDMyOTg4ZDYyMjEyY2IzNWEw',
         'tracks': {'href': 'https://api.spotify.com/v1/playlists/6ro7JwspABtrlTErGYO53a/tracks', 'total': 14},
         'type': 'playlist', 'uri': 'spotify:playlist:6ro7JwspABtrlTErGYO53a'},
        {'collaborative': False, 'description': 'Why aren&#x27;t you swimming ?',
         'external_urls': {'spotify': 'https://open.spotify.com/playlist/1MyrUZxvtixPsblkXjDioP'},
         'href': 'https://api.spotify.com/v1/playlists/1MyrUZxvtixPsblkXjDioP', 'id': '1MyrUZxvtixPsblkXjDioP',
         'images': [{'height': 640,
                     'url': 'https://mosaic.scdn.co/640/ab67616d0000b27333e96c0ff58f371cf75cb16eab67616d0000b27386734c2b36be7adcaa4ab1f0ab67616d0000b273bcda9701e49a3e3a13abbaeeab67616d0000b273cdfe41cd475f8ad3a29b3537',
                     'width': 640}, {'height': 300,
                                     'url': 'https://mosaic.scdn.co/300/ab67616d0000b27333e96c0ff58f371cf75cb16eab67616d0000b27386734c2b36be7adcaa4ab1f0ab67616d0000b273bcda9701e49a3e3a13abbaeeab67616d0000b273cdfe41cd475f8ad3a29b3537',
                                     'width': 300}, {'height': 60,
                                                     'url': 'https://mosaic.scdn.co/60/ab67616d0000b27333e96c0ff58f371cf75cb16eab67616d0000b27386734c2b36be7adcaa4ab1f0ab67616d0000b273bcda9701e49a3e3a13abbaeeab67616d0000b273cdfe41cd475f8ad3a29b3537',
                                                     'width': 60}], 'name': 'Calm Waters',
         'owner': {'display_name': 'Rushab Shah',
                   'external_urls': {'spotify': 'https://open.spotify.com/user/rushabshah32'},
                   'href': 'https://api.spotify.com/v1/users/rushabshah32', 'id': 'rushabshah32', 'type': 'user',
                   'uri': 'spotify:user:rushabshah32'}, 'primary_color': None, 'public': True,
         'snapshot_id': 'NDUsNzg2ZDI5NGE5YzhmNmY3NDAxZTcxNzg5M2NhOTcyMzFiMTM3YjBiNQ==',
         'tracks': {'href': 'https://api.spotify.com/v1/playlists/1MyrUZxvtixPsblkXjDioP/tracks', 'total': 46},
         'type': 'playlist', 'uri': 'spotify:playlist:1MyrUZxvtixPsblkXjDioP'},
        {'collaborative': False, 'description': 'go away pls',
         'external_urls': {'spotify': 'https://open.spotify.com/playlist/6MMOZBrYL07sfaPdVnQ38c'},
         'href': 'https://api.spotify.com/v1/playlists/6MMOZBrYL07sfaPdVnQ38c', 'id': '6MMOZBrYL07sfaPdVnQ38c',
         'images': [{'height': 640,
                     'url': 'https://mosaic.scdn.co/640/ab67616d0000b2736c112ab47442b526755ffe36ab67616d0000b2737bf1b91bc05ea3b837e8eb94ab67616d0000b273bf33fdea7b0ff3c71b6faf75ab67616d0000b273e9b6f26ff354f4d70847f02d',
                     'width': 640}, {'height': 300,
                                     'url': 'https://mosaic.scdn.co/300/ab67616d0000b2736c112ab47442b526755ffe36ab67616d0000b2737bf1b91bc05ea3b837e8eb94ab67616d0000b273bf33fdea7b0ff3c71b6faf75ab67616d0000b273e9b6f26ff354f4d70847f02d',
                                     'width': 300}, {'height': 60,
                                                     'url': 'https://mosaic.scdn.co/60/ab67616d0000b2736c112ab47442b526755ffe36ab67616d0000b2737bf1b91bc05ea3b837e8eb94ab67616d0000b273bf33fdea7b0ff3c71b6faf75ab67616d0000b273e9b6f26ff354f4d70847f02d',
                                                     'width': 60}], 'name': 'Rockless Bottom',
         'owner': {'display_name': 'Rushab Shah',
                   'external_urls': {'spotify': 'https://open.spotify.com/user/rushabshah32'},
                   'href': 'https://api.spotify.com/v1/users/rushabshah32', 'id': 'rushabshah32', 'type': 'user',
                   'uri': 'spotify:user:rushabshah32'}, 'primary_color': None, 'public': True,
         'snapshot_id': 'NTgsZDIzYWI4MTgwMzc1NWU4MmM3MDg5YzA0ZTZiMzA0YzNiOWE4MjVlNQ==',
         'tracks': {'href': 'https://api.spotify.com/v1/playlists/6MMOZBrYL07sfaPdVnQ38c/tracks', 'total': 58},
         'type': 'playlist', 'uri': 'spotify:playlist:6MMOZBrYL07sfaPdVnQ38c'},
        {'collaborative': False, 'description': 'A playlist to overpower all the noise in your head',
         'external_urls': {'spotify': 'https://open.spotify.com/playlist/1LinCArgs5903itZ6IEsp2'},
         'href': 'https://api.spotify.com/v1/playlists/1LinCArgs5903itZ6IEsp2', 'id': '1LinCArgs5903itZ6IEsp2',
         'images': [{'height': 640,
                     'url': 'https://mosaic.scdn.co/640/ab67616d0000b2735721adac031512b903f10d03ab67616d0000b27360cf7c8dd93815ccd6cb4830ab67616d0000b273bb85bcab29cd1c193c46afb1ab67616d0000b273bc7ddb77993dd1d8d19c22a2',
                     'width': 640}, {'height': 300,
                                     'url': 'https://mosaic.scdn.co/300/ab67616d0000b2735721adac031512b903f10d03ab67616d0000b27360cf7c8dd93815ccd6cb4830ab67616d0000b273bb85bcab29cd1c193c46afb1ab67616d0000b273bc7ddb77993dd1d8d19c22a2',
                                     'width': 300}, {'height': 60,
                                                     'url': 'https://mosaic.scdn.co/60/ab67616d0000b2735721adac031512b903f10d03ab67616d0000b27360cf7c8dd93815ccd6cb4830ab67616d0000b273bb85bcab29cd1c193c46afb1ab67616d0000b273bc7ddb77993dd1d8d19c22a2',
                                                     'width': 60}], 'name': 'White Rock Noise',
         'owner': {'display_name': 'Rushab Shah',
                   'external_urls': {'spotify': 'https://open.spotify.com/user/rushabshah32'},
                   'href': 'https://api.spotify.com/v1/users/rushabshah32', 'id': 'rushabshah32', 'type': 'user',
                   'uri': 'spotify:user:rushabshah32'}, 'primary_color': None, 'public': True,
         'snapshot_id': 'MTY2LGY3MTBhM2EzYTM2ZDVlYTFhMzJiOGU1NWVmMjA2Y2RkYjBjMDU0M2U=',
         'tracks': {'href': 'https://api.spotify.com/v1/playlists/1LinCArgs5903itZ6IEsp2/tracks', 'total': 307},
         'type': 'playlist', 'uri': 'spotify:playlist:1LinCArgs5903itZ6IEsp2'},
        {'collaborative': False, 'description': '',
         'external_urls': {'spotify': 'https://open.spotify.com/playlist/2hEP8skwpqslLEVQ2E1H6f'},
         'href': 'https://api.spotify.com/v1/playlists/2hEP8skwpqslLEVQ2E1H6f', 'id': '2hEP8skwpqslLEVQ2E1H6f',
         'images': [{'height': 640,
                     'url': 'https://mosaic.scdn.co/640/ab67616d0000b27339864a5777bfcb8b451db79fab67616d0000b273595274875c0a7650e2c5bb4dab67616d0000b27360cf7c8dd93815ccd6cb4830ab67616d0000b273736145b97bab8fa92cb6113f',
                     'width': 640}, {'height': 300,
                                     'url': 'https://mosaic.scdn.co/300/ab67616d0000b27339864a5777bfcb8b451db79fab67616d0000b273595274875c0a7650e2c5bb4dab67616d0000b27360cf7c8dd93815ccd6cb4830ab67616d0000b273736145b97bab8fa92cb6113f',
                                     'width': 300}, {'height': 60,
                                                     'url': 'https://mosaic.scdn.co/60/ab67616d0000b27339864a5777bfcb8b451db79fab67616d0000b273595274875c0a7650e2c5bb4dab67616d0000b27360cf7c8dd93815ccd6cb4830ab67616d0000b273736145b97bab8fa92cb6113f',
                                                     'width': 60}], 'name': 'Anguish!',
         'owner': {'display_name': 'Rushab Shah',
                   'external_urls': {'spotify': 'https://open.spotify.com/user/rushabshah32'},
                   'href': 'https://api.spotify.com/v1/users/rushabshah32', 'id': 'rushabshah32', 'type': 'user',
                   'uri': 'spotify:user:rushabshah32'}, 'primary_color': None, 'public': True,
         'snapshot_id': 'MjEsOTRkNGEwYmQ2OTJlNmEyNDU1M2U3NTM5MmRlNTA5YTUyNDRlNGFhYQ==',
         'tracks': {'href': 'https://api.spotify.com/v1/playlists/2hEP8skwpqslLEVQ2E1H6f/tracks', 'total': 44},
         'type': 'playlist', 'uri': 'spotify:playlist:2hEP8skwpqslLEVQ2E1H6f'},
        {'collaborative': False, 'description': '',
         'external_urls': {'spotify': 'https://open.spotify.com/playlist/2fr0uT8blZ4YujtYCz8WdO'},
         'href': 'https://api.spotify.com/v1/playlists/2fr0uT8blZ4YujtYCz8WdO', 'id': '2fr0uT8blZ4YujtYCz8WdO',
         'images': [{'height': 640,
                     'url': 'https://mosaic.scdn.co/640/ab67616d0000b2739dfee5404d5e0763998c958eab67616d0000b273c8a11e48c91a982d086afc69ab67616d0000b273d55ec7fcfacd95e73877b787ab67616d0000b273e44963b8bb127552ac761873',
                     'width': 640}, {'height': 300,
                                     'url': 'https://mosaic.scdn.co/300/ab67616d0000b2739dfee5404d5e0763998c958eab67616d0000b273c8a11e48c91a982d086afc69ab67616d0000b273d55ec7fcfacd95e73877b787ab67616d0000b273e44963b8bb127552ac761873',
                                     'width': 300}, {'height': 60,
                                                     'url': 'https://mosaic.scdn.co/60/ab67616d0000b2739dfee5404d5e0763998c958eab67616d0000b273c8a11e48c91a982d086afc69ab67616d0000b273d55ec7fcfacd95e73877b787ab67616d0000b273e44963b8bb127552ac761873',
                                                     'width': 60}], 'name': 'Old is gold',
         'owner': {'display_name': 'Rushab Shah',
                   'external_urls': {'spotify': 'https://open.spotify.com/user/rushabshah32'},
                   'href': 'https://api.spotify.com/v1/users/rushabshah32', 'id': 'rushabshah32', 'type': 'user',
                   'uri': 'spotify:user:rushabshah32'}, 'primary_color': None, 'public': True,
         'snapshot_id': 'NTAsOTk5MDg0NDc5OTM1Y2ViZDk0ZGE3MGM5ZWQ2OTY2NGE1NDM0NGJlYw==',
         'tracks': {'href': 'https://api.spotify.com/v1/playlists/2fr0uT8blZ4YujtYCz8WdO/tracks', 'total': 46},
         'type': 'playlist', 'uri': 'spotify:playlist:2fr0uT8blZ4YujtYCz8WdO'},
        {'collaborative': False, 'description': '',
         'external_urls': {'spotify': 'https://open.spotify.com/playlist/4Kb9y65b3bV1jwEGhADCC2'},
         'href': 'https://api.spotify.com/v1/playlists/4Kb9y65b3bV1jwEGhADCC2', 'id': '4Kb9y65b3bV1jwEGhADCC2',
         'images': [{'height': 640,
                     'url': 'https://mosaic.scdn.co/640/ab67616d0000b273206dcb32282da4c6a778d073ab67616d0000b2732363f794af17d154dc17bbb6ab67616d0000b27371abe464f5a4b276cb5a9ff7ab67616d0000b273877f4dbc82a9dfd850bb52c8',
                     'width': 640}, {'height': 300,
                                     'url': 'https://mosaic.scdn.co/300/ab67616d0000b273206dcb32282da4c6a778d073ab67616d0000b2732363f794af17d154dc17bbb6ab67616d0000b27371abe464f5a4b276cb5a9ff7ab67616d0000b273877f4dbc82a9dfd850bb52c8',
                                     'width': 300}, {'height': 60,
                                                     'url': 'https://mosaic.scdn.co/60/ab67616d0000b273206dcb32282da4c6a778d073ab67616d0000b2732363f794af17d154dc17bbb6ab67616d0000b27371abe464f5a4b276cb5a9ff7ab67616d0000b273877f4dbc82a9dfd850bb52c8',
                                                     'width': 60}], 'name': 'Anime',
         'owner': {'display_name': 'Rushab Shah',
                   'external_urls': {'spotify': 'https://open.spotify.com/user/rushabshah32'},
                   'href': 'https://api.spotify.com/v1/users/rushabshah32', 'id': 'rushabshah32', 'type': 'user',
                   'uri': 'spotify:user:rushabshah32'}, 'primary_color': None, 'public': True,
         'snapshot_id': 'MjcsZDNiNjU0ZWY5MjA3OWU1NmYyMzNhMGQ5YWI1Y2QyMTViYzQ2ZmQ4NA==',
         'tracks': {'href': 'https://api.spotify.com/v1/playlists/4Kb9y65b3bV1jwEGhADCC2/tracks', 'total': 25},
         'type': 'playlist', 'uri': 'spotify:playlist:4Kb9y65b3bV1jwEGhADCC2'}], 'limit': 50, 'next': None, 'offset': 0,
    'previous': None, 'total': 12}

json_playlist = {
    "href": "https://api.spotify.com/v1/users/rushabshah32/playlists?offset=0&limit=50",
    "items": [
        {
            "collaborative": False,
            "description": "",
            "external_urls": {
                "spotify": "https://open.spotify.com/playlist/3wxUTHoNAT60QsyXfCJRaG"
            },
            "href": "https://api.spotify.com/v1/playlists/3wxUTHoNAT60QsyXfCJRaG",
            "id": "3wxUTHoNAT60QsyXfCJRaG",
            "images": [
                {
                    "height": 640,
                    "url": "https://i.scdn.co/image/ab67616d0000b273593b46ea89cf97dc62152757",
                    "width": 640
                }
            ],
            "name": "My Shazam Tracks",
            "owner": {
                "display_name": "Rushab Shah",
                "external_urls": {
                    "spotify": "https://open.spotify.com/user/rushabshah32"
                },
                "href": "https://api.spotify.com/v1/users/rushabshah32",
                "id": "rushabshah32",
                "type": "user",
                "uri": "spotify:user:rushabshah32"
            },
            "primary_color": None,
            "public": True,
            "snapshot_id": "Miw1MTA0OTE5ZTNhOGIxZjhhZWY5NWM2YTdhODRmYzczZjkyZTYxZGM1",
            "tracks": {
                "href": "https://api.spotify.com/v1/playlists/3wxUTHoNAT60QsyXfCJRaG/tracks",
                "total": 1
            },
            "type": "playlist",
            "uri": "spotify:playlist:3wxUTHoNAT60QsyXfCJRaG"
        },
        {
            "collaborative": False,
            "description": "",
            "external_urls": {
                "spotify": "https://open.spotify.com/playlist/03m0iBzmmSFmoEuKcQLDZz"
            },
            "href": "https://api.spotify.com/v1/playlists/03m0iBzmmSFmoEuKcQLDZz",
            "id": "03m0iBzmmSFmoEuKcQLDZz",
            "images": [
                {
                    "height": 640,
                    "url": "https://mosaic.scdn.co/640"
                           "/ab67616d0000b27338d5b2e2c465d4743acc7b37ab67616d0000b27339522c242d7f10c0b8"
                           "0eb9b9ab67616d0000b273be43a3cafaca1c258ec23730ab67616d0000b273c6e4471284adb80e9dd45f8f",
                    "width": 640
                },
                {
                    "height": 300,
                    "url": "https://mosaic.scdn.co/300/ab67616d0000b27338d5b2e2c465d4743acc7b37ab67616d0000b27339522c242d7f10c0b80eb9b9ab67616d0000b273be43a3cafaca1c258ec23730ab67616d0000b273c6e4471284adb80e9dd45f8f",
                    "width": 300
                },
                {
                    "height": 60,
                    "url": "https://mosaic.scdn.co/60/ab67616d0000b27338d5b2e2c465d4743acc7b37ab67616d0000b27339522c242d7f10c0b80eb9b9ab67616d0000b273be43a3cafaca1c258ec23730ab67616d0000b273c6e4471284adb80e9dd45f8f",
                    "width": 60
                }
            ],
            "name": "Post Rock",
            "owner": {
                "display_name": "Rushab Shah",
                "external_urls": {
                    "spotify": "https://open.spotify.com/user/rushabshah32"
                },
                "href": "https://api.spotify.com/v1/users/rushabshah32",
                "id": "rushabshah32",
                "type": "user",
                "uri": "spotify:user:rushabshah32"
            },
            "primary_color": None,
            "public": True,
            "snapshot_id": "MTEsZGE1ZTA4YzIwMTFmNjM0NWQyZTNlNDkyNTAxODQ4MzNkZDFhYmIwNw==",
            "tracks": {
                "href": "https://api.spotify.com/v1/playlists/03m0iBzmmSFmoEuKcQLDZz/tracks",
                "total": 8
            },
            "type": "playlist",
            "uri": "spotify:playlist:03m0iBzmmSFmoEuKcQLDZz"
        },
        {
            "collaborative": False,
            "description": "I ain&#x27;t no doctor but if I could fix others&#x27; hearts I&#x27;d make them listen to this without changing the order of the tracks :)",
            "external_urls": {
                "spotify": "https://open.spotify.com/playlist/18n6rIA0rAkk20PQdgcA6j"
            },
            "href": "https://api.spotify.com/v1/playlists/18n6rIA0rAkk20PQdgcA6j",
            "id": "18n6rIA0rAkk20PQdgcA6j",
            "images": [
                {
                    "height": 640,
                    "url": "https://mosaic.scdn.co/640/ab67616d0000b2734ae1c4c5c45aabe565499163ab67616d0000b2736b3fa88bdd4af566fbbf2bbfab67616d0000b273b1f8da74f225fa1225cdfaceab67616d0000b273fc5f23d71de7ad824565f94c",
                    "width": 640
                },
                {
                    "height": 300,
                    "url": "https://mosaic.scdn.co/300/ab67616d0000b2734ae1c4c5c45aabe565499163ab67616d0000b2736b3fa88bdd4af566fbbf2bbfab67616d0000b273b1f8da74f225fa1225cdfaceab67616d0000b273fc5f23d71de7ad824565f94c",
                    "width": 300
                },
                {
                    "height": 60,
                    "url": "https://mosaic.scdn.co/60/ab67616d0000b2734ae1c4c5c45aabe565499163ab67616d0000b2736b3fa88bdd4af566fbbf2bbfab67616d0000b273b1f8da74f225fa1225cdfaceab67616d0000b273fc5f23d71de7ad824565f94c",
                    "width": 60
                }
            ],
            "name": "Arctic Monkeys being a cardiologist",
            "owner": {
                "display_name": "Rushab Shah",
                "external_urls": {
                    "spotify": "https://open.spotify.com/user/rushabshah32"
                },
                "href": "https://api.spotify.com/v1/users/rushabshah32",
                "id": "rushabshah32",
                "type": "user",
                "uri": "spotify:user:rushabshah32"
            },
            "primary_color": None,
            "public": True,
            "snapshot_id": "MzYsZjgwZTJiMDBjOWZkODk2MGE3MTYyMzkxNGZiNDFhZjRmNzE4MWFiNA==",
            "tracks": {
                "href": "https://api.spotify.com/v1/playlists/18n6rIA0rAkk20PQdgcA6j/tracks",
                "total": 22
            },
            "type": "playlist",
            "uri": "spotify:playlist:18n6rIA0rAkk20PQdgcA6j"
        },
        {
            "collaborative": False,
            "description": "Fantasy land for the virgins",
            "external_urls": {
                "spotify": "https://open.spotify.com/playlist/62V0MssVsUYGcmWp75D833"
            },
            "href": "https://api.spotify.com/v1/playlists/62V0MssVsUYGcmWp75D833",
            "id": "62V0MssVsUYGcmWp75D833",
            "images": [
                {
                    "height": 640,
                    "url": "https://mosaic.scdn.co/640/ab67616d0000b2734ae1c4c5c45aabe565499163ab67616d0000b273b1f8da74f225fa1225cdfaceab67616d0000b273f65d720a5d70dbb93e96d528ab67616d0000b273f7017fd086b1f27d90993175",
                    "width": 640
                },
                {
                    "height": 300,
                    "url": "https://mosaic.scdn.co/300/ab67616d0000b2734ae1c4c5c45aabe565499163ab67616d0000b273b1f8da74f225fa1225cdfaceab67616d0000b273f65d720a5d70dbb93e96d528ab67616d0000b273f7017fd086b1f27d90993175",
                    "width": 300
                },
                {
                    "height": 60,
                    "url": "https://mosaic.scdn.co/60/ab67616d0000b2734ae1c4c5c45aabe565499163ab67616d0000b273b1f8da74f225fa1225cdfaceab67616d0000b273f65d720a5d70dbb93e96d528ab67616d0000b273f7017fd086b1f27d90993175",
                    "width": 60
                }
            ],
            "name": "Hot stuff",
            "owner": {
                "display_name": "Rushab Shah",
                "external_urls": {
                    "spotify": "https://open.spotify.com/user/rushabshah32"
                },
                "href": "https://api.spotify.com/v1/users/rushabshah32",
                "id": "rushabshah32",
                "type": "user",
                "uri": "spotify:user:rushabshah32"
            },
            "primary_color": None,
            "public": True,
            "snapshot_id": "MjYsZGY5ZWQzZjRhZDlkYmZmMzY4YjRmZjQ5MzBhMDYxZWExYzQxMTk5Nw==",
            "tracks": {
                "href": "https://api.spotify.com/v1/playlists/62V0MssVsUYGcmWp75D833/tracks",
                "total": 24
            },
            "type": "playlist",
            "uri": "spotify:playlist:62V0MssVsUYGcmWp75D833"
        },
        {
            "collaborative": False,
            "description": "",
            "external_urls": {
                "spotify": "https://open.spotify.com/playlist/0K8Z3rRTTON1V348WDQz8Z"
            },
            "href": "https://api.spotify.com/v1/playlists/0K8Z3rRTTON1V348WDQz8Z",
            "id": "0K8Z3rRTTON1V348WDQz8Z",
            "images": [
                {
                    "height": 640,
                    "url": "https://mosaic.scdn.co/640/ab67616d0000b2732c30fdeffd0d99638a98416dab67616d0000b2733395f3e809dfbc2b1101d464ab67616d0000b2734fe83775017dd8af28079187ab67616d0000b273ee0d0dce888c6c8a70db6e8b",
                    "width": 640
                },
                {
                    "height": 300,
                    "url": "https://mosaic.scdn.co/300/ab67616d0000b2732c30fdeffd0d99638a98416dab67616d0000b2733395f3e809dfbc2b1101d464ab67616d0000b2734fe83775017dd8af28079187ab67616d0000b273ee0d0dce888c6c8a70db6e8b",
                    "width": 300
                },
                {
                    "height": 60,
                    "url": "https://mosaic.scdn.co/60/ab67616d0000b2732c30fdeffd0d99638a98416dab67616d0000b2733395f3e809dfbc2b1101d464ab67616d0000b2734fe83775017dd8af28079187ab67616d0000b273ee0d0dce888c6c8a70db6e8b",
                    "width": 60
                }
            ],
            "name": "Something different",
            "owner": {
                "display_name": "Rushab Shah",
                "external_urls": {
                    "spotify": "https://open.spotify.com/user/rushabshah32"
                },
                "href": "https://api.spotify.com/v1/users/rushabshah32",
                "id": "rushabshah32",
                "type": "user",
                "uri": "spotify:user:rushabshah32"
            },
            "primary_color": None,
            "public": True,
            "snapshot_id": "MjEsNzQ5Y2RkNTA2OWM2MDhlNzJhNTA5YTg2MDU1MmI3NmYwZTFlNDJiNg==",
            "tracks": {
                "href": "https://api.spotify.com/v1/playlists/0K8Z3rRTTON1V348WDQz8Z/tracks",
                "total": 18
            },
            "type": "playlist",
            "uri": "spotify:playlist:0K8Z3rRTTON1V348WDQz8Z"
        },
        {
            "collaborative": False,
            "description": "",
            "external_urls": {
                "spotify": "https://open.spotify.com/playlist/6ro7JwspABtrlTErGYO53a"
            },
            "href": "https://api.spotify.com/v1/playlists/6ro7JwspABtrlTErGYO53a",
            "id": "6ro7JwspABtrlTErGYO53a",
            "images": [
                {
                    "height": 640,
                    "url": "https://mosaic.scdn.co/640/ab67616d0000b27314d5029214f9f8e0ce2a9e3bab67616d0000b2733e653df72e6eb1ccb89576b3ab67616d0000b273cd3b5853d5cc9f9fdbaa7640ab67616d0000b273d9126888f214ca8521d83d2a",
                    "width": 640
                },
                {
                    "height": 300,
                    "url": "https://mosaic.scdn.co/300/ab67616d0000b27314d5029214f9f8e0ce2a9e3bab67616d0000b2733e653df72e6eb1ccb89576b3ab67616d0000b273cd3b5853d5cc9f9fdbaa7640ab67616d0000b273d9126888f214ca8521d83d2a",
                    "width": 300
                },
                {
                    "height": 60,
                    "url": "https://mosaic.scdn.co/60/ab67616d0000b27314d5029214f9f8e0ce2a9e3bab67616d0000b2733e653df72e6eb1ccb89576b3ab67616d0000b273cd3b5853d5cc9f9fdbaa7640ab67616d0000b273d9126888f214ca8521d83d2a",
                    "width": 60
                }
            ],
            "name": "Modern Instrumentals",
            "owner": {
                "display_name": "Rushab Shah",
                "external_urls": {
                    "spotify": "https://open.spotify.com/user/rushabshah32"
                },
                "href": "https://api.spotify.com/v1/users/rushabshah32",
                "id": "rushabshah32",
                "type": "user",
                "uri": "spotify:user:rushabshah32"
            },
            "primary_color": None,
            "public": True,
            "snapshot_id": "OCwyZmRiYjliZmQwYmZkZjI5YTE5OTJkMDMyOTg4ZDYyMjEyY2IzNWEw",
            "tracks": {
                "href": "https://api.spotify.com/v1/playlists/6ro7JwspABtrlTErGYO53a/tracks",
                "total": 14
            },
            "type": "playlist",
            "uri": "spotify:playlist:6ro7JwspABtrlTErGYO53a"
        },
        {
            "collaborative": False,
            "description": "Why aren&#x27;t you swimming ?",
            "external_urls": {
                "spotify": "https://open.spotify.com/playlist/1MyrUZxvtixPsblkXjDioP"
            },
            "href": "https://api.spotify.com/v1/playlists/1MyrUZxvtixPsblkXjDioP",
            "id": "1MyrUZxvtixPsblkXjDioP",
            "images": [
                {
                    "height": 640,
                    "url": "https://mosaic.scdn.co/640/ab67616d0000b27333e96c0ff58f371cf75cb16eab67616d0000b27386734c2b36be7adcaa4ab1f0ab67616d0000b273bcda9701e49a3e3a13abbaeeab67616d0000b273cdfe41cd475f8ad3a29b3537",
                    "width": 640
                },
                {
                    "height": 300,
                    "url": "https://mosaic.scdn.co/300/ab67616d0000b27333e96c0ff58f371cf75cb16eab67616d0000b27386734c2b36be7adcaa4ab1f0ab67616d0000b273bcda9701e49a3e3a13abbaeeab67616d0000b273cdfe41cd475f8ad3a29b3537",
                    "width": 300
                },
                {
                    "height": 60,
                    "url": "https://mosaic.scdn.co/60/ab67616d0000b27333e96c0ff58f371cf75cb16eab67616d0000b27386734c2b36be7adcaa4ab1f0ab67616d0000b273bcda9701e49a3e3a13abbaeeab67616d0000b273cdfe41cd475f8ad3a29b3537",
                    "width": 60
                }
            ],
            "name": "Calm Waters",
            "owner": {
                "display_name": "Rushab Shah",
                "external_urls": {
                    "spotify": "https://open.spotify.com/user/rushabshah32"
                },
                "href": "https://api.spotify.com/v1/users/rushabshah32",
                "id": "rushabshah32",
                "type": "user",
                "uri": "spotify:user:rushabshah32"
            },
            "primary_color": None,
            "public": True,
            "snapshot_id": "NDUsNzg2ZDI5NGE5YzhmNmY3NDAxZTcxNzg5M2NhOTcyMzFiMTM3YjBiNQ==",
            "tracks": {
                "href": "https://api.spotify.com/v1/playlists/1MyrUZxvtixPsblkXjDioP/tracks",
                "total": 46
            },
            "type": "playlist",
            "uri": "spotify:playlist:1MyrUZxvtixPsblkXjDioP"
        },
        {
            "collaborative": False,
            "description": "go away pls",
            "external_urls": {
                "spotify": "https://open.spotify.com/playlist/6MMOZBrYL07sfaPdVnQ38c"
            },
            "href": "https://api.spotify.com/v1/playlists/6MMOZBrYL07sfaPdVnQ38c",
            "id": "6MMOZBrYL07sfaPdVnQ38c",
            "images": [
                {
                    "height": 640,
                    "url": "https://mosaic.scdn.co/640/ab67616d0000b2736c112ab47442b526755ffe36ab67616d0000b2737bf1b91bc05ea3b837e8eb94ab67616d0000b273bf33fdea7b0ff3c71b6faf75ab67616d0000b273e9b6f26ff354f4d70847f02d",
                    "width": 640
                },
                {
                    "height": 300,
                    "url": "https://mosaic.scdn.co/300/ab67616d0000b2736c112ab47442b526755ffe36ab67616d0000b2737bf1b91bc05ea3b837e8eb94ab67616d0000b273bf33fdea7b0ff3c71b6faf75ab67616d0000b273e9b6f26ff354f4d70847f02d",
                    "width": 300
                },
                {
                    "height": 60,
                    "url": "https://mosaic.scdn.co/60/ab67616d0000b2736c112ab47442b526755ffe36ab67616d0000b2737bf1b91bc05ea3b837e8eb94ab67616d0000b273bf33fdea7b0ff3c71b6faf75ab67616d0000b273e9b6f26ff354f4d70847f02d",
                    "width": 60
                }
            ],
            "name": "Rockless Bottom",
            "owner": {
                "display_name": "Rushab Shah",
                "external_urls": {
                    "spotify": "https://open.spotify.com/user/rushabshah32"
                },
                "href": "https://api.spotify.com/v1/users/rushabshah32",
                "id": "rushabshah32",
                "type": "user",
                "uri": "spotify:user:rushabshah32"
            },
            "primary_color": None,
            "public": True,
            "snapshot_id": "NTgsZDIzYWI4MTgwMzc1NWU4MmM3MDg5YzA0ZTZiMzA0YzNiOWE4MjVlNQ==",
            "tracks": {
                "href": "https://api.spotify.com/v1/playlists/6MMOZBrYL07sfaPdVnQ38c/tracks",
                "total": 58
            },
            "type": "playlist",
            "uri": "spotify:playlist:6MMOZBrYL07sfaPdVnQ38c"
        },
        {
            "collaborative": False,
            "description": "A playlist to overpower all the noise in your head",
            "external_urls": {
                "spotify": "https://open.spotify.com/playlist/1LinCArgs5903itZ6IEsp2"
            },
            "href": "https://api.spotify.com/v1/playlists/1LinCArgs5903itZ6IEsp2",
            "id": "1LinCArgs5903itZ6IEsp2",
            "images": [
                {
                    "height": 640,
                    "url": "https://mosaic.scdn.co/640/ab67616d0000b2735721adac031512b903f10d03ab67616d0000b27360cf7c8dd93815ccd6cb4830ab67616d0000b273bb85bcab29cd1c193c46afb1ab67616d0000b273bc7ddb77993dd1d8d19c22a2",
                    "width": 640
                },
                {
                    "height": 300,
                    "url": "https://mosaic.scdn.co/300/ab67616d0000b2735721adac031512b903f10d03ab67616d0000b27360cf7c8dd93815ccd6cb4830ab67616d0000b273bb85bcab29cd1c193c46afb1ab67616d0000b273bc7ddb77993dd1d8d19c22a2",
                    "width": 300
                },
                {
                    "height": 60,
                    "url": "https://mosaic.scdn.co/60/ab67616d0000b2735721adac031512b903f10d03ab67616d0000b27360cf7c8dd93815ccd6cb4830ab67616d0000b273bb85bcab29cd1c193c46afb1ab67616d0000b273bc7ddb77993dd1d8d19c22a2",
                    "width": 60
                }
            ],
            "name": "White Rock Noise",
            "owner": {
                "display_name": "Rushab Shah",
                "external_urls": {
                    "spotify": "https://open.spotify.com/user/rushabshah32"
                },
                "href": "https://api.spotify.com/v1/users/rushabshah32",
                "id": "rushabshah32",
                "type": "user",
                "uri": "spotify:user:rushabshah32"
            },
            "primary_color": None,
            "public": True,
            "snapshot_id": "MTY2LGY3MTBhM2EzYTM2ZDVlYTFhMzJiOGU1NWVmMjA2Y2RkYjBjMDU0M2U=",
            "tracks": {
                "href": "https://api.spotify.com/v1/playlists/1LinCArgs5903itZ6IEsp2/tracks",
                "total": 307
            },
            "type": "playlist",
            "uri": "spotify:playlist:1LinCArgs5903itZ6IEsp2"
        },
        {
            "collaborative": False,
            "description": "",
            "external_urls": {
                "spotify": "https://open.spotify.com/playlist/2hEP8skwpqslLEVQ2E1H6f"
            },
            "href": "https://api.spotify.com/v1/playlists/2hEP8skwpqslLEVQ2E1H6f",
            "id": "2hEP8skwpqslLEVQ2E1H6f",
            "images": [
                {
                    "height": 640,
                    "url": "https://mosaic.scdn.co/640/ab67616d0000b27339864a5777bfcb8b451db79fab67616d0000b273595274875c0a7650e2c5bb4dab67616d0000b27360cf7c8dd93815ccd6cb4830ab67616d0000b273736145b97bab8fa92cb6113f",
                    "width": 640
                },
                {
                    "height": 300,
                    "url": "https://mosaic.scdn.co/300/ab67616d0000b27339864a5777bfcb8b451db79fab67616d0000b273595274875c0a7650e2c5bb4dab67616d0000b27360cf7c8dd93815ccd6cb4830ab67616d0000b273736145b97bab8fa92cb6113f",
                    "width": 300
                },
                {
                    "height": 60,
                    "url": "https://mosaic.scdn.co/60/ab67616d0000b27339864a5777bfcb8b451db79fab67616d0000b273595274875c0a7650e2c5bb4dab67616d0000b27360cf7c8dd93815ccd6cb4830ab67616d0000b273736145b97bab8fa92cb6113f",
                    "width": 60
                }
            ],
            "name": "Anguish!",
            "owner": {
                "display_name": "Rushab Shah",
                "external_urls": {
                    "spotify": "https://open.spotify.com/user/rushabshah32"
                },
                "href": "https://api.spotify.com/v1/users/rushabshah32",
                "id": "rushabshah32",
                "type": "user",
                "uri": "spotify:user:rushabshah32"
            },
            "primary_color": None,
            "public": True,
            "snapshot_id": "MjEsOTRkNGEwYmQ2OTJlNmEyNDU1M2U3NTM5MmRlNTA5YTUyNDRlNGFhYQ==",
            "tracks": {
                "href": "https://api.spotify.com/v1/playlists/2hEP8skwpqslLEVQ2E1H6f/tracks",
                "total": 44
            },
            "type": "playlist",
            "uri": "spotify:playlist:2hEP8skwpqslLEVQ2E1H6f"
        },
        {
            "collaborative": False,
            "description": "",
            "external_urls": {
                "spotify": "https://open.spotify.com/playlist/2fr0uT8blZ4YujtYCz8WdO"
            },
            "href": "https://api.spotify.com/v1/playlists/2fr0uT8blZ4YujtYCz8WdO",
            "id": "2fr0uT8blZ4YujtYCz8WdO",
            "images": [
                {
                    "height": 640,
                    "url": "https://mosaic.scdn.co/640/ab67616d0000b2739dfee5404d5e0763998c958eab67616d0000b273c8a11e48c91a982d086afc69ab67616d0000b273d55ec7fcfacd95e73877b787ab67616d0000b273e44963b8bb127552ac761873",
                    "width": 640
                },
                {
                    "height": 300,
                    "url": "https://mosaic.scdn.co/300/ab67616d0000b2739dfee5404d5e0763998c958eab67616d0000b273c8a11e48c91a982d086afc69ab67616d0000b273d55ec7fcfacd95e73877b787ab67616d0000b273e44963b8bb127552ac761873",
                    "width": 300
                },
                {
                    "height": 60,
                    "url": "https://mosaic.scdn.co/60/ab67616d0000b2739dfee5404d5e0763998c958eab67616d0000b273c8a11e48c91a982d086afc69ab67616d0000b273d55ec7fcfacd95e73877b787ab67616d0000b273e44963b8bb127552ac761873",
                    "width": 60
                }
            ],
            "name": "Old is gold",
            "owner": {
                "display_name": "Rushab Shah",
                "external_urls": {
                    "spotify": "https://open.spotify.com/user/rushabshah32"
                },
                "href": "https://api.spotify.com/v1/users/rushabshah32",
                "id": "rushabshah32",
                "type": "user",
                "uri": "spotify:user:rushabshah32"
            },
            "primary_color": None,
            "public": True,
            "snapshot_id": "NTAsOTk5MDg0NDc5OTM1Y2ViZDk0ZGE3MGM5ZWQ2OTY2NGE1NDM0NGJlYw==",
            "tracks": {
                "href": "https://api.spotify.com/v1/playlists/2fr0uT8blZ4YujtYCz8WdO/tracks",
                "total": 46
            },
            "type": "playlist",
            "uri": "spotify:playlist:2fr0uT8blZ4YujtYCz8WdO"
        },
        {
            "collaborative": False,
            "description": "",
            "external_urls": {
                "spotify": "https://open.spotify.com/playlist/4Kb9y65b3bV1jwEGhADCC2"
            },
            "href": "https://api.spotify.com/v1/playlists/4Kb9y65b3bV1jwEGhADCC2",
            "id": "4Kb9y65b3bV1jwEGhADCC2",
            "images": [
                {
                    "height": 640,
                    "url": "https://mosaic.scdn.co/640/ab67616d0000b273206dcb32282da4c6a778d073ab67616d0000b2732363f794af17d154dc17bbb6ab67616d0000b27371abe464f5a4b276cb5a9ff7ab67616d0000b273877f4dbc82a9dfd850bb52c8",
                    "width": 640
                },
                {
                    "height": 300,
                    "url": "https://mosaic.scdn.co/300/ab67616d0000b273206dcb32282da4c6a778d073ab67616d0000b2732363f794af17d154dc17bbb6ab67616d0000b27371abe464f5a4b276cb5a9ff7ab67616d0000b273877f4dbc82a9dfd850bb52c8",
                    "width": 300
                },
                {
                    "height": 60,
                    "url": "https://mosaic.scdn.co/60/ab67616d0000b273206dcb32282da4c6a778d073ab67616d0000b2732363f794af17d154dc17bbb6ab67616d0000b27371abe464f5a4b276cb5a9ff7ab67616d0000b273877f4dbc82a9dfd850bb52c8",
                    "width": 60
                }
            ],
            "name": "Anime",
            "owner": {
                "display_name": "Rushab Shah",
                "external_urls": {
                    "spotify": "https://open.spotify.com/user/rushabshah32"
                },
                "href": "https://api.spotify.com/v1/users/rushabshah32",
                "id": "rushabshah32",
                "type": "user",
                "uri": "spotify:user:rushabshah32"
            },
            "primary_color": None,
            "public": True,
            "snapshot_id": "MjcsZDNiNjU0ZWY5MjA3OWU1NmYyMzNhMGQ5YWI1Y2QyMTViYzQ2ZmQ4NA==",
            "tracks": {
                "href": "https://api.spotify.com/v1/playlists/4Kb9y65b3bV1jwEGhADCC2/tracks",
                "total": 25
            },
            "type": "playlist",
            "uri": "spotify:playlist:4Kb9y65b3bV1jwEGhADCC2"
        }
    ],
    "limit": 50,
    "next": None,
    "offset": 0,
    "previous": None,
    "total": 12
}

# print(json.dumps(playlist_list, sort_keys=True,indent=4))

items = json_playlist['items']

# get list of all playlists
playlist_list = sp.current_user_playlists()
items = playlist_list['items']
playlist_ids = dict()
for item in items:
    playlist_ids[item['id']] = (item['name'], item['tracks']['total'])

# you get
# playlist_ids = {'3wxUTHoNAT60QsyXfCJRaG': 'My Shazam Tracks', '03m0iBzmmSFmoEuKcQLDZz': 'Post Rock', '18n6rIA0rAkk20PQdgcA6j': 'Arctic Monkeys being a cardiologist', '62V0MssVsUYGcmWp75D833': 'Hot stuff', '0K8Z3rRTTON1V348WDQz8Z': 'Something different', '6ro7JwspABtrlTErGYO53a': 'Modern Instrumentals', '1MyrUZxvtixPsblkXjDioP': 'Calm Waters', '6MMOZBrYL07sfaPdVnQ38c': 'Rockless Bottom', '1LinCArgs5903itZ6IEsp2': 'White Rock Noise', '2hEP8skwpqslLEVQ2E1H6f': 'Anguish!', '2fr0uT8blZ4YujtYCz8WdO': 'Old is gold', '4Kb9y65b3bV1jwEGhADCC2': 'Anime'}


# playlist_raw=sp.playlist_tracks(playlist_id=ID, fields='items.track.album.artists,items.track.album.name,items.track.artists,items.track.name,total',additional_types=['track'])
# you get
playlist_raw = {
    'items': [{'track': {'album': {'artists': [
        {'external_urls': {'spotify': 'https://open.spotify.com/artist/70BYFdaZbEKbeauJ670ysI'},
         'href': 'https://api.spotify.com/v1/artists/70BYFdaZbEKbeauJ670ysI', 'id': '70BYFdaZbEKbeauJ670ysI',
         'name': 'Shinedown', 'type': 'artist', 'uri': 'spotify:artist:70BYFdaZbEKbeauJ670ysI'}],
        'name': 'ATTENTION ATTENTION'}, 'artists': [
        {'external_urls': {'spotify': 'https://open.spotify.com/artist/70BYFdaZbEKbeauJ670ysI'},
         'href': 'https://api.spotify.com/v1/artists/70BYFdaZbEKbeauJ670ysI', 'id': '70BYFdaZbEKbeauJ670ysI',
         'name': 'Shinedown', 'type': 'artist', 'uri': 'spotify:artist:70BYFdaZbEKbeauJ670ysI'}], 'name': 'MONSTERS'}},
        {
            'track': {'album': {'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/4DWX7u8BV0vZIQSpJQQDWU'},
                'href': 'https://api.spotify.com/v1/artists/4DWX7u8BV0vZIQSpJQQDWU',
                'id': '4DWX7u8BV0vZIQSpJQQDWU', 'name': 'Alter Bridge',
                'type': 'artist',
                'uri': 'spotify:artist:4DWX7u8BV0vZIQSpJQQDWU'}],
                'name': 'One Day Remains'}, 'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/4DWX7u8BV0vZIQSpJQQDWU'},
                'href': 'https://api.spotify.com/v1/artists/4DWX7u8BV0vZIQSpJQQDWU',
                'id': '4DWX7u8BV0vZIQSpJQQDWU',
                'name': 'Alter Bridge',
                'type': 'artist',
                'uri': 'spotify:artist:4DWX7u8BV0vZIQSpJQQDWU'}],
                'name': 'Open Your Eyes'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
             'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF', 'id': '1Ffb6ejR6Fe5IamqA5oRUF',
             'name': 'Bring Me The Horizon', 'type': 'artist', 'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
            'name': 'Sempiternal (Deluxe Edition)'},
            'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
                'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF',
                'id': '1Ffb6ejR6Fe5IamqA5oRUF',
                'name': 'Bring Me The Horizon',
                'type': 'artist',
                'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
            'name': 'Hospital For Souls'}}, {
            'track': {'album': {'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
                'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF',
                'id': '1Ffb6ejR6Fe5IamqA5oRUF',
                'name': 'Bring Me The Horizon', 'type': 'artist',
                'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
                'name': 'Sempiternal (Deluxe Edition)'}, 'artists': [{
                'external_urls': {
                    'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
                'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF',
                'id': '1Ffb6ejR6Fe5IamqA5oRUF',
                'name': 'Bring Me The Horizon',
                'type': 'artist',
                'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
                'name': 'And The Snakes Start To Sing'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/6XyY86QOPPrYVGvF9ch6wz'},
             'href': 'https://api.spotify.com/v1/artists/6XyY86QOPPrYVGvF9ch6wz', 'id': '6XyY86QOPPrYVGvF9ch6wz',
             'name': 'Linkin Park', 'type': 'artist', 'uri': 'spotify:artist:6XyY86QOPPrYVGvF9ch6wz'}],
            'name': 'The Hunting Party'},
            'artists': [{
                'external_urls': {
                    'spotify': 'https://open.spotify.com/artist/6XyY86QOPPrYVGvF9ch6wz'},
                'href': 'https://api.spotify.com/v1/artists/6XyY86QOPPrYVGvF9ch6wz',
                'id': '6XyY86QOPPrYVGvF9ch6wz',
                'name': 'Linkin Park',
                'type': 'artist',
                'uri': 'spotify:artist:6XyY86QOPPrYVGvF9ch6wz'}],
            'name': 'Wastelands'}}, {
            'track': {'album': {'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
                'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF',
                'id': '1Ffb6ejR6Fe5IamqA5oRUF',
                'name': 'Bring Me The Horizon', 'type': 'artist',
                'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
                'name': 'Sempiternal (Deluxe Edition)'}, 'artists': [{
                'external_urls': {
                    'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
                'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF',
                'id': '1Ffb6ejR6Fe5IamqA5oRUF',
                'name': 'Bring Me The Horizon',
                'type': 'artist',
                'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
                'name': 'Deathbeds'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
             'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF', 'id': '1Ffb6ejR6Fe5IamqA5oRUF',
             'name': 'Bring Me The Horizon', 'type': 'artist', 'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
            'name': "That's The Spirit"},
            'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
                'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF',
                'id': '1Ffb6ejR6Fe5IamqA5oRUF',
                'name': 'Bring Me The Horizon',
                'type': 'artist',
                'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
            'name': 'Drown'}}, {'track': {'album': {
            'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/00YTqRClk82aMchQQpYMd5'},
                         'href': 'https://api.spotify.com/v1/artists/00YTqRClk82aMchQQpYMd5',
                         'id': '00YTqRClk82aMchQQpYMd5',
                         'name': 'Our Last Night', 'type': 'artist', 'uri': 'spotify:artist:00YTqRClk82aMchQQpYMd5'}],
            'name': '1-800-273-8255'}, 'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/00YTqRClk82aMchQQpYMd5'},
             'href': 'https://api.spotify.com/v1/artists/00YTqRClk82aMchQQpYMd5', 'id': '00YTqRClk82aMchQQpYMd5',
             'name': 'Our Last Night', 'type': 'artist', 'uri': 'spotify:artist:00YTqRClk82aMchQQpYMd5'}],
            'name': '1-800-273-8255'}},
        {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
             'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF',
             'id': '1Ffb6ejR6Fe5IamqA5oRUF', 'name': 'Bring Me The Horizon', 'type': 'artist',
             'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
            'name': 'Sempiternal (Deluxe Edition)'}, 'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
             'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF',
             'id': '1Ffb6ejR6Fe5IamqA5oRUF', 'name': 'Bring Me The Horizon', 'type': 'artist',
             'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}], 'name': 'Seen It All Before'}}, {
            'track': {'album': {'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/5BtHciL0e0zOP7prIHn3pP'},
                'href': 'https://api.spotify.com/v1/artists/5BtHciL0e0zOP7prIHn3pP',
                'id': '5BtHciL0e0zOP7prIHn3pP',
                'name': 'Breaking Benjamin', 'type': 'artist',
                'uri': 'spotify:artist:5BtHciL0e0zOP7prIHn3pP'}],
                'name': 'Dear Agony'}, 'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/5BtHciL0e0zOP7prIHn3pP'},
                'href': 'https://api.spotify.com/v1/artists/5BtHciL0e0zOP7prIHn3pP',
                'id': '5BtHciL0e0zOP7prIHn3pP',
                'name': 'Breaking Benjamin',
                'type': 'artist',
                'uri': 'spotify:artist:5BtHciL0e0zOP7prIHn3pP'}],
                'name': 'Dear Agony'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/00YTqRClk82aMchQQpYMd5'},
             'href': 'https://api.spotify.com/v1/artists/00YTqRClk82aMchQQpYMd5', 'id': '00YTqRClk82aMchQQpYMd5',
             'name': 'Our Last Night', 'type': 'artist', 'uri': 'spotify:artist:00YTqRClk82aMchQQpYMd5'}],
            'name': 'Oak Island'}, 'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/00YTqRClk82aMchQQpYMd5'},
             'href': 'https://api.spotify.com/v1/artists/00YTqRClk82aMchQQpYMd5', 'id': '00YTqRClk82aMchQQpYMd5',
             'name': 'Our Last Night', 'type': 'artist', 'uri': 'spotify:artist:00YTqRClk82aMchQQpYMd5'}],
            'name': 'Sunrise'}}, {'track': {'album': {
            'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/58lV9VcRSjABbAbfWS6skp'},
                         'href': 'https://api.spotify.com/v1/artists/58lV9VcRSjABbAbfWS6skp',
                         'id': '58lV9VcRSjABbAbfWS6skp', 'name': 'Bon Jovi', 'type': 'artist',
                         'uri': 'spotify:artist:58lV9VcRSjABbAbfWS6skp'}], 'name': 'Cross Road'}, 'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/58lV9VcRSjABbAbfWS6skp'},
             'href': 'https://api.spotify.com/v1/artists/58lV9VcRSjABbAbfWS6skp', 'id': '58lV9VcRSjABbAbfWS6skp',
             'name': 'Bon Jovi', 'type': 'artist', 'uri': 'spotify:artist:58lV9VcRSjABbAbfWS6skp'}], 'name': 'Always'}},
        {
            'track': {'album': {'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/7FBcuc1gsnv6Y1nwFtNRCb'},
                'href': 'https://api.spotify.com/v1/artists/7FBcuc1gsnv6Y1nwFtNRCb',
                'id': '7FBcuc1gsnv6Y1nwFtNRCb',
                'name': 'My Chemical Romance', 'type': 'artist',
                'uri': 'spotify:artist:7FBcuc1gsnv6Y1nwFtNRCb'}],
                'name': 'Number Three'}, 'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/7FBcuc1gsnv6Y1nwFtNRCb'},
                'href': 'https://api.spotify.com/v1/artists/7FBcuc1gsnv6Y1nwFtNRCb',
                'id': '7FBcuc1gsnv6Y1nwFtNRCb',
                'name': 'My Chemical Romance',
                'type': 'artist',
                'uri': 'spotify:artist:7FBcuc1gsnv6Y1nwFtNRCb'}],
                'name': 'The Light Behind Your Eyes'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/05fG473iIaoy82BF1aGhL8'},
             'href': 'https://api.spotify.com/v1/artists/05fG473iIaoy82BF1aGhL8', 'id': '05fG473iIaoy82BF1aGhL8',
             'name': 'Slipknot', 'type': 'artist', 'uri': 'spotify:artist:05fG473iIaoy82BF1aGhL8'}],
            'name': 'All Hope Is Gone'},
            'artists': [{
                'external_urls': {
                    'spotify': 'https://open.spotify.com/artist/05fG473iIaoy82BF1aGhL8'},
                'href': 'https://api.spotify.com/v1/artists/05fG473iIaoy82BF1aGhL8',
                'id': '05fG473iIaoy82BF1aGhL8',
                'name': 'Slipknot',
                'type': 'artist',
                'uri': 'spotify:artist:05fG473iIaoy82BF1aGhL8'}],
            'name': 'Snuff'}}, {
            'track': {'album': {'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
                'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF',
                'id': '1Ffb6ejR6Fe5IamqA5oRUF',
                'name': 'Bring Me The Horizon', 'type': 'artist',
                'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}, {
                'external_urls': {
                    'spotify': 'https://open.spotify.com/artist/4rojTfP5nRkmYpdSbWQgV4'},
                'href': 'https://api.spotify.com/v1/artists/4rojTfP5nRkmYpdSbWQgV4',
                'id': '4rojTfP5nRkmYpdSbWQgV4',
                'name': 'Death Stranding: Timefall', 'type': 'artist',
                'uri': 'spotify:artist:4rojTfP5nRkmYpdSbWQgV4'}],
                'name': 'Ludens'}, 'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
                'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF',
                'id': '1Ffb6ejR6Fe5IamqA5oRUF',
                'name': 'Bring Me The Horizon',
                'type': 'artist',
                'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'},
                {'external_urls': {
                    'spotify': 'https://open.spotify.com/artist/4rojTfP5nRkmYpdSbWQgV4'},
                    'href': 'https://api.spotify.com/v1/artists/4rojTfP5nRkmYpdSbWQgV4',
                    'id': '4rojTfP5nRkmYpdSbWQgV4',
                    'name': 'Death Stranding: Timefall',
                    'type': 'artist',
                    'uri': 'spotify:artist:4rojTfP5nRkmYpdSbWQgV4'}],
                'name': 'Ludens'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
             'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF', 'id': '1Ffb6ejR6Fe5IamqA5oRUF',
             'name': 'Bring Me The Horizon', 'type': 'artist', 'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
            'name': "That's The Spirit"},
            'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
                'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF',
                'id': '1Ffb6ejR6Fe5IamqA5oRUF',
                'name': 'Bring Me The Horizon',
                'type': 'artist',
                'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
            'name': 'True Friends'}}, {'track': {'album': {
            'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
                         'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF',
                         'id': '1Ffb6ejR6Fe5IamqA5oRUF', 'name': 'Bring Me The Horizon', 'type': 'artist',
                         'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}], 'name': "That's The Spirit"}, 'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
             'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF', 'id': '1Ffb6ejR6Fe5IamqA5oRUF',
             'name': 'Bring Me The Horizon', 'type': 'artist', 'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
            'name': 'Happy Song'}},
        {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
             'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF',
             'id': '1Ffb6ejR6Fe5IamqA5oRUF', 'name': 'Bring Me The Horizon', 'type': 'artist',
             'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
            'name': 'wonderful life (feat. Dani Filth)'}, 'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
             'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF',
             'id': '1Ffb6ejR6Fe5IamqA5oRUF', 'name': 'Bring Me The Horizon', 'type': 'artist',
             'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'},
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/76qhZXwfMnhJPXacLwGcNK'},
             'href': 'https://api.spotify.com/v1/artists/76qhZXwfMnhJPXacLwGcNK',
             'id': '76qhZXwfMnhJPXacLwGcNK', 'name': 'Dani Filth', 'type': 'artist',
             'uri': 'spotify:artist:76qhZXwfMnhJPXacLwGcNK'}],
            'name': 'wonderful life (feat. Dani Filth)'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
             'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF', 'id': '1Ffb6ejR6Fe5IamqA5oRUF',
             'name': 'Bring Me The Horizon', 'type': 'artist', 'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
            'name': 'Sempiternal (Expanded Edition)'},
            'artists': [{
                'external_urls': {
                    'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
                'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF',
                'id': '1Ffb6ejR6Fe5IamqA5oRUF',
                'name': 'Bring Me The Horizon',
                'type': 'artist',
                'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
            'name': "Go to Hell, for Heaven's Sake"}},
        {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
             'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF',
             'id': '1Ffb6ejR6Fe5IamqA5oRUF', 'name': 'Bring Me The Horizon', 'type': 'artist',
             'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}], 'name': "That's The Spirit"},
            'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
                'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF',
                'id': '1Ffb6ejR6Fe5IamqA5oRUF', 'name': 'Bring Me The Horizon',
                'type': 'artist', 'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
            'name': 'Blasphemy'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
             'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF', 'id': '1Ffb6ejR6Fe5IamqA5oRUF',
             'name': 'Bring Me The Horizon', 'type': 'artist', 'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
            'name': 'amo'}, 'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
             'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF', 'id': '1Ffb6ejR6Fe5IamqA5oRUF',
             'name': 'Bring Me The Horizon', 'type': 'artist', 'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'},
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/6vunRaBya0Sx6CMJZAlHTZ'},
             'href': 'https://api.spotify.com/v1/artists/6vunRaBya0Sx6CMJZAlHTZ', 'id': '6vunRaBya0Sx6CMJZAlHTZ',
             'name': 'Rahzel', 'type': 'artist', 'uri': 'spotify:artist:6vunRaBya0Sx6CMJZAlHTZ'}],
            'name': 'heavy metal (feat. Rahzel)'}}, {
            'track': {'album': {'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
                'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF',
                'id': '1Ffb6ejR6Fe5IamqA5oRUF',
                'name': 'Bring Me The Horizon', 'type': 'artist',
                'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
                'name': "That's The Spirit"}, 'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
                'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF',
                'id': '1Ffb6ejR6Fe5IamqA5oRUF',
                'name': 'Bring Me The Horizon',
                'type': 'artist',
                'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
                'name': 'Run'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
             'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF', 'id': '1Ffb6ejR6Fe5IamqA5oRUF',
             'name': 'Bring Me The Horizon', 'type': 'artist', 'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
            'name': 'Sempiternal (Expanded Edition)'},
            'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
                'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF',
                'id': '1Ffb6ejR6Fe5IamqA5oRUF',
                'name': 'Bring Me The Horizon',
                'type': 'artist',
                'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
            'name': 'Can You Feel My Heart'}}, {'track': {
            'album': {
                'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
                             'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF',
                             'id': '1Ffb6ejR6Fe5IamqA5oRUF', 'name': 'Bring Me The Horizon', 'type': 'artist',
                             'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
                'name': 'Sempiternal (Expanded Edition)'}, 'artists': [
                {'external_urls': {'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
                 'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF', 'id': '1Ffb6ejR6Fe5IamqA5oRUF',
                 'name': 'Bring Me The Horizon', 'type': 'artist', 'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
            'name': 'Sleepwalking'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/4YZ5ECfbM2xSTSQTJGBbO5'},
             'href': 'https://api.spotify.com/v1/artists/4YZ5ECfbM2xSTSQTJGBbO5', 'id': '4YZ5ECfbM2xSTSQTJGBbO5',
             'name': 'Gerard Way', 'type': 'artist', 'uri': 'spotify:artist:4YZ5ECfbM2xSTSQTJGBbO5'}],
            'name': 'Hazy Shade of Winter (feat. Ray Toro)'}, 'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/4YZ5ECfbM2xSTSQTJGBbO5'},
             'href': 'https://api.spotify.com/v1/artists/4YZ5ECfbM2xSTSQTJGBbO5', 'id': '4YZ5ECfbM2xSTSQTJGBbO5',
             'name': 'Gerard Way', 'type': 'artist', 'uri': 'spotify:artist:4YZ5ECfbM2xSTSQTJGBbO5'},
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/7vtO3glDQwyFDY5cTymz4E'},
             'href': 'https://api.spotify.com/v1/artists/7vtO3glDQwyFDY5cTymz4E', 'id': '7vtO3glDQwyFDY5cTymz4E',
             'name': 'Ray Toro', 'type': 'artist', 'uri': 'spotify:artist:7vtO3glDQwyFDY5cTymz4E'}],
            'name': 'Hazy Shade of Winter (feat. Ray Toro)'}}, {'track': {'album': {
            'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/0RqtSIYZmd4fiBKVFqyIqD'},
                         'href': 'https://api.spotify.com/v1/artists/0RqtSIYZmd4fiBKVFqyIqD',
                         'id': '0RqtSIYZmd4fiBKVFqyIqD', 'name': 'Thirty Seconds To Mars', 'type': 'artist',
                         'uri': 'spotify:artist:0RqtSIYZmd4fiBKVFqyIqD'}], 'name': 'A Beautiful Lie'}, 'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/0RqtSIYZmd4fiBKVFqyIqD'},
             'href': 'https://api.spotify.com/v1/artists/0RqtSIYZmd4fiBKVFqyIqD', 'id': '0RqtSIYZmd4fiBKVFqyIqD',
             'name': 'Thirty Seconds To Mars', 'type': 'artist', 'uri': 'spotify:artist:0RqtSIYZmd4fiBKVFqyIqD'}],
            'name': 'The Kill'}},
        {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/2xiIXseIJcq3nG7C8fHeBj'},
             'href': 'https://api.spotify.com/v1/artists/2xiIXseIJcq3nG7C8fHeBj',
             'id': '2xiIXseIJcq3nG7C8fHeBj', 'name': 'Three Days Grace', 'type': 'artist',
             'uri': 'spotify:artist:2xiIXseIJcq3nG7C8fHeBj'}], 'name': 'One-X'}, 'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/2xiIXseIJcq3nG7C8fHeBj'},
             'href': 'https://api.spotify.com/v1/artists/2xiIXseIJcq3nG7C8fHeBj',
             'id': '2xiIXseIJcq3nG7C8fHeBj', 'name': 'Three Days Grace', 'type': 'artist',
             'uri': 'spotify:artist:2xiIXseIJcq3nG7C8fHeBj'}], 'name': 'Never Too Late'}}, {'track': {
            'album': {
                'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/6B5c4sch27tWHAGdarpPaW'},
                             'href': 'https://api.spotify.com/v1/artists/6B5c4sch27tWHAGdarpPaW',
                             'id': '6B5c4sch27tWHAGdarpPaW', 'name': 'Seether', 'type': 'artist',
                             'uri': 'spotify:artist:6B5c4sch27tWHAGdarpPaW'}],
                'name': 'Finding Beauty In Negative Spaces (Bonus Track Version)'}, 'artists': [
                {'external_urls': {'spotify': 'https://open.spotify.com/artist/6B5c4sch27tWHAGdarpPaW'},
                 'href': 'https://api.spotify.com/v1/artists/6B5c4sch27tWHAGdarpPaW', 'id': '6B5c4sch27tWHAGdarpPaW',
                 'name': 'Seether', 'type': 'artist', 'uri': 'spotify:artist:6B5c4sch27tWHAGdarpPaW'}],
            'name': 'Fake It'}},
        {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/6B5c4sch27tWHAGdarpPaW'},
             'href': 'https://api.spotify.com/v1/artists/6B5c4sch27tWHAGdarpPaW',
             'id': '6B5c4sch27tWHAGdarpPaW', 'name': 'Seether', 'type': 'artist',
             'uri': 'spotify:artist:6B5c4sch27tWHAGdarpPaW'}], 'name': 'Disclaimer II'}, 'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/6B5c4sch27tWHAGdarpPaW'},
             'href': 'https://api.spotify.com/v1/artists/6B5c4sch27tWHAGdarpPaW',
             'id': '6B5c4sch27tWHAGdarpPaW', 'name': 'Seether', 'type': 'artist',
             'uri': 'spotify:artist:6B5c4sch27tWHAGdarpPaW'},
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/0fGVuq5ed21pM7iWwTcMyk'},
             'href': 'https://api.spotify.com/v1/artists/0fGVuq5ed21pM7iWwTcMyk',
             'id': '0fGVuq5ed21pM7iWwTcMyk', 'name': 'Amy Lee', 'type': 'artist',
             'uri': 'spotify:artist:0fGVuq5ed21pM7iWwTcMyk'}], 'name': 'Broken'}}, {'track': {
            'album': {
                'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/2xiIXseIJcq3nG7C8fHeBj'},
                             'href': 'https://api.spotify.com/v1/artists/2xiIXseIJcq3nG7C8fHeBj',
                             'id': '2xiIXseIJcq3nG7C8fHeBj', 'name': 'Three Days Grace', 'type': 'artist',
                             'uri': 'spotify:artist:2xiIXseIJcq3nG7C8fHeBj'}], 'name': 'One-X'}, 'artists': [
                {'external_urls': {'spotify': 'https://open.spotify.com/artist/2xiIXseIJcq3nG7C8fHeBj'},
                 'href': 'https://api.spotify.com/v1/artists/2xiIXseIJcq3nG7C8fHeBj', 'id': '2xiIXseIJcq3nG7C8fHeBj',
                 'name': 'Three Days Grace', 'type': 'artist', 'uri': 'spotify:artist:2xiIXseIJcq3nG7C8fHeBj'}],
            'name': 'Pain'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/0DrXhci3WAyo0WJv1RBOG6'},
             'href': 'https://api.spotify.com/v1/artists/0DrXhci3WAyo0WJv1RBOG6', 'id': '0DrXhci3WAyo0WJv1RBOG6',
             'name': '12 Stones', 'type': 'artist', 'uri': 'spotify:artist:0DrXhci3WAyo0WJv1RBOG6'}],
            'name': 'Anthem For The Underdog (Bonus Track Version)'}, 'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/0DrXhci3WAyo0WJv1RBOG6'},
             'href': 'https://api.spotify.com/v1/artists/0DrXhci3WAyo0WJv1RBOG6', 'id': '0DrXhci3WAyo0WJv1RBOG6',
             'name': '12 Stones', 'type': 'artist', 'uri': 'spotify:artist:0DrXhci3WAyo0WJv1RBOG6'}],
            'name': 'World So Cold'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/01crEa9G3pNpXZ5m7wuHOk'},
             'href': 'https://api.spotify.com/v1/artists/01crEa9G3pNpXZ5m7wuHOk', 'id': '01crEa9G3pNpXZ5m7wuHOk',
             'name': 'Red', 'type': 'artist', 'uri': 'spotify:artist:01crEa9G3pNpXZ5m7wuHOk'}],
            'name': 'Until We Have Faces'},
            'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/01crEa9G3pNpXZ5m7wuHOk'},
                'href': 'https://api.spotify.com/v1/artists/01crEa9G3pNpXZ5m7wuHOk',
                'id': '01crEa9G3pNpXZ5m7wuHOk',
                'name': 'Red', 'type': 'artist',
                'uri': 'spotify:artist:01crEa9G3pNpXZ5m7wuHOk'}],
            'name': 'Let It Burn'}}, {'track': {
            'album': {
                'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/6GfiCQDFYANz5wUkSmb3Dr'},
                             'href': 'https://api.spotify.com/v1/artists/6GfiCQDFYANz5wUkSmb3Dr',
                             'id': '6GfiCQDFYANz5wUkSmb3Dr', 'name': 'Thousand Foot Krutch', 'type': 'artist',
                             'uri': 'spotify:artist:6GfiCQDFYANz5wUkSmb3Dr'}], 'name': 'The End Is Where We Begin'},
            'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/6GfiCQDFYANz5wUkSmb3Dr'},
                         'href': 'https://api.spotify.com/v1/artists/6GfiCQDFYANz5wUkSmb3Dr',
                         'id': '6GfiCQDFYANz5wUkSmb3Dr', 'name': 'Thousand Foot Krutch', 'type': 'artist',
                         'uri': 'spotify:artist:6GfiCQDFYANz5wUkSmb3Dr'}], 'name': 'Fly on the Wall'}}, {'track': {
            'album': {
                'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/6B5c4sch27tWHAGdarpPaW'},
                             'href': 'https://api.spotify.com/v1/artists/6B5c4sch27tWHAGdarpPaW',
                             'id': '6B5c4sch27tWHAGdarpPaW', 'name': 'Seether', 'type': 'artist',
                             'uri': 'spotify:artist:6B5c4sch27tWHAGdarpPaW'}],
                'name': 'Finding Beauty In Negative Spaces (Bonus Track Version)'}, 'artists': [
                {'external_urls': {'spotify': 'https://open.spotify.com/artist/6B5c4sch27tWHAGdarpPaW'},
                 'href': 'https://api.spotify.com/v1/artists/6B5c4sch27tWHAGdarpPaW', 'id': '6B5c4sch27tWHAGdarpPaW',
                 'name': 'Seether', 'type': 'artist', 'uri': 'spotify:artist:6B5c4sch27tWHAGdarpPaW'}],
            'name': 'Breakdown'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
             'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF', 'id': '1Ffb6ejR6Fe5IamqA5oRUF',
             'name': 'Bring Me The Horizon', 'type': 'artist', 'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
            'name': 'Sempiternal (Deluxe Edition)'}, 'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
             'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF', 'id': '1Ffb6ejR6Fe5IamqA5oRUF',
             'name': 'Bring Me The Horizon', 'type': 'artist', 'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
            'name': 'Join The Club'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
             'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF', 'id': '1Ffb6ejR6Fe5IamqA5oRUF',
             'name': 'Bring Me The Horizon', 'type': 'artist', 'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
            'name': 'Sempiternal (Deluxe Edition)'},
            'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
                'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF',
                'id': '1Ffb6ejR6Fe5IamqA5oRUF',
                'name': 'Bring Me The Horizon',
                'type': 'artist',
                'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
            'name': 'Crooked Young'}}, {'track': {
            'album': {
                'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/6XyY86QOPPrYVGvF9ch6wz'},
                             'href': 'https://api.spotify.com/v1/artists/6XyY86QOPPrYVGvF9ch6wz',
                             'id': '6XyY86QOPPrYVGvF9ch6wz', 'name': 'Linkin Park', 'type': 'artist',
                             'uri': 'spotify:artist:6XyY86QOPPrYVGvF9ch6wz'}], 'name': 'Meteora'}, 'artists': [
                {'external_urls': {'spotify': 'https://open.spotify.com/artist/6XyY86QOPPrYVGvF9ch6wz'},
                 'href': 'https://api.spotify.com/v1/artists/6XyY86QOPPrYVGvF9ch6wz', 'id': '6XyY86QOPPrYVGvF9ch6wz',
                 'name': 'Linkin Park', 'type': 'artist', 'uri': 'spotify:artist:6XyY86QOPPrYVGvF9ch6wz'}],
            'name': 'Numb'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/7FBcuc1gsnv6Y1nwFtNRCb'},
             'href': 'https://api.spotify.com/v1/artists/7FBcuc1gsnv6Y1nwFtNRCb', 'id': '7FBcuc1gsnv6Y1nwFtNRCb',
             'name': 'My Chemical Romance', 'type': 'artist', 'uri': 'spotify:artist:7FBcuc1gsnv6Y1nwFtNRCb'}],
            'name': 'The Black Parade'}, 'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/7FBcuc1gsnv6Y1nwFtNRCb'},
             'href': 'https://api.spotify.com/v1/artists/7FBcuc1gsnv6Y1nwFtNRCb', 'id': '7FBcuc1gsnv6Y1nwFtNRCb',
             'name': 'My Chemical Romance', 'type': 'artist', 'uri': 'spotify:artist:7FBcuc1gsnv6Y1nwFtNRCb'}],
            'name': 'Welcome to the Black Parade'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/2xiIXseIJcq3nG7C8fHeBj'},
             'href': 'https://api.spotify.com/v1/artists/2xiIXseIJcq3nG7C8fHeBj', 'id': '2xiIXseIJcq3nG7C8fHeBj',
             'name': 'Three Days Grace', 'type': 'artist', 'uri': 'spotify:artist:2xiIXseIJcq3nG7C8fHeBj'}],
            'name': 'Three Days Grace'},
            'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/2xiIXseIJcq3nG7C8fHeBj'},
                'href': 'https://api.spotify.com/v1/artists/2xiIXseIJcq3nG7C8fHeBj',
                'id': '2xiIXseIJcq3nG7C8fHeBj',
                'name': 'Three Days Grace',
                'type': 'artist',
                'uri': 'spotify:artist:2xiIXseIJcq3nG7C8fHeBj'}],
            'name': 'I Hate Everything About You'}},
        {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/00YTqRClk82aMchQQpYMd5'},
             'href': 'https://api.spotify.com/v1/artists/00YTqRClk82aMchQQpYMd5',
             'id': '00YTqRClk82aMchQQpYMd5', 'name': 'Our Last Night', 'type': 'artist',
             'uri': 'spotify:artist:00YTqRClk82aMchQQpYMd5'}], 'name': 'Oak Island'}, 'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/00YTqRClk82aMchQQpYMd5'},
             'href': 'https://api.spotify.com/v1/artists/00YTqRClk82aMchQQpYMd5',
             'id': '00YTqRClk82aMchQQpYMd5', 'name': 'Our Last Night', 'type': 'artist',
             'uri': 'spotify:artist:00YTqRClk82aMchQQpYMd5'}], 'name': 'Same Old War'}}, {'track': {
            'album': {
                'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/5eAWCfyUhZtHHtBdNk56l1'},
                             'href': 'https://api.spotify.com/v1/artists/5eAWCfyUhZtHHtBdNk56l1',
                             'id': '5eAWCfyUhZtHHtBdNk56l1', 'name': 'System Of A Down', 'type': 'artist',
                             'uri': 'spotify:artist:5eAWCfyUhZtHHtBdNk56l1'}], 'name': 'Toxicity'}, 'artists': [
                {'external_urls': {'spotify': 'https://open.spotify.com/artist/5eAWCfyUhZtHHtBdNk56l1'},
                 'href': 'https://api.spotify.com/v1/artists/5eAWCfyUhZtHHtBdNk56l1', 'id': '5eAWCfyUhZtHHtBdNk56l1',
                 'name': 'System Of A Down', 'type': 'artist', 'uri': 'spotify:artist:5eAWCfyUhZtHHtBdNk56l1'}],
            'name': 'Chop Suey!'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/6XyY86QOPPrYVGvF9ch6wz'},
             'href': 'https://api.spotify.com/v1/artists/6XyY86QOPPrYVGvF9ch6wz', 'id': '6XyY86QOPPrYVGvF9ch6wz',
             'name': 'Linkin Park', 'type': 'artist', 'uri': 'spotify:artist:6XyY86QOPPrYVGvF9ch6wz'}],
            'name': 'Hybrid Theory (Bonus Edition)'}, 'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/6XyY86QOPPrYVGvF9ch6wz'},
             'href': 'https://api.spotify.com/v1/artists/6XyY86QOPPrYVGvF9ch6wz', 'id': '6XyY86QOPPrYVGvF9ch6wz',
             'name': 'Linkin Park', 'type': 'artist', 'uri': 'spotify:artist:6XyY86QOPPrYVGvF9ch6wz'}],
            'name': 'Crawling'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/6XyY86QOPPrYVGvF9ch6wz'},
             'href': 'https://api.spotify.com/v1/artists/6XyY86QOPPrYVGvF9ch6wz', 'id': '6XyY86QOPPrYVGvF9ch6wz',
             'name': 'Linkin Park', 'type': 'artist', 'uri': 'spotify:artist:6XyY86QOPPrYVGvF9ch6wz'}],
            'name': 'Hybrid Theory (Bonus Edition)'},
            'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/6XyY86QOPPrYVGvF9ch6wz'},
                'href': 'https://api.spotify.com/v1/artists/6XyY86QOPPrYVGvF9ch6wz',
                'id': '6XyY86QOPPrYVGvF9ch6wz',
                'name': 'Linkin Park',
                'type': 'artist',
                'uri': 'spotify:artist:6XyY86QOPPrYVGvF9ch6wz'}],
            'name': 'Papercut'}}, {'track': {'album': {
            'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/3YQKmKGau1PzlVlkL1iodx'},
                         'href': 'https://api.spotify.com/v1/artists/3YQKmKGau1PzlVlkL1iodx',
                         'id': '3YQKmKGau1PzlVlkL1iodx', 'name': 'Twenty One Pilots', 'type': 'artist',
                         'uri': 'spotify:artist:3YQKmKGau1PzlVlkL1iodx'}], 'name': 'Vessel'}, 'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/3YQKmKGau1PzlVlkL1iodx'},
             'href': 'https://api.spotify.com/v1/artists/3YQKmKGau1PzlVlkL1iodx', 'id': '3YQKmKGau1PzlVlkL1iodx',
             'name': 'Twenty One Pilots', 'type': 'artist', 'uri': 'spotify:artist:3YQKmKGau1PzlVlkL1iodx'}],
            'name': 'Car Radio'}},
        {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/00YTqRClk82aMchQQpYMd5'},
             'href': 'https://api.spotify.com/v1/artists/00YTqRClk82aMchQQpYMd5',
             'id': '00YTqRClk82aMchQQpYMd5', 'name': 'Our Last Night', 'type': 'artist',
             'uri': 'spotify:artist:00YTqRClk82aMchQQpYMd5'}], 'name': 'Selective Hearing'},
            'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/00YTqRClk82aMchQQpYMd5'},
                'href': 'https://api.spotify.com/v1/artists/00YTqRClk82aMchQQpYMd5',
                'id': '00YTqRClk82aMchQQpYMd5', 'name': 'Our Last Night',
                'type': 'artist', 'uri': 'spotify:artist:00YTqRClk82aMchQQpYMd5'}],
            'name': 'Common Ground'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/5nGIFgo0shDenQYSE0Sn7c'},
             'href': 'https://api.spotify.com/v1/artists/5nGIFgo0shDenQYSE0Sn7c', 'id': '5nGIFgo0shDenQYSE0Sn7c',
             'name': 'Evanescence', 'type': 'artist', 'uri': 'spotify:artist:5nGIFgo0shDenQYSE0Sn7c'}],
            'name': 'Fallen'},
            'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/5nGIFgo0shDenQYSE0Sn7c'},
                'href': 'https://api.spotify.com/v1/artists/5nGIFgo0shDenQYSE0Sn7c',
                'id': '5nGIFgo0shDenQYSE0Sn7c',
                'name': 'Evanescence',
                'type': 'artist',
                'uri': 'spotify:artist:5nGIFgo0shDenQYSE0Sn7c'}],
            'name': 'Bring Me To Life'}}, {'track': {
            'album': {
                'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/3hE8S8ohRErocpkY7uJW4a'},
                             'href': 'https://api.spotify.com/v1/artists/3hE8S8ohRErocpkY7uJW4a',
                             'id': '3hE8S8ohRErocpkY7uJW4a', 'name': 'Within Temptation', 'type': 'artist',
                             'uri': 'spotify:artist:3hE8S8ohRErocpkY7uJW4a'}], 'name': 'The Silent Force'},
            'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/3hE8S8ohRErocpkY7uJW4a'},
                         'href': 'https://api.spotify.com/v1/artists/3hE8S8ohRErocpkY7uJW4a',
                         'id': '3hE8S8ohRErocpkY7uJW4a', 'name': 'Within Temptation', 'type': 'artist',
                         'uri': 'spotify:artist:3hE8S8ohRErocpkY7uJW4a'}], 'name': 'Angels'}}, {'track': {'album': {
            'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/74XFHRwlV6OrjEM0A2NCMF'},
                         'href': 'https://api.spotify.com/v1/artists/74XFHRwlV6OrjEM0A2NCMF',
                         'id': '74XFHRwlV6OrjEM0A2NCMF', 'name': 'Paramore', 'type': 'artist',
                         'uri': 'spotify:artist:74XFHRwlV6OrjEM0A2NCMF'}], 'name': 'Riot!'}, 'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/74XFHRwlV6OrjEM0A2NCMF'},
             'href': 'https://api.spotify.com/v1/artists/74XFHRwlV6OrjEM0A2NCMF', 'id': '74XFHRwlV6OrjEM0A2NCMF',
             'name': 'Paramore', 'type': 'artist', 'uri': 'spotify:artist:74XFHRwlV6OrjEM0A2NCMF'}],
            'name': 'Misery Business'}},
        {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/74XFHRwlV6OrjEM0A2NCMF'},
             'href': 'https://api.spotify.com/v1/artists/74XFHRwlV6OrjEM0A2NCMF',
             'id': '74XFHRwlV6OrjEM0A2NCMF', 'name': 'Paramore', 'type': 'artist',
             'uri': 'spotify:artist:74XFHRwlV6OrjEM0A2NCMF'}], 'name': 'Riot!'}, 'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/74XFHRwlV6OrjEM0A2NCMF'},
             'href': 'https://api.spotify.com/v1/artists/74XFHRwlV6OrjEM0A2NCMF',
             'id': '74XFHRwlV6OrjEM0A2NCMF', 'name': 'Paramore', 'type': 'artist',
             'uri': 'spotify:artist:74XFHRwlV6OrjEM0A2NCMF'}], 'name': "That's What You Get"}}, {
            'track': {'album': {'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/1SImpQO0GbjRgvlwCcCtFo'},
                'href': 'https://api.spotify.com/v1/artists/1SImpQO0GbjRgvlwCcCtFo',
                'id': '1SImpQO0GbjRgvlwCcCtFo',
                'name': 'The Red Jumpsuit Apparatus', 'type': 'artist',
                'uri': 'spotify:artist:1SImpQO0GbjRgvlwCcCtFo'}],
                'name': "Don't You Fake It"}, 'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/1SImpQO0GbjRgvlwCcCtFo'},
                'href': 'https://api.spotify.com/v1/artists/1SImpQO0GbjRgvlwCcCtFo',
                'id': '1SImpQO0GbjRgvlwCcCtFo',
                'name': 'The Red Jumpsuit Apparatus',
                'type': 'artist',
                'uri': 'spotify:artist:1SImpQO0GbjRgvlwCcCtFo'}],
                'name': 'Face Down'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/1SImpQO0GbjRgvlwCcCtFo'},
             'href': 'https://api.spotify.com/v1/artists/1SImpQO0GbjRgvlwCcCtFo', 'id': '1SImpQO0GbjRgvlwCcCtFo',
             'name': 'The Red Jumpsuit Apparatus', 'type': 'artist', 'uri': 'spotify:artist:1SImpQO0GbjRgvlwCcCtFo'}],
            'name': "Don't You Fake It"},
            'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/1SImpQO0GbjRgvlwCcCtFo'},
                'href': 'https://api.spotify.com/v1/artists/1SImpQO0GbjRgvlwCcCtFo',
                'id': '1SImpQO0GbjRgvlwCcCtFo',
                'name': 'The Red Jumpsuit Apparatus',
                'type': 'artist',
                'uri': 'spotify:artist:1SImpQO0GbjRgvlwCcCtFo'}],
            'name': 'Your Guardian Angel'}}, {'track': {
            'album': {
                'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/74XFHRwlV6OrjEM0A2NCMF'},
                             'href': 'https://api.spotify.com/v1/artists/74XFHRwlV6OrjEM0A2NCMF',
                             'id': '74XFHRwlV6OrjEM0A2NCMF', 'name': 'Paramore', 'type': 'artist',
                             'uri': 'spotify:artist:74XFHRwlV6OrjEM0A2NCMF'}], 'name': 'Riot!'}, 'artists': [
                {'external_urls': {'spotify': 'https://open.spotify.com/artist/74XFHRwlV6OrjEM0A2NCMF'},
                 'href': 'https://api.spotify.com/v1/artists/74XFHRwlV6OrjEM0A2NCMF', 'id': '74XFHRwlV6OrjEM0A2NCMF',
                 'name': 'Paramore', 'type': 'artist', 'uri': 'spotify:artist:74XFHRwlV6OrjEM0A2NCMF'}],
            'name': 'crushcrushcrush'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/2p4FqHnazRucYQHyDCdBrJ'},
             'href': 'https://api.spotify.com/v1/artists/2p4FqHnazRucYQHyDCdBrJ', 'id': '2p4FqHnazRucYQHyDCdBrJ',
             'name': 'Simple Plan', 'type': 'artist', 'uri': 'spotify:artist:2p4FqHnazRucYQHyDCdBrJ'}],
            'name': 'Still Not Getting Any'}, 'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/2p4FqHnazRucYQHyDCdBrJ'},
             'href': 'https://api.spotify.com/v1/artists/2p4FqHnazRucYQHyDCdBrJ', 'id': '2p4FqHnazRucYQHyDCdBrJ',
             'name': 'Simple Plan', 'type': 'artist', 'uri': 'spotify:artist:2p4FqHnazRucYQHyDCdBrJ'}],
            'name': 'Welcome to My Life'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/74XFHRwlV6OrjEM0A2NCMF'},
             'href': 'https://api.spotify.com/v1/artists/74XFHRwlV6OrjEM0A2NCMF', 'id': '74XFHRwlV6OrjEM0A2NCMF',
             'name': 'Paramore', 'type': 'artist', 'uri': 'spotify:artist:74XFHRwlV6OrjEM0A2NCMF'}],
            'name': 'All We Know Is Falling'},
            'artists': [{
                'external_urls': {
                    'spotify': 'https://open.spotify.com/artist/74XFHRwlV6OrjEM0A2NCMF'},
                'href': 'https://api.spotify.com/v1/artists/74XFHRwlV6OrjEM0A2NCMF',
                'id': '74XFHRwlV6OrjEM0A2NCMF',
                'name': 'Paramore',
                'type': 'artist',
                'uri': 'spotify:artist:74XFHRwlV6OrjEM0A2NCMF'}],
            'name': 'Pressure'}}, {
            'track': {'album': {'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/7oPftvlwr6VrsViSDV7fJY'},
                'href': 'https://api.spotify.com/v1/artists/7oPftvlwr6VrsViSDV7fJY',
                'id': '7oPftvlwr6VrsViSDV7fJY', 'name': 'Green Day',
                'type': 'artist',
                'uri': 'spotify:artist:7oPftvlwr6VrsViSDV7fJY'}],
                'name': 'American Idiot'}, 'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/7oPftvlwr6VrsViSDV7fJY'},
                'href': 'https://api.spotify.com/v1/artists/7oPftvlwr6VrsViSDV7fJY',
                'id': '7oPftvlwr6VrsViSDV7fJY',
                'name': 'Green Day',
                'type': 'artist',
                'uri': 'spotify:artist:7oPftvlwr6VrsViSDV7fJY'}],
                'name': 'Wake Me up When September Ends'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/5BtHciL0e0zOP7prIHn3pP'},
             'href': 'https://api.spotify.com/v1/artists/5BtHciL0e0zOP7prIHn3pP', 'id': '5BtHciL0e0zOP7prIHn3pP',
             'name': 'Breaking Benjamin', 'type': 'artist', 'uri': 'spotify:artist:5BtHciL0e0zOP7prIHn3pP'}],
            'name': 'Dear Agony'},
            'artists': [{
                'external_urls': {
                    'spotify': 'https://open.spotify.com/artist/5BtHciL0e0zOP7prIHn3pP'},
                'href': 'https://api.spotify.com/v1/artists/5BtHciL0e0zOP7prIHn3pP',
                'id': '5BtHciL0e0zOP7prIHn3pP',
                'name': 'Breaking Benjamin',
                'type': 'artist',
                'uri': 'spotify:artist:5BtHciL0e0zOP7prIHn3pP'}],
            'name': 'I Will Not Bow'}},
        {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/6GfiCQDFYANz5wUkSmb3Dr'},
             'href': 'https://api.spotify.com/v1/artists/6GfiCQDFYANz5wUkSmb3Dr',
             'id': '6GfiCQDFYANz5wUkSmb3Dr', 'name': 'Thousand Foot Krutch', 'type': 'artist',
             'uri': 'spotify:artist:6GfiCQDFYANz5wUkSmb3Dr'}], 'name': 'The End Is Where We Begin'},
            'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/6GfiCQDFYANz5wUkSmb3Dr'},
                'href': 'https://api.spotify.com/v1/artists/6GfiCQDFYANz5wUkSmb3Dr',
                'id': '6GfiCQDFYANz5wUkSmb3Dr', 'name': 'Thousand Foot Krutch',
                'type': 'artist', 'uri': 'spotify:artist:6GfiCQDFYANz5wUkSmb3Dr'}],
            'name': 'Courtesy Call'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/0kD8IT1CzF7js2XKM9lLLa'},
             'href': 'https://api.spotify.com/v1/artists/0kD8IT1CzF7js2XKM9lLLa', 'id': '0kD8IT1CzF7js2XKM9lLLa',
             'name': 'STARSET', 'type': 'artist', 'uri': 'spotify:artist:0kD8IT1CzF7js2XKM9lLLa'}],
            'name': 'Transmissions (Deluxe Version)'},
            'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/0kD8IT1CzF7js2XKM9lLLa'},
                'href': 'https://api.spotify.com/v1/artists/0kD8IT1CzF7js2XKM9lLLa',
                'id': '0kD8IT1CzF7js2XKM9lLLa',
                'name': 'STARSET',
                'type': 'artist',
                'uri': 'spotify:artist:0kD8IT1CzF7js2XKM9lLLa'}],
            'name': 'My Demons'}}, {'track': {'album': {
            'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/5BtHciL0e0zOP7prIHn3pP'},
                         'href': 'https://api.spotify.com/v1/artists/5BtHciL0e0zOP7prIHn3pP',
                         'id': '5BtHciL0e0zOP7prIHn3pP', 'name': 'Breaking Benjamin', 'type': 'artist',
                         'uri': 'spotify:artist:5BtHciL0e0zOP7prIHn3pP'}], 'name': 'Phobia (Clean Version)'},
            'artists': [
                {'external_urls': {'spotify': 'https://open.spotify.com/artist/5BtHciL0e0zOP7prIHn3pP'},
                 'href': 'https://api.spotify.com/v1/artists/5BtHciL0e0zOP7prIHn3pP', 'id': '5BtHciL0e0zOP7prIHn3pP',
                 'name': 'Breaking Benjamin', 'type': 'artist', 'uri': 'spotify:artist:5BtHciL0e0zOP7prIHn3pP'}],
            'name': 'The Diary of Jane - Single Version'}},
        {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/6GfiCQDFYANz5wUkSmb3Dr'},
             'href': 'https://api.spotify.com/v1/artists/6GfiCQDFYANz5wUkSmb3Dr',
             'id': '6GfiCQDFYANz5wUkSmb3Dr', 'name': 'Thousand Foot Krutch', 'type': 'artist',
             'uri': 'spotify:artist:6GfiCQDFYANz5wUkSmb3Dr'}], 'name': 'OXYGEN:INHALE'}, 'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/6GfiCQDFYANz5wUkSmb3Dr'},
             'href': 'https://api.spotify.com/v1/artists/6GfiCQDFYANz5wUkSmb3Dr',
             'id': '6GfiCQDFYANz5wUkSmb3Dr', 'name': 'Thousand Foot Krutch', 'type': 'artist',
             'uri': 'spotify:artist:6GfiCQDFYANz5wUkSmb3Dr'}], 'name': 'Untraveled Road'}}, {
            'track': {'album': {'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
                'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF',
                'id': '1Ffb6ejR6Fe5IamqA5oRUF',
                'name': 'Bring Me The Horizon', 'type': 'artist',
                'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
                'name': "That's The Spirit (Track by Track Commentary)"}, 'artists': [
                {'external_urls': {
                    'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
                    'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF',
                    'id': '1Ffb6ejR6Fe5IamqA5oRUF', 'name': 'Bring Me The Horizon', 'type': 'artist',
                    'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}], 'name': 'Throne'}}, {'track': {
            'album': {
                'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/7Ln80lUS6He07XvHI8qqHH'},
                             'href': 'https://api.spotify.com/v1/artists/7Ln80lUS6He07XvHI8qqHH',
                             'id': '7Ln80lUS6He07XvHI8qqHH', 'name': 'Arctic Monkeys', 'type': 'artist',
                             'uri': 'spotify:artist:7Ln80lUS6He07XvHI8qqHH'}], 'name': 'AM'}, 'artists': [
                {'external_urls': {'spotify': 'https://open.spotify.com/artist/7Ln80lUS6He07XvHI8qqHH'},
                 'href': 'https://api.spotify.com/v1/artists/7Ln80lUS6He07XvHI8qqHH', 'id': '7Ln80lUS6He07XvHI8qqHH',
                 'name': 'Arctic Monkeys', 'type': 'artist', 'uri': 'spotify:artist:7Ln80lUS6He07XvHI8qqHH'}],
            'name': "Why'd You Only Call Me When You're High?"}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/711MCceyCBcFnzjGY4Q7Un'},
             'href': 'https://api.spotify.com/v1/artists/711MCceyCBcFnzjGY4Q7Un', 'id': '711MCceyCBcFnzjGY4Q7Un',
             'name': 'AC/DC', 'type': 'artist', 'uri': 'spotify:artist:711MCceyCBcFnzjGY4Q7Un'}],
            'name': 'Back In Black'},
            'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/711MCceyCBcFnzjGY4Q7Un'},
                'href': 'https://api.spotify.com/v1/artists/711MCceyCBcFnzjGY4Q7Un',
                'id': '711MCceyCBcFnzjGY4Q7Un',
                'name': 'AC/DC', 'type': 'artist',
                'uri': 'spotify:artist:711MCceyCBcFnzjGY4Q7Un'}],
            'name': 'Back In Black'}}, {'track': {
            'album': {
                'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/711MCceyCBcFnzjGY4Q7Un'},
                             'href': 'https://api.spotify.com/v1/artists/711MCceyCBcFnzjGY4Q7Un',
                             'id': '711MCceyCBcFnzjGY4Q7Un', 'name': 'AC/DC', 'type': 'artist',
                             'uri': 'spotify:artist:711MCceyCBcFnzjGY4Q7Un'}], 'name': 'Highway to Hell'},
            'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/711MCceyCBcFnzjGY4Q7Un'},
                         'href': 'https://api.spotify.com/v1/artists/711MCceyCBcFnzjGY4Q7Un',
                         'id': '711MCceyCBcFnzjGY4Q7Un', 'name': 'AC/DC', 'type': 'artist',
                         'uri': 'spotify:artist:711MCceyCBcFnzjGY4Q7Un'}], 'name': 'Highway to Hell'}}, {'track': {
            'album': {
                'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/7FBcuc1gsnv6Y1nwFtNRCb'},
                             'href': 'https://api.spotify.com/v1/artists/7FBcuc1gsnv6Y1nwFtNRCb',
                             'id': '7FBcuc1gsnv6Y1nwFtNRCb', 'name': 'My Chemical Romance', 'type': 'artist',
                             'uri': 'spotify:artist:7FBcuc1gsnv6Y1nwFtNRCb'}], 'name': 'The Black Parade'},
            'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/7FBcuc1gsnv6Y1nwFtNRCb'},
                         'href': 'https://api.spotify.com/v1/artists/7FBcuc1gsnv6Y1nwFtNRCb',
                         'id': '7FBcuc1gsnv6Y1nwFtNRCb', 'name': 'My Chemical Romance', 'type': 'artist',
                         'uri': 'spotify:artist:7FBcuc1gsnv6Y1nwFtNRCb'}], 'name': 'Famous Last Words'}}, {'track': {
            'album': {
                'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/2xiIXseIJcq3nG7C8fHeBj'},
                             'href': 'https://api.spotify.com/v1/artists/2xiIXseIJcq3nG7C8fHeBj',
                             'id': '2xiIXseIJcq3nG7C8fHeBj', 'name': 'Three Days Grace', 'type': 'artist',
                             'uri': 'spotify:artist:2xiIXseIJcq3nG7C8fHeBj'}], 'name': 'Human'}, 'artists': [
                {'external_urls': {'spotify': 'https://open.spotify.com/artist/2xiIXseIJcq3nG7C8fHeBj'},
                 'href': 'https://api.spotify.com/v1/artists/2xiIXseIJcq3nG7C8fHeBj', 'id': '2xiIXseIJcq3nG7C8fHeBj',
                 'name': 'Three Days Grace', 'type': 'artist', 'uri': 'spotify:artist:2xiIXseIJcq3nG7C8fHeBj'}],
            'name': 'Painkiller'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/6GfiCQDFYANz5wUkSmb3Dr'},
             'href': 'https://api.spotify.com/v1/artists/6GfiCQDFYANz5wUkSmb3Dr', 'id': '6GfiCQDFYANz5wUkSmb3Dr',
             'name': 'Thousand Foot Krutch', 'type': 'artist', 'uri': 'spotify:artist:6GfiCQDFYANz5wUkSmb3Dr'}],
            'name': 'The End Is Where We Begin'}, 'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/6GfiCQDFYANz5wUkSmb3Dr'},
             'href': 'https://api.spotify.com/v1/artists/6GfiCQDFYANz5wUkSmb3Dr', 'id': '6GfiCQDFYANz5wUkSmb3Dr',
             'name': 'Thousand Foot Krutch', 'type': 'artist', 'uri': 'spotify:artist:6GfiCQDFYANz5wUkSmb3Dr'}],
            'name': 'War of Change'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/7Ln80lUS6He07XvHI8qqHH'},
             'href': 'https://api.spotify.com/v1/artists/7Ln80lUS6He07XvHI8qqHH', 'id': '7Ln80lUS6He07XvHI8qqHH',
             'name': 'Arctic Monkeys', 'type': 'artist', 'uri': 'spotify:artist:7Ln80lUS6He07XvHI8qqHH'}],
            'name': 'AM'},
            'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/7Ln80lUS6He07XvHI8qqHH'},
                'href': 'https://api.spotify.com/v1/artists/7Ln80lUS6He07XvHI8qqHH',
                'id': '7Ln80lUS6He07XvHI8qqHH',
                'name': 'Arctic Monkeys',
                'type': 'artist',
                'uri': 'spotify:artist:7Ln80lUS6He07XvHI8qqHH'}],
            'name': 'Do I Wanna Know?'}}, {
            'track': {'album': {'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/49qiE8dj4JuNdpYGRPdKbF'},
                'href': 'https://api.spotify.com/v1/artists/49qiE8dj4JuNdpYGRPdKbF',
                'id': '49qiE8dj4JuNdpYGRPdKbF', 'name': 'Stone Sour',
                'type': 'artist',
                'uri': 'spotify:artist:49qiE8dj4JuNdpYGRPdKbF'}],
                'name': 'Stone Sour'}, 'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/49qiE8dj4JuNdpYGRPdKbF'},
                'href': 'https://api.spotify.com/v1/artists/49qiE8dj4JuNdpYGRPdKbF',
                'id': '49qiE8dj4JuNdpYGRPdKbF',
                'name': 'Stone Sour',
                'type': 'artist',
                'uri': 'spotify:artist:49qiE8dj4JuNdpYGRPdKbF'}],
                'name': 'Bother'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/4Z8W4fKeB5YxbusRsdQVPb'},
             'href': 'https://api.spotify.com/v1/artists/4Z8W4fKeB5YxbusRsdQVPb', 'id': '4Z8W4fKeB5YxbusRsdQVPb',
             'name': 'Radiohead', 'type': 'artist', 'uri': 'spotify:artist:4Z8W4fKeB5YxbusRsdQVPb'}],
            'name': 'OK Computer'}, 'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/4Z8W4fKeB5YxbusRsdQVPb'},
             'href': 'https://api.spotify.com/v1/artists/4Z8W4fKeB5YxbusRsdQVPb', 'id': '4Z8W4fKeB5YxbusRsdQVPb',
             'name': 'Radiohead', 'type': 'artist', 'uri': 'spotify:artist:4Z8W4fKeB5YxbusRsdQVPb'}],
            'name': 'Exit Music (For a Film)'}}, {'track': {
            'album': {
                'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
                             'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF',
                             'id': '1Ffb6ejR6Fe5IamqA5oRUF', 'name': 'Bring Me The Horizon', 'type': 'artist',
                             'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}], 'name': "That's The Spirit"},
            'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
                         'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF',
                         'id': '1Ffb6ejR6Fe5IamqA5oRUF', 'name': 'Bring Me The Horizon', 'type': 'artist',
                         'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}], 'name': 'Avalanche'}}, {'track': {'album': {
            'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/0RqtSIYZmd4fiBKVFqyIqD'},
                         'href': 'https://api.spotify.com/v1/artists/0RqtSIYZmd4fiBKVFqyIqD',
                         'id': '0RqtSIYZmd4fiBKVFqyIqD', 'name': 'Thirty Seconds To Mars', 'type': 'artist',
                         'uri': 'spotify:artist:0RqtSIYZmd4fiBKVFqyIqD'}], 'name': 'A Beautiful Lie'}, 'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/0RqtSIYZmd4fiBKVFqyIqD'},
             'href': 'https://api.spotify.com/v1/artists/0RqtSIYZmd4fiBKVFqyIqD', 'id': '0RqtSIYZmd4fiBKVFqyIqD',
             'name': 'Thirty Seconds To Mars', 'type': 'artist', 'uri': 'spotify:artist:0RqtSIYZmd4fiBKVFqyIqD'}],
            'name': 'Was It A Dream?'}},
        {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/1caBfBEapzw8z2Qz9q0OaQ'},
             'href': 'https://api.spotify.com/v1/artists/1caBfBEapzw8z2Qz9q0OaQ',
             'id': '1caBfBEapzw8z2Qz9q0OaQ', 'name': 'Asking Alexandria', 'type': 'artist',
             'uri': 'spotify:artist:1caBfBEapzw8z2Qz9q0OaQ'}], 'name': 'Asking Alexandria'},
            'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/1caBfBEapzw8z2Qz9q0OaQ'},
                'href': 'https://api.spotify.com/v1/artists/1caBfBEapzw8z2Qz9q0OaQ',
                'id': '1caBfBEapzw8z2Qz9q0OaQ', 'name': 'Asking Alexandria',
                'type': 'artist', 'uri': 'spotify:artist:1caBfBEapzw8z2Qz9q0OaQ'}],
            'name': 'Into The Fire'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/412BedlPBwXH6Dz6xetzGI'},
             'href': 'https://api.spotify.com/v1/artists/412BedlPBwXH6Dz6xetzGI', 'id': '412BedlPBwXH6Dz6xetzGI',
             'name': 'Picturesque', 'type': 'artist', 'uri': 'spotify:artist:412BedlPBwXH6Dz6xetzGI'}],
            'name': 'Do Re Mi'},
            'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/412BedlPBwXH6Dz6xetzGI'},
                'href': 'https://api.spotify.com/v1/artists/412BedlPBwXH6Dz6xetzGI',
                'id': '412BedlPBwXH6Dz6xetzGI',
                'name': 'Picturesque',
                'type': 'artist',
                'uri': 'spotify:artist:412BedlPBwXH6Dz6xetzGI'}],
            'name': 'Do Re Mi'}}, {'track': {'album': {
            'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/6vwjIs0tbIiseJMR3pqwiL'},
                         'href': 'https://api.spotify.com/v1/artists/6vwjIs0tbIiseJMR3pqwiL',
                         'id': '6vwjIs0tbIiseJMR3pqwiL', 'name': 'Beartooth', 'type': 'artist',
                         'uri': 'spotify:artist:6vwjIs0tbIiseJMR3pqwiL'}], 'name': 'Disease'}, 'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/6vwjIs0tbIiseJMR3pqwiL'},
             'href': 'https://api.spotify.com/v1/artists/6vwjIs0tbIiseJMR3pqwiL', 'id': '6vwjIs0tbIiseJMR3pqwiL',
             'name': 'Beartooth', 'type': 'artist', 'uri': 'spotify:artist:6vwjIs0tbIiseJMR3pqwiL'}],
            'name': 'Afterall'}},
        {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/0RqtSIYZmd4fiBKVFqyIqD'},
             'href': 'https://api.spotify.com/v1/artists/0RqtSIYZmd4fiBKVFqyIqD',
             'id': '0RqtSIYZmd4fiBKVFqyIqD', 'name': 'Thirty Seconds To Mars', 'type': 'artist',
             'uri': 'spotify:artist:0RqtSIYZmd4fiBKVFqyIqD'}], 'name': 'This Is War (Deluxe)'},
            'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/0RqtSIYZmd4fiBKVFqyIqD'},
                'href': 'https://api.spotify.com/v1/artists/0RqtSIYZmd4fiBKVFqyIqD',
                'id': '0RqtSIYZmd4fiBKVFqyIqD', 'name': 'Thirty Seconds To Mars',
                'type': 'artist', 'uri': 'spotify:artist:0RqtSIYZmd4fiBKVFqyIqD'}],
            'name': 'This Is War'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
             'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF', 'id': '1Ffb6ejR6Fe5IamqA5oRUF',
             'name': 'Bring Me The Horizon', 'type': 'artist', 'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
            'name': "That's The Spirit"},
            'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
                'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF',
                'id': '1Ffb6ejR6Fe5IamqA5oRUF',
                'name': 'Bring Me The Horizon',
                'type': 'artist',
                'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
            'name': 'What You Need'}}, {'track': {
            'album': {
                'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/0L8ExT028jH3ddEcZwqJJ5'},
                             'href': 'https://api.spotify.com/v1/artists/0L8ExT028jH3ddEcZwqJJ5',
                             'id': '0L8ExT028jH3ddEcZwqJJ5', 'name': 'Red Hot Chili Peppers', 'type': 'artist',
                             'uri': 'spotify:artist:0L8ExT028jH3ddEcZwqJJ5'}],
                'name': 'Californication (Deluxe Edition)'}, 'artists': [
                {'external_urls': {'spotify': 'https://open.spotify.com/artist/0L8ExT028jH3ddEcZwqJJ5'},
                 'href': 'https://api.spotify.com/v1/artists/0L8ExT028jH3ddEcZwqJJ5', 'id': '0L8ExT028jH3ddEcZwqJJ5',
                 'name': 'Red Hot Chili Peppers', 'type': 'artist', 'uri': 'spotify:artist:0L8ExT028jH3ddEcZwqJJ5'}],
            'name': 'Californication'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/2CmaKO2zEGJ1NWpS1yfVGz'},
             'href': 'https://api.spotify.com/v1/artists/2CmaKO2zEGJ1NWpS1yfVGz', 'id': '2CmaKO2zEGJ1NWpS1yfVGz',
             'name': 'Falling In Reverse', 'type': 'artist', 'uri': 'spotify:artist:2CmaKO2zEGJ1NWpS1yfVGz'}],
            'name': 'Popular Monster'}, 'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/2CmaKO2zEGJ1NWpS1yfVGz'},
             'href': 'https://api.spotify.com/v1/artists/2CmaKO2zEGJ1NWpS1yfVGz', 'id': '2CmaKO2zEGJ1NWpS1yfVGz',
             'name': 'Falling In Reverse', 'type': 'artist', 'uri': 'spotify:artist:2CmaKO2zEGJ1NWpS1yfVGz'}],
            'name': 'Popular Monster'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/2C2sVVXanbOpymYBMpsi89'},
             'href': 'https://api.spotify.com/v1/artists/2C2sVVXanbOpymYBMpsi89', 'id': '2C2sVVXanbOpymYBMpsi89',
             'name': 'The Cab', 'type': 'artist', 'uri': 'spotify:artist:2C2sVVXanbOpymYBMpsi89'}],
            'name': 'Symphony Soldier'},
            'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/2C2sVVXanbOpymYBMpsi89'},
                'href': 'https://api.spotify.com/v1/artists/2C2sVVXanbOpymYBMpsi89',
                'id': '2C2sVVXanbOpymYBMpsi89',
                'name': 'The Cab',
                'type': 'artist',
                'uri': 'spotify:artist:2C2sVVXanbOpymYBMpsi89'}],
            'name': 'Temporary Bliss'}}, {
            'track': {'album': {'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
                'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF',
                'id': '1Ffb6ejR6Fe5IamqA5oRUF',
                'name': 'Bring Me The Horizon', 'type': 'artist',
                'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
                'name': "That's The Spirit (Track by Track Commentary)"}, 'artists': [
                {'external_urls': {
                    'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
                    'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF',
                    'id': '1Ffb6ejR6Fe5IamqA5oRUF', 'name': 'Bring Me The Horizon', 'type': 'artist',
                    'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}], 'name': 'Doomed'}}, {'track': {
            'album': {
                'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
                             'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF',
                             'id': '1Ffb6ejR6Fe5IamqA5oRUF', 'name': 'Bring Me The Horizon', 'type': 'artist',
                             'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
                'name': "That's The Spirit (Track by Track Commentary)"}, 'artists': [
                {'external_urls': {'spotify': 'https://open.spotify.com/artist/1Ffb6ejR6Fe5IamqA5oRUF'},
                 'href': 'https://api.spotify.com/v1/artists/1Ffb6ejR6Fe5IamqA5oRUF', 'id': '1Ffb6ejR6Fe5IamqA5oRUF',
                 'name': 'Bring Me The Horizon', 'type': 'artist', 'uri': 'spotify:artist:1Ffb6ejR6Fe5IamqA5oRUF'}],
            'name': 'Follow You'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/7FBcuc1gsnv6Y1nwFtNRCb'},
             'href': 'https://api.spotify.com/v1/artists/7FBcuc1gsnv6Y1nwFtNRCb', 'id': '7FBcuc1gsnv6Y1nwFtNRCb',
             'name': 'My Chemical Romance', 'type': 'artist', 'uri': 'spotify:artist:7FBcuc1gsnv6Y1nwFtNRCb'}],
            'name': 'The Black Parade'}, 'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/7FBcuc1gsnv6Y1nwFtNRCb'},
             'href': 'https://api.spotify.com/v1/artists/7FBcuc1gsnv6Y1nwFtNRCb', 'id': '7FBcuc1gsnv6Y1nwFtNRCb',
             'name': 'My Chemical Romance', 'type': 'artist', 'uri': 'spotify:artist:7FBcuc1gsnv6Y1nwFtNRCb'}],
            'name': 'Teenagers'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/6XyY86QOPPrYVGvF9ch6wz'},
             'href': 'https://api.spotify.com/v1/artists/6XyY86QOPPrYVGvF9ch6wz', 'id': '6XyY86QOPPrYVGvF9ch6wz',
             'name': 'Linkin Park', 'type': 'artist', 'uri': 'spotify:artist:6XyY86QOPPrYVGvF9ch6wz'}],
            'name': 'Meteora'},
            'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/6XyY86QOPPrYVGvF9ch6wz'},
                'href': 'https://api.spotify.com/v1/artists/6XyY86QOPPrYVGvF9ch6wz',
                'id': '6XyY86QOPPrYVGvF9ch6wz',
                'name': 'Linkin Park',
                'type': 'artist',
                'uri': 'spotify:artist:6XyY86QOPPrYVGvF9ch6wz'}],
            'name': 'Breaking the Habit'}}, {'track': {
            'album': {
                'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/502ZZTWlqgS1Ht62ewubEJ'},
                             'href': 'https://api.spotify.com/v1/artists/502ZZTWlqgS1Ht62ewubEJ',
                             'id': '502ZZTWlqgS1Ht62ewubEJ', 'name': 'Dead By Sunrise', 'type': 'artist',
                             'uri': 'spotify:artist:502ZZTWlqgS1Ht62ewubEJ'}], 'name': 'Out Of Ashes'}, 'artists': [
                {'external_urls': {'spotify': 'https://open.spotify.com/artist/502ZZTWlqgS1Ht62ewubEJ'},
                 'href': 'https://api.spotify.com/v1/artists/502ZZTWlqgS1Ht62ewubEJ', 'id': '502ZZTWlqgS1Ht62ewubEJ',
                 'name': 'Dead By Sunrise', 'type': 'artist', 'uri': 'spotify:artist:502ZZTWlqgS1Ht62ewubEJ'}],
            'name': 'Inside of Me'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/502ZZTWlqgS1Ht62ewubEJ'},
             'href': 'https://api.spotify.com/v1/artists/502ZZTWlqgS1Ht62ewubEJ', 'id': '502ZZTWlqgS1Ht62ewubEJ',
             'name': 'Dead By Sunrise', 'type': 'artist', 'uri': 'spotify:artist:502ZZTWlqgS1Ht62ewubEJ'}],
            'name': 'Out Of Ashes'}, 'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/502ZZTWlqgS1Ht62ewubEJ'},
             'href': 'https://api.spotify.com/v1/artists/502ZZTWlqgS1Ht62ewubEJ', 'id': '502ZZTWlqgS1Ht62ewubEJ',
             'name': 'Dead By Sunrise', 'type': 'artist', 'uri': 'spotify:artist:502ZZTWlqgS1Ht62ewubEJ'}],
            'name': 'Crawl Back In'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/502ZZTWlqgS1Ht62ewubEJ'},
             'href': 'https://api.spotify.com/v1/artists/502ZZTWlqgS1Ht62ewubEJ', 'id': '502ZZTWlqgS1Ht62ewubEJ',
             'name': 'Dead By Sunrise', 'type': 'artist', 'uri': 'spotify:artist:502ZZTWlqgS1Ht62ewubEJ'}],
            'name': 'Out Of Ashes'},
            'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/502ZZTWlqgS1Ht62ewubEJ'},
                'href': 'https://api.spotify.com/v1/artists/502ZZTWlqgS1Ht62ewubEJ',
                'id': '502ZZTWlqgS1Ht62ewubEJ',
                'name': 'Dead By Sunrise',
                'type': 'artist',
                'uri': 'spotify:artist:502ZZTWlqgS1Ht62ewubEJ'}],
            'name': 'Let Down'}}, {'track': {
            'album': {
                'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/502ZZTWlqgS1Ht62ewubEJ'},
                             'href': 'https://api.spotify.com/v1/artists/502ZZTWlqgS1Ht62ewubEJ',
                             'id': '502ZZTWlqgS1Ht62ewubEJ', 'name': 'Dead By Sunrise', 'type': 'artist',
                             'uri': 'spotify:artist:502ZZTWlqgS1Ht62ewubEJ'}], 'name': 'Out Of Ashes'}, 'artists': [
                {'external_urls': {'spotify': 'https://open.spotify.com/artist/502ZZTWlqgS1Ht62ewubEJ'},
                 'href': 'https://api.spotify.com/v1/artists/502ZZTWlqgS1Ht62ewubEJ', 'id': '502ZZTWlqgS1Ht62ewubEJ',
                 'name': 'Dead By Sunrise', 'type': 'artist', 'uri': 'spotify:artist:502ZZTWlqgS1Ht62ewubEJ'}],
            'name': 'Too Late'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/6XyY86QOPPrYVGvF9ch6wz'},
             'href': 'https://api.spotify.com/v1/artists/6XyY86QOPPrYVGvF9ch6wz', 'id': '6XyY86QOPPrYVGvF9ch6wz',
             'name': 'Linkin Park', 'type': 'artist', 'uri': 'spotify:artist:6XyY86QOPPrYVGvF9ch6wz'}],
            'name': 'Hybrid Theory (Bonus Edition)'}, 'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/6XyY86QOPPrYVGvF9ch6wz'},
             'href': 'https://api.spotify.com/v1/artists/6XyY86QOPPrYVGvF9ch6wz', 'id': '6XyY86QOPPrYVGvF9ch6wz',
             'name': 'Linkin Park', 'type': 'artist', 'uri': 'spotify:artist:6XyY86QOPPrYVGvF9ch6wz'}],
            'name': 'One Step Closer'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/4RddZ3iHvSpGV4dvATac9X'},
             'href': 'https://api.spotify.com/v1/artists/4RddZ3iHvSpGV4dvATac9X', 'id': '4RddZ3iHvSpGV4dvATac9X',
             'name': 'Papa Roach', 'type': 'artist', 'uri': 'spotify:artist:4RddZ3iHvSpGV4dvATac9X'}],
            'name': 'Infest'},
            'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/4RddZ3iHvSpGV4dvATac9X'},
                'href': 'https://api.spotify.com/v1/artists/4RddZ3iHvSpGV4dvATac9X',
                'id': '4RddZ3iHvSpGV4dvATac9X',
                'name': 'Papa Roach',
                'type': 'artist',
                'uri': 'spotify:artist:4RddZ3iHvSpGV4dvATac9X'}],
            'name': 'Last Resort'}}, {'track': {
            'album': {
                'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/7oPftvlwr6VrsViSDV7fJY'},
                             'href': 'https://api.spotify.com/v1/artists/7oPftvlwr6VrsViSDV7fJY',
                             'id': '7oPftvlwr6VrsViSDV7fJY', 'name': 'Green Day', 'type': 'artist',
                             'uri': 'spotify:artist:7oPftvlwr6VrsViSDV7fJY'}], 'name': 'American Idiot'}, 'artists': [
                {'external_urls': {'spotify': 'https://open.spotify.com/artist/7oPftvlwr6VrsViSDV7fJY'},
                 'href': 'https://api.spotify.com/v1/artists/7oPftvlwr6VrsViSDV7fJY', 'id': '7oPftvlwr6VrsViSDV7fJY',
                 'name': 'Green Day', 'type': 'artist', 'uri': 'spotify:artist:7oPftvlwr6VrsViSDV7fJY'}],
            'name': 'American Idiot'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/7oPftvlwr6VrsViSDV7fJY'},
             'href': 'https://api.spotify.com/v1/artists/7oPftvlwr6VrsViSDV7fJY', 'id': '7oPftvlwr6VrsViSDV7fJY',
             'name': 'Green Day', 'type': 'artist', 'uri': 'spotify:artist:7oPftvlwr6VrsViSDV7fJY'}],
            'name': 'American Idiot'}, 'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/7oPftvlwr6VrsViSDV7fJY'},
             'href': 'https://api.spotify.com/v1/artists/7oPftvlwr6VrsViSDV7fJY', 'id': '7oPftvlwr6VrsViSDV7fJY',
             'name': 'Green Day', 'type': 'artist', 'uri': 'spotify:artist:7oPftvlwr6VrsViSDV7fJY'}],
            'name': 'Jesus of Suburbia'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/7oPftvlwr6VrsViSDV7fJY'},
             'href': 'https://api.spotify.com/v1/artists/7oPftvlwr6VrsViSDV7fJY', 'id': '7oPftvlwr6VrsViSDV7fJY',
             'name': 'Green Day', 'type': 'artist', 'uri': 'spotify:artist:7oPftvlwr6VrsViSDV7fJY'}],
            'name': '21st Century Breakdown'},
            'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/7oPftvlwr6VrsViSDV7fJY'},
                'href': 'https://api.spotify.com/v1/artists/7oPftvlwr6VrsViSDV7fJY',
                'id': '7oPftvlwr6VrsViSDV7fJY',
                'name': 'Green Day',
                'type': 'artist',
                'uri': 'spotify:artist:7oPftvlwr6VrsViSDV7fJY'}],
            'name': '21 Guns'}}, {
            'track': {'album': {'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/0CEFCo8288kQU7mJi25s6E'},
                'href': 'https://api.spotify.com/v1/artists/0CEFCo8288kQU7mJi25s6E',
                'id': '0CEFCo8288kQU7mJi25s6E',
                'name': 'Hollywood Undead', 'type': 'artist',
                'uri': 'spotify:artist:0CEFCo8288kQU7mJi25s6E'}],
                'name': 'Notes From The Underground'}, 'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/0CEFCo8288kQU7mJi25s6E'},
                'href': 'https://api.spotify.com/v1/artists/0CEFCo8288kQU7mJi25s6E',
                'id': '0CEFCo8288kQU7mJi25s6E',
                'name': 'Hollywood Undead',
                'type': 'artist',
                'uri': 'spotify:artist:0CEFCo8288kQU7mJi25s6E'}],
                'name': 'We Are'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/0kD8IT1CzF7js2XKM9lLLa'},
             'href': 'https://api.spotify.com/v1/artists/0kD8IT1CzF7js2XKM9lLLa', 'id': '0kD8IT1CzF7js2XKM9lLLa',
             'name': 'STARSET', 'type': 'artist', 'uri': 'spotify:artist:0kD8IT1CzF7js2XKM9lLLa'}], 'name': 'Vessels'},
            'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/0kD8IT1CzF7js2XKM9lLLa'},
                'href': 'https://api.spotify.com/v1/artists/0kD8IT1CzF7js2XKM9lLLa',
                'id': '0kD8IT1CzF7js2XKM9lLLa',
                'name': 'STARSET', 'type': 'artist',
                'uri': 'spotify:artist:0kD8IT1CzF7js2XKM9lLLa'}],
            'name': 'DIE FOR YOU'}}, {'track': {'album': {
            'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/6vwjIs0tbIiseJMR3pqwiL'},
                         'href': 'https://api.spotify.com/v1/artists/6vwjIs0tbIiseJMR3pqwiL',
                         'id': '6vwjIs0tbIiseJMR3pqwiL', 'name': 'Beartooth', 'type': 'artist',
                         'uri': 'spotify:artist:6vwjIs0tbIiseJMR3pqwiL'}], 'name': 'Disease'}, 'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/6vwjIs0tbIiseJMR3pqwiL'},
             'href': 'https://api.spotify.com/v1/artists/6vwjIs0tbIiseJMR3pqwiL', 'id': '6vwjIs0tbIiseJMR3pqwiL',
             'name': 'Beartooth', 'type': 'artist', 'uri': 'spotify:artist:6vwjIs0tbIiseJMR3pqwiL'}],
            'name': 'Disease'}}, {
            'track': {'album': {'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/00YTqRClk82aMchQQpYMd5'},
                'href': 'https://api.spotify.com/v1/artists/00YTqRClk82aMchQQpYMd5',
                'id': '00YTqRClk82aMchQQpYMd5', 'name': 'Our Last Night',
                'type': 'artist',
                'uri': 'spotify:artist:00YTqRClk82aMchQQpYMd5'}],
                'name': 'Habits (Stay High) [Rock]'}, 'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/00YTqRClk82aMchQQpYMd5'},
                'href': 'https://api.spotify.com/v1/artists/00YTqRClk82aMchQQpYMd5',
                'id': '00YTqRClk82aMchQQpYMd5',
                'name': 'Our Last Night',
                'type': 'artist',
                'uri': 'spotify:artist:00YTqRClk82aMchQQpYMd5'}],
                'name': 'Habits (Stay High) - Rock'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/5BtHciL0e0zOP7prIHn3pP'},
             'href': 'https://api.spotify.com/v1/artists/5BtHciL0e0zOP7prIHn3pP', 'id': '5BtHciL0e0zOP7prIHn3pP',
             'name': 'Breaking Benjamin', 'type': 'artist', 'uri': 'spotify:artist:5BtHciL0e0zOP7prIHn3pP'}],
            'name': 'Phobia (Explicit Version)'},
            'artists': [{
                'external_urls': {
                    'spotify': 'https://open.spotify.com/artist/5BtHciL0e0zOP7prIHn3pP'},
                'href': 'https://api.spotify.com/v1/artists/5BtHciL0e0zOP7prIHn3pP',
                'id': '5BtHciL0e0zOP7prIHn3pP',
                'name': 'Breaking Benjamin',
                'type': 'artist',
                'uri': 'spotify:artist:5BtHciL0e0zOP7prIHn3pP'}],
            'name': 'Dance With The Devil'}},
        {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/10Z7WzKMeIdNBKexi1YarP'},
             'href': 'https://api.spotify.com/v1/artists/10Z7WzKMeIdNBKexi1YarP',
             'id': '10Z7WzKMeIdNBKexi1YarP', 'name': 'Fame on Fire', 'type': 'artist',
             'uri': 'spotify:artist:10Z7WzKMeIdNBKexi1YarP'}], 'name': 'Heavy (feat. Rain Paris)'},
            'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/10Z7WzKMeIdNBKexi1YarP'},
                'href': 'https://api.spotify.com/v1/artists/10Z7WzKMeIdNBKexi1YarP',
                'id': '10Z7WzKMeIdNBKexi1YarP', 'name': 'Fame on Fire',
                'type': 'artist', 'uri': 'spotify:artist:10Z7WzKMeIdNBKexi1YarP'}, {
                'external_urls': {
                    'spotify': 'https://open.spotify.com/artist/10TCOjSPs9ywBN1Q083BnB'},
                'href': 'https://api.spotify.com/v1/artists/10TCOjSPs9ywBN1Q083BnB',
                'id': '10TCOjSPs9ywBN1Q083BnB', 'name': 'Rain Paris',
                'type': 'artist', 'uri': 'spotify:artist:10TCOjSPs9ywBN1Q083BnB'}],
            'name': 'Heavy (feat. Rain Paris)'}}, {'track': {'album': {'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/6XyY86QOPPrYVGvF9ch6wz'},
             'href': 'https://api.spotify.com/v1/artists/6XyY86QOPPrYVGvF9ch6wz', 'id': '6XyY86QOPPrYVGvF9ch6wz',
             'name': 'Linkin Park', 'type': 'artist', 'uri': 'spotify:artist:6XyY86QOPPrYVGvF9ch6wz'}],
            'name': 'Minutes to Midnight'},
            'artists': [{'external_urls': {
                'spotify': 'https://open.spotify.com/artist/6XyY86QOPPrYVGvF9ch6wz'},
                'href': 'https://api.spotify.com/v1/artists/6XyY86QOPPrYVGvF9ch6wz',
                'id': '6XyY86QOPPrYVGvF9ch6wz',
                'name': 'Linkin Park',
                'type': 'artist',
                'uri': 'spotify:artist:6XyY86QOPPrYVGvF9ch6wz'}],
            'name': "Valentine's Day"}}],
    'total': 307}


def cleanup_playlist(playlist_raw=None):
    """
    Cleans up unnecessary cruft from spotify playlist objects like urls, thumbnails, added_at etc :param
    playlist_raw: raw Spotify playlist object :return: Cleaned up list of tracks in provided playlist. Each item
    contains the track's TITLE, ALBUM, ALBUMARTIST and ARTIST
    """
    print("Received ", type(playlist_raw))

    def get_artist(artist_list=None):
        """
        Helper to lookup all available artists
        :param artist_list:
        :return: Either a string or a list of artists
        """
        if len(artist_list) == 1:
            alist = artist_list[0]['name']
        else:
            alist = []
            for artist in artist_list:
                alist.append(artist['name'])
        print(f"Artists list: {alist}")
        return alist

    cleaned_playlist = []
    for item in playlist_raw['items']:
        track = dict()
        track['TITLE'] = item['track']['name']
        track['ALBUM'] = item['track']['album']['name']
        track['ALBUMARTIST'] = get_artist(item['track']['album']['artists'])
        track['ARTIST'] = get_artist(item['track']['artists'])
        cleaned_playlist.append(track)
    return cleaned_playlist
