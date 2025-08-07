from playlist import *

# INPUT FUNCTIONS

"""
Asks the user if they want to save the used playlist
PRE: The given playlist can't be in memory (to avoid duplicated playlists in memory)
"""
def ask_if_save_playlist(name_playlist, url):
    response = ""
    allowed_values = ["S", "s", "N", "n"]
    while not response in allowed_values:
        if response != "": print("Valor inválido. Vuelva a intentarlo")
        response = input("Quiere guardar la playlist usada? (s/n) ")

    if response == "S" or response == "s":
        save_playlist(name_playlist, url)

"""
Main function
"""
def main():
    # Read saved playlists
    playlists = get_playlists()

    # No playlists found, then we use it normally
    if not playlists:
        url = input("Introduzca la URL (de la playlist o la canción): ")
        name_playlist = download_playlist(url)
        if name_playlist and not playlist_in_database(url): ask_if_save_playlist(name_playlist, url)

    # Exists saved playlists
    else:
        num_playlists = len(playlists)

        # Select if the user wants to use a saved playlist
        init = -3
        i = init
        first = True # This is for making a print when the user puts an invalid input
        while i < -2 or i > num_playlists:
            if not first: print("Número inválido. Vuelva a intentarlo.")
            else:
                first = False
                print("Opciones extra:")
                print("-2: Eliminar playlist existente")
                print("-1: Actualizar todas las playlists")
                print("0: Introducir URL manualmente")

                print("Playlists guardadas: ")
                i = 0
                for playlist in playlists:
                    print(f"{i + 1}: {playlist.name}")
                    i += 1
            try:
                i = int(input("Seleccione el índice de la playlist a actualizar: "))
            except ValueError: i = init

        # The user wants to delete an existing playlist
        if i == -2:
            print("Playlists guardadas: ")
            j = 0
            for playlist in playlists:
                print(f"{j + 1}: {playlist.name}")
                j += 1

            first = True
            while i < 1 or i > num_playlists:
                if not first: print("Índice inválido")
                else: first = False
                try:
                    i = int(input("¿Qué playlist desea eliminar?: "))
                except ValueError: i = -2

            delete_playlist(i, playlist.name)

        # The user wants to update all the saved playlists
        elif i == -1:
            print("Se actualizarán todas las playlist.")
            update_all_playlists()

        # The user wants to use a new playlist
        elif i == 0:
            url = input("Introduzca la URL (de la playlist o la canción): ")
            name_playlist = download_playlist(url)
            if name_playlist and not playlist_in_database(url): ask_if_save_playlist(name_playlist, url)
        
        # The user wants to use a saved playlist
        else:
            url = playlists[i - 1].url
            download_playlist(url)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSe ha detenido el programa.")