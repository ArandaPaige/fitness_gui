import sqlite3
from pathlib import Path

BASE_DIR = Path().resolve()
DATABASE = 'user.db'
DATABASE_PATH = BASE_DIR / DATABASE


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
        PERSON              INT NOT NULL,
        FOREIGN KEY(PERSON) REFERENCES USER(USER_ID));'''
                )
    db.commit()
    db.close()


def retrieve_user(user_id):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    if cur.execute("SELECT USER_ID from USER where USER_ID = ?", (user_id,)) == "":
        return None
    else:
        cur.execute("SELECT USER_ID, NAME, WEIGHT, GOAL, HEIGHT from USER where USER_ID = ?", (user_id,))


def insert_user(user):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('''
    INSERT INTO USER (USER_ID,NAME,WEIGHT,GOAL,HEIGHT) \
        VALUES (?,?,?,?,?)'''), (user.user_id, user.name, user.weight, user.goal_weight, user.height)
    db.commit()
    db.close()


def update_user_name(name, user_id):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('''
        UPDATE USER SET NAME = ? WHERE USER_ID = ?'''), (name, user_id)
    db.commit()
    db.close()


def update_user_weight(weight, user_id):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('''
        UPDATE USER SET WEIGHT = ? WHERE USER_ID = ?'''), (weight, user_id)
    db.commit()
    db.close()

def update_user_goal(goal, user_id):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('''
        UPDATE USER SET GOAL = ? WHERE USER_ID = ?'''), (goal, user_id)
    db.commit()
    db.close()

def update_user_height(height, user_id):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('''
        UPDATE USER SET HEIGHT = ? WHERE USER_ID = ?'''), (height, user_id)
    db.commit()
    db.close()


def insert_weight_entry(entry_id, date, weight):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('''
    INSERT INTO WEIGHT_HISTORY (ID, DATE, WEIGHT) \
        VALUES (?,?,?)'''), (entry_id, date, weight)
    db.commit()
    db.close()


def update_weight_entry(entry_id, weight, date):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('''
    UPDATE WEIGHT_HISTORY SET WEIGHT = ?, SET DATE = ? WHERE ID = ?'''), (weight, date, entry_id)
    db.commit()
    db.close()


def delete_weight_entry(entry_id, date):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('''DELETE from WEIGHT_HISTORY where ID = ?'''), (entry_id,)
    db.commit()
    db.close()
