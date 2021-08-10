import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3

DATABASE_LOCATION = "sqlite:///my_plyaed_tracks.sqlite"
USER_ID = "31d3azkkli57h3nsszrzq2af37x4"
TOKEN = "BQC6C62KBUrOgW0K7QYYomEW2HSENLXEh3MLAIIPSOY9H9U4NhtQkrR68CCQsuLc_oU4tGhsj1hW5Ybvodi6_qZAkGPdYlKXfZfLyf13ZvnJEWLIlHJe6TdGIBE_0jBn6gH29Y5cHwz3iAL0lMO4eS9OhbEPlbKx-aFFeRMo"
if __name__ == "__main__":

    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }

    # convert time to Unix timestamp in miliseconds
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    # Download all songs you've listened to after yesterday -> in the last 24 hours
    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp), headers = headers)

    data = r.json()
    
    
    '''
        buat list untuk menyimpan etracted data, 
        dipilih informasi yang dibutuhkan saja dari JSON object
    '''
    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])

    

    """
        buat dictionary untuk pandas dataframe
        sebagai representasi kolom tabel nanti. 
    """
    song_dict = {
        "song_name" : song_names,
        "artist_name" : artist_names,
        "played_at" : played_at_list,
        "timestamp" : timestamps
    }

    song_df = pd.DataFrame(song_dict, columns=["song_name", "artist_name", "played_at", "timestamp"])

    print(song_df)

