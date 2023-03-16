from PyQt6.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QMainWindow,
    QLabel,
    QPushButton,
    QLineEdit,
    QWidget,
    QMessageBox
)

from validators.fio_validator import FioValidator 

from PyQt6.QtCore import Qt

from database.database import DB

import datetime

class NewUserAddWindow(QMainWindow):
    def __init__(self,parent,new_user):
        super().__init__()
        self.add_window = parent
        self.new_user = new_user
        self.DB = DB()
        self.setGeometry(600,300,300,200)
        self.setWindowTitle("Добавьте пользователя")
        self.setCentralWidget(QWidget())
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)
        self.initUI()

    def initUI(self):
        self.main_grid = QGridLayout()

        #inpit
        self.FIO_input = QLineEdit()
        self.FIO_input.setMaxLength(44)
        self.FIO_input.textChanged.connect(lambda: FioValidator(self.FIO_input,self.FIO_input.text()))
        self.phone_input = QLineEdit()
        self.email = QLineEdit()



        self.btn_add = QPushButton("Добавить")
        self.btn_add.clicked.connect(lambda: self.add_new_user())

        self.btn_back = QPushButton("Назад")
        self.btn_back.clicked.connect(lambda: self.closeEvent())

        self.main_grid.addWidget(QLabel("Имя"), 0, 0)
        self.main_grid.addWidget(self.FIO_input, 0, 1)
        self.main_grid.addWidget(QLabel("телефон"), 1, 0)
        self.main_grid.addWidget(self.phone_input, 1, 1)
        self.main_grid.addWidget(QLabel("Почта"), 2, 0)
        self.main_grid.addWidget(self.email, 2, 1)
        self.main_grid.addWidget(self.btn_add, 3, 0)
        self.main_grid.addWidget(self.btn_back, 3, 1)

        self.centralWidget().setLayout(self.main_grid)

    def add_new_user(self):
        print('add_new_user')
        FIO = self.FIO_input.text()
        phone_input = self.phone_input.text()
        email = self.email.text()
        result = self.DB.add_user(FIO,phone_input,email)
        if result:
            QMessageBox.information(self, "Успешно", "Пользователь успешно добавлен")
        else:
            QMessageBox.warning(self, "Ошибка", "УПС что-то пошло не так:) мы уже работаем над этим")
                

    def closeEvent(self):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure you want to quit?")
        if reply == QMessageBox.StandardButton.Yes:
            self.add_window.show()
            self.hide()

            
           

        