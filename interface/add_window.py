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
#модальное окно
from interface.new_user_window import NewUserAddWindow

import datetime
#Класс для добавление информации о заказе
class AddWindow(QMainWindow):
    def __init__(self,parent,login_personal):
        super().__init__()
        #здесь лежит логин авторизированного пользователя
        self.login_personal = login_personal
        #экземпляр для работы с БД
        self.DB = DB()
        #подгружаем из БД названия всех услуг
        options = self.DB.get_all_service()
        # print(options)
        #QComboBox - как select в html .Выпадающий список - ниже пример как его создать
        self.combo = QComboBox()
        for option in options:
            self.combo.addItem(option[1])
            print(option[1])
        #прокинули сюда родителя . Родитель для него PersonalWindow
        self.parent_personal_window = parent
        #Здесь создаем экзмепляр модального окна для добавления пользователя
        self.new_user = NewUserAddWindow(self,None)
        #настройки окна
        self.setGeometry(600,350,300,200)
        self.setWindowTitle("Добавить заказ")
        self.setCentralWidget(QWidget())
        #Отключили крестик справа сверху на окне . Красненький такой он не вписывается в логику. Вообще ну никак не вписывается
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)

        #это как create_gui просто название другое.
        self.initUI()

    #инициализация GUI
    def initUI(self):
        
        #грид 
        self.main_grid = QGridLayout()

        #инпут для id сосуда
        self.id_input = QLineEdit()
        #инпут для имя пользователя ( не сотрудник отк ИМЕННО пользователь)
        self.name_user = QLineEdit()
        self.name_user.setMaxLength(44)
        self.name_user.textChanged.connect(lambda: FioValidator(self.name_user,self.name_user.text()))
        #кнопка
        self.btn_add = QPushButton("Добавить")
        #привязали функции  к кнопке
        self.btn_add.clicked.connect(lambda: self.add())

        self.btn_back = QPushButton("Назад")
        self.btn_back.clicked.connect(lambda: self.closeEvent())

        #закинули все в основной грид
        self.main_grid.addWidget(QLabel("Номер сосуда"), 0, 0)
        self.main_grid.addWidget(self.id_input, 0, 1)
        self.main_grid.addWidget(QLabel("Имя клиента"), 2, 0)
        self.main_grid.addWidget(self.name_user, 2, 1)
        self.main_grid.addWidget(QLabel("Выберите услугу"), 3, 0)
        self.main_grid.addWidget(self.combo, 3, 1,1,2)
        self.main_grid.addWidget(self.btn_add, 4, 0)
        self.main_grid.addWidget(self.btn_back, 4, 1)

        #в контейнер положили наш грид В КОТОРОМ УЖЕ лежат наши кнопочки лейбы инпуты и тд
        self.centralWidget().setLayout(self.main_grid)

    #функция добавления данных о заказе 
    def add(self):
        #reinit db 
        self.DB =DB()
        print('add')
        #  с помощью метода text() из инпута можно достать данные лежащие в нем
        id = self.id_input.text()
        # currentText - а этот метод вовзращает выбранную опцию из селекта
        name_service = self.combo.currentText()
        # узнаем у базы данных стоимость услуги 
        price = self.DB.get_price_service(name_service)
        #из инпута логин забираем - 
        name = self.name_user.text()

        if id != '' and name_service != '' and price != '' and name != '':
            #проверяем если ли такой пользователь в БД 
            result = self.DB.check_user(str(name))
            if result is not None:
                # Если есть такой пользователь ( ну клиент точнее) мы под него заказа создаем
                date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.DB.add_order(id_container=id,date=date,name_service=name_service,name_user=name,name_personal=self.login_personal)
            else:
                #Если пользователя нет мы его должны создать вызываем очередной QMessageBox
                reply = QMessageBox.question(self, 'Челика нет',
                            "Пользователь с таким именем не существует, Добавим?")
                if reply == QMessageBox.StandardButton.Yes:
                    #сохраняем имя пользователя для модального окна 
                    self.new_user.FIO_input.setText(name)
                    #инпут с именем пользователя заморозили
                    self.new_user.FIO_input.setReadOnly(True)
                    #открыли окно для добавления нового пользователя
                    self.new_user.show()
                    #скрыли текущее
                    self.hide()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Необходимо заполнить поля')
        id = self.id_input.clear()
        name = self.name_user.clear()

                
    #закрытие текущего окна и откытие родительского 
    def closeEvent(self):
        reply = QMessageBox.question(self, 'Выход',
            "Выйти?")
        if reply == QMessageBox.StandardButton.Yes:
            self.parent_personal_window.show()
            self.hide()


            
           

        