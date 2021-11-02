import pandas as pd
from spotify_api import SpotifyAPI

client_id = '3818e4e25f4c430c822a0948f79791a7'
client_secret = '7ba09f5ff3a5432fb6a80b9183aa95db'

client = SpotifyAPI(client_id, client_secret)
client.get_token()

featured_songs = {}

for year in range(2010,2022):
    timestamp = str(year)+'-11-01T09:00:00'
    featured_songs_new = client.featured_songs(timestamp)
    featured_songs = featured_songs | featured_songs_new

df = pd.DataFrame.from_dict(featured_songs,orient='index',columns=['year featured','track_name','track_popularity','release_date','playlist_id', 'playlist_name','lead_artist','supporting_artists'])
df.to_csv('featured_playlist_songs.csv')
