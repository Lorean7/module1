#все импорты из QtWidgets это набор объектов (окна, сетки, кнопки, инпуты и т д)
#Посмотри подробнее о них в документации
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
#подгрузили валидатор для полей с FIO
from validators.fio_validator import FioValidator

#Qt - данное проство имен имеет огромный набор различных методов, индификаторов и т д.
#В данном примере я использовал Qt для установки различных флгов и положения элементов относитетльно каких либо объектов
from PyQt6.QtCore import Qt
#QPixmap - объект который поможет отрисовать ваши картинки 
from PyQt6.QtGui import QPixmap

#импорт нашего класса DB
from database.database import DB

#импорт окна который является дочерним и откроется после логического завершения данного окна
from interface.personal_window import PersonalWindow

#создание класса MainWindow
class MainWindow(QMainWindow):
    #контруктор класса
    def __init__(self):
        super().__init__()
        #создание экземпляра DB для работы с базой данных
        self.DB = DB()
        #создание экземпляра дочернего окна PersonalWindow а еще передали ему текущее окно оно будет его родителям
        self.children_window = PersonalWindow(self)
        #установка пустого контейнера где будут лежать все наши gui элементы
        self.setCentralWidget(QWidget())
        #установка рапсоложения окна по оси x,y на вашем экране а затем установка его длины и высоты
        self.setGeometry(600,300,300,200)
        #заголовок окна
        self.setWindowTitle('Отдел технического контроля ЗАО ')
        #вызов функции создание GUI (в этой функции инициализируются наши элементы)
        self.create_gui()

    def create_gui(self):
        #данные grids будут использоваться для хранеие элементов для регистрации и авторизации
        self.grid_auth = QGridLayout()
        self.grid_reg = QGridLayout()
        #а здесь будут хранится группы с этими grid'ами
        self.grid_main = QGridLayout()

        #group
        self.group_auth = QGroupBox('Авторизация')
        self.group_reg = QGroupBox('Регистрация')

        #прижимаем группу к верху сетки
        self.group_auth.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.group_reg.setAlignment(Qt.AlignmentFlag.AlignTop)

        #ALL BTN
        self.btn_mode = QPushButton('Перейти к регистрации')
        # привязываем функцию к кнопку это как OnClick 
        self.btn_mode.clicked.connect(lambda: self.change_mode())

        self.btn_registration=QPushButton('регистрация')
          # привязываем функцию к кнопку это как OnClick 
        self.btn_registration.clicked.connect(lambda: self.registration())

        self.btn_auth=QPushButton('авторизация')
          # привязываем функцию к кнопку это как OnClick 
        self.btn_auth.clicked.connect(lambda: self.auth())

        #add group data
        # группах можно хранит grid для удобной компоновки элементов на экране. setLayout - устанавливает в группу grid 
        self.group_auth.setLayout(self.grid_auth)
        self.group_reg.setLayout(self.grid_reg)
        #добавляем наши группы в основной grid устанавливаем координаты 0,0 друг на друга 
        #так как при открытие окна один будет скрыт)))
        self.grid_main.addWidget(self.group_auth,0,0)
        self.grid_main.addWidget(self.group_reg,0,0)

        #добавляем кнопочку для переключения между авторизацией и регистрацией
        self.grid_main.addWidget(self.btn_mode,1,0)

        #input_auth
        #  QLineEdit - это инпут
        self.login_auth = QLineEdit()
        #setMaxLength - max символов для ввода
        self.login_auth.setMaxLength(24)
        #setPlaceholderText - placeholder text когда инпут пустой будет эта надпись Введите логин
        self.login_auth.setPlaceholderText('Введите логин')
        self.password_auth = QLineEdit()
        #setEchoMode - устанавливаем тип поля для password_auth  пароль
        self.password_auth.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_auth.setPlaceholderText('Введите пароль')


        #init group auth добавляем все наши элемнеты
        #QLabel - надпись , просто текст
        self.grid_auth.addWidget(QLabel('Логин'),0,0)
        self.grid_auth.addWidget(self.login_auth,0,1)
        self.grid_auth.addWidget(QLabel('Пароль'),1,0)
        self.grid_auth.addWidget(self.password_auth,1,1)
        self.grid_auth.addWidget(self.btn_auth,2,1)

        #input_reg
        #копия авторизации
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
        #кнопка для вызова функции self.selectImage()
        self.browse_button = QPushButton("Выбрать файл", self)
        self.browse_button.clicked.connect(lambda: self.selectImage())
        #просто надпись
        self.img_info = QLabel('Файл не выбран')


        #init group reg
        #все элементы для регистрации помещаем в grid 
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
        #при первом открытие оена скроем group_reg - он нам не интересен. Мы ведь указали одинаковые координаты 
        #для груп авторизации и регистрации - если кого ты не скрыть будет каша :(
        self.group_reg.hide()

        #наконец-то мы устанавливаем в центральный контейнер наш главный грид ведь там лежат наши группы 
        self.centralWidget().setLayout(self.grid_main)
    #функция для переключение между авторизацией и регистрацией
    def change_mode(self):
        #проверка у group_auth а он скрыт?
        if self.group_auth.isVisible():
            #скрыли его 
            self.group_auth.hide()
            #почистили все его поля
            self.login_auth.clear()
            self.password_auth.clear()
            #показали группу с регистрацей
            self.group_reg.show()
            #не забываем про кнопочку ведь она нас вела к регистрации а теперь будет думать что к авторизации)
            self.btn_mode.setText('Перейти к авторизации')
        else:
            #все как выше но наоборот
            self.group_auth.show()
            self.group_reg.hide()
            self.login_reg.clear()
            self.password_reg.clear()
            self.FIO_reg.clear()
            self.btn_mode.setText('Перейти к регистрации')

    #передача текста из полей и вызов функции регистрации для работы с базой данных
    def registration(self):
        if self.login_reg.text() != '' and self.password_reg.text() != '' and self.FIO_reg.text() !='' and self.img_info.text() != 'Файл не выбран':
            #вызвали функции регистрации
            response = self.DB.registration(self.login_reg.text(), self.password_reg.text(),self.FIO_reg.text(),self.img_info.text())
            if response != False:
                #QMessageBox - это как alert в js . Можете почитать подробнее подробнее о нем. Здесь в виде информацинного алерта
                QMessageBox.information(self, 'Регистрация', 'Регистрация успешна')
            else:
                QMessageBox.warning(self, 'Ошибка', 'Логин занят')
        else:
             #QMessageBox - это как alert в js . Можете почитать подробнее подробнее о нем. Здесь в виде алерта об ошибке
            QMessageBox.warning(self,'error', 'Поля не заполнены')

    #авторизация пользователя . Открытие нового окна
    def auth(self):
        avatar_data = self.DB.auth(self.login_auth.text(), self.password_auth.text())
        if avatar_data is not False:
            QMessageBox.information(self,'accepted', 'Авторизация успешна...')
            self.children_window.login_personal = self.login_auth.text()
            self.children_window.label_hello_personal.setText(f'Здравстуйте, {self.login_auth.text()}')
            #создаем объект картинки
            pixmap = QPixmap()
            #подгружаем данные картинки( они если че в бинарном виде)
            pixmap.loadFromData(avatar_data)
            #устанвка аватарки в дочернем окне
            self.children_window.avatar.setPixmap(pixmap)
            self.children_window.avatar.setScaledContents(True)  # Масштабирование изображения по размеру QLabel
            self.children_window.avatar.setMaximumSize(70, 70)  # Максимальный размер QLabel
            #открываем наше дочернее окно
            self.children_window.show()
            #скрываем текущее - на этом его полномочия все
            self.hide()
            

        else:
            QMessageBox.warning(self,'error', 'Неверный логин или пароль')


    def selectImage(self):
        QFileDialog()
        #сохраняю путь к файлу
        fileName, _ = QFileDialog.getOpenFileName(self,"Выберите изображение", "","Images (*.png *.xpm *.jpg *.bmp);;All Files (*)")
        if fileName:
            #записываю путь к файлу  в переменную img_info
            self.img_info.setText(fileName)


            




