import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow


class MainWindow(QMainWindow):
    """Main window for the Artist Manager application."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Artist Manager")
        self.resize(1000, 650)

        welcome_label = QLabel("Artist Manager setup successful!")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(welcome_label)


def main() -> None:
    """Start the desktop application."""

    application = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(application.exec())


if __name__ == "__main__":
    main()