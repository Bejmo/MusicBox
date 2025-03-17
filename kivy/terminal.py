from modules.download_music import descargar_video

def terminal():
    with open('terminal_input.txt', 'r') as file:
        list_urls = file.readlines()
    for url in list_urls:
        descargar_video(url.strip())

terminal()
