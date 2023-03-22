from PyQt6.QtWidgets import (
    QGridLayout,
    QMainWindow,
    QLabel,
    QPushButton,
    QLineEdit,
    QWidget,
    QMessageBox
)

from validators.fio_validator import FioValidator 
#Qt - данное проство имен имеет огромный набор различных методов, индификаторов и т д.
#В данном примере я использовал Qt для установки различных флгов и положения элементов относитетльно каких либо объектов
from PyQt6.QtCore import Qt

from database.database import DB

#Создание класса
class NewUserAddWindow(QMainWindow):
    #конструктор класса
    def __init__(self,parent,new_user):
        super().__init__()
        #родительское окно . 
        self.add_window = parent
        #имя КЛИЕНТА НЕ АВТОРИЗИРОВАННОГО ПОЛЬЗОВАТЕЛЯ А КЛИЕНТА КОТОРОГО СОЗДАЕМ
        self.new_user = new_user
        #создаем экземпляр класса для работы с БД
        self.DB = DB()
        #настройки окна
        self.setGeometry(600,300,300,200)
        self.setWindowTitle("Добавьте пользователя")

        #пустой контейнер QWidget()
        self.setCentralWidget(QWidget())
        #УБираем злой крестик, блокаем его.
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)
        #ВЫзываем функцию инициализации GUI
        self.initUI()

    #функция инициализации GUI
    def initUI(self):
        #наш основной grid - здесь будут лежать все наши элементы графического интерфейса
        self.main_grid = QGridLayout()

        #инпуты
        self.FIO_input = QLineEdit()
        self.FIO_input.setMaxLength(44)
        self.FIO_input.textChanged.connect(lambda: FioValidator(self.FIO_input,self.FIO_input.text()))
        self.phone_input = QLineEdit()
        self.email = QLineEdit()


        #кнопки
        self.btn_add = QPushButton("Добавить")
        self.btn_add.clicked.connect(lambda: self.add_new_user())

        self.btn_back = QPushButton("Назад")
        self.btn_back.clicked.connect(lambda: self.closeEvent())

        #Кладем в основной грид все наши элементы
        self.main_grid.addWidget(QLabel("Имя"), 0, 0)
        self.main_grid.addWidget(self.FIO_input, 0, 1)

        self.main_grid.addWidget(QLabel("телефон"), 1, 0)
        self.main_grid.addWidget(self.phone_input, 1, 1)

        self.main_grid.addWidget(QLabel("Почта"), 2, 0)

        self.main_grid.addWidget(self.email, 2, 1)

        self.main_grid.addWidget(self.btn_add, 3, 0)
        self.main_grid.addWidget(self.btn_back, 3, 1)

        #Кладем основной грид в контейнер.
        self.centralWidget().setLayout(self.main_grid)

    #функция добавления нового пользователя
    def add_new_user(self):
        print('add_new_user')
        #сохраняем имя пользователя из инпута в переменную
        FIO = self.FIO_input.text()
        #сохраняем телефон пользователя из инпута в переменную
        phone_input = self.phone_input.text()
        #сохраняем почту пользователя из инпута в переменную
        email = self.email.text()
        #проверяем что все поля были заполнены
        if FIO != '' and phone_input != '' and email != '':
            #вызваем функцию добавления пользователя из класса предназначенного для работы с Базой даных . Она возвращает true или false
            result = self.DB.add_user(FIO,phone_input,email)
            if result:
                QMessageBox.information(self, "Успешно", "Пользователь успешно добавлен")
                self.hide()
            else:
                QMessageBox.warning(self, "Ошибка", "УПС что-то пошло не так:) мы уже работаем над этим")
        else:
            QMessageBox.warning(self, "Ошибка", "Не все поля заполнены")

                
    #закрытие окна
    def closeEvent(self):
        reply = QMessageBox.question(self, 'Выход',
            "Выйти?")
        if reply == QMessageBox.StandardButton.Yes:
            #открываем родительское окно
            self.add_window.show()
            #закрываем текущее
            self.hide()

            
           

        