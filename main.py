from PyQt6.QtWidgets import QApplication
from interface.main_window import MainWindow
from PyQt6.QtGui import QIcon

# условие в IF это проверка на то что текущий файл является исполняемым и запускается
if __name__ == "__main__":

    #создали приложение
    app= QApplication([])
    #установка иконки глобально для всего приложения
    app.setWindowIcon(QIcon('assets/icon.png'))
    #создаение экземпляра окна
    window = MainWindow()
    #открытие окна
    window.show()
    #запустили цикл событий приложения (метод exec) - в двух словах если закрыть все окна цикл событий
    # поймет что ему больше нечего ловить и закроет приложение но это далеко не все что он делает
    app.exec()