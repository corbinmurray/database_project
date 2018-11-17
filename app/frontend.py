import backend
import tkinter
import ast

class WeatherApp(tkinter.Tk):

    def __init__(self, window_name, window_size):

        self.city = None
        self.date = None
        self.op_list = ["10-1-2018", "Wichita"]

    
        self.database = backend.Database("data/weather.db")

        tkinter.Tk.__init__(self)

        self.frame = HomePage(master=self)
        self.frame.pack(fill="both", expand=True)

        self.title(window_name)
        self.geometry(window_size)  

        # self.switchFrames(HomePage)

    def switchFrames(self, frame):


        if frame is SecondPage:
            try:
                self.op_list = self.frame.test
            except AttributeError:
                pass


        self.frame.destroy()


        initFrame = frame(master=self)
        self.frame = initFrame
        self.frame.pack(fill="both", expand=True)


    def getCity(self):
        # self.city = self.first.getSpinboxCity()
        return self.op_list[1]

    def getDate(self):
        # self.date = self.first.getSpinboxDate()
        return self.op_list[0]

    def getop(self):
        return self.op_list

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


        self.home_label = tkinter.Label(master=self, text="Welcome to Weather Finder", justify = "center", font = ("Tahoma", 18), bg="#42f4e5")
        self.home_label.grid(row=0, column=2, pady = 20)

        self.city_label = tkinter.Label(master = self, text = "Pick Your City", font = ("Tahoma", 16), bg="#42f4e5")
        self.city_label.grid(row = 2, column = 1)

        self.date_label = tkinter.Label(master = self, text = "Choose A Date", font = ("Tahoma", 16), bg="#42f4e5")
        self.date_label.grid(row = 2, column = 3, pady = 20)

        self.run_button = tkinter.Button(master = self, text = "Run", font = ("Tahoma", 16), relief = "sunken", command = lambda: master.switchFrames(SecondPage))
        self.run_button.grid(row = 5, column = 2, pady = 20)

        selectCity = ("Wichita", "Chicago", "Miami")
        self.cities = tkinter.Spinbox(master = self, values = selectCity, font = ("Tahoma", 14))
        self.cities.grid(row = 3, column = 1)

        
        """ Creating List of dates, less complicated than trying to generate from database """
        date_list = []

        date_string = "{_month}-{_day}-2018"

        for month in range(10,12):        
            for day in range(1, 32):
                if month == 11 and day == 31:
                    break
                else:
                    date_list.append(date_string.format(_month=month, _day=day))

        self.date = tkinter.Spinbox(master = self, values = tuple(date_list), font = ("Tahoma", 14))
        self.date.grid (row = 3, column = 3)

        self.cities.bind("<Leave>", self.update_current_spinbox_data)
        self.date.bind("<Leave>", self.update_current_spinbox_data)


    # def getSpinboxDate(self):
    #     print("From getSpinboxDate: ", self.date.get())
    #     return self.date.get()
        
    # def getSpinboxCity(self):
    #     print("From getSpinboxCity: ", self.cities.get())
    #     return self.cities.get()

    def update_current_spinbox_data(self, event):
        self.test = [self.date.get(), self.cities.get()]


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
        

        self.title_label = tkinter.Label(master = self, text = weatherString, font = ("Tahoma", 18), padx=10, pady=10)
        self.title_label.grid(row = 0, column = 2, pady=10, padx=10)

        user_city = master.getCity()
        _date = master.getDate()

        weather = master.database.get_weather(city_name=user_city, user_date=_date)

        coord = weather[2]
        coord = ast.literal_eval(weather[2])
        lon = coord["lon"]
        lat = coord["lat"]

        self.columnconfigure(index = 0, weight = 2)

        # # # print(weather)

        """SHOWS COORDINATES"""
        coordString = "Coordinates ({la}, {lo})".format(la = lat, lo = lon)
        self.coord_label = tkinter.Label(master = self, text = coordString, font = ("Tahoma", 12))
        self.coord_label.grid(row = 1, column = 2)

        condition = weather[3]
        condition = ast.literal_eval(weather[3])
        condition = condition["description"]

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
        self.average.grid(row = 3, column = 3)

        """SHOWS MIN TEMP"""
        min_temp = weather[6]
        mintempString = "Minimum temperature: {min} \u00b0F".format(min = min_temp)
        self.minimum = tkinter.Label(master = self, text = mintempString, font = ("Tahoma", 14))
        self.minimum.grid(row = 4, column = 3)

        """SHOWS MAX TEMP"""
        max_temp = weather[7]
        maxtempString = "Maximum temperature: {max} \u00b0F".format(max = max_temp, )
        self.maximum = tkinter.Label(master = self, text = maxtempString, font = ("Tahoma", 14))
        self.maximum.grid(row = 2, column = 3)

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


# test = WeatherApp(window_name="Fiesta Weather", window_size="700x300")
test = WeatherApp(window_name="Fiesta Weather", window_size="900x500")
test.run()
