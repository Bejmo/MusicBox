from download_music import descargar_musica
from yt_dlp import YoutubeDL
import os
from paths import PATHS

url_file = ""
url_file_name = "terminal_input"

"""
Downloads the new songs of the playlist (the ones that are now downloaded on the devide)
"""
def update_playlist(url):
    # Options yt-dlp
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
        'restrictfilenames': True,
        'outtmpl': '%(title)s__%(id)s', #  TODO Antes: os.path.join(PATHS['download_folder'], '%(title)s__%(id)s.%(ext)s')
    }

    # Execute yt-dlp
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

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
            PATHS['download_folder'] = os.path.join(PATHS['download_folder'], playlist_name)

            entries = info['entries']
            urls = []
            for entry in entries:
                file_name = ydl.prepare_filename(entry)
                file_path = os.path.join(PATHS['download_folder'], f"{file_name}.mp3")

                # If it is now downloaded, it is added to the URL's that will be downloaded
                if not os.path.exists(file_path):
                    print(f"Se descargará la canción: {file_name}")
                    urls.append(entry['url'])
            print()


            # Writes the URL's songs of the playlist in the file f"{url_file_name}_{i}.txt"
            for i in range(100):
                if not os.path.exists(f'{url_file_name}_{i}.txt'):
                    with open(f'{url_file_name}_{i}.txt', 'w') as file:
                        for url in urls:
                            file.write(url + '\n')
                    global url_file
                    url_file = f"{url_file_name}_{i}.txt"
                    break
        
        else: # It is a song
            song_name = info.get('title', 'unknown_title')
            print(f"Se descargará la canción: {song_name}")
            descargar_musica(url)
            return "not_a_playlist"

        return playlist_name

def terminal():
    with open(url_file, 'r') as file:
        list_urls = file.readlines()
    os.remove(url_file)
    
    for url in list_urls:
        url = url.split("\n")[0] # Delete the final \n that the url has (in order to print it well)
        try:
            name = descargar_musica(url)
            print(f"Se ha descargado la canción: {name}")
        except:
            print(f"ERROR - No se ha podido descargar la canción con URL: {url}. Más información en el fichero \"error_logs_unavailable.txt\"")

def main():
    # Input user
    url = input("Introduzca la URL (de la playlist o la canción): ")

    # Computations
    playlist_name = update_playlist(url)
    if playlist_name == "not_a_playlist":
        print("Se ha finalizado la descarga de la canción.")
    else:
        terminal()
        print(f"Se ha finalizado la actualización de la playlist {playlist_name}")

if __name__ == "__main__":
    main()