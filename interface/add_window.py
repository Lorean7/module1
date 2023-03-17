from PyQt6.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QMainWindow,
    QLabel,
    QPushButton,
    QLineEdit,
    QWidget,
    QMessageBox,
    QComboBox
)

from validators.fio_validator import FioValidator 

from PyQt6.QtCore import Qt

from database.database import DB
from interface.new_user_window import NewUserAddWindow

import datetime

class AddWindow(QMainWindow):
    def __init__(self,parent):
        super().__init__()
        self.DB = DB()
        options = self.DB.get_all_service()
        # print(options)
        self.combo = QComboBox()
        for option in options:
            self.combo.addItem(option[1])
            print(option[1])
        self.parent_personal_window = parent
        self.new_user = NewUserAddWindow(self,None)
        self.setGeometry(600,350,300,200)
        self.setWindowTitle("Добавить заказ")
        self.setCentralWidget(QWidget())
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)
        self.initUI()

    def initUI(self):
        self.main_grid = QGridLayout()

        #inpit
        self.id_input = QLineEdit()
        self.name_user = QLineEdit()
        self.name_user.setMaxLength(44)
        self.name_user.textChanged.connect(lambda: FioValidator(self.name_user,self.name_user.text()))

        self.btn_add = QPushButton("Добавить")
        self.btn_add.clicked.connect(lambda: self.add())

        self.btn_back = QPushButton("Назад")
        self.btn_back.clicked.connect(lambda: self.closeEvent())

        self.main_grid.addWidget(QLabel("Номер сосуда"), 0, 0)
        self.main_grid.addWidget(self.id_input, 0, 1)
        self.main_grid.addWidget(QLabel("Имя клиента"), 2, 0)
        self.main_grid.addWidget(self.name_user, 2, 1)
        self.main_grid.addWidget(QLabel("Выберите услугу"), 3, 0)
        self.main_grid.addWidget(self.combo, 3, 1,1,2)
        self.main_grid.addWidget(self.btn_add, 4, 0)
        self.main_grid.addWidget(self.btn_back, 4, 1)

        self.centralWidget().setLayout(self.main_grid)

    def add(self):
        #reinit db 
        self.DB =DB()
        print('add')
        id = self.id_input.text()
        name_service = self.combo.currentText()
        price = self.DB.get_price_service(name_service)
        name = self.name_user.text()

        if id != '' and name_service != '' and price != '' and name != '':
            result = self.DB.check_user(str(name))
            if result is not None:
                date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.DB.add_order(id=id,date=date,name_service=name_service,price=int(price),name_user=name)
            else:
                reply = QMessageBox.question(self, 'Челика нет',
                            "Пользователь с таким именем не существует, Добавим?")
                if reply == QMessageBox.StandardButton.Yes:
                    self.new_user.FIO_input.setText(name)
                    self.new_user.FIO_input.setReadOnly(True)
                    self.new_user.show()
                    self.hide()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Необходимо заполнить поля')

                

    def closeEvent(self):
        reply = QMessageBox.question(self, 'Выход',
            "Выйти?")
        if reply == QMessageBox.StandardButton.Yes:
            self.parent_personal_window.show()
            self.hide()


            
           

        