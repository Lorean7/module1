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


class PersonalWindow(QMainWindow):
    def __init__(self,login,parent):
        super().__init__()
        self.parent = parent
        self.add_window = AddWindow(self)
        self.setCentralWidget(QWidget())
        self.setWindowTitle("Личный кабинет сотрудника ОТК")
        self.create_gui()
        self.setGeometry(600,300,300,130)

    
    def create_gui(self):

        self.main_grid = QGridLayout()
        self.main_grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.login_user = QLabel()

        self.btn_back = QPushButton("Назад")
        self.btn_back.clicked.connect(lambda: self.go_back())
        self.btn_add = QPushButton("Добавить")
        self.btn_add.clicked.connect(lambda: self.show_add())

        self.main_grid.addWidget(self.login_user, 0, 0)
        self.main_grid.addWidget(self.btn_add, 1, 0)
        self.main_grid.addWidget(self.btn_back, 2, 0, 1, 2)
        

        self.centralWidget().setLayout(self.main_grid)
        
    def go_back(self):
        self.hide()
        self.parent.show()

    def show_add(self):
        self.add_window.show()
        self.hide()       
        