import os
from yt_dlp import YoutubeDL
from metadata import modificar_metadata
from paths import PATHS
import requests
import traceback

"""
Descarga la música de la url indicada
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
        'outtmpl': os.path.join(PATHS['download_folder'], '%(title)s.%(ext)s'),
        'restrictfilenames': True,  # Usar nombres de archivo seguros
        'no_warnings': True, # Evita warnings
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        
        try:    
            # TODO Pensar si hacerlo trambién para playlist
            # if 'entries' in info:  # Es una playlist
            #     for entry in info['entries']:
            #         try:
            #             # Se ejecuta modificar_metadata para cada archivo de la playlist
            #             file_path = os.path.join(PATHS['download_folder'], entry['title'] + '.mp3')
            #             modificar_metadata(file_path, entry)
            #         except Exception as e:
            #             print(f'Error al modificar metadata de {file_path}: {e}')
            #             continue
            # else:  # Es un video
            file_path = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
            modificar_metadata(file_path, info)
        except:
            with open("error_logs_unavailable.txt", "a") as log_file:
                log_file.write(f"Error al descargar el vídeo: [{url}]\n")

if __name__ == "__main__":
    url = input("Ingrese la URL del video o playlist: ")
    while url:
        descargar_musica(url)
        url = input("Ingrese la URL del video o playlist: ")
