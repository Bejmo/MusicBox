from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from download_music import descargar_musica
import os
from global_variables import PATHS

app = FastAPI()

@app.post("/generar_audio/")
async def generar_audio(url: str = Form(...)):
    # Carpeta temporal absoluta
    carpeta_tmp = os.path.abspath("tmp")
    os.makedirs(carpeta_tmp, exist_ok=True)

    # Decirle a tu script dónde guardar
    PATHS['download_folder'] = carpeta_tmp

    # Descargar el archivo (ruta completa)
    ruta = descargar_musica(url)

    # Si la función devuelve solo el nombre, construir la ruta completa
    if not os.path.isabs(ruta):
        ruta = os.path.join(carpeta_tmp, ruta)

    # Comprobar que existe
    if not os.path.exists(ruta):
        return {"error": f"El archivo no existe en {ruta}"}

    # Devolver el archivo
    return FileResponse(path=ruta, filename=os.path.basename(ruta), media_type="audio/mpeg")
