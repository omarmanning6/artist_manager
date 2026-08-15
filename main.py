"""Application entry point for Artist Manager."""

import sys

from PyQt6.QtWidgets import QApplication

from app.ui.main_window import MainWindow


def main() -> int:
    """Create and start the Qt application."""

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())