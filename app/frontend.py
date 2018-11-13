import backend
import tkinter

class WeatherApp(tkinter.Tk):

    def __init__(self, window_name, window_size):

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

        self.run_button = tkinter.Button(master = self, text = "Run", font = ("Tahoma", 14), relief = "sunken", command = lambda: master.switchFrames(SecondPage))
        self.run_button.grid(row = 5, column = 2, pady = 20)

        selectCity = ("Denver", "Wichita", "Chicago", "Miami")
        self.cities = tkinter.Spinbox(master = self, values = selectCity, font = ("Tahoma", 14))
        self.cities.grid(row = 3, column = 1)

        database = backend.Database("data/weather.db")
        
        #selectDate = ("Mackenzie", "Mckenzie", "McKenzie", "Mac", "Cheese", "mmmm")
        self.date = tkinter.Spinbox(master = self, values = tuple(database.get_range_dates()), font = ("Tahoma", 14))
        self.date.grid (row = 3, column = 3)

    def getSpinboxDate(self):
        return self.date.get()
        
    def getSpinboxCity(self):
        return self.cities.get()


class SecondPage(tkinter.Frame):

    def __init__(self, master):
        tkinter.Frame.__init__(self, master=master, background="#42f480")

        weatherString = "Weather for {city} on {date}".format(city = master.getCity(), date = master.getDate())

        self.title_label = tkinter.Label(master = self, text = weatherString, font = ("Tahoma", 14))
        self.title_label.grid(row=0, column=0)

        coordString = "Lat: {lat}, Lon: {lon}". format(lat = master.getLat(), lon = master.getLon())
        self.coord_label = tkinter.Label(master = self, text = coordString)

        self.description = tkinter.Label(master = self, text = "Weather Description", font = ("Tahoma", 14))
        self.description.grid(row = 2, column = 0)

test = WeatherApp(window_name="Fiesta Weather", window_size="700x300")

test.run()
