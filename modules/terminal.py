from download_music import descargar_musica
from yt_dlp import YoutubeDL

def actualizar_playlist(playlist_url, num):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
        if 'entries' in info:
            urls = [entry['url'] for entry in info['entries'][:int(num)]]
            with open('terminal_input.txt', 'w') as file:
                for url in urls:
                    file.write(url + '\n')

def terminal():
    with open('terminal_input.txt', 'r') as file:
        list_urls = file.readlines()
    for url in list_urls:
        descargar_musica(url.strip())


playlist_url = input("Playlist: ")
num = input("Numero de canciones a descargar: ")
actualizar_playlist(playlist_url, num)
terminal() 