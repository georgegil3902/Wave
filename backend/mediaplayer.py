import logging
import signal
import sys
import time
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl, QCoreApplication, QTimer
from PySide6.QtMultimedia import QMediaDevices

# Setup logging configuration to write to an external file
logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("media_player.log"),  # Log to external file
        logging.StreamHandler()  # Optionally, keep logging to the console
    ]
)

class MediaPlayer:
    def __init__(self):
        self.app = QCoreApplication.instance()  # Get existing instance or create a new one
        if self.app is None:
            self.app = QCoreApplication(sys.argv)  # Initialize the app only if it's not running
        self.audio_output = QAudioOutput(QMediaDevices.defaultAudioOutput())  # Create an audio output instance
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)  # Connect player to the audio output
        self.audio_output.setVolume(0.5)  # Set volume (0.0 to 1.0)
        logging.info("Media player initialized with default volume set to 50%")

        # Connect signals to track media status and errors
        self.player.mediaStatusChanged.connect(self.on_media_status_changed)
        self.player.errorOccurred.connect(self.on_media_error)

    def load_media(self, media_path):
        self.player.setSource(QUrl.fromLocalFile(media_path))
        logging.info(f"Media loaded: {media_path}")

    def play(self):
        if self.player.mediaStatus() == QMediaPlayer.NoMedia:
            logging.warning("Attempted to play but no media is loaded")
        else:
            self.player.play()
            logging.info("Playing media")
            logging.info(f"Current volume: {self.audio_output.volume() * 100}%")

    def pause(self):
        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.player.pause()
            logging.info("Pausing media")
        else:
            logging.warning("Attempted to pause but media is not playing")

    def stop(self):
        self.player.stop()
        logging.info("Stopping media")

    def setVolume(self, volume):
        # Volume is set between 0.0 (min) and 1.0 (max)
        self.audio_output.setVolume(volume / 100.0)
        logging.info(f"Volume set to: {volume}%")
        return True

    def getVolume(self):
        return int(self.audio_output.volume() * 100)
    
    def state(self):
        return self.player.playbackState()
    
    @property
    def PlayingState(self):
        return QMediaPlayer.PlayingState
    
    @property
    def PausedState(self):
        return QMediaPlayer.PausedState
    
    @property
    def StoppedState(self):
        return QMediaPlayer.StoppedState

    def on_media_status_changed(self, status):
        logging.info(f"Media status changed: {status}")
        if status == QMediaPlayer.EndOfMedia:
            logging.info("Media playback finished")
            self.app.quit()  # Exit event loop when media ends

    def on_media_error(self, error):
        logging.error(f"Media error occurred: {error}")
        self.app.quit()  # Exit event loop on error

    def quit(self):   
        logging.info("Quitting the application")
        self.app.quit()  # Gracefully quit the app and stop event loop


if __name__ == '__main__':

    player = MediaPlayer()
    player.load_media('backend/song.mp3')
    player.play()
