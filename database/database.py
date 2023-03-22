import mysql.connector

#Данный файл представляет собой класс необходимый для работы с базой данных.
#В нем инициализируется подключение к Базе даных . 
#Так же создается экземпляр объектов cursor который позволяет выполнять SQL запросы
#В данном классе описаны основные функцие необходимые для работы с БД

#объявление класса
class DB():
    #функции __init__ конструктор класса
    #в Здесь при создение объекта выполняется подключение к базе данных db_otk
    # где user  - необходимо ввести имя вашего пользователя в БД
    #password - его пароль
    #database - название бд
    def __init__(self):
        self.db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='db_otk'
            )
        self.cursor = self.db.cursor()

    #функция регистрации пользователя
    def registration(self,login,password,FIO,img_path):
        self.cursor.execute("SELECT * FROM personal WHERE login=%s",(login,))
        #обработка img  для хранения в бд
        with open(img_path, 'rb') as file:
            image_data = file.read()


        if self.cursor.fetchone() is None:
            self.cursor.execute("INSERT INTO personal (login,password,FIO,avatar) VALUES (%s,%s,%s,%s)",(login,password,FIO,image_data))
             #commit сохраняем изменение в БД после выполнение запроса SQL
            self.db.commit()
            print("User added")
        else:
            print("User already exists")
            return False


    #функция авторизации
    def auth(self,login,password):
        print('call DB.auth')
        self.cursor.execute("SELECT * FROM personal WHERE login=%s AND password=%s",(login,password))
        result = self.cursor.fetchone()
        if result is not None:
            return result[4]
        else:
            return False
    #функция добавление нового заказа    
    def add_order(self,id_container,date, name_service,name_user,name_personal):
        self.cursor.execute("SELECT id FROM service WHERE name_service=%s",(name_service,))
        response = self.cursor.fetchone()
        id_service = response[0]
        print(id_service)
        #получение id клиента
        self.cursor.execute("SELECT id from users WHERE FIO=%s", (name_user,))
        response = self.cursor.fetchone()
        id_user = response[0]

        self.cursor.execute("SELECT id from personal WHERE login=%s", (name_personal,))
        print(name_personal)
        #получение id сотрудника отк
        response = self.cursor.fetchone()
        id_personal = response[0]
        if id_service is not None and id_user is not None:
            self.cursor.execute("INSERT INTO orders (date,id_container,users_id,personal_id,service_id) VALUES (%s,%s,%s,%s,%s)",(date,id_container, id_user,id_personal,id_service))
             #commit сохраняем изменение в БД после выполнение запроса SQL
            self.db.commit()
            print("Order added")
        else:
            print("User or service not found")

    #функция проверки пользователя на сущестовавние ( по дефолту вернет данные пользователя)
    def check_user(self,FIO):
        self.cursor.execute("SELECT * from users WHERE FIO=%s",(FIO,))
        result = self.cursor.fetchone()
        print(result)
        return result
    
    #функция добавление нового пользователя 
    def add_user(self,FIO,telephone,email):
        self.cursor.execute("SELECT * FROM users WHERE FIO=%s",(FIO,))
        reslut = self.cursor.fetchone()
        if reslut is None:
            self.cursor.execute("INSERT INTO users (FIO,telephone,email) VALUES (%s,%s,%s)",(FIO,telephone,email))
             #commit сохраняем изменение в БД после выполнение запроса SQL
            self.db.commit()
            print("User added")
            return True
        else:
            return False

    #функция получение всех услуг из базы данных хранящихся в таблице service 
    def get_all_service(self):
        options = self.cursor.execute("SELECT * FROM service")
       
        # получаем первую строку данных
        data = self.cursor.fetchall()
        #преобразовали кортеж в список так как метод fethall всегда возвращает кортеж или массив кортежей
        list(data)
        return data
    
    #функция получение цены товара
    def get_price_service(self,name):
        
        self.cursor.execute("SELECT price FROM service WHERE name_service=%s",(name,))
        price = self.cursor.fetchone()
        return price[0]
    
    #функция получение заказа по id
    def get_order(self,id):
        print(type(id))

        self.cursor.execute("SELECT * FROM orders WHERE id=%s",(id,))
        order = self.cursor.fetchone()

        if order is not None:
            

            #Здесь я вытягиваю нужные данные из таблиц для формирования  необходимого мне списка
            #Вот так делать можно, но проще конечно использовать left join для того чтобы вытянуть все необходимое
            #в одном запросе)))))
            self.cursor.execute("SELECT * FROM users WHERE id=%s",(int(order[3]),))
            data_user = self.cursor.fetchone()

            self.cursor.execute("SELECT * FROM personal WHERE id=%s",(int(order[4]),))
            data_personal = self.cursor.fetchone()

            self.cursor.execute("SELECT * FROM service WHERE id=%s",(int(order[5]),))
            data_service = self.cursor.fetchone()


            #собрали все нужные данные
            data_to_display = { 
                "id_order": order[0],
                "name_user": data_user[1],
                'name_service': data_service[1],
                "id_container": order[2], 
                "name_personal": data_personal[1],
                "date": order[1],
                "price": data_service[2]
            }
            #для отладки выводик в консоль можете убрать
            print(data_to_display)
            #вернул собранные данные
            return data_to_display
        else:
            #если условие не выполнилось вернул FALSE 
            return False
        
    #Удаление заказа по id
    def remove_order(self,id):

        #получил кортеж с 1 элементом и вытащил его на всякий случай указал тип int 
        id =int(*id) 
        self.cursor.execute('DELETE FROM orders WHERE id=%s',(id,))
        #commit сохраняем изменение в БД после выполнение запроса SQL
        self.db.commit()

    #обновление информации в заказе
    def update_order(self, id_order, name_user, name_service, id_container):
        print('update func called')
       


        #Получение инф и таблиц 
        result = self.check_user(name_user)
        self.cursor.execute("SELECT id FROM users WHERE FIO=%s",(name_user,))
        user_id = self.cursor.fetchone()

        self.cursor.execute("SELECT * FROM service WHERE name_service=%s",(name_service,))
        data_service = self.cursor.fetchone()
        if data_service is None:
            print(f"No service found with name {name_service}")
            return False
        print(data_service)


        if result is not None:
            self.cursor.execute("UPDATE orders SET id_container=%s,users_id=%s, service_id=%s WHERE id=%s", 
                                (int(id_container),user_id[0],int(data_service[0]),id_order))
             #commit сохраняем изменение в БД после выполнение запроса SQL
            self.db.commit()
            return True
        else:
            return False
    
    #функция закрывает подключение к бд и вырубает  cursor
    def close(self):
        self.cursor.close()
        self.db.close()







        