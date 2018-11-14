import backend
import tkinter
import ast

class WeatherApp(tkinter.Tk):

    def __init__(self, window_name, window_size):

        self.database = backend.Database("data/weather.db")

        tkinter.Tk.__init__(self)

        self.title(window_name)
        self.geometry(window_size)

        self.frame = None

        
        self.first = HomePage(master=self)
        self.second = SecondPage(master=self)
        
        self.switchFrames(HomePage)

        # frame = HomePage(master=self)

        # self.frames.append(frame)

        # self.frames[0].pack(fill="both", expand=True)

        # frameTwo = SecondPage(master = self)
        # self.frames.append(frameTwo)

    def switchFrames(self, frame):
        initFrame = frame(master=self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = initFrame
        self.frame.pack(fill="both", expand=True)


    def getCity(self):
        self.city = self.first.getSpinboxCity()
        return self.city
    def getDate(self):
        self.date = self.first.getSpinboxDate()
        return self.date


        
    def run(self):
        self.mainloop()


class HomePage(tkinter.Frame):

    def __init__(self, master):
        tkinter.Frame.__init__(self, master=master, background="#42f4e5")

        self.columnconfigure(index = 0, weight = 1)
        #self.columnconfigure(index = 3, weight = 1)
        self.columnconfigure(index = 4, weight = 1)
        
        #self.rowconfigure(index = 0, weight = 1)
        self.rowconfigure(index = 1, weight = 1)
        self.rowconfigure(index = 7, weight = 1)
        self.rowconfigure(index = 6, weight = 2)


        self.home_label = tkinter.Label(master=self, text="Welcome to Weather Finder", justify = "center", font = ("Tahoma", 18))
        self.home_label.grid(row=0, column=2, pady = 20)

        self.city_label = tkinter.Label(master = self, text = "Pick Your City", font = ("Tahoma", 16))
        self.city_label.grid(row = 2, column = 1)

        self.date_label = tkinter.Label(master = self, text = "Choose A Date", font = ("Tahoma", 16))
        self.date_label.grid(row = 2, column = 3, pady = 20)

        self.run_button = tkinter.Button(master = self, text = "Run", font = ("Tahoma", 16), relief = "sunken", command = lambda: master.switchFrames(SecondPage))
        self.run_button.grid(row = 5, column = 2, pady = 20)

        selectCity = ("Denver", "Wichita", "Chicago", "Miami")
        self.cities = tkinter.Spinbox(master = self, values = selectCity, font = ("Tahoma", 14))
        self.cities.grid(row = 3, column = 1)

        
        
        #selectDate = ("Mackenzie", "Mckenzie", "McKenzie", "Mac", "Cheese", "mmmm")
        self.date = tkinter.Spinbox(master = self, values = tuple(master.database.get_range_dates()), font = ("Tahoma", 14))
        self.date.grid (row = 3, column = 3)

    def getSpinboxDate(self):
        return self.date.get()
        
    def getSpinboxCity(self):
        return self.cities.get()


class SecondPage(tkinter.Frame):

    def __init__(self, master):
        tkinter.Frame.__init__(self, master=master)

        """BACK BUTTON"""
        self.back = tkinter.Button(master = self, text = "Back", font = ("Tahoma", 15), relief = "sunken", command = lambda: master.switchFrames(HomePage))
        self.back.grid(row = 7, column = 3)

        self.columnconfigure(index = 6, weight = 2)
        self.rowconfigure(index = 6, weight = 1)
        self.rowconfigure(index = 8, weight = 2)

        """SHOWS TITLE"""
        weatherString = "Weather for {city} on {date}".format(city = master.getCity(), date = master.getDate())
        self.title_label = tkinter.Label(master = self, text = weatherString, font = ("Tahoma", 18))
        self.title_label.grid(row = 0, column = 2, pady = 10)

        user_city = master.getCity()
        _date = master.getDate()

        weather = master.database.get_weather(city_name=user_city, user_date=_date)

        coord = weather[2]
        coord = ast.literal_eval(weather[2])
        lon = coord["lon"]
        lat = coord["lat"]

        self.columnconfigure(index = 0, weight = 2)

        # print(weather)

        """SHOWS COORDINATES"""
        coordString = "Coordinates ({la}, {lo})".format(la = lat, lo = lon)
        self.coord_label = tkinter.Label(master = self, text = coordString, font = ("Tahoma", 12))
        self.coord_label.grid(row = 1, column = 2)

        condition = weather[3]
        condition = ast.literal_eval(weather[3])
        condition = condition["main"]

        """SHOWS WEATHER DESCRIPTION"""
        descString = "Weather Description: {description}".format(description = condition)
        self.description = tkinter.Label(master = self, text = descString, font = ("Tahoma", 14))
        self.description.grid(row = 2, column = 1)

        """SHOWS VISABILITY"""
        vis = weather[4]
        visString = "Visability: {show_vis} miles".format(show_vis = vis)
        self.visability = tkinter.Label(master = self, text = visString, font = ("Tahoma", 14))
        self.visability.grid(row = 3, column = 1)

        self.columnconfigure(index = 2, weight = 2)

        """SHOWS TEMPERATURE"""
        ave_temp = weather[5]
        tempString = "Average temperature: {temp} \u00b0F".format(temp = ave_temp)
        self.average = tkinter.Label(master = self, text = tempString, font = ("Tahoma", 14))
        self.average.grid(row = 2, column = 3)

        """SHOWS MIN TEMP"""
        min_temp = weather[6]
        mintempString = "Minimum temperature: {min} \u00b0F".format(min = min_temp)
        self.minimum = tkinter.Label(master = self, text = mintempString, font = ("Tahoma", 14))
        self.minimum.grid(row = 3, column = 3)

        """SHOWS MAX TEMP"""
        max_temp = weather[6]
        maxtempString = "Maximum temperature: {max} \u00b0F".format(max = max_temp, )
        self.maximum = tkinter.Label(master = self, text = maxtempString, font = ("Tahoma", 14))
        self.maximum.grid(row = 4, column = 3)

        """SHOWS WIND SPEED"""
        windDes = weather[10]
        #windDes = ast.literal_eval(windDes[10])
        col_loc = windDes.find(":")
        com_loc = windDes.find(",")
        speed = windDes[col_loc+2:com_loc]

        wind_junior = windDes[com_loc+2:]
        jr_col_loc = wind_junior.find(":")
        direction = wind_junior[jr_col_loc+3:-2]

        # print(direction)
        _windSpeed = "Wind Speed: {_wind} mph".format(_wind = speed)
        self._windspeed = tkinter.Label(master = self, text = _windSpeed, font = ("Tahoma", 14))
        self._windspeed.grid(row = 4, column = 1)

        _windDeg = "Wind Direction: {_deg}".format(_deg = direction)
        self._windDeg = tkinter.Label(master = self, text = _windDeg, font = ("Tahoma", 14))
        self._windDeg.grid(row = 5, column = 1)


test = WeatherApp(window_name="Fiesta Weather", window_size="700x300")

test.run()
