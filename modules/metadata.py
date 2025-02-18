from mutagen.easyid3 import EasyID3

from modules.download_thumnails import *

"""
Modifica la metadata de un archivo de audio.
Modificar el título, artista, álbum y fecha de lanzamiento.
"""
def modificar_metadata(archivo, info):
    try:
        titulo = info.get('title', 'Desconocido')
    except: pass
    try:
        artista = info.get('artist', 'Desconocido')
    except: pass
    try:
        album = info.get('album', 'Desconocido')
    except: pass
    try:
        año = info.get('release_date', 'Desconocida')[:4]
    except: pass

    # Modificar metadata (igual que en tu código original)
    audio = EasyID3(archivo)
    try:
        audio['title'] = titulo
    except: pass
    try:
        audio['artist'] = artista
    except: pass
    try:
        audio['album'] = album
    except: pass
    try:
        audio['date'] = año
    except: pass
    audio.save()

    # Añadir carátula
    download_thumnail(info['id'], archivo)