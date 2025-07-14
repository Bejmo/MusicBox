from download_music import descargar_musica
from yt_dlp import YoutubeDL
import os
from paths import PATHS

def actualizar_playlist(playlist_url, num_downloads=False):
    # Options yt-dlp
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
    }

    # Execute yt-dlp
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)

        # Set download_folder's name
        playlist_name = info.get('title', 'no_name') # Gets the playlist name (if not, returns "no_name")
        PATHS['download_folder'] = os.path.join(PATHS['download_folder'], playlist_name)

        if 'entries' in info:
            """
            Formato de "info":

            info = {
                'id': 'PL123...',
                'title': 'Nombre de la playlist',
                'entries': [
                    {'id': 'abc123', 'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', 'title': 'DONT WATCH'},
                    {'id': 'def456', 'url': 'https://www.youtube.com/watch?v=def456', 'title': 'Video 2'},
                    ...
                ]
            }
            """

            entries = info['entries']
            # Filter number of entries
            if num_downloads: entries = entries[:int(num_downloads)]

            urls = [entry['url'] for entry in entries] # Take the first "num_downloads" songs

            # Writes the URL's songs of the playlist (only the first "num_downloads" songs) in the file "terminal_input.txt"
            with open('terminal_input.txt', 'w') as file:
                for url in urls:
                    file.write(url + '\n')

def terminal():
    with open('terminal_input.txt', 'r') as file:
        list_urls = file.readlines()
    for url in list_urls:
        descargar_musica(url.strip())


# Paths (mobile)
dir = os.path.dirname(__file__)
out_dir = os.path.dirname(dir)
path_AIMP = os.path.join(out_dir, "AIMP")
PATHS['download_folder'] = path_AIMP

# Input user
playlist_url = input("Playlist: ")
# playlist_name = input("Introduzca el nombre de la carpeta de la playlist: ")
num = input("Numero de canciones a descargar: ")

# Compute
actualizar_playlist(playlist_url, num)
terminal()