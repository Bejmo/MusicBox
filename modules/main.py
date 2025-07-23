from download_music import descargar_musica
from yt_dlp import YoutubeDL
from paths import PATHS
import os
import csv

# Global variables to store the name of the file that contains the url's of the songs to download
url_file = ""
url_file_name = "terminal_input"


# Download playlist functions

"""
Downloads the new songs of the playlist (the ones that are now downloaded on the devide)
"""
def get_new_songs(url):
    # Options yt-dlp
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
        'restrictfilenames': True,
        'outtmpl': '%(title)s__%(id)s'
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

"""
Downloads the files.
"""
def download():
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


# INPUT FUNCTIONS

"""
Asks the user if they want to save the used playlist
"""
def ask_if_save_playlist(url, name_playlist):
    playlist_file_name = "playlists.csv"

    response = ""
    allowed_values = ["S", "s", "N", "n"]
    while not response in allowed_values:
        if response != "": print("Valor inválido. Vuelva a intentarlo")
        response = input("Quiere guardar la playlist usada? (s/n) ")

    if response == "S" or response == "s":
        with open(playlist_file_name, "a", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["nombre_playlist","url"])
            # We have to write the header if the file does not exists or has nothing inside.
            if not os.path.exists(playlist_file_name) or os.path.getsize(playlist_file_name) == 0:
                writer.writeheader()
            writer.writerow({"nombre_playlist": name_playlist, "url": url})

"""
Charges the playlists saved in memory previously
"""
def charge_playlists():
    playlist_file_name = "playlists.csv"

    playlists = []
    if os.path.exists(playlist_file_name): # If exists, it uses it
        with open(playlist_file_name, "r", newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                playlists.append([row["nombre_playlist"], row["url"]])
    else: # Create the file if it doesn't exist
        with open(playlist_file_name, "w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["nombre_playlist","url"])
            writer.writeheader()

    return playlists

"""
Deletes the playlist in the "i" row 
"""
def delete_playlist(i):
    playlist_file_name = "playlists.csv"

    # Read all the rows except from the ones that we want to delete
    new_rows = []
    with open(playlist_file_name, "r", newline='') as f:
        reader = csv.DictReader(f)
        j = 1
        for row in reader:
            if i != j: new_rows.append(row)
            j += 1

    # Overwrite the file
    with open(playlist_file_name, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["nombre_playlist", "url"])
        writer.writeheader()
        writer.writerows(new_rows)

"""
Downloads the playlist given its url.
Returns True if it is a playlist, False otherwise.
"""
def download_playlist(url):
    playlist_name = get_new_songs(url)
    if playlist_name == "not_a_playlist":
        print("Se ha finalizado la descarga de la canción.")
        return False

    download()
    print(f"Se ha finalizado la actualización de la playlist {playlist_name}")
    return playlist_name

"""
Main function
"""
def main():
    # Read saved playlists
    playlists = charge_playlists()

    # No playlists found, then we use it normally
    if not playlists:
        url = input("Introduzca la URL (de la playlist o la canción): ")
        name_playlist = download_playlist(url)
        if name_playlist: ask_if_save_playlist(url, name_playlist)

    # Exists saved playlists
    else:
        num_playlists = len(playlists)

        # Select if the user wants to use a saved playlist
        i = -2
        first = True # This is for making a print when the user puts an invalid input
        while i < -1 or i > num_playlists:
            if not first: print("Número inválido. Vuelva a intentarlo.")
            else:
                first = False
                print("Opciones extra:")
                print("-1: Eliminar playlist existente")
                print("0: Introducir playlist manualmente")

                print("Playlists guardadas: ")
                i = 0
                for playlist in playlists:
                    print(f"{i + 1}: {playlist[0]}")
                    i += 1
                    
            try:
                i = int(input("Seleccione el índice de la playlist a actualizar: "))
            except ValueError: i = -2

        # The user wants to delete an existing playlist
        if i == -1:
            print("Playlists guardadas: ")
            j = 0
            for playlist in playlists:
                print(f"{j + 1}: {playlist[0]}")
                j += 1

            first = True
            while i < 1 or i > num_playlists:
                if not first: print("Índice inválido")
                try:
                    i = int(input("¿Qué playlist desea eliminar?: "))
                except ValueError: i = -2

            delete_playlist(i)

        # The user wants to use a new playlist
        elif i == 0:
            url = input("Introduzca la URL (de la playlist o la canción): ")
            name_playlist = download_playlist(url)
            if name_playlist: ask_if_save_playlist(url, name_playlist)
         
        # The user wants to use a saved playlist
        else:
            url = playlists[i - 1][1]
            download_playlist(url)

if __name__ == "__main__":
    main()