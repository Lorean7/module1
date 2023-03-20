from PyQt6.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QMainWindow,
    QLabel,
    QPushButton,
    QLineEdit,
    QWidget,
    QMessageBox,
    QComboBox,
)

from validators.fio_validator import FioValidator 

from PyQt6.QtCore import Qt

from database.database import DB

import datetime

class UpdateWindow(QMainWindow):
    def __init__(self,parent,id_order):
        super().__init__()
        self.id_order = id_order
        # print(options)
        self.DB = DB()
        options = self.DB.get_all_service()
        # print(options)
        self.service = QComboBox()
        for option in options:
            self.service.addItem(option[1])
            print(option[1])
        self.parent_personal_window = parent
        self.setGeometry(600,350,300,200)
        self.setWindowTitle("Обновление данных ")
        self.setCentralWidget(QWidget())
        self.initUI()

    def initUI(self):
        self.main_grid = QGridLayout()

        #inpit
    
        self.name_user = QLineEdit()
        self.name_user.textChanged.connect(lambda: FioValidator(self.name_user,self.name_user.text()))
        self.id_sosud =QLineEdit()
        self.btn_add = QPushButton("Обновить данные")
        self.btn_add.clicked.connect(lambda: self.update())
        self.main_grid.addWidget(QLabel("Имя пользователя"),0,0)
        self.main_grid.addWidget(self.name_user,0,1)
        self.main_grid.addWidget(QLabel("Идентификатор сосуда"),1,0)
        self.main_grid.addWidget(self.id_sosud,1,1)
        self.main_grid.addWidget(QLabel("название услуги"),2,0)
        self.main_grid.addWidget(self.service,2,1)
        self.main_grid.addWidget(self.btn_add,3,0,1,2)


        self.centralWidget().setLayout(self.main_grid)

    def update(self):
       
        name_user = self.name_user.text()
        name_service = self.service.currentText()
        id_sosud = self.id_sosud.text()
        respone = self.DB.update_order(self.id_order,name_user,name_service, id_sosud)
        if respone:
            QMessageBox.information(self,"Данные обновленны","Успешно обновлены данные")
            self.hide()
        else:
            QMessageBox.warning(self,"Ошибка","Не удалось обновить данные")
            self.hide()



            
           

        