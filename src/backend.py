import sqlite3 
from data import Data


class Database:

    def __init__(self, database):
        self.database = database

    def create_table(self):

        sql_cmmnd = "CREATE TABLE IF NOT EXISTS Weather(city TEXT, date TEXT, coord BLOB, main TEXT, visibility INTEGER, conditions TEXT, wind TEXT)"

        try:
            self.curs.execute(sql_cmmnd)
        except Error as e:
            print(e)
            print("Error executing create_table")
 

        
    def open(self):

        try:
            self.conn = sqlite3.connect(self.database)
            self.curs = self.conn.cursor()
        except:
            print("Error making database connection")
        
    def close(self):

        self.conn.close()




# --- Testing --- #


test = Database("weather.db")

test.open()

test.create_table()

test.close()
