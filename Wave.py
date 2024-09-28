from desktop.WaveGui import initiate_ui
from backend.mediaplayer import MediaPlayer

if __name__=="__main__":
    player = MediaPlayer()
    player.load_media('backend/song.mp3')
    initiate_ui(player)