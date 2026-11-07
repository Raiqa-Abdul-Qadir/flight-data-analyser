"""
****************************************************************************
Additional info
 1. I declare that my work contins no examples of misconduct, such as
 plagiarism, or collusion.
 2. Any code taken from other sources is referenced within my code solution.
 3. Student ID: w2181572
 4. Date: 09/11/2025
****************************************************************************

"""
from graphics import *
import csv
import math

data_list = []   # data_list An empty list to load and hold data from csv file

def load_csv(CSV_chosen):
    """
    This function loads any csv file by name (set by the variable 'selected_data_file') into the list "data_list"
    YOU DO NOT NEED TO CHANGE THIS BLOCK OF CODE
    """
    with open(CSV_chosen, 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            data_list.append(row)



#************************************************************************************************************

#EDIT THE CODE BELOW TO COMPLETE YOUR SUBMISSION

def main():
    """
    This function is to analyze and visualize flight data from CSV files
    """
    # valid airport codes
    valid_airports = {
        "LHR" : "London Heathrow",
        "MAD" : "Madrid Adolfo Suárez-Barajas",
        "CDG" : "Charles De Gaulle International",
        "IST" : "Istanbul Airport International",
        "AMS" : "Amsterdam Schiphol",
        "LIS" : "Lisbon Portela",
        "FRA" : "Frankfurt Main",
        "FCO" : "Rome Fiumicino",
        "MUC" : "Munich International",
        "BCN" : "Barcelona International",
    }

    while True:
        
        # city code prompt
        print("\nPlease enter a three-letter city code: ", end = "")
        while True:
            airport_input = input().upper().strip()
            if len(airport_input) != 3:
                print("Wrong code length - please enter a three-letter city code: ", end = "")
                continue # skips the current iteration and continues the loop
            elif airport_input not in valid_airports:
                print("Unavailable city code - please enter a valid city code: ", end = "")
                continue # skips the current iteration and continues the loop
            else:
                break # loop stops entirely


        # year prompt
        print("\nPlease enter the year required in the format YYYY: ", end = "")
        while True:
            year_input = input().upper().strip()
            if not year_input.isdigit() or len(year_input) != 4:
                print("Wrong data type - please enter a four-digit year value: ", end = "")
                continue # skips the current iteration and continues the loop
            elif int(year_input) < 2000 or int(year_input) > 2025:
                print("Out of range - please enter a value from 2000 to 2025: ", end = "")
                continue # skips the current iteration and continues the loop
            else:
                break # loop stops entirely
        
        # the variable "selected_data_file" is set based on user input
        selected_data_file = f"{airport_input}{year_input}.csv"

        # console output
        print("\n" + "*" * 75)
        print(f"{selected_data_file} selected - Planes departing {valid_airports[airport_input]} {year_input}")
        print("" + "*" * 75)


        # load the CSV file
        data_list.clear() # clears all the data from the previous run
        try:
            data = load_csv(selected_data_file) # loads CSV into a new variable
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            continue # skips the current iteration and continues the loop
 
        # Initialization
        total_flights = len(data_list)
        terminal_2_count = 0
        under_600_miles_count = 0
        air_france_count = 0
        temperatures_below_15_count = 0
        british_departures_per_hour = [0] * 12  # assuming a 12 hour period
        total_departures_british = 0
        delayed_departure_air_france = 0
        rain_hours_set = set() # to track unique hours with rain 
        destination_counts = {}

        for row in data_list:
            airport_code = row[0]
            flight_num = row[1]
            scheduled_departure = row[2]
            actual_departure = row[3]
            destination = row[4]
            distance_miles = row[5]
            scheduled_arrival = row[6]
            actual_arrival = row[7]
            terminal = row[8]
            runway = row[9]
            weather_conditions = row[10]

            # terminal 2 count 
            if terminal == "2":
                terminal_2_count += 1

            # under 600 miles
            if distance_miles.isdigit() and int(distance_miles) < 600:
                under_600_miles_count += 1

            # air france
            if flight_num[:2] == "AF":
                air_france_count += 1

                # delayed air france flights
                if scheduled_departure != actual_departure:
                    delayed_departure_air_france += 1

            # british airways departures per hour
            if flight_num[:2] == "BA":
                total_departures_british += 1
                hour = int(scheduled_departure.split(":")[0])
                if 0 <= hour < 12:
                    british_departures_per_hour[hour] += 1

            # temperatures below 15
            temp = "".join(c for c in weather_conditions if c.isdigit())
            if temp != "":
                temp = int(temp)
                if temp < 15:
                    temperatures_below_15_count += 1

            # rain hours 
            if "rain" in weather_conditions.lower():
                hour = int(scheduled_departure.split(":")[0])
                rain_hours_set.add(hour)

            # destination count
            if destination not in destination_counts:
                destination_counts[destination] = 1
            else:
                destination_counts[destination] += 1

        # calculations
        try:
            british_average_per_hour = round(total_departures_british / 12, 2) # average of british airways
        except ZeroDivisionError:
            british_average_per_hour = 0

        try:
            british_departures_percentage = round((total_departures_british / total_flights) * 100, 2) # percentage of british airways
        except ZeroDivisionError:
            british_departures_percentage = 0

        try:
            air_france_delayed_percentage = round((delayed_departure_air_france / air_france_count) * 100, 2) # percentage of delayed air france
        except ZeroDivisionError:
            air_france_delayed_percentage = 0

        rain_hours = len(rain_hours_set) # total hours of rain

        if not destination_counts:
            return # ends the function immediately
        minimum_destination_count = min(destination_counts.values())
        least_common_destinations = [valid_airports[d] for d, c in destination_counts.items() if c == minimum_destination_count] # least common destination

        # results saved to a text file
        output_file = "results.txt"

        # result format
        results_text = "\n"
        results_text += f"The total number of flights from this airport was {total_flights}\n"
        results_text += f"The total number of flights departing Terminal Two was {terminal_2_count}\n"
        results_text += f"The total number of departures on flights under 600 miles was {under_600_miles_count}\n"
        results_text += f"There were {air_france_count} Air France flights from this airport\n"
        results_text += f"There were {temperatures_below_15_count} flights departing in temperatures below 15 degrees\n"
        results_text += f"There was an average of {british_average_per_hour} British Airways flights per hour from this airport\n"
        results_text += f"British Airways planes made up {british_departures_percentage}% of all departures\n"
        results_text += f"{air_france_delayed_percentage}% of Air France departures were delayed\n"
        results_text += f"There were {rain_hours} hours in which rain fell\n"
        results_text += f"The least common destinations are {least_common_destinations}\n"


        print(results_text) # console output


        # write to results.txt
        try:
            with open (output_file, "a") as file:
                file.write("\n" + "*" * 75 + "\n")
                file.write(f"{selected_data_file} selected - Planes departing {valid_airports[airport_input]} {year_input}")
                file.write("\n" + "*" * 75 + "\n")
                file.write(results_text)
        except Exception as e:
            print(f"Error writing to file: {e}")

        # valid airline codes
        valid_airlines = {
            "BA": "British Airways",
            "AF": "Air France",
            "AY": "Finnair",
            "KL": "KLM",
            "SK": "Scandinavian Airlines",
            "TP": "TAP Air Portugal",
            "TK": "Turkish Airlines",
            "W6": "Wizz Air",
            "U2": "easyJet",
            "FR": "Ryanair",
            "A3": "Aegean Airlines",
            "SN": "Brussels Airlines",
            "EK": "Emirates",
            "QR": "Qatar Airways",
            "IB": "Iberia",
            "LH": "Lufthansa"
        }

        # prompt for airline code to plot the histogram
        print("\nEnter a two-character Airline code to plot a histogram: ", end = "")
        while True:
            airline_code = input().upper().strip()
            if len(airline_code) == 2 and airline_code in valid_airlines:
                break # loop stops entirely
            else:
                print("Unavailable Airline code, please try again: ", end = "")
                continue # skips the current iteration and continues the loop
            break # loop stops entirely

        # airline name
        airline_name = valid_airlines[airline_code]

        # airport name using airport_input
        airport_name = valid_airports[airport_input]  # uses valid_airports dictionary

        # function to get hourly flight counts 
        def get_hourly_flights(data_list, airline_code):
            """
            This function calculates the number of departures per hour for a given airline
            """
            
            hourly_counts = [0] * 12  # 12 hours from 00 to 11
            
            for row in data_list:
                if row[1][:2].upper() == airline_code.upper():  # check airline
                    hour = int(row[2].split(":")[0])  # get hour from scheduled departure
                    if 0 <= hour <= 11:
                        hourly_counts[hour] += 1  # count flight
                        
            return hourly_counts

        # calls the function
        hourly_counts = get_hourly_flights(data_list, airline_code)

        # graphics window
        win = GraphWin("Histogram", 800, 600)
        win.setBackground("grey")

        # title formatting
        title = Text(Point(400, 30), f"Departures by hour for {airline_name} from {airport_name} {year_input}")
        title.setSize(14)
        title.setTextColor("black")
        title.setStyle("bold")
        title.draw(win)

        # y-axis
        y_axis = Line(Point(100, 60), Point(100, 526))
        y_axis.draw(win)

        # y-axis label 
        y_label = Text(Point(35, 300), "Hours\n\n 00:00\n to\n 12:00")
        y_label.setTextColor("black")
        y_label.setStyle("bold")
        y_label.draw(win)

        # hour labels
        for hour in range(12): # 00 to 11
            y = 70 + hour * 40 # calculates y-position for each hour
            hour_text = Text(Point(80, y), f"{hour:02d}")
            hour_text.draw(win)

        # maximum flights for scaling
        if max(hourly_counts) == 0:
            max_flights = 1 # prevents ZeroDivisionError
        else:
            max_flights = max(hourly_counts)

        # calculates scale and bar height   
        bar_scale = (win.getWidth() - 150) / max_flights
        bar_height = 30

        for hour in range(12): # 00 to 11
            count = hourly_counts[hour]
            bar_width = count * bar_scale
            
            bar_center_y = 70 + (hour * 40) # center position for each bar

            # drawing each bar in the histogram
            if count > 0:
                bar = Rectangle(Point(100, bar_center_y - bar_height/2), Point(100 + bar_width, bar_center_y + bar_height/2))
            
                bar.setFill("blue")
                bar.draw(win)

            # displaying numerical values
            if count > 0:
                value_text = Text(Point(100 + bar_width + 20, bar_center_y), str(count))
                value_text.setTextColor("black")
                value_text.setStyle("bold")
                value_text.draw(win)

        # closes the histogram
        win.getMouse() # pause to view result
        win.close() # close window when done

        # new CSV file prompt
        print("\nDo you want to select a new data file? Y/N: ", end = "")
        while True:
            choice = input().upper().strip()
            if choice == "Y":
                data_list.clear() # clears all the data from the previous run
                break # loop stops entirely
            elif choice == "N":
                print("Thank you. End of run", end = "")
                return # ends the function immediately
            else:
                print("Please enter Y or N: ", end = "")

# runs the program               
main()
