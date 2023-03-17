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

    def registration(self,login,password,FIO,img_path):
        self.cursor.execute("SELECT * FROM personal WHERE login=%s",(login,))
        #обработка img  для хранения в бд
        with open(img_path, 'rb') as f:  # rb - rb - это режим открытия файла для чтения в двоичном режиме.
            image_data = f.read()
            print (image_data)
        if self.cursor.fetchone() is None:
            self.cursor.execute("INSERT INTO personal (login,password,FIO,avatar) VALUES (%s,%s,%s,%s)",(login,password,FIO,image_data))
            self.db.commit()
            print("User added")
        else:
            print("User already exists")

    def auth(self,login,password):
        print('call DB.auth')
        self.cursor.execute("SELECT * FROM personal WHERE login=%s AND password=%s",(login,password))
        result = self.cursor.fetchone()
        if result is not None:
            
            print(result[4])
            return result[4]
        else:
            return False
        
    def add_order(self,id,date, name_service, price,name_user):
        self.cursor.execute("SELECT id FROM service WHERE name_service=%s",(name_service,))
        id_service = self.cursor.fetchone()
        if self.cursor.fetchone() is None:
            self.cursor.execute("INSERT INTO orders (date,id_service, price,name_user,id_sosud) VALUES (%s,%s,%s,%s,%s)",(date, id_service[0], price,name_user,id))
            self.db.commit()
            print("Order added")

    def check_user(self,FIO):
        self.cursor.execute("SELECT * from users WHERE FIO=%s",(FIO,))
        result = self.cursor.fetchone()
        print(result)
        return result
        
    def add_user(self,FIO,telephone,email):
        self.cursor.execute("SELECT * FROM users WHERE FIO=%s",(FIO,))
        reslut = self.cursor.fetchone()
        if reslut is None:
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
    
    def get_order(self,id):
        print(id)
        print(type(id))
        self.cursor.execute("SELECT * FROM orders WHERE id=%s",(int(id),))
        result = self.cursor.fetchone()
        if result is not None:
            
            print(result)
            return result
        else:
            return False
        
    def remove_order(self,id):

        id =int(*id) #из-за кортежа я мучаюсь с типами данных АААААААААААААА
        self.cursor.execute('DELETE FROM orders WHERE id=%s',(id,))
        self.db.commit()

    def update_order(self,id_order,name_user,name_service,price,id_sosud):
        self.cursor.execute("SELECT id FROM service WHERE name_service=%s",(name_service,))
        id_service = self.cursor.fetchone()
        print(id_service[0])
        print(id_sosud)
        print(price)
        print(name_service)
        print(id_order)
        
        result = self.check_user(name_user)
        if result == True:
            self.cursor.execute("UPDATE orders SET id_service=%s,price=%s,name_user=%s,id_sosud=%s WHERE id=%s",(id_service[0],price,name_user,id_sosud,id_order))
            self.db.commit()
            return True
        else:
            return False





        