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
        self.id_order = id_order
        print(f'self.id-order{self.id_order}')
        print(type(self.id_order))
        self.data_order = self.DB.get_order(self.id_order)
        self.create_gui()
    
    def create_gui(self):

        self.main_layout = QHBoxLayout()
        print('create order window')
        if self.data_order != False:
            group_order = QGroupBox(f'Заказ № {self.data_order[0]}')
            grid_order = QGridLayout()
            self.btn_remove = QPushButton('Удалить')
            self.btn_remove.clicked.connect(lambda: self.remove_order())
            self.btn_update = QPushButton('Изменить')
            self.btn_update.clicked.connect(lambda: self.show_update_order())

            grid_order.addWidget(QLabel(f'Имя клиента: {self.data_order[4]}'),0,0)
            grid_order.addWidget(QLabel(f'номер услуги: {self.data_order[2]}'),1,0)
            grid_order.addWidget(QLabel(f'Номер сосуда: {self.data_order[5]}'),2,0)
            grid_order.addWidget(QLabel(f'Дата: {self.data_order[1]}'),3,0)
            grid_order.addWidget(QLabel(f'цена: {self.data_order[3]}'),4,0)
            grid_order.addWidget(self.btn_remove,5,0)
            grid_order.addWidget(self.btn_update,5,1)
            

            group_order.setLayout(grid_order)
            self.main_layout.addWidget(group_order)
        else:
            self.main_layout.addWidget(QLabel('Заказ не найден'))     

        self.centralWidget().setLayout(self.main_layout)

    def remove_order(self):
        result = QMessageBox.question(self,'Удаление заказа','Подтверите удаление заказа?')
        if result == QMessageBox.StandardButton.Yes:
            self.DB.remove_order({self.data_order[0]})
            QMessageBox.information(self,f'Удаление заказа',f'Заказ№ {self.data_order[0]} УДАЛЕН')
            self.hide()

    def show_update_order(self):
        update_window = UpdateWindow(self,self.data_order[0])
        update_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        
        update_window.name_user.setText(self.data_order[4])
        update_window.id_sosud.setText(self.data_order[5])
        update_window.id_sosud.setText(self.data_order[5])
        update_window.show()
        self.hide()