from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QSlider, QLabel, QProgressBar, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
import sys


class WaveGui(QWidget):
    def __init__(self) -> None:
        super().__init__()

        # Window Setup
        self.setWindowTitle("Wave Media Player")
        self.setGeometry(100, 100, 600, 200)
        self.setStyleSheet('''
            background-color: #121212;
        ''')

        # Create main layout
        main_layout = QVBoxLayout()

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

        # Push Button CSS
        self.pushbutton_css = '''
            QPushButton {
                background-color: #1DE9B6;
                border: none;
                border-radius: 25px;
            }
            QPushButton:hover {
                background-color: #14CBA8;
            }
            QPushButton:pressed {
                background-color: #0FB89A;
            }
        '''

        # Control Buttons
        self.prev_button = QPushButton()
        self.prev_button.setIcon(self.prev_icon)
        self.prev_button.setFixedSize(40, 40)
        self.prev_button.setIconSize(QSize(24, 24))
        self.prev_button.setStyleSheet(self.pushbutton_css)

        self.playpause_button = QPushButton()
        self.playpause_button.setIcon(self.play_icon)
        self.playpause_button.setFixedSize(40, 40)
        self.playpause_button.setIconSize(QSize(24, 24))
        self.playpause_button.setStyleSheet(self.pushbutton_css)

        self.next_button = QPushButton()
        self.next_button.setIcon(self.next_icon)
        self.next_button.setFixedSize(40, 40)
        self.next_button.setIconSize(QSize(24, 24))
        self.next_button.setStyleSheet(self.pushbutton_css)

        # Add control buttons to layout
        control_layout.addWidget(self.prev_button)
        control_layout.addWidget(self.playpause_button)
        control_layout.addWidget(self.next_button)

        # Add a spacer to push the volume controls to the right
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        control_layout.addItem(spacer)

        # Volume control
        self.volume_button = QPushButton()
        self.volume_button.setIcon(self.volume_low_icon)
        self.volume_button.setFixedSize(40, 40)
        self.volume_button.setIconSize(QSize(24, 24))
        self.volume_button.setStyleSheet(self.pushbutton_css)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setFixedWidth(150)  # Adjust width as needed

        # Add volume controls to the control layout
        control_layout.addWidget(self.volume_button)
        control_layout.addWidget(self.volume_slider)

        # Add control layout to main layout
        main_layout.addLayout(control_layout)

        # Set the main layout
        self.setLayout(main_layout)

        # Button and slider connections
        self.playpause_button.clicked.connect(self.toggle_play_pause)
        self.prev_button.clicked.connect(self.prev)
        self.next_button.clicked.connect(self.next)
        self.volume_slider.valueChanged.connect(self.change_volume)
        self.volume_button.clicked.connect(self.toggle_mute)

        # Variables to handle volume state
        self.is_muted = False
        self.previous_volume = self.volume_slider.value()

    # Dummy play/pause functions for now
    def toggle_play_pause(self):
        if self.playpause_button.icon().cacheKey() == self.play_icon.cacheKey():
            self.playpause_button.setIcon(self.pause_icon)
            print("Paused")
        else:
            self.playpause_button.setIcon(self.play_icon)
            print("Playing")
            
    def prev(self):
        print("Previous button clicked")

    def next(self):
        print("Next button clicked")

    def change_volume(self, value):
        if not self.is_muted:
            print(f"Volume set to {value}")
            # Update the volume icon based on the volume level
            if value == 0:
                self.volume_button.setIcon(self.volume_mute_icon)
            elif value <= 50:
                self.volume_button.setIcon(self.volume_low_icon)
            else:
                self.volume_button.setIcon(self.volume_high_icon)
        else:
            self.volume_button.setIcon(self.volume_mute_icon)
            print("Volume is muted")

        # Update the previous volume if not muted
        if not self.is_muted:
            self.previous_volume = value

    def toggle_mute(self):
        if self.is_muted:
            # Unmute and restore previous volume
            self.is_muted = False
            self.volume_slider.setValue(self.previous_volume)
            print(f"Unmuted, volume restored to {self.previous_volume}")
        else:
            # Mute and save current volume
            self.is_muted = True
            self.previous_volume = self.volume_slider.value()
            self.volume_slider.setValue(0)
            print("Muted")

        # Update the volume icon
        self.change_volume(self.volume_slider.value())


def runui():
    app = QApplication(sys.argv)
    window = WaveGui()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    runui()
