import requests

class Data:

    def __init__(self, city_name, city_country):

        self.API_KEY = "7e78e9dc22987c9b04c69f1dd31bc505"
        self.BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
        self.city = city_name
        self.country = city_country

        self.weather_data = self.download_json()

        self.scrub()
        self.change_units()


    def download_json(self):

        params = self.city + "," + self.country
        payload = {"q": params, "appid": self.API_KEY, "units": "imperial"}
        req = requests.get(self.BASE_URL, params = payload)

        return req.json()

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