import sqlite3 
from data import Data
from datetime import datetime
from sqlite3 import Error


class Database:

    def __init__(self, database):
        self.database = database

    def create_table(self):

        sql_commnd = "CREATE TABLE IF NOT EXISTS Weather\
                        (city TEXT, date TEXT, coord TEXT, weather TEXT, visibility INTEGER, temp INTEGER, tempMin INTEGER, tempMax INTEGER, pressure INTEGER, humidity INTEGER, wind TEXT)"

        try:
            self.curs.execute(sql_commnd)
        except Error as e:
            print(e)
            print("Error executing create_table")

    def insert(self, data_obj):
        # Anything CAPITALIZED is a sql command 
        today_date = datetime.today()
        today = "{month}-{day}-{year}".format(month=today_date.month,day=today_date.day, year=today_date.year)
        
        sql_insert_command = "INSERT INTO Weather (city, date, coord, weather, visibility, temp, tempMin, tempMax, pressure, humidity, wind) VALUES (?,?,?,?,?,?,?,?,?,?,?)"
        
        value_tuple = [] 

        value_tuple.append(data_obj.weather_data["name"])
        value_tuple.append(today)
        value_tuple.append(str(data_obj.weather_data["coord"]))
        value_tuple.append(str(data_obj.weather_data["weather"][0]))
        value_tuple.append(data_obj.weather_data["visibility"])
        value_tuple.append(data_obj.weather_data["main"]["temp"])
        value_tuple.append(data_obj.weather_data["main"]["temp_min"])
        value_tuple.append(data_obj.weather_data["main"]["temp_max"])
        value_tuple.append(data_obj.weather_data["main"]["pressure"])
        value_tuple.append(data_obj.weather_data["main"]["humidity"])
        value_tuple.append(str(data_obj.weather_data["wind"]))

        value_tuple = tuple(value_tuple)

        try:
            self.curs.execute(sql_insert_command, value_tuple)
            self.conn.commit()
        except Error as e:
            print(e, "\nError inserting")

        
    def open(self):

        try:
            self.conn = sqlite3.connect(self.database)
            self.curs = self.conn.cursor()
        except:
            print("Error making database connection")
        
    def close(self):

        self.conn.close()

    def view_all(self):

        self.curs.execute("SELECT * FROM Weather")
        

        [print(row, "\n") for row in self.curs.fetchall()]
    
    def delete_table(self):

        self.curs.execute("DROP TABLE IF EXISTS Weather")
        self.conn.commit()



      




# --- Testing --- #


test = Database("weather.db")

test.open()


test.close()
