from PyQt6.QtWidgets import QApplication
from interface.main_window import MainWindow
from PyQt6.QtGui import QIcon

if __name__ == "__main__":
    app= QApplication([])
    app.setWindowIcon(QIcon('assets/icon.png'))
    window = MainWindow()
    window.show()
    app.exec()