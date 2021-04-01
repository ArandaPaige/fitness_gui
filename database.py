import sqlite3

DATABASE = 'user.db'


class UserDB(sqlite3):
    '''Class docstring'''

    def __init__(self):
        super().__init__()
        self.user = None

    @staticmethod
    def create_user_table(self):
        db = sqlite3.connect(DATABASE)
        cur = db.cursor()
        cur.execute('''
        CREATE TABLE USER
            (ID INT PRIMARY KEY NOT NULL,
            NAME            TEXT NOT NULL,
            WEIGHT          REAL NOT NULL,
            HEIGHT          INT NOT NULL);'''
                    )
        db.commit()
        db.close()

    @staticmethod
    def create_weight_history_table(self):
        db = sqlite3.connect(DATABASE)
        cur = db.cursor()
        cur.execute('''
        CREATE TABLE WEIGHT_HISTORY
            (DATE TEXT PRIMARY KEY NOT NULL,
            WEIGHT             REAL NOT NULL);'''
                    )
        db.commit()
        db.close()

    def retrieve_user(self, user_id):
        db = sqlite3.connect(DATABASE)
        cur = db.cursor()
        if cur.execute("SELECT ID from USER where ID = 1") == "":
            pass
        else:
            cur.execute("SELECT ID, NAME, WEIGHT, HEIGHT from USER where ID = 1")

    def insert_user(self, user_id, name, weight, height):
        db = sqlite3.connect(DATABASE)
        cur = db.cursor()
        cur.execute('''
        INSERT INTO USER (ID,NAME,WEIGHT,HEIGHT) \
            VALUES (?,?,?,?)'''), (user_id, name, weight, height)
        db.commit()
        db.close()

    def insert_weight_entry(self, date, weight):
        db = sqlite3.connect(DATABASE)
        cur = db.cursor()
        cur.execute('''
        INSERT INTO WEIGHT_HISTORY (DATE, WEIGHT) \
            VALUES (?,?)'''), (date, weight)
        db.commit()
        db.close()

    def update_weight_entry(self, date, weight):
        db = sqlite3.connect(DATABASE)
        cur = db.cursor()
        cur.execute('''
        UPDATE WEIGHT_HISTORY SET WEIGHT = ? WHERE ID = ?'''), (weight, date)
        db.commit()
        db.close()

    def delete_weight_entry(self, date):
        db = sqlite3.connect(DATABASE)
        cur = db.cursor()
        cur.execute('''DELETE from WEIGHT_HISTORY where DATE = ?'''), (date,)
        db.commit()
        db.close()
