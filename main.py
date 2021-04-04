from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint

pp = pprint.PrettyPrinter(sort_dicts=True)
SPOTIPY_CLIENT_ID = '2106a157fe8b4badb48d9a547cf009ce'
SPOTIPY_CLIENT_SECRET = '5aa102bb8e4345768db115743c5af17e'
SPOTIPY_REDIRECT_URI = 'http://example.com'

date = input("Which year would you like to travel back to? Type the date in this format YYYY-MM-DD:")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
soup = BeautifulSoup(response.text, 'html.parser')

scope = "playlist-modify-private"

#Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        show_dialog=True,
        cache_path='token.txt'
    )
)
user_id = sp.current_user()['id']

year = date.split("-")[0]

# ------------------LONGER WAY HERE VVV------------------------------
# song_titles = []
# for song in song_title:
#     print(song_titles.append(song.getText()))

song_title = soup.find_all('span', class_='chart-element__information__song text--truncate color--primary')
song_titles = [song.getText() for song in song_title]
# print(song_titles)

song_uris = []
for song in song_titles:
    result = sp.search(q=f"track:{song} year:{year}", type='track')
    pp.pprint(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#Creating a new private playlist in Spotify

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

#Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
