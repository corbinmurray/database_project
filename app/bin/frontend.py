import backend
import tkinter
import ast
# import PIL

class WeatherApp(tkinter.Tk):

    def __init__(self, window_name, window_size):

        self.city = None
        self.date = None
        self.op_list = ["10-1-2018", "Wichita"]

    
        self.database = backend.Database("../data/weather.db")

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


        self.home_label = tkinter.Label(master=self, text="Welcome to Fiesta Weather!", justify = "center", font = ("Tahoma", 20), bg="#42f4e5")
        self.home_label.grid(row=0, column=2, pady = 20)

        self.city_label = tkinter.Label(master = self, text = "Pick Your City", font = ("Tahoma", 18), bg="#42f4e5")
        self.city_label.grid(row = 2, column = 1)

        self.date_label = tkinter.Label(master = self, text = "Choose A Date", font = ("Tahoma", 18), bg="#42f4e5")
        self.date_label.grid(row = 2, column = 3, pady = 20)

        self.run_button = tkinter.Button(master = self, text = "Run", font = ("Tahoma", 18), relief = "sunken", command = lambda: master.switchFrames(SecondPage))
        self.run_button.grid(row = 5, column = 2, pady = 20)

        selectCity = ("Wichita", "Chicago", "Miami")
        self.cities = tkinter.Spinbox(master = self, values = selectCity, font = ("Tahoma", 16))
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

    def update_current_spinbox_data(self, event):
        self.test = [self.date.get(), self.cities.get()]


class SecondPage(tkinter.Frame):

    def __init__(self, master):
        tkinter.Frame.__init__(self, master=master)
        
        """ This is the background color list of our jpgs """
        self.color_dict = {"snowyGIF": "#01ABF5", "cloudsGIF": {"header": "#878787", "body": "#141414"}, "rainingGIF": {"header": "#878787", "body": "#141414"}, "sunnyGIF": "#FEC327"}
        
        self._user_city = master.getCity()
        self._user_date = master.getDate()

        self.weather = master.database.get_weather(city_name=master.getCity(), user_date=master.getDate())
        
        condition = self.weather[3]
        condition = ast.literal_eval(self.weather[3])
        condition = condition["description"]

        self.insert_image(condition)

        self.add_widgets_colorized(condition)


        """BACK BUTTON"""
        self.back = tkinter.Button(master = self, text = "Back", font = ("Tahoma", 17), relief = "sunken", command = lambda: master.switchFrames(HomePage))
        self.back.grid(row = 7, column = 2)

        self.columnconfigure(index = 6, weight = 2)
        self.rowconfigure(index = 6, weight = 1)
        self.rowconfigure(index = 8, weight = 2)

 
    def insert_image(self, weather_condition):
        
        if weather_condition == "Cloudy" or weather_condition == "Partly Cloudy" or weather_condition == "Overcast" or weather_condition == "Mostly Cloudy" or weather_condition == "Scattered Clouds":
            self.fname = "../images/{description}.gif".format(description="clouds")
        elif weather_condition == "Rainy" or weather_condition == "Rain":
            self.fname = "../images/{description}.gif".format(description="raining")
        elif weather_condition == "Snowy" or weather_condition == "Snow":
            self.fname = "../images/{description}.gif".format(description="snowy")
        else:
            self.fname = "../images/{description}.gif".format(description="sunny")

        self.photo = tkinter.PhotoImage(file=self.fname)

        self.test_label = tkinter.Label(master=self, image=self.photo)
        self.test_label.image = self.photo
        self.test_label.place(x=0, y=0, relwidth=1, relheight=1)

        # self.test_label.grid(row=10, column=0)

    def add_widgets_colorized(self, weather_condition):


        if weather_condition == "Cloudy" or weather_condition == "Partly Cloudy" or weather_condition == "Overcast" or weather_condition == "Mostly Cloudy" or weather_condition == "Scattered Clouds":
            hex_color = self.color_dict["cloudsGIF"]
            header = hex_color["header"]
            body = hex_color["body"]

        elif weather_condition == "Rainy" or weather_condition == "Rain":
            hex_color = self.color_dict["rainingGIF"]
            header = hex_color["header"]
            body = hex_color["body"]
            
        elif weather_condition == "Snowy" or weather_condition == "Snow":
            hex_color = self.color_dict["snowyGIF"]
            
        else:
            hex_color = self.color_dict["sunnyGIF"] 

        if type(hex_color) is dict:

            """SHOWS TITLE"""
            
            weatherString = "Weather for {city} on {date}".format(city = self._user_city, date = self._user_date)

            self.title_label = tkinter.Label(master = self, text = weatherString, font = ("Tahoma", 16), bg=header, fg="#ffffff")
            self.title_label.grid(row = 0, column = 2, pady=10)


            coord = self.weather[2]
            coord = ast.literal_eval(self.weather[2])
            lon = coord["lon"]
            lat = coord["lat"]

            self.columnconfigure(index = 0, weight = 2)


            """SHOWS COORDINATES"""
            coordString = "Coordinates ({la}, {lo})".format(la = lat, lo = lon)
            self.coord_label = tkinter.Label(master = self, text = coordString, font = ("Tahoma", 14), bg=body, fg="#ffffff")
            self.coord_label.grid(row = 1, column = 2)

            condition = self.weather[3]
            condition = ast.literal_eval(self.weather[3])
            condition = condition["description"]

            """SHOWS WEATHER DESCRIPTION"""
            descString = "Weather Description: {description}".format(description = condition)
            self.description = tkinter.Label(master = self, text = descString, font = ("Tahoma", 16), bg=body, fg="#ffffff")
            self.description.grid(row = 2, column = 1, padx = 20)

            """SHOWS VISABILITY"""
            vis = self.weather[4]
            if vis >= 10:
                visString = "Visability: {show_vis} miles".format(show_vis = vis)
            else: 
                visString = "Visability: {show_vis} mile".format(show_vis = vis)

            self.visability = tkinter.Label(master = self, text = visString, font = ("Tahoma", 16), bg=body, fg="#ffffff")
            self.visability.grid(row = 3, column = 1, padx = 20)

            self.columnconfigure(index = 2, weight = 2)

            """SHOWS TEMPERATURE"""
            ave_temp = self.weather[5]
            tempString = "Average temperature: {temp} \u00b0F".format(temp = ave_temp)
            self.average = tkinter.Label(master = self, text = tempString, font = ("Tahoma", 16), bg=body, fg="#ffffff")
            self.average.grid(row = 2, column = 3, pady = 5, padx = 20)

            """SHOWS MIN TEMP"""
            min_temp = self.weather[6]
            mintempString = "Minimum temperature: {min} \u00b0F".format(min = min_temp)
            self.minimum = tkinter.Label(master = self, text = mintempString, font = ("Tahoma", 16), bg=body, fg="#ffffff")
            self.minimum.grid(row = 3, column = 3, pady = 5)

            """SHOWS MAX TEMP"""
            max_temp = self.weather[7]
            maxtempString = "Maximum temperature: {max} \u00b0F".format(max = max_temp, )
            self.maximum = tkinter.Label(master = self, text = maxtempString, font = ("Tahoma", 16), bg=body, fg="#ffffff")
            self.maximum.grid(row = 4, column = 3, pady = 5)

            """SHOWS WIND SPEED"""
            windDes = self.weather[10]
            #windDes = ast.literal_eval(windDes[10])
            col_loc = windDes.find(":")
            com_loc = windDes.find(",")
            speed = windDes[col_loc+2:com_loc]

            wind_junior = windDes[com_loc+2:]
            jr_col_loc = wind_junior.find(":")
            direction = wind_junior[jr_col_loc+3:-2]

            # print(direction)
            _windSpeed = "Wind Speed: {_wind} mph".format(_wind = speed)
            self._windspeed = tkinter.Label(master = self, text = _windSpeed, font = ("Tahoma", 16), bg=body, fg="#ffffff")
            self._windspeed.grid(row = 4, column = 1, padx = 20)

            _windDeg = "Wind Direction: {_deg}".format(_deg = direction)
            self._windDeg = tkinter.Label(master = self, text = _windDeg, font = ("Tahoma", 16), bg=body, fg="#ffffff")
            self._windDeg.grid(row = 5, column = 1, padx = 20)
        
        else:

            """SHOWS TITLE"""

            # self._user_city
            # self._user_date
            
            weatherString = "Weather for {city} on {date}".format(city = self._user_city, date = self._user_date)

            self.title_label = tkinter.Label(master = self, text = weatherString, font = ("Tahoma", 17), bg=hex_color)
            self.title_label.grid(row = 0, column = 2, pady=10)


            coord = self.weather[2]
            coord = ast.literal_eval(self.weather[2])
            lon = coord["lon"]
            lat = coord["lat"]

            self.columnconfigure(index = 0, weight = 2)


            """SHOWS COORDINATES"""
            coordString = "Coordinates ({la}, {lo})".format(la = lat, lo = lon)
            self.coord_label = tkinter.Label(master = self, text = coordString, font = ("Tahoma", 14), bg=hex_color)
            self.coord_label.grid(row = 1, column = 2)

            condition = self.weather[3]
            condition = ast.literal_eval(self.weather[3])
            condition = condition["description"]

            """SHOWS WEATHER DESCRIPTION"""
            descString = "Weather Description: {description}".format(description = condition)
            self.description = tkinter.Label(master = self, text = descString, font = ("Tahoma", 16), bg=hex_color)
            self.description.grid(row = 2, column = 1, padx = 20)

            """SHOWS VISABILITY"""
            vis = self.weather[4]
            if vis >= 10:
                visString = "Visability: {show_vis} miles".format(show_vis = vis)
            else: 
                visString = "Visability: {show_vis} mile".format(show_vis = vis)

            self.visability = tkinter.Label(master = self, text = visString, font = ("Tahoma", 16), bg=hex_color)
            self.visability.grid(row = 3, column = 1, padx = 20)

            self.columnconfigure(index = 2, weight = 2)

            """SHOWS TEMPERATURE"""
            ave_temp = self.weather[5]
            tempString = "Average temperature: {temp} \u00b0F".format(temp = ave_temp)
            self.average = tkinter.Label(master = self, text = tempString, font = ("Tahoma", 16), bg=hex_color)
            self.average.grid(row = 2, column = 3, pady = 5, padx = 20)

            """SHOWS MIN TEMP"""
            min_temp = self.weather[6]
            mintempString = "Minimum temperature: {min} \u00b0F".format(min = min_temp)
            self.minimum = tkinter.Label(master = self, text = mintempString, font = ("Tahoma", 16), bg=hex_color)
            self.minimum.grid(row = 3, column = 3, pady = 5)

            """SHOWS MAX TEMP"""
            max_temp = self.weather[7]
            maxtempString = "Maximum temperature: {max} \u00b0F".format(max = max_temp, )
            self.maximum = tkinter.Label(master = self, text = maxtempString, font = ("Tahoma", 16), bg=hex_color)
            self.maximum.grid(row = 4, column = 3, pady = 5)

            """SHOWS WIND SPEED"""
            windDes = self.weather[10]
            #windDes = ast.literal_eval(windDes[10])
            col_loc = windDes.find(":")
            com_loc = windDes.find(",")
            speed = windDes[col_loc+2:com_loc]

            wind_junior = windDes[com_loc+2:]
            jr_col_loc = wind_junior.find(":")
            direction = wind_junior[jr_col_loc+3:-2]

            _windSpeed = "Wind Speed: {_wind} mph".format(_wind = speed)
            self._windspeed = tkinter.Label(master = self, text = _windSpeed, font = ("Tahoma", 16), bg=hex_color)
            self._windspeed.grid(row = 4, column = 1, padx = 20)

            _windDeg = "Wind Direction: {_deg}".format(_deg = direction)
            self._windDeg = tkinter.Label(master = self, text = _windDeg, font = ("Tahoma", 16), bg=hex_color)
            self._windDeg.grid(row = 5, column = 1, padx = 20)







test = WeatherApp(window_name="Fiesta Weather", window_size="800x350")
# test = WeatherApp(window_name="Fiesta Weather", window_size="900x500")
test.run()