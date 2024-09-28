from desktop.WaveGui import initiate_ui, WaveGui
from backend.mediaplayer import MediaPlayer

from PySide6.QtWidgets import QApplication
import sys


if __name__=="__main__":
    player = MediaPlayer()

    app = QApplication(sys.argv)
    ui = WaveGui(player)
    ui.show()

    player.load_media('backend/song.mp3')

    sys.exit(app.exec())