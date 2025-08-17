import os
from yt_dlp import YoutubeDL # type: ignore
from metadata import modificar_metadata
from global_variables import *

# Exceptions
class IsAPlaylistError(Exception):
    """
    The url introduced is a Playlist.
    """
    pass

"""
Downloads the music from a YouTube Video.
PRE: It can't be a playlist.
Raises IsAPlaylistError and FileNotFound.
"""
def descargar_musica(url):
    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ignoreerrors': True,
        'outtmpl': os.path.join(PATHS['download_folder'], f'%(title)s{SEPARATOR}%(id)s.%(ext)s'),
        'restrictfilenames': True,  # Use save filenames
        'no_warnings': True, # Delete warnings
        'no_fragment': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        if 'entries' in info and len(info['entries']) > 1: 
            raise IsAPlaylistError("El enlace indicado es una playlist.")
        
        try:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            file_path = file_path.replace('.webm', '.mp3').replace('.m4a', '.mp3').replace('.mp4', '.mp3') # Change format

            try:
                modificar_metadata(file_path, info)
            except FileNotFoundError as e:
                print(e)
                raise FileNotFoundError
        except:
            print(f"File path: {file_path}") #TODO
            with open("error_logs_unavailable.txt", "a") as log_file:
                log_file.write(f"Error al descargar el vídeo: [{url}]\n")
        finally:
            return os.path.basename(file_path) # Return the name of the file

if __name__ == "__main__":
    url = input("Ingrese la URL del vídeo (NO PUEDE SER UNA PLAYLIST): ")
    while url:
        descargar_musica(url)
        url = input("Ingrese la URL del vídeo (NO PUEDE SER UNA PLAYLIST): ")