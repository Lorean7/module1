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
    QVBoxLayout,
    QHBoxLayout
)

from PyQt6.QtCore import Qt

from interface.update_window import UpdateWindow

from database.database import DB

class OrderWindow(QMainWindow):

    def __init__(self,parent,id_order):
        super().__init__()
        self.parent = parent
        print(self.parent)
        self.setCentralWidget(QWidget())
        self.DB = DB()
        self.data_order = self.DB.get_order(id_order)
        self.create_gui()
    
    def create_gui(self):

        self.main_layout = QHBoxLayout()
        print('create order window')
        if self.data_order != False:
            group_order = QGroupBox(f"Заказ № {self.data_order['id_order']}")
            grid_order = QGridLayout()
            self.btn_remove = QPushButton('Удалить')
            self.btn_remove.clicked.connect(lambda: self.remove_order())
            self.btn_update = QPushButton('Изменить')
            self.btn_update.clicked.connect(lambda: self.show_update_order())

            grid_order.addWidget(QLabel(f"Имя клиента: {self.data_order['name_user']}"),0,0)
            grid_order.addWidget(QLabel(f"Название услуги: {self.data_order['name_service']}"),3,0)
            grid_order.addWidget(QLabel(f"Номер сосуда: {self.data_order['id_container']}"),2,0)
            grid_order.addWidget(QLabel(f"Имя сотрудника: {self.data_order['name_personal']}"),1,0)
            grid_order.addWidget(QLabel(f"Дата: {self.data_order['date']}"),4,0)
            grid_order.addWidget(QLabel(f"Цена: {self.data_order['price']}"),5,0)
            
            grid_order.addWidget(self.btn_remove,7,1)
            grid_order.addWidget(self.btn_update,6,1)
            

            group_order.setLayout(grid_order)
            self.main_layout.addWidget(group_order)
        else:
            self.main_layout.addWidget(QLabel('Заказ не найден'))     

        self.centralWidget().setLayout(self.main_layout)

    def remove_order(self):
        result = QMessageBox.question(self,'Удаление заказа','Подтверите удаление заказа?')
        if result == QMessageBox.StandardButton.Yes:
            self.DB.remove_order({self.data_order['id_order']})
            QMessageBox.information(self,f'Удаление заказа',f"Заказ№ {self.data_order['id_order']} УДАЛЕН")
            self.hide()

    def show_update_order(self):
        print('show update order')
        update_window = UpdateWindow(self,self.data_order['id_order'])
        update_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        
        update_window.name_user.setText(str(self.data_order['name_user']))
        update_window.id_sosud.setText(str(self.data_order['id_container']))
        update_window.show()
        self.hide()