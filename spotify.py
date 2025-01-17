import spotipy
from spotipy.oauth2 import SpotifyOAuth
import subprocess
import os
import json

# Spotify API kimlik bilgileri
SPOTIPY_CLIENT_ID = ''
SPOTIPY_CLIENT_SECRET = ''
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'

# Spotify API'sine bağlan
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope="playlist-read-private"))

# Oynatma listesi ID'lerini yükle
with open('Ids.json', 'r') as f:
    playlist_ids = json.load(f)

# Her oynatma listesi için işlemleri yap
for playlist_id in playlist_ids:
    # Oynatma listesindeki şarkıları al
    try:
        results = sp.playlist_tracks(playlist_id)
        tracks = results['items']
    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API hatası: {e}")
        continue

    # Oynatma listesi için bir klasör oluştur
    playlist_folder = os.path.join('downloads', playlist_id)
    os.makedirs(playlist_folder, exist_ok=True)

    # Her şarkıyı indir
    for item in tracks:
        track = item['track']
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        search_query = f"{track_name} {artist_name}"

        print(f"İndiriliyor: {track_name} - {artist_name}")

        # YouTube'dan MP3 indir
        subprocess.run([
            "./yt-dlp.exe",  # yt-dlp'nin tam yolu
            "-x",
            "--audio-format", "mp3",
            "--ffmpeg-location", "./ffmpeg/bin",  # ffmpeg'in tam yolu
            "--output", f"{playlist_folder}/%(title)s.%(ext)s",
            f"ytsearch:{search_query}"
        ])

print("İndirme işlemi tamamlandı.")