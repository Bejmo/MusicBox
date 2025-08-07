import os
from yt_dlp import YoutubeDL # type: ignore
from metadata import modificar_metadata
from global_variables import *

"""
Downloads the music from a YouTube Video
PRE: It can't be a playlist
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
        info = ydl.extract_info(url, download=True)
        try:
            file_path = ydl.prepare_filename(info)
            file_path = file_path.replace('.webm', '.mp3').replace('.m4a', '.mp3') # Change format
            modificar_metadata(file_path, info)
        except:
            with open("error_logs_unavailable.txt", "a") as log_file:
                log_file.write(f"Error al descargar el vídeo: [{url}]\n")
        finally:
            return os.path.basename(file_path) # Return the name of the file

if __name__ == "__main__":
    url = input("Ingrese la URL del vídeo (NO PUEDE SER UNA PLAYLIST): ")
    while url:
        descargar_musica(url)
        url = input("Ingrese la URL del vídeo (NO PUEDE SER UNA PLAYLIST): ")