import logging
import sys
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl
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
        self.audio_output = QAudioOutput(QMediaDevices.defaultAudioOutput())  # Create an audio output instance
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)  # Connect player to the audio output
        self.audio_output.setVolume(0.5)  # Set volume (0.0 to 1.0)
        logging.info("Media player initialized with default volume set to 50%")

        # Connect signals to track media status, duration, position, and errors
        self.player.mediaStatusChanged.connect(self.on_media_status_changed)
        self.player.errorOccurred.connect(self.on_media_error)
        self.player.durationChanged.connect(self.on_duration_changed)
        self.player.positionChanged.connect(self.on_position_changed)

        self._duration = 0
        self._position = 0

    def load_media(self, media_path):
        self.player.setSource(QUrl.fromLocalFile(media_path))
        logging.info(f"Media loaded: {media_path}")

    def play(self):
        if self.player.mediaStatus() == QMediaPlayer.NoMedia:
            logging.warning("Attempted to play but no media is loaded")
            return False
        else:
            self.player.play()
            logging.info("Playing media")
            logging.info(f"Current volume: {self.audio_output.volume() * 100}%")
            return True

    def pause(self):
        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.player.pause()
            logging.info("Pausing media")
            return True
        else:
            logging.warning("Attempted to pause but media is not playing")
            return False

    def stop(self):
        self.player.stop()
        logging.info("Stopping media")
        return True

    def setVolume(self, volume):
        self.audio_output.setVolume(volume / 100.0)
        logging.info(f"Volume set to: {volume}%")
        return True

    def getVolume(self):
        return int(self.audio_output.volume() * 100)
    
    def state(self):
        return self.player.playbackState()
    
    # Properties for the media states
    @property
    def PlayingState(self):
        return QMediaPlayer.PlayingState
    
    @property
    def PausedState(self):
        return QMediaPlayer.PausedState
    
    @property
    def StoppedState(self):
        return QMediaPlayer.StoppedState

    # Handle media duration change (set when media is loaded)
    def on_duration_changed(self, duration):
        self._duration = duration
        logging.info(f"Media duration set to: {duration} ms")

    # Handle media position change (triggered during playback)
    def on_position_changed(self, position):
        self._position = position
        logging.info(f"Media position updated: {position} ms")

    # Return the duration of the media
    def get_duration(self):
        return self._duration

    # Return the current position of the media
    def get_position(self):
        return self._position

    def on_media_status_changed(self, status):
        logging.info(f"Media status changed: {status}")
        if status == QMediaPlayer.EndOfMedia:
            logging.info("Media playback finished")
            self.stop()

    def on_media_error(self, error):
        logging.error(f"Media error occurred: {error}")
        self.stop()

    def quit(self):
        logging.info("Quitting the application")
        self.stop()

if __name__ == '__main__':
    player = MediaPlayer()
    player.load_media('backend/song.mp3')
    player.play()

    # Example to print media position and duration for 5 seconds
    import time
    for _ in range(5):
        print(f"Position: {player.get_position()} / {player.get_duration()} ms")
        time.sleep(1)
