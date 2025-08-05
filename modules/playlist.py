# This file contains the main functions for managing playlists #

from download_music import descargar_musica
from yt_dlp import YoutubeDL
from paths import PATHS
import os
import csv

# Structs and global variables
# Global variables to store the name of the file that contains the url's of the songs to download
DATABASE_FILE_NAME = "playlists.csv"
URL_FILE = ""
URL_FILE_NAME = "terminal_input"

class Playlist:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __repr__(self):
        return f"Playlist(name={self.name}, url={self.url})"


# Playlist functions #

"""
Changes the download path to the path with the name of the given playlist.
PRE: The url is a playlist.
"""
def change_download_path(url):
    playlist_name = get_playlist_name(url)
    PATHS['download_folder'] = os.path.join(PATHS['original_folder'], playlist_name)

"""
Returns the name of the playlist. You can give the ydl command, in order to don't create more requests.
If it's not a playlist, returns NONE.
PRE: The url is a playlist.
"""
def get_playlist_name(url, ydl):
    if not ydl:
        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'force_generic_extractor': True,
            'restrictfilenames': True,
            'outtmpl': '%(title)s__%(id)s'
        }
        with YoutubeDL(ydl_opts) as ydl:
            return get_playlist_name(url, ydl)

    else:
        info = ydl.extract_info(url, download=False)
        if 'entries' in info: # If it is a playlist
            return i.get('title', 'no_name')
        return "NONE"

"""
Downloads the new songs of the playlist (the ones that are not downloaded on the devide)
"""
def get_new_songs(url):
    # Options yt-dlp
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
        'restrictfilenames': True,
        'outtmpl': '%(title)s__%(id)s',
    }

    # Execute yt-dlp
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
        except Exception as e:
            print(f"Error extracting info: {e}")
            raise Exception("Failed to extract information from the URL.")
            return "not_a_playlist"

        if 'entries' in info: # It is a playlist
            """
            Format of "info":

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

            # Set download_folder's name
            playlist_name = info.get('title', 'no_name') # Gets the playlist name (if not, returns "no_name")
            print(f"Se iniciará la actualización de la playlist {playlist_name}")
            PATHS['download_folder'] = os.path.join(PATHS['original_folder'], playlist_name)

            entries = info['entries']
            urls = []
            for entry in entries:
                file_name = ydl.prepare_filename(entry)
                file_path = os.path.join(PATHS['download_folder'], f"{file_name}.mp3")

                # If it is now downloaded, it is added to the URL's that will be downloaded
                if not os.path.exists(file_path):
                    print(f"Se descargará la canción: {file_name}")
                    urls.append(entry['url'])

            # Writes the URL's songs of the playlist in the file f"{URL_FILE_NAME}_{i}.txt"
            for i in range(100):
                if not os.path.exists(f'{URL_FILE_NAME}_{i}.txt'):
                    with open(f'{URL_FILE_NAME}_{i}.txt', 'w') as file:
                        for url in urls:
                            file.write(url + '\n')
                    global URL_FILE
                    URL_FILE = f"{URL_FILE_NAME}_{i}.txt"
                    break
        
        else: # It is a song
            song_name = info.get('title', 'unknown_title')
            print(f"Se descargará la canción: {song_name}")
            descargar_musica(url)
            return "not_a_playlist"

        return playlist_name

"""
Deletes the songs download locally that are not in the playlist
"""
def delete_old_songs(url):
    PATHS['download_folder'] = os.path.join(PATHS['original_folder'], playlist_name)

    # Recorrer canciones descargadas
    downloaded_songs = os.listdir(PATHS['download_folder'])
    for song in downloaded_songs:
        song_name, _ = os.path.splitext(song)  # Remove file extension
        song_url = f"https://www.youtube.com/watch?v={song_name}"  # Construct URL based on song name
        if song_url not in urls:
            print(f"Eliminando canción: {song}")
            os.remove(os.path.join(PATHS['download_folder'], song))

        # Verificar que la canción está en la playlist

        # Si no lo está, eliminar


"""
Updates all the saved playlists.
"""
def update_all_playlists():
    # Read all the saved playlists
    playlists = get_playlists()

    for playlist in playlists:
        url = playlist.url
        download_playlist(url)

"""
Downloads the files.
"""
def download():
    with open(URL_FILE, 'r') as file:
        list_urls = file.readlines()
    os.remove(URL_FILE)
    
    for url in list_urls:
        url = url.split("\n")[0] # Delete the final \n that the url has (in order to print it well)
        try:
            name = descargar_musica(url)
            print(f"Se ha descargado la canción: {name}")
        except:
            print(f"ERROR - No se ha podido descargar la canción con URL: {url}. Más información en el fichero \"error_logs_unavailable.txt\"")

"""
Downloads the playlist given its url.
Returns True if it is a playlist, False otherwise.
"""
def download_playlist(url):
    playlist_name = get_new_songs(url)
    if playlist_name == "not_a_playlist":
        print("Se ha finalizado la descarga de la canción.")
        return # TODO PUEDE QUE FALLE (si falla, poner "")

    download()
    print(f"Se ha finalizado la actualización de la playlist {playlist_name}")
    return playlist_name





# DATABASE FUNCTIONS #

"""
Returns the playlists saved in memory as a list.
"""
def get_playlists():
    playlists = []
    if os.path.exists(DATABASE_FILE_NAME): # If exists, it uses it
        with open(DATABASE_FILE_NAME, "r", newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                playlist = Playlist(row["nombre_playlist"], row["url"])
                playlists.append(playlist)
    else: # Create the file if it doesn't exist
        with open(DATABASE_FILE_NAME, "w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["nombre_playlist","url"])
            writer.writeheader()

    return playlists

"""
Deletes the playlist in the "i" row
"""
def delete_playlist(i):
    # Read all the rows except from the ones that we want to delete
    new_rows = []
    with open(DATABASE_FILE_NAME, "r", newline='') as f:
        reader = csv.DictReader(f)
        j = 1
        for row in reader:
            if i != j: new_rows.append(row)
            j += 1

    print("Se ha eliminado la playlist seleccionada.")

    # Overwrite the file
    with open(DATABASE_FILE_NAME, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["nombre_playlist", "url"])
        writer.writeheader()
        writer.writerows(new_rows)

"""
Checks if the playlist is already in the database
"""
def playlist_in_database(url):
    with open(DATABASE_FILE_NAME, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["url"] == url: return True
    return False

"""
Saves the playlist with the given name and url
PRE: The url can't already be in the playlist
"""
def save_playlist(name_playlist, url):
    with open(DATABASE_FILE_NAME, "a", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["nombre_playlist","url"])
        # We have to write the header if the file does not exists or has nothing inside.
        if not os.path.exists(DATABASE_FILE_NAME) or os.path.getsize(DATABASE_FILE_NAME) == 0:
            writer.writeheader()
        writer.writerow({"nombre_playlist": name_playlist, "url": url})