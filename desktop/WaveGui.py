# Built in modules
import logging
import sys

# Externally installed modules
# PySide modules
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QMenuBar, QMenu,
    QSlider, QLabel, QProgressBar, QSpacerItem, QSizePolicy, QFileDialog, QWidget
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon


# Setup logging configuration
logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("desktop/wave_media_player.log"),  # Log to external file
        logging.StreamHandler()  # Optionally, keep logging to the console
    ]
)


class WaveGui(QMainWindow):
    def __init__(self, media_player=None) -> None:
        super().__init__()

        # Setup media player
        self.media_player = media_player

        # Window Setup
        self.setWindowTitle("Wave Media Player")
        self.setGeometry(100, 100, 600, 200)
        self.setStyleSheet('''
            background-color: #121212;
        ''')
        
        # Create central widget and set layout
        central_widget = QWidget(self)
        main_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # Create menubar
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        # Add 'Open' action under 'File' menu
        open_action = file_menu.addAction("Open")
        open_action.triggered.connect(self.open_file)

        # Media metadata (song title, artist, etc.)
        self.song_label = QLabel("Song Title - Artist Name")
        self.song_label.setAlignment(Qt.AlignCenter)
        self.song_label.setStyleSheet('color: #fff')
        main_layout.addWidget(self.song_label)

        # Progress bar for tracking media progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet('background-color: #000')
        main_layout.addWidget(self.progress_bar)

        # Layout for control buttons (Play, Pause, Stop)
        control_layout = QHBoxLayout()

        # Icons
        self.play_icon = QIcon("shared/icons/play.png")
        self.pause_icon = QIcon("shared/icons/pause.png")
        self.prev_icon = QIcon("shared/icons/prev.png")
        self.next_icon = QIcon("shared/icons/next.png")
        self.volume_high_icon = QIcon("shared/icons/volume-high.png")
        self.volume_low_icon = QIcon("shared/icons/volume-low.png")
        self.volume_mute_icon = QIcon("shared/icons/volume-mute.png")

        self.pushbutton_qss = ("""
        QPushButton {
            background-color: #1DE9B6;        /* Main background color */
            color: white;                     /* Text color */
            border: none;                     /* Remove default border */
            padding: 10px 20px;               /* Add padding */
            border-radius: 15px;              /* Rounded corners */
            font-size: 16px;                  /* Adjust font size */
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #14CBA8;        /* Darker background on hover */
        }

        QPushButton:pressed {
            background-color: #0FB89A;        /* Even darker background on press */
        }

        QPushButton:focus {
            outline: none;                    /* Remove focus border */
        }

        """)

        # Previous Button
        self.prev_button = QPushButton()
        self.prev_button.setIcon(self.prev_icon)
        self.prev_button.setFixedSize(40, 40)
        self.prev_button.setIconSize(QSize(24, 24))
        self.prev_button.setStyleSheet(self.pushbutton_qss)
        control_layout.addWidget(self.prev_button)

        # Play/Pause Button
        self.playpause_button = QPushButton()
        self.playpause_button.setIcon(self.play_icon)
        self.playpause_button.setFixedSize(40, 40)
        self.playpause_button.setIconSize(QSize(24, 24))
        self.playpause_button.setStyleSheet(self.pushbutton_qss)
        control_layout.addWidget(self.playpause_button)

        # Next Button
        self.next_button = QPushButton()
        self.next_button.setIcon(self.next_icon)
        self.next_button.setFixedSize(40, 40)
        self.next_button.setIconSize(QSize(24, 24))
        self.next_button.setStyleSheet(self.pushbutton_qss)
        control_layout.addWidget(self.next_button)

        # Spacer
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        control_layout.addItem(spacer)

        # Volume Button
        self.volume_button = QPushButton()
        self.volume_button.setIcon(self.volume_low_icon)
        self.volume_button.setFixedSize(40, 40)
        self.volume_button.setIconSize(QSize(24, 24))
        self.volume_button.setStyleSheet(self.pushbutton_qss)
        control_layout.addWidget(self.volume_button)

        # Volume Slider
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setFixedWidth(150)
        control_layout.addWidget(self.volume_slider)

        # Add control layout to main layout
        main_layout.addLayout(control_layout)

        # Button and slider connections
        self.playpause_button.clicked.connect(self.toggle_play_pause)
        self.prev_button.clicked.connect(self.prev)
        self.next_button.clicked.connect(self.next)
        self.volume_slider.valueChanged.connect(self.change_volume)
        self.volume_button.clicked.connect(self.toggle_mute)

        # Variables to handle volume state
        self.previous_volume = self.volume_slider.value()

    # Open file dialog to load media
    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Audio File", "", "Audio Files (*.mp3 *.wav *.ogg)")
        if file_name:
            logging.info(f"Selected file: {file_name}")
            self.song_label.setText(file_name)  # Update the label with the file name
            if self.media_player:
                self.media_player.load_media(file_name)
                logging.info(f"Loaded media: {file_name}")

    # Updated to logging from print
    def toggle_play_pause(self):
        logging.info("Clicked Play/Pause button")
        if self.media_player.state() == self.media_player.PlayingState:
            logging.info("Already playing, pausing")
            if self.media_player.pause():
                self.playpause_button.setIcon(self.play_icon)
                logging.info("Paused")
        elif self.media_player.state() == self.media_player.PausedState:
            logging.info("Already paused, resuming")
            if self.media_player.play():
                self.playpause_button.setIcon(self.pause_icon)
                logging.info("Playing")
        elif self.media_player.state() == self.media_player.StoppedState:
            logging.info("Loading media..., playing")
            if self.media_player.play():
                self.playpause_button.setIcon(self.pause_icon)
                logging.info("Playing")
        else:
            logging.error(f"Failed to toggle play/pause... Current State: {self.media_player.state()}")

    def prev(self):
        logging.info("Previous button clicked")

    def next(self):
        logging.info("Next button clicked")

    def change_volume(self, value):
        if self.media_player.setVolume(value):  # Assuming setVolume returns True if successful
            if value == 0:
                self.volume_button.setIcon(self.volume_mute_icon)
            elif value <= 50:
                self.volume_button.setIcon(self.volume_low_icon)
            else:
                self.volume_button.setIcon(self.volume_high_icon)
            logging.info(f"Volume set to {value}")
        else:
            logging.warning(f"Failed to set volume to {value}")

    def toggle_mute(self):
        current_volume = self.media_player.getVolume()  # Assuming getVolume retrieves the current volume
        if current_volume == 0:
            if self.media_player.setVolume(self.previous_volume):  # Restore previous volume
                self.volume_slider.setValue(self.previous_volume)
                logging.info(f"Volume restored to {self.previous_volume}")
        else:
            self.previous_volume = current_volume   # Save the current volume
            if self.media_player.setVolume(0):      # Mute
                self.volume_slider.setValue(0)
                logging.info("Muted")

def initiate_ui(media_player=None) -> None:
    app = QApplication(sys.argv)
    window = WaveGui(media_player)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    initiate_ui()
