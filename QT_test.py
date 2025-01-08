import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QGridLayout
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

class ChessUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Check-M.A.T.E")
        self.setGeometry(100, 100, 1024, 600)  # Set screen size to 1024x600
        self.setStyleSheet("background-color: black;")

        # Main Layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Header
        header_layout = QHBoxLayout()
        main_layout.addLayout(header_layout)

        title_label = QLabel("Check-M.A.T.E")
        title_label.setFont(QFont("Arial", 36, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        header_layout.addWidget(title_label, alignment=Qt.AlignLeft)

        # Add resized logo
        logo_pixmap = QPixmap("Figures/logo.png").scaled(90, 121, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label = QLabel()
        logo_label.setPixmap(logo_pixmap)
        header_layout.addWidget(logo_label, alignment=Qt.AlignRight)

        # Quickplay Section
        quickplay_frame = QFrame()
        quickplay_frame.setStyleSheet("background-color: black;")
        main_layout.addWidget(quickplay_frame, alignment=Qt.AlignLeft)
        quickplay_layout = QGridLayout(quickplay_frame)

        self.create_quickplay_button(quickplay_layout, "🌐", "Play Online", 0, 0)
        self.create_quickplay_button(quickplay_layout, "🤖", "Play Bot", 0, 1)
        self.create_quickplay_button(quickplay_layout, "👥", "Play Local", 0, 2)
        self.create_quickplay_button(quickplay_layout, "🔄", "Replay", 0, 3)

        # Footer
        footer_layout = QHBoxLayout()
        main_layout.addLayout(footer_layout)

        play_game_button = QPushButton("▶ Play Game")
        play_game_button.setFont(QFont("Arial", 20))
        play_game_button.setStyleSheet(
            "background-color: gray; color: white; padding: 10px; border-radius: 10px;"
        )
        play_game_button.clicked.connect(self.play_game)
        footer_layout.addWidget(play_game_button)

        local_play_button = QPushButton("Local Play\n10 min standard")
        local_play_button.setFont(QFont("Arial", 18))
        local_play_button.setStyleSheet(
            "background-color: gray; color: white; padding: 10px; border-radius: 10px;"
        )
        local_play_button.clicked.connect(self.local_play)
        footer_layout.addWidget(local_play_button)

    def create_quickplay_button(self, layout, icon, text, row, col):
        """Helper to create quickplay buttons."""
        button_layout = QVBoxLayout()
        frame = QFrame()
        frame.setStyleSheet(
            "background-color: gray; color: white; border-radius: 10px; padding: 10px;"
        )
        frame.setLayout(button_layout)

        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Arial", 36))
        icon_label.setAlignment(Qt.AlignCenter)
        button_layout.addWidget(icon_label)

        text_label = QLabel(text)
        text_label.setFont(QFont("Arial", 16))
        text_label.setAlignment(Qt.AlignCenter)
        button_layout.addWidget(text_label)

        layout.addWidget(frame, row, col)

    def play_game(self):
        print("Play Game button clicked.")

    def local_play(self):
        print("Local Play button clicked.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChessUI()
    window.show()
    sys.exit(app.exec_())
