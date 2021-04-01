import sqlite3
from pathlib import Path

BASE_DIR = Path().resolve()
DATABASE = 'user.db'
DATABASE_PATH = BASE_DIR / DATABASE


def create_database():
    if DATABASE_PATH.exists() == False:
        create_user_table()
        create_weight_history_table()
    else:
        retrieve_user(user_id=1)


def create_user_table():
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


def create_weight_history_table():
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('''
    CREATE TABLE WEIGHT_HISTORY
        (DATE TEXT PRIMARY KEY NOT NULL,
        WEIGHT             REAL NOT NULL);'''
                )
    db.commit()
    db.close()


def retrieve_user(user_id):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    if cur.execute("SELECT ID from USER where ID = ?", (user_id,)) == "":
        pass
    else:
        cur.execute("SELECT ID, NAME, WEIGHT, HEIGHT from USER where ID = ?", (user_id,))


def insert_user(user):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('''
    INSERT INTO USER (ID,NAME,WEIGHT,HEIGHT) \
        VALUES (?,?,?,?)'''), (user.user_id, user.name, user.weight, user.height)
    db.commit()
    db.close()


def insert_weight_entry(date, weight):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('''
    INSERT INTO WEIGHT_HISTORY (DATE, WEIGHT) \
        VALUES (?,?)'''), (date, weight)
    db.commit()
    db.close()


def update_weight_entry(date, weight):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('''
    UPDATE WEIGHT_HISTORY SET WEIGHT = ? WHERE ID = ?'''), (weight, date)
    db.commit()
    db.close()


def delete_weight_entry(date):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('''DELETE from WEIGHT_HISTORY where DATE = ?'''), (date,)
    db.commit()
    db.close()
