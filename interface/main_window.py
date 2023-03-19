from PyQt6.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QMainWindow,
    QLabel,
    QPushButton,
    QLineEdit,
    QWidget,
    QMessageBox,
    QFileDialog,
    
)
from validators.fio_validator import FioValidator

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from database.database import DB

from interface.personal_window import PersonalWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.DB = DB()
        self.children_window = PersonalWindow(self)
        self.setCentralWidget(QWidget())
        self.setGeometry(600,300,300,200)
        self.setWindowTitle('Отдел технического контроля ЗАО ')
        self.create_gui()

    def create_gui(self):
        #grid
        self.grid_auth = QGridLayout()
        self.grid_reg = QGridLayout()
        self.grid_main = QGridLayout()

        #group
        self.group_auth = QGroupBox('Авторизация')
        self.group_reg = QGroupBox('Регистрация')

        self.group_auth.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.group_reg.setAlignment(Qt.AlignmentFlag.AlignTop)

        #ALL BTN
        
        self.btn_mode = QPushButton('Перейти к регистрации')
        self.btn_mode.clicked.connect(lambda: self.change_mode())

        self.btn_registration=QPushButton('регистрация')
        self.btn_registration.clicked.connect(lambda: self.registration())

        self.btn_auth=QPushButton('авторизация')
        self.btn_auth.clicked.connect(lambda: self.auth())

        #add group data
        self.group_auth.setLayout(self.grid_auth)
        self.group_reg.setLayout(self.grid_reg)
        self.grid_main.addWidget(self.group_auth,0,0)
        self.grid_main.addWidget(self.group_reg,0,0)


        self.grid_main.addWidget(self.btn_mode,1,0)

        #input_auth
        self.login_auth = QLineEdit()
        self.login_auth.setMaxLength(24)
        self.login_auth.setPlaceholderText('Введите логин')
        self.password_auth = QLineEdit()
        self.password_auth.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_auth.setPlaceholderText('Введите пароль')


        #init group auth
        self.grid_auth.addWidget(QLabel('Логин'),0,0)
        self.grid_auth.addWidget(self.login_auth,0,1)
        self.grid_auth.addWidget(QLabel('Пароль'),1,0)
        self.grid_auth.addWidget(self.password_auth,1,1)
        self.grid_auth.addWidget(self.btn_auth,2,1)

        #input_reg
        self.login_reg = QLineEdit()
        self.login_reg.setMaxLength(16)
        self.login_reg.setPlaceholderText('Введите логин')
        self.FIO_reg = QLineEdit()
        self.FIO_reg.setMaxLength(44)
        self.FIO_reg.setPlaceholderText('Введите FIO')
        self.FIO_reg.textChanged.connect(lambda: FioValidator(self.FIO_reg,self.FIO_reg.text()))
        self.password_reg = QLineEdit()
        self.password_reg.setPlaceholderText('Введите пароль')
        self.password_reg.setEchoMode(QLineEdit.EchoMode.Password)
        self.browse_button = QPushButton("Выбрать файл", self)
        self.browse_button.clicked.connect(lambda: self.selectImage())
        self.img_info = QLabel('Файл не выбран')


        #init group reg
        self.grid_reg.addWidget(QLabel('Логин'),0,0)
        self.grid_reg.addWidget(self.login_reg,0,1)
        self.grid_reg.addWidget(QLabel('Пароль'),1,0)
        self.grid_reg.addWidget(self.password_reg,1,1)
        self.grid_reg.addWidget(QLabel('ФИО'),2,0)
        self.grid_reg.addWidget(self.FIO_reg,2,1)
        self.grid_reg.addWidget(QLabel('Загрузить файл'),3,0)
        self.grid_reg.addWidget(self.browse_button,3,1)
        self.grid_reg.addWidget(self.img_info,4,1)
        self.grid_reg.addWidget(self.btn_registration,5,1)
        

        #hide reg group
        self.group_reg.hide()

        self.centralWidget().setLayout(self.grid_main)

    def change_mode(self):
        if self.group_auth.isVisible():
            self.group_auth.hide()
            self.login_auth.clear()
            self.password_auth.clear()
            self.group_reg.show()
            self.btn_mode.setText('Перейти к авторизации')
        else:
            self.group_auth.show()
            self.group_reg.hide()
            self.login_reg.clear()
            self.password_reg.clear()
            self.FIO_reg.clear()
            self.btn_mode.setText('Перейти к регистрации')
    #передача текста из полей и вызов функции регистрации для работы с базой данных
    def registration(self):
        if self.login_reg.text() != '' and self.password_reg.text() != '' and self.FIO_reg.text() !='':
            self.DB.registration(self.login_reg.text(), self.password_reg.text(),self.FIO_reg.text(),self.img_info.text())
            QMessageBox.information(self, 'Регистрация', 'Регистрация успешна')
        else:
            QMessageBox.warning(self,'error', 'Поля не заполнены')
    #авторизация пользователя . Открытие нового окна
    def auth(self):
        avatar_data = self.DB.auth(self.login_auth.text(), self.password_auth.text())
        if avatar_data is not False:
            QMessageBox.information(self,'accepted', 'Авторизация успешна...')
            self.children_window.login_personal = self.login_auth.text()
            self.children_window.label_hello_personal.setText(f'Здравстуйте, {self.login_auth.text()}')
            pixmap = QPixmap()
            pixmap.loadFromData(avatar_data)
            self.children_window.avatar.setPixmap(pixmap)
            self.children_window.avatar.setScaledContents(True)  # Масштабирование изображения по размеру QLabel
            self.children_window.avatar.setMaximumSize(70, 70)  # Максимальный размер QLabel
            self.children_window.show()
            self.hide()
            

        else:
            QMessageBox.warning(self,'error', 'Неверный логин или пароль')

    #контроллер поля 

    def selectImage(self):
        options = QFileDialog()
        fileName, _ = QFileDialog.getOpenFileName(self,"Выберите изображение", "","Images (*.png *.xpm *.jpg *.bmp);;All Files (*)")
        if fileName:
            self.img_info.setText(fileName)


            




