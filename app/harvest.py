import backend
import sys



def main():

	
	database = backend.Database("data/weather.db")

	if sys.argv[1] == None:

		cities = ["Wichita", "Chicago", "Miami"]

		for city in cities:
			obj = backend.Data(city_name=city)
			database.insert(obj)

	if sys.argv[1] == "-v" or sys.argv[1] == "--view":
		database.pretty_print()
	elif sys.argv[1] == "-d" or sys.argv[1] == "-dates":
		print(database.get_range_dates())



if __name__ == "__main__":
    main()