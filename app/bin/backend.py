import sqlite3 
from datetime import datetime
from sqlite3 import Error
import requests
import pprint

class Data:

    def __init__(self, city_name, city_country="United States"):

        self.API_KEY = "7e78e9dc22987c9b04c69f1dd31bc505"
        self.BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
        self.city = city_name
        self.country = city_country

        self.weather_data = self.download_json()

        self.scrub()
        self.change_units()


    def download_json(self):

        try:
            params = self.city + "," + self.country
            payload = {"q": params, "appid": self.API_KEY, "units": "imperial"}
            req = requests.get(self.BASE_URL, params = payload)
            return req.json()
        except Exception as e:
            print(e, "\n\n")
            print("Error downloading json")
            return None
        

    def scrub(self):
        # base, clouds, cod, dt, id, sys, [weather][icon], [weather][id]

        del self.weather_data["base"]
        del self.weather_data["clouds"]
        del self.weather_data["cod"]
        del self.weather_data["dt"]
        del self.weather_data["id"]
        del self.weather_data["sys"]
        del self.weather_data["weather"][0]["icon"]
        del self.weather_data["weather"][0]["id"]

    def change_units(self):
        # 33.8638 hPa to 1 inHg -> converting hPa to inHg
        self.weather_data["main"]["pressure"] /= 33.8638
        self.weather_data["main"]["pressure"] = round(self.weather_data["main"]["pressure"], 2)

        # 0.000621371 miles in 1 meter -> meters to miles
        self.weather_data["visibility"] *= 0.000621371
        self.weather_data["visibility"] = round(self.weather_data["visibility"], 2) 

        # 0 is N, 90 is E, 180 is S, 270 is W  -> changing meterological directions to cardinal
        try:
            degree = self.weather_data["wind"]["deg"]
            if degree > 0 and degree < 90:
                self.weather_data["wind"]["deg"] = "NE"
            elif degree > 90 and degree < 180:
                self.weather_data["wind"]["deg"] = "SE"
            elif degree > 180 and degree < 270:
                self.weather_data["wind"]["deg"] = "SW"
            elif degree > 270 and degree < 360:
                self.weather_data["wind"]["deg"] = "NW"
            elif degree == 0:
                self.weather_data["wind"]["deg"] = "N"
            elif degree == 90:
                self.weather_data["wind"]["deg"] = "E"
            elif degree == 180:
                self.weather_data["wind"]["deg"] = "S"
            elif degree == 270:
                self.weather_data["wind"]["deg"] = "W"
        except KeyError:
            pass

class Database:

    def __init__(self, database):
        self.database = database

    def create_table(self):
        self.open()

        sql_commnd = "CREATE TABLE IF NOT EXISTS Weather\
                        (city TEXT, date TEXT, coord TEXT, weather TEXT, visibility INTEGER, temp INTEGER, tempMin INTEGER, tempMax INTEGER, pressure INTEGER, humidity INTEGER, wind TEXT)"

        try:
            self.curs.execute(sql_commnd)
        except sqlite3.Error as e:
            print(e)
            print("Error executing create_table")
        
        self.close()

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

        self.open()

        try:
            self.curs.execute(sql_insert_command, value_tuple)
            self.conn.commit()
        except sqlite3.Error as e:
            print(e, "\nError inserting")

        self.close()

        
    def open(self):

        try:
            self.conn = sqlite3.connect(self.database)
            self.curs = self.conn.cursor()
        except:
            print("Error making database connection")
        
    def close(self):

        self.conn.close()

    def view_all(self):

        self.open()

        self.curs.execute("SELECT * FROM Weather")
        

        [print(row, "\n") for row in self.curs.fetchall()]

        self.close()
    
    def delete_table(self):
        self.open()

        self.curs.execute("DROP TABLE IF EXISTS Weather")
        self.conn.commit()

        self.close()

    def get_weather(self, city_name, user_date):
        self.open()

        sql_command = "SELECT * FROM Weather WHERE city = (?) AND date = (?)"

        try:
            self.curs.execute(sql_command, (city_name,user_date) )
            return self.curs.fetchall()[0]
        except Exception as e:
            print(e, "\n\n")
            print("Error in get_weather")

        self.close()
    
    def pretty_print(self):
        pp = pprint.PrettyPrinter(indent=4)
        self.open()
        self.curs.execute("SELECT * From Weather")
        [pp.pprint(data) for data in self.curs.fetchall()]
        self.close()

    # def get_range_dates(self):
    #     self.open()
    #     self.curs.execute("SELECT date From Weather")
    #     dates = list(set(self.curs.fetchall()))
    #     self.close()

    #     temp = dates.copy()
    #     dates.clear()

    #     [dates.append(element[0]) for element in temp]

    #     dates.sort()
    #     print(dates)

    #     dates.insert(1, dates[11])
    #     dates.insert(2, dates[22])

        
    #     # [print(element) for element in dates]
    #     # print("Dates: ", dates, "\n", "Type: ", type(dates), "\n\n")
    #     # print("Type of each element: ", type(dates[0][0]))
    #     # dates = set(sorted(dates))
        
    #     return dates
    
    def getCoord(self, user_city):
        self.open()
        string = "SELECT coord FROM Weather WHERE city = (?)"
        self.curs.execute(string, (user_city))
        temp = self.curs.fetchall()
        self.close()
        return temp

        
        

        
        
        