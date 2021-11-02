import base64
import requests
import datetime
import pandas as pd

class SpotifyAPI:
    client_id = None
    client_secret = None
    access_token = None

    token_url = 'https://accounts.spotify.com/api/token'
    base_url = 'https://api.spotify.com/v1/'

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def client_creds(self):
        client_id = self.client_id
        client_secret = self.client_secret

        if client_id == None or client_secret == None:
            raise Exception('You must set client_id and client_secret')

        client_creds = f'{client_id}:{client_secret}'
        client_creds_uft8 = client_creds.encode()
        client_creds_b64 = base64.b64encode(client_creds_uft8)
        return client_creds_b64.decode()

    def token_data(self):
        return {
            'grant_type':'client_credentials'
        }

    def token_header(self):
        client_creds = self.client_creds()
        return {
            'Authorization': f'Basic {client_creds}'
        }

    def get_token(self):
        token_url = self.token_url
        token_data = self.token_data()
        token_header = self.token_header()

        response = requests.post(token_url, data = token_data, headers = token_header)

        if response.status_code not in range(200,299):
            return False

        token_data = response.json()
        access_token = token_data['access_token']

        self.access_token = access_token

        return True

    '''
    Get Data
    '''

    def headers(self):
        access_token = self.access_token

        return {
            'Authorization': f'Bearer {access_token}'
        }

    def get_featured_playlist(self,timestamp):
        base_url = self.base_url
        headers = self.headers()

        #featured_playlists_endpoint = 'browse/featured-playlists/?limit=50'
        #featured_playlists_url = f'{base_url}{featured_playlists_endpoint}'
        featured_playlists_endpoint = 'browse/featured-playlists/?'
        q1 = 'limit=50'
        q2 = 'timestamp='+timestamp
        featured_playlists_url = f'{base_url}{featured_playlists_endpoint}?{q1}&{q2}'


        response = requests.get(featured_playlists_url,headers=headers)

        #List of dictionaries - one for each playlist
        return response.json()['playlists']['items']

    def get_playlist_details(self, playlist_id):
        base_url = self.base_url
        headers = self.headers()

        playlist_url_endpoint = f'playlists/{playlist_id}/tracks'
        playlist_url = f'{base_url}{playlist_url_endpoint}'

        playlist_response = requests.get(playlist_url, headers=headers)

        #Should return a list of dictionaries - one for each track
        return playlist_response.json()['items']

    def extract_track_details(self, track_info):
        track = track_info['track']

        if track == None:
            return ('','','','')

        track_name = track['name']
        track_id = track['id']
        track_pop = track['popularity']
        release_date = track['album']['release_date']

        artists = track['artists']

        lead_artist = artists[0]['name']
        artists.remove(artists[0])

        supporting_artists = ''
        for artist in artists:
            artist_name = artist['name']
            supporting_artists += f'{artist_name}, '

        return track_name,track_id,track_pop,release_date,lead_artist,supporting_artists

    def featured_songs(self,timestamp):
        featured_songs = {}

        featured_playlists_list = self.get_featured_playlist(timestamp)

        for playlist_info in featured_playlists_list:

            playlist_id = playlist_info['id']
            playlist_name = playlist_info['name']

            track_list = self.get_playlist_details(playlist_id)

            for track_info in track_list:

                track_name,track_id, track_pop,release_date, lead_artist, supporting_artists = self.extract_track_details(track_info)
                if track_id in featured_songs.keys():
                    continue
                featured_songs[track_id]=[timestamp[:4],track_name,track_pop,release_date, playlist_id, playlist_name,lead_artist,supporting_artists]

        return featured_songs
