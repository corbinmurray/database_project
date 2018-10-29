import backend
import tkinter

class WeatherApp(tkinter.Tk):

    def __init__(self, window_name, window_size):

        tkinter.Tk.__init__(self)

        self.title(window_name)
        self.geometry(window_size)

        self.frames = []

        frame = HomePage(master=self)

        self.frames.append(frame)

        self.frames[0].pack(fill="both", expand=True)

        
    def run(self):
        self.mainloop()


class HomePage(tkinter.Frame):

    def __init__(self, master):
        tkinter.Frame.__init__(self, master=master, background="#42f4e5")

        self.home_label = tkinter.Label(master=self, text="Home Page Label Bitches")
        self.home_label.grid(row=0, column=0)



test = WeatherApp(window_name="Weather Application", window_size="600x500")

test.run()
