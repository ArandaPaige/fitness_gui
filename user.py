import sqlite3
import datetime

DATETODAY = datetime.date.today()
DATABASE = 'user.db'


class User:
    '''
    A user is documented with their personal health and fitness statistics.
    These statistics are collated to generate useful data, like the trajectory of
    their weight loss/gain.
    '''

    def __init__(self, name=None, starting_weight=None, current_weight=None, height=None,
                 weight_history=None):
        self.ID = 1
        self.name = name
        self.starting_weight = starting_weight
        self.current_weight = current_weight
        self.height = height
        self.weight_history = weight_history

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

    def retrieve_user(self):
        db = sqlite3.connect(DATABASE)
        cur = db.cursor()
        if cur.execute("SELECT name from USER") == None:
            pass

    def insert_user(self):
        db = sqlite3.connect(DATABASE)
        cur = db.cursor()
        cur.execute('''
        INSERT INTO USER (ID,NAME,WEIGHT,HEIGHT) \
            VALUES (?,?,?,?)'''), (self.ID, self.name, self.current_weight, self.height)
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
        UPDATE WEIGHT_HISTORY SET WEIGHT = ? WHERE ID =  ?'''), (weight, date)
        db.commit()
        db.close()

    def delete_weight_entry(self, date):
        db = sqlite3.connect(DATABASE)
        cur = db.cursor()
        cur.execute('''DELETE from WEIGHT_HISTORY where DATE = (?)'''), (date,)
        db.commit()
        db.close()

    def user_setup(self, name=None, starting_weight=None, current_weight=None, height=None):
        if name != None:
            self.name = name
            print(f'Name is {name.text()}')
        if starting_weight != None:
            self.starting_weight = float(starting_weight.text())
            print(f'Starting weight is {starting_weight.text()}')
        if current_weight != None:
            self.current_weight = float(current_weight.text())
            print(f'Current weight is {current_weight.text()}')
        if height != None:
            self.height = int(height.text())
            print(f'Height is {height.text()}')

    def set_name(self, name):
        self.name = name

    def set_starting_weight(self, weight):
        self.starting_weight = weight

    def set_current_weight(self, weight):
        self.current_weight = weight

    def set_height(self, height):
        self.height = height

    def convert_height_metric(self):
        pass

    def convert_weight_metric(self):
        pass

    def user_dict_create(self, name, startingweight, currentweight, height, weight_history=None):
        '''
        Creates a dictionary with all of the user's personal statistics to be serialized as JSON.
        :param name: User's full name
        :param startingweight: The user's starting weight.
        :param currentweight: The user's current weight.
        :param height: The user's height.
        :param weight_history: User's weight history is mapped by date.
        :return Dictionary: a dictionary containing the user's personal statistics.
        '''
        if weight_history == None:
            return {
                'name': name,
                'starting weight': startingweight,
                'current weight': currentweight,
                'height': height,
                'weight history': {
                    str(DATETODAY): currentweight
                }
            }
        else:
            return {
                'name': name,
                'starting weight': startingweight,
                'current weight': currentweight,
                'height': height,
                'weight history': weight_history
            }