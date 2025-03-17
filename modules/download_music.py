import os
from modules.metadata import modificar_metadata
from data.paths import PATHS
from yt_dlp import YoutubeDL

"""
Descarga la música de la url indicada
"""
def descargar_video(url, imagen=False):
    formato = 'mp4' if imagen else 'mp3'

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': formato,
            'preferredquality': '192',
        }],
        'ignoreerrors': True,
        'outtmpl': os.path.join(PATHS['download_folder'], '%(title)s.%(ext)s'),
        'restrictfilenames': True  # Usar nombres de archivo seguros
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
    
    if 'entries' in info: # Es una playlist
        for entry in info['entries']:
            try:
                # Se ejecuta modificar_metadata para cada archivo de la playlist
                file_path = os.path.join(PATHS['download_folder'], entry['title'] + '.mp3')
                modificar_metadata(file_path, entry)
            except Exception as e:
                print(f'Error al modificar metadata de {file_path}: {e}')
                continue
    else: # Es un video
        modificar_metadata(file_path, info)

def descargar_playlist():
    pass

def actualizar_playlist():
    pass

def actualizar_path():
    pass



if __name__ == "__main__":
    url = input("Ingrese la URL del video o playlist: ")
    descargar_video(url)