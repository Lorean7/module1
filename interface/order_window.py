from PyQt6.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QMainWindow,
    QLabel,
    QPushButton,
    QWidget,
    QMessageBox,
    QHBoxLayout
)

from PyQt6.QtCore import Qt

from interface.update_window import UpdateWindow

from database.database import DB

#Создаем объект OrderWindow который предназначен для отображение инф о заказе
class OrderWindow(QMainWindow):
    #конструктор 
    def __init__(self,parent,id_order):
        super().__init__()
        #создаем переменную для работы с родительским окном
        self.parent = parent
        #print(self.parent)
        #создаем пустой контейнер
        self.setCentralWidget(QWidget())
        #создаем экземпляр класса DB для работы с базой данных
        self.DB = DB()
        #получаем данные о заказе по id заказа, предварительно на этапе создания этого окна  родителе мы передали этот id
        self.data_order = self.DB.get_order(id_order)

        #инициализция GUI
        self.create_gui()
    
    def create_gui(self):

        #QHBoxLayout - это как grid, но попроще . В нем не нужно устанавливать координы. Он также служит 
        #Хранилищем(слоем) , автоматически выставляя их поочередно в горизантальном положении
        self.main_layout = QHBoxLayout()
        print('create order window')
        #если ответ из БД пришел не пустой мы начинаем формировать 
        if self.data_order != False:
            #Создание группы 
            group_order = QGroupBox(f"Заказ № {self.data_order['id_order']}")
            #Создание грида 
            grid_order = QGridLayout()
            #создаем кнопку для удаления
            self.btn_remove = QPushButton('Удалить')
            self.btn_remove.clicked.connect(lambda: self.remove_order())
            #создаем кнопку для обновления данных
            self.btn_update = QPushButton('Изменить')
            self.btn_update.clicked.connect(lambda: self.show_update_order())

            #устанавливаем элементы в грид
            grid_order.addWidget(QLabel(f"Имя клиента: {self.data_order['name_user']}"),0,0)
            grid_order.addWidget(QLabel(f"Название услуги: {self.data_order['name_service']}"),3,0)
            grid_order.addWidget(QLabel(f"Номер сосуда: {self.data_order['id_container']}"),2,0)
            grid_order.addWidget(QLabel(f"Имя сотрудника: {self.data_order['name_personal']}"),1,0)
            grid_order.addWidget(QLabel(f"Дата: {self.data_order['date']}"),4,0)
            grid_order.addWidget(QLabel(f"Цена: {self.data_order['price']}"),5,0)
            
            grid_order.addWidget(self.btn_remove,7,1)
            grid_order.addWidget(self.btn_update,6,1)
            
            #грид заказа кладем в группу
            group_order.setLayout(grid_order)
            #группу кладем в основной слой 
            self.main_layout.addWidget(group_order)
        else:
            #если ответ из БД не пришел в оснвное хранилище кладем надпись что заказ не найден
            self.main_layout.addWidget(QLabel('Заказ не найден'))     

        #Устанавливаем наш слой для отображения в центральный контейнер
        self.centralWidget().setLayout(self.main_layout)

    #функция удаления заказа
    def remove_order(self):
        #алерт с вопросом для пользователя( ПОДТВЕРЖДЕНИЕ УДАЛЕНИЯ)
        result = QMessageBox.question(self,'Удаление заказа','Подтверите удаление заказа?')
        if result == QMessageBox.StandardButton.Yes:
            #вызов функции удаления заказа ( принимает id текущего заказа)
            self.DB.remove_order({self.data_order['id_order']})
             #информационный алерт сообщающий об удалении заказа
            QMessageBox.information(self,f'Удаление заказа',f"Заказ№ {self.data_order['id_order']} УДАЛЕН")
            #Закрытие  окна
            self.hide()

    #функция обновления заказа
    def show_update_order(self):
        print('show update order')
        #Создание модального окна UpdateWindow
        update_window = UpdateWindow(self,self.data_order['id_order'])
        #Устанавливаем свойство ApplicationModal, сообщая что это окно будет восприниматься как модальное
        update_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        #устанавливаем имя клиента в поле модального окна
        update_window.name_user.setText(str(self.data_order['name_user']))
        #устанавливаем id сосуда в поле модального окна
        update_window.id_sosud.setText(str(self.data_order['id_container']))
        #отображение модального окна
        update_window.show()
        #закрыть текущее окно
        self.hide()