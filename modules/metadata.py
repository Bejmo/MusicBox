from mutagen.easyid3 import EasyID3

from download_thumnails import *
import os

"""
Modifica la metadata de un archivo de audio.
Modificar el título, artista, álbum y fecha de lanzamiento.
"""
def modificar_metadata(archivo, info):
    if not os.path.isfile(archivo):
        print(f"El archivo {archivo} no existe.")
        return

    titulo = "NO HAY TITULO"
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

    # Modificar metadata
    try:
        audio = EasyID3(archivo)
    except: # TODO NO ESTA TESTEADO ESTA PARTE
        print("Error al guardar los metadatos.")
        with open("error_logs_not_saved.txt", 'a') as f:
            f.write(f"No se ha guardado: {titulo} \n")
    
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

    try:
        audio.save()
    except: # TODO NO ESTA TESTEADO ESTA PARTE
        print("Error al guardar los metadatos.")
        with open("error_logs_not_saved.txt", 'a') as f:
            f.write(f"No se ha guardado (.save): {titulo} \n")


    # Añadir carátula
    download_thumnail(info['id'], archivo)