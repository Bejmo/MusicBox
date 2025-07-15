from download_music import descargar_musica
from yt_dlp import YoutubeDL
import os
from paths import PATHS

url_file = ""
url_file_name = "terminal_input"

"""
Downloads the new songs of the playlist (the ones that are now downloaded on the devide)

Pre: (IMPORTANT) The YouTube playlist MUST be sorted by date of inclusion to the playlist if we want to update it correctly.
"""
def update_playlist(playlist_url):
    # Options yt-dlp
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
        'restrictfilenames': True
    }

    # Execute yt-dlp
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)

        # Set download_folder's name
        playlist_name = info.get('title', 'no_name') # Gets the playlist name (if not, returns "no_name")
        PATHS['download_folder'] = os.path.join(PATHS['download_folder'], playlist_name)
        if 'entries' in info:
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

            entries = info['entries']
            urls = []
            for entry in entries:
                file_name = ydl.prepare_filename(entry)
                file_name = f"{file_name.rsplit('-[', 1)[0].strip()}.mp3" # TODO antes: file_name = f"{file_name.split('-')[0].strip()}.mp3"

                file_path = os.path.join(PATHS['download_folder'], file_name)

                print(f"FILE PATH: {file_path}") # TODO

                # If it is now downloaded, it is added to the URL's that will be downloaded
                if not os.path.exists(file_path): urls.append(entry['url'])
                else: print("NO SE HA AÑADIDO PORQUE YA ESTA") # TODO
                print("\n")


            # Writes the URL's songs of the playlist in the file f"{url_file_name}_{i}.txt"
            for i in range(100):
                if not os.path.exists(f'{url_file_name}_{i}.txt'):
                    with open(f'{url_file_name}_{i}.txt', 'w') as file:
                        for url in urls:
                            file.write(url + '\n')
                    global url_file
                    url_file = f"{url_file_name}_{i}.txt"
                    break


"""
Downloads the first "num_downloads" songs of the playlist.
If "num_downloads" is not used, it downloads the whole playlist.
"""
# TODO Falta por modificar (hay que ponerlo igual que la función de "update")
def download_playlist(playlist_url, num_downloads=False):
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
            if num_downloads: entries = entries[:int(num_downloads)] # Take the first "num_downloads" songs

            urls = [entry['url'] for entry in entries]

            # Writes the URL's songs of the playlist (only the first "num_downloads" songs) in the file "terminal_input.txt"
            with open('terminal_input.txt', 'w') as file:
                for url in urls:
                    file.write(url + '\n')

def terminal():
    with open(url_file, 'r') as file:
        list_urls = file.readlines()
    os.remove(url_file)
    
    for url in list_urls:
        descargar_musica(url.strip())

def main():
    # Paths (mobile)
    dir = os.path.dirname(__file__)
    out_dir = os.path.dirname(dir)
    path_AIMP = os.path.join(out_dir, "AIMP")
    PATHS['download_folder'] = path_AIMP

    # Input user
    playlist_url = input("Playlist: ")
    # num = input("Numero de canciones a descargar: ") # TODO

    # Compute
    update_playlist(playlist_url)
    terminal()

if __name__ == "__main__":
    main()