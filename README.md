# Flight Data Analyser

A Python program that analyses airport departure data from CSV files and plots a histogram of departures by hour.

Built for the **Software Development I** module.

## Features

- Choose an airport (by three-letter code) and a year (2000–2025)
- Loads the matching CSV file, e.g. `LHR2025.csv`
- Calculates statistics such as:
  - Total flights and flights from Terminal 2
  - Flights under 600 miles
  - Air France flights and the percentage delayed
  - British Airways average flights per hour and share of departures
  - Flights departing in temperatures below 15°
  - Hours with rain
  - Least common destinations
- Prints the results and saves them to `results.txt`
- Plots a histogram of departures by hour for a chosen airline

## Supported Airports

LHR, MAD, CDG, IST, AMS, LIS, FRA, FCO, MUC, BCN

## Tech Stack

- Python 3
- `graphics.py` (John Zelle's graphics library) for the histogram
- Built-in modules: `csv`, `math`

## How to Run

1. Make sure Python 3 is installed.
2. Clone the repository:
   ```
   git clone https://github.com/Raiqa-Abdul-Qadir/flight-data-analyser.git
   cd flight-data-analyser
   ```
3. Make sure `graphics.py` and the CSV data files are in the same folder as `flight_data_analyser.py`.
4. Run the program:
   ```
   python flight_data_analyser.py
   ```
5. Enter an airport code, a year, and then an airline code (e.g. `BA`) to see the histogram. Click the histogram window to close it.
