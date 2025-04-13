import os
from yt_dlp import YoutubeDL
from metadata import modificar_metadata
from paths import PATHS
import requests

"""
Descarga la música de la url indicada
"""
def descargar_musica(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ignoreerrors': True,
        'outtmpl': os.path.join(PATHS['download_folder'], '%(title)s.%(ext)s'),
        'restrictfilenames': True  # Usar nombres de archivo seguros
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        
        if 'entries' in info:  # Es una playlist
            for entry in info['entries']:
                try:
                    # Se ejecuta modificar_metadata para cada archivo de la playlist
                    file_path = os.path.join(PATHS['download_folder'], entry['title'] + '.mp3')
                    modificar_metadata(file_path, entry)
                except Exception as e:
                    print(f'Error al modificar metadata de {file_path}: {e}')
                    continue
        else:  # Es un video
            file_path = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
            modificar_metadata(file_path, info)

if __name__ == "__main__":
    url = input("Ingrese la URL del video o playlist: ")
    while url:
        descargar_musica(url)
        url = input("Ingrese la URL del video o playlist: ")
