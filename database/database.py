import mysql.connector


class DB():
    def __init__(self):
        self.db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='db_otk'
            )
        self.cursor = self.db.cursor()

    def registration(self,login,password,FIO):
        self.cursor.execute("SELECT * FROM personal WHERE login=%s",(login,))
        if self.cursor.fetchone() is None:
            self.cursor.execute("INSERT INTO personal (login,password,FIO) VALUES (%s,%s,%s)",(login,password,FIO))
            self.db.commit()
            print("User added")
        else:
            print("User already exists")

    def auth(self,login,password):
        print('call DB.auth')
        self.cursor.execute("SELECT * FROM personal WHERE login=%s AND password=%s",(login,password))
        if self.cursor.fetchone() is not None:
            return True
        else:
            return False
        
    def add_order(self,id,date, name_service, price,name_user):
        self.cursor.execute("SELECT id FROM service WHERE name_service=%s",(name_service,))
        id_service = self.cursor.fetchone()
        if self.cursor.fetchone() is None:
            self.cursor.execute("INSERT INTO orders (id,date,id_service, price,name_user) VALUES (%s,%s,%s,%s,%s)",(id,date, id_service[0], price,name_user))
            self.db.commit()
            print("Order added")

    def check_user(self,FIO):
        print('call DB.check_user')
        print(FIO)
        self.cursor.execute("SELECT * FROM users WHERE FIO=%s",(FIO,))
        if self.cursor.fetchone() is None:
            return False
        else:
            return True
        
    def add_user(self,FIO,telephone,email):
        self.cursor.execute("SELECT * FROM users WHERE FIO=%s",(FIO,))
        if self.cursor.fetchone() is None:
            self.cursor.execute("INSERT INTO users (FIO,telephone,email) VALUES (%s,%s,%s)",(FIO,telephone,email))
            self.db.commit()
            print("User added")
            return True
        else:
            return False
        
    def get_all_service(self):
        options = self.cursor.execute("SELECT * FROM service")
       
        # получаем первую строку данных
        data = self.cursor.fetchall()
        list(data)
        # for item in data:
        #     print(item)

        return data
    def get_price_service(self,name):
        
        self.cursor.execute("SELECT price FROM service WHERE name_service=%s",(name,))
        price = self.cursor.fetchone()
        return price[0]



        