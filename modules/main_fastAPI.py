from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
# ZIP
import shutil
# JSON data
from pydantic import BaseModel
from typing import List
# Files
from download_music import descargar_musica
from playlist import *
from global_variables import PATHS
import tempfile # Temporal files
import os

app = FastAPI()

def cleanup_temp_dir(path: str): 
    shutil.rmtree(path, ignore_errors=True)

class PetitionPlaylist(BaseModel):
    url: str
    downloaded_files: List[str]

class PetitionURL(BaseModel):
    url: str

@app.post("/download_video/")
async def download_video_api(background_tasks: BackgroundTasks, data: PetitionURL):
    """
    Downloads the song from an URL.
    """
    url = data.url
    PATHS['original_folder'] = tempfile.mkdtemp()
    try:
        ruta = descargar_musica(url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


    # Si la función devuelve solo el nombre, construir la ruta completa
    if not os.path.isabs(ruta):
        ruta = os.path.join(PATHS['download_folder'], ruta)

    # Comprobar que existe
    if not os.path.exists(ruta):
        cleanup_temp_dir(PATHS['original_folder'])
        return {"error": f"El archivo no existe en {ruta}"}

    # Limpiar temp_dir después
    background_tasks.add_task(cleanup_temp_dir, PATHS['original_folder'])

    # Devolver el archivo
    return FileResponse(path=ruta, filename=os.path.basename(ruta), media_type="audio/mpeg")


@app.post("/get_songs_playlist/")
async def get_songs_playlist_api(data: PetitionPlaylist):
    """
    Returns a list with all the url's of the playlist
    """
    url = data.url
    downloaded_files = data.downloaded_files

    try:
        urls = get_songs_playlist(url, downloaded_files)
    except NotAPlaylistError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return urls


@app.post("/get_playlist_name/")
async def get_playlist_name_api(data: PetitionURL):
    """
    Returns a list with all the url's of the playlist
    """
    url = data.url
    try:
        playlist_name = get_playlist_name(url)
    except NotAPlaylistError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    return playlist_name