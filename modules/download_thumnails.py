import os
import requests
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
from io import BytesIO
from PIL import Image

"""
Descarga la miniatura del "video" en "imagen"
"""
def descargar_miniatura_y_redimensionar(video_id, imagen):
    # DESCARGAR MINIATURA #
    try:
        # Obtener la URL de la miniatura
        # miniatura_url = video.thumbnail_url
        miniatura_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        
        # Descargar la imagen
        response = requests.get(miniatura_url)
        
    except Exception as e:
        print(f"Error: {e}")

    # REDIMENSIONAR #

    # Calcular el tamaño del recorte (cuadrado)
    img = Image.open(BytesIO(response.content))
    width, height = img.size
    min_dimension = min(width, height)
    left = (width - min_dimension) / 2
    top = (height - min_dimension) / 2
    right = (width + min_dimension) / 2
    bottom = (height + min_dimension) / 2

    # Recortar la imagen a un cuadrado
    img_cuadrada = img.crop((left, top, right, bottom))

    # Redimensionar la imagen a 500x500 píxeles
    img_redimensionada = img_cuadrada.resize((500, 500))

    img_redimensionada.save(imagen)

"""
Añade la miniatura descargada al archivo .mp3
"""
def agregar_miniatura_a_mp3(mp3_path, image_path):
    try:
        # Cargar el archivo .mp3 y su metadata
        audio = MP3(mp3_path, ID3=ID3)

        # Si el archivo no tiene una etiqueta ID3, se la añadimos
        try:
            audio.add_tags()
        except error:
            pass

        # Cargar la imagen descargada
        with open(image_path, 'rb') as img:
            # Añadir la imagen a la metadata del archivo .mp3
            audio.tags.add(
                APIC(
                    encoding=3,  # UTF-8
                    mime='image/jpeg',  # Tipo MIME de la imagen
                    type=3,  # Tipo 3 es la portada frontal
                    desc='Cover',
                    data=img.read()  # Cargar los datos de la imagen
                )
            )

        # Guardar los cambios en el archivo .mp3
        audio.save()
        # print(f'Miniatura añadida a {mp3_path}') # TODO PRINT OPCIONAL

    except Exception as e:
        print(f'Error al agregar la miniatura a {mp3_path}: {e}')

"""
Elimina la imagen en "image_path"
"""
def eliminar_imagen(image_path):
    try:
        os.remove(image_path)
        # print(f'Imagen {image_path} eliminada.') # TODO PRINT OPCIONAL
    except Exception as e:
        print(f'Error al eliminar {image_path}: {e}')


"""
Descarga la miniatura del video con "video_id" y la añade al archivo .mp3 con nombre "archivo_mp3"
(FUNCIÓN QUE SE LLAMA DESDE funciones_yt.py)
"""
def download_thumnail(video_id, archivo_mp3):
    carpeta = os.path.dirname(archivo_mp3)
    nombre_archivo, _ = os.path.splitext(archivo_mp3) # Quita la extensión
    ruta_imagen = os.path.join(carpeta, f'{nombre_archivo}.jpg')

    # Descargar la miniatura y redimensionar
    descargar_miniatura_y_redimensionar(video_id, ruta_imagen)

    # Agregar la miniatura al archivo .mp3
    ruta_mp3 = os.path.join(carpeta, archivo_mp3)
    agregar_miniatura_a_mp3(ruta_mp3, ruta_imagen)

    # Eliminar la miniatura después de haberla añadido al archivo .mp3
    eliminar_imagen(ruta_imagen)

if __name__ == "__main__":
    video_id = input("Introduzca el ID del video: ")
    archivo_mp3 = input("Introduzca el nombre del archivo .mp3: ")
    download_thumnail(video_id, archivo_mp3)