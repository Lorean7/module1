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

from PyQt6.QtCore import Qt

#импорт модальных окон
from interface.add_window import AddWindow
from interface.order_window import OrderWindow

#Создание класса
class PersonalWindow(QMainWindow):
    #конструктор
    def __init__(self,parent):
        super().__init__()
        #ловим окно родителя для взаимодействия с ним
        self.parent = parent
        #data for Order Window
        #childrent window
        #переменных для дранения данных
        self.login_personal = None
        #сюда мы позже закинем экземпляр окна с информацией о заказе
        self.show_window = None
        #допрожелательная надпись
        self.label_hello_personal = QLabel(f'Здравствуйте, {self.login_personal}')
        #аватарка пользователя хранится в QLabel. Этот Виджет обеспечивает отображение текста или изображения.Забыл сказать раньше))
        self.avatar = QLabel()

        #очередной центральный контейнер и т д
        self.setCentralWidget(QWidget())
        self.setWindowTitle("Личный кабинет сотрудника ОТК")
        self.create_gui()
        self.setGeometry(600,300,300,130)

    #функция инициализации элементов для окошечка))
    def create_gui(self):

        #грид
        self.main_grid = QGridLayout()
        #прижали грид к верху окна
        self.main_grid.setAlignment(Qt.AlignmentFlag.AlignTop)

        #кнопочка
        self.btn_back = QPushButton("Назад")
        #привязали к кнопочке функцию
        self.btn_back.clicked.connect(lambda: self.go_back())
        #еще кнопочка
        self.btn_add = QPushButton("Добавить")
        #привязали к кнопочке функцию
        self.btn_add.clicked.connect(lambda: self.show_add())
        #кнопочка
        self.btn_show_order = QPushButton('Показать заказы')
        #инпут для ввода id заказа
        self.input_id_order = QLineEdit()
        self.input_id_order.setPlaceholderText("Введите ID заказа")
        #привязали к кнопочке функцию
        self.btn_show_order.clicked.connect(lambda: self.show_order())



        #В грид закинули все наши элементы и указали их координаты 
        self.main_grid.addWidget(self.label_hello_personal, 0, 0)
        self.main_grid.addWidget(self.avatar, 0, 1)
        #а здесь закинули уже собранную картинку прижали для надежности к верху окна и направо чтоб не убежала
        self.main_grid.setAlignment(self.avatar, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        #продолжаем закидывать остальные элементы
        self.main_grid.addWidget(self.btn_add, 1, 0)
        self.main_grid.addWidget(self.btn_show_order,2,0)
        self.main_grid.addWidget(self.input_id_order,2,1)
        self.main_grid.addWidget(self.btn_back, 3, 0, 1, 2)
        
        #основный грид снова ложим в центральный контейнер - вот что здесь лежит будет отображаться в окне
        self.centralWidget().setLayout(self.main_grid)
    
    #функция для кнопки назад она же осуществляет выход из текущего окна и открывает окно родитель .Родитель у нас mainWindow
    def go_back(self):
        self.hide()
        self.parent.show()

    #открывает модального окно - происходит заморозка текущего
    def show_add(self):
        self.add_window = AddWindow(self,self.login_personal)
        #setWindowModality(Qt.WindowModality.ApplicationModal) - делаем из обыного окна модальное :)
        self.add_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.add_window.show()
    #функция открытия окна с информацией о заказе. Нужно указать id в поле input_id_order иначе никак
    def show_order(self):
        id = self.input_id_order.text()
        if id =='':
            QMessageBox.warning(self,'Ошибка','Где ID заказа брат?')
        else:
            #создали экзмепляр OrderWindow и сделали его модальным. Передали id заказа
            self.show_window = OrderWindow(self,id)
            self.show_window.setWindowModality(Qt.WindowModality.ApplicationModal)
            self.show_window.show()
   
        