from modules.download_music import descargar_musica

def terminal():
    url = input("Introduce la URL de la canción: ")
    descargar_musica(url)

list_urls = [
    "https://music.youtube.com/watch?v=ClygFI5zSWM&si=rdBxIJuLMDP-jAQa",
    "https://music.youtube.com/watch?v=Sb-01um7kBw&si=XjHP8Yw4C96Xp76k",
    "https://music.youtube.com/watch?v=Sb-01um7kBw&si=bYqO8-Xf07JxNtbc",
    "https://music.youtube.com/watch?v=gRr9Nj8T61s&si=VBSmAU-sacQCYbYN",
    "https://music.youtube.com/watch?v=ZyWprQkwYSA&si=S-2baS-dllExBzh9",
    "https://music.youtube.com/watch?v=kH90E3UYpd8&si=sA6Ha85_udQbvU_m",
    "https://music.youtube.com/watch?v=9ucJfFiT_L8&si=Vxt8hVQlr8D-T8tM",
    "https://music.youtube.com/watch?v=6ryriywY9Cg&si=Pnm89kW_UYndirWF",
    "https://music.youtube.com/watch?v=6ryriywY9Cg&si=PJBAwlv92ihIob9b",
    "https://music.youtube.com/watch?v=vqhreNlJD6s&si=4CtbBzOy8MEgaxL8",
    "https://music.youtube.com/watch?v=wKuENHUS82Y&si=3DzjI_QCxoTaIId7",
    "https://music.youtube.com/watch?v=qGhuebQB2hg&si=uLQunUE7UYXt_Uod",
    "https://music.youtube.com/watch?v=YCglf9t-AFE&si=hrNHHr9fdmrObK9Z",
    "https://music.youtube.com/watch?v=F4qv-_SKsvY&si=XpceCXVRW1tOpIFe",
    "https://music.youtube.com/watch?v=FdLusJ1qs8w&si=kkuKCBCh2BwUHv0J",
    "https://music.youtube.com/watch?v=FmcUr2FbEHQ&si=DBFvwFhvc0bn_xfg",
    "https://music.youtube.com/watch?v=m9LxvMIVBYk&si=6dvfDeHfWd7h21CI",
    "https://music.youtube.com/watch?v=BoCbm0pgQl4&si=b9s6gp7SYbNn_nwm",
    "https://music.youtube.com/watch?v=3VCY27vTULw&si=nxYVYPvJL_OSWSzJ",
    "https://music.youtube.com/watch?v=tQDh9RjpdMg&si=UKbr2xS4WGFww2ey",
    "https://music.youtube.com/watch?v=d__0UWxD5bg&si=2-48K6tsZRHj_hMh"
]

for url in list_urls:
    descargar_musica(url)
