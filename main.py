from bs4 import BeautifulSoup
import requests

# DATE = input("Which year would you like to travel back to? Type the date in this format YYYY-MM-DD:")

response = requests.get(f"https://www.billboard.com/charts/hot-100/2012-08-04")

soup = BeautifulSoup(response.text, 'html.parser')

#------------------LONGER WAY HERE VVV------------------------------
# song_titles = []
# for song in song_title:
#     print(song_titles.append(song.getText()))


song_title = soup.find_all('span', class_='chart-element__information__song text--truncate color--primary')
song_titles = [song.getText() for song in song_title]
print(song_titles)

