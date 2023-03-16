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

from database.database import DB

from interface.add_window import AddWindow
from interface.order_window import OrderWindow


class PersonalWindow(QMainWindow):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        #data for Order Window
        #childrent window
        self.add_window = AddWindow(self)
        self.show_window = None

        self.login_user = QLabel()
        self.setCentralWidget(QWidget())
        self.setWindowTitle("Личный кабинет сотрудника ОТК")
        self.create_gui()
        self.setGeometry(600,300,300,130)

    
    def create_gui(self):

        self.main_grid = QGridLayout()
        self.main_grid.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.btn_back = QPushButton("Назад")
        self.btn_back.clicked.connect(lambda: self.go_back())
        self.btn_add = QPushButton("Добавить")
        self.btn_add.clicked.connect(lambda: self.show_add())
        self.btn_show_order = QPushButton('Показать заказы')
        self.input_id_order = QLineEdit()
        self.input_id_order.setPlaceholderText("Введите ID заказа")
        self.btn_show_order.clicked.connect(lambda: self.show_order())


        self.main_grid.addWidget(self.login_user, 0, 0)
        self.main_grid.addWidget(self.btn_add, 1, 0)
        self.main_grid.addWidget(self.btn_show_order,2,0)
        self.main_grid.addWidget(self.input_id_order,2,1)
        self.main_grid.addWidget(self.btn_back, 3, 0, 1, 2)
        

        self.centralWidget().setLayout(self.main_grid)
        
    def go_back(self):
        self.hide()
        self.parent.show()

    def show_add(self):
        self.add_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.add_window.show()

    def show_order(self):
        id = self.input_id_order.text()
        if id =='':
            QMessageBox.warning(self,'Ошибка','Где ID заказа брат?')
        else:
            self.show_window = OrderWindow(self,id)
            self.show_window.setWindowModality(Qt.WindowModality.ApplicationModal)
            self.show_window.show()
   
        