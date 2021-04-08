import sqlite3
from pathlib import Path
import datetime
from user import User

BASE_DIR = Path().resolve()
DATABASE = 'user.db'
DATABASE_PATH = BASE_DIR / DATABASE
DATETODAY = str(datetime.date.today())


def create_user_tables():
    db = sqlite3.connect(DATABASE)
    db.execute("PRAGMA foreign_keys = 1")
    cur = db.cursor()
    cur.execute('''
    CREATE TABLE USER
        (USER_ID INTEGER PRIMARY KEY NOT NULL,
        NAME            TEXT NOT NULL,
        WEIGHT          REAL NOT NULL,
        GOAL            REAL NOT NULL,
        HEIGHT          INT NOT NULL);'''
                )

    cur.execute('''
    CREATE TABLE WEIGHT_HISTORY
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        DATE                TEXT NOT NULL,
        WEIGHT              REAL NOT NULL,
        PERSON_ID           INT NOT NULL,
        FOREIGN KEY(PERSON_ID) REFERENCES USER(USER_ID));'''
                )
    db.commit()
    db.close()


def retrieve_user(user_id):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    if cur.execute("SELECT USER_ID from USER where USER_ID = ?", (user_id,)) == "":
        return None
    else:
        user_data = cur.execute("SELECT NAME, WEIGHT, GOAL, HEIGHT from USER where USER_ID = ?", (user_id,))
        row = user_data.fetchone()
        user_history = cur.execute("SELECT DATE, WEIGHT from WEIGHT_HISTORY where PERSON_ID = ?", (user_id,))
        row_history = user_history.fetchall()
        user = User(name=row[0], weight=row[1], goal=row[2], height=row[3], weight_history=row_history)
        return user


def insert_user(user):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('''
    INSERT INTO USER (NAME,WEIGHT,GOAL,HEIGHT) 
        VALUES (?,?,?,?)''', (user.name, user.weight, user.goal, user.height))
    cur.execute('''
    INSERT INTO WEIGHT_HISTORY (DATE, WEIGHT, PERSON_ID)
        VALUES (?,?,?)''', (DATETODAY, user.weight, user.user_id))
    db.commit()
    db.close()


def load_user_history(user):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    user_history = cur.execute("SELECT DATE, WEIGHT from WEIGHT_HISTORY where PERSON_ID = ?", (user.user_id,))
    row_history = user_history.fetchall()
    user.set_weight_history(row_history)


def update_user_name(name, user_id):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('''
        UPDATE USER SET NAME = ? WHERE USER_ID = ?''', (name, user_id))
    db.commit()
    db.close()


def update_user_weight(weight, user_id):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('''
        UPDATE USER SET WEIGHT = ? WHERE USER_ID = ?''', (weight, user_id))
    db.commit()
    db.close()


def update_user_goal(goal, user_id):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('''
        UPDATE USER SET GOAL = ? WHERE USER_ID = ?''', (goal, user_id))
    db.commit()
    db.close()


def update_user_height(height, user_id):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('''
        UPDATE USER SET HEIGHT = ? WHERE USER_ID = ?''', (height, user_id))
    db.commit()
    db.close()


def insert_weight_entry(date, weight, person_id):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('''
    INSERT INTO WEIGHT_HISTORY (DATE, WEIGHT, PERSON_ID) 
        VALUES (?,?,?)''', (date, weight, person_id))
    db.commit()
    db.close()


def update_weight_entry(entry_id, weight, date):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('''
    UPDATE WEIGHT_HISTORY SET WEIGHT = ?, SET DATE = ? WHERE ID = ?''', (weight, date, entry_id))
    db.commit()
    db.close()


def delete_weight_entry(entry_id):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('''DELETE from WEIGHT_HISTORY where ID = ?''', (entry_id,))
    db.commit()
    db.close()
