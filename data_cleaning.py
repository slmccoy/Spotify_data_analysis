!pip install pandas
!pip install pandasql
import pandas as pd
import pandasql as ps

file = 'C:/Users/sarah/github/Spotify_data_analysis/featured_playlist_songs.csv'
df = pd.read_csv(file)

df.dtypes
'''
Unnamed: 0            object
year featured          int64
track_name            object
track_popularity       int64
release_date          object
playlist_id           object
playlist_name         object
lead_artist           object
supporting_artists    object
dtype: object
'''

q = 'SELECT * FROM df LIMIT 5'
ps.sqldf(q,locals())

'''
Make track id the index/first column
Need to name first column 'track_id'
track_id, track_name, playlist_id, playlist_name, lead_artist, supporting_artist should be strings
realease date column as datetime

look for missing values and remove entries

Is there a link between realease date and featured year?
Go back and get track position in playlist and compare to track popularity
Highest appearing artist vs track track popularity
How often artists appear in the sporting artist
'''

df['release_date']= pd.to_datetime(df['release_date'],format='%y%m%d')

df.astype({
    'track_name':'string'
})
