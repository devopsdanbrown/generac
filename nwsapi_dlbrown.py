import requests
import pgeocode
from dateutil import parser

nomi = pgeocode.Nominatim('us')

# Prompt user for start date
def get_zip_code():
    zip_code = input("Enter zip code: ")
    while not (zip_code.isdigit()) and len(zip_code) != 5:
        print("Invalid zip code. Please enter a valid zip code.")
        zip_code = input("Enter zip code: ")
    return zip_code

def get_start_date_time():
    start_date_time = input("Enter start date (YYYY-MM-DDThh:mm:ss): ")
    while not (start_date_time.isdigit()) and len(start_date_time) != 10:
        print("Invalid start date. Please enter a valid start date.")
        start_date_time = input("Enter start date (YYYY-MM-DDThh:mm:ss): ")
    return start_date_time

def get_end_date_time():
    end_date_time = input("Enter end date (YYYY-MM-DDThh:mm:ss): ")
    while not (end_date_time.isdigit()) and len(end_date_time) != 10:
        print("Invalid start date. Please enter a valid start date.")
        end_date_time = input("Enter end date (YYYY-MM-DDThh:mm:ss): ")
    return end_date_time

def get_closest_weather_station(latitude, longitude):
    url = f"https://api.weather.gov/points/{latitude},{longitude}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        station_url = data["properties"]["observationStations"]
        station_response = requests.get(station_url)
        if station_response.status_code == 200:
            station_data = station_response.json()
            closest_station = station_data["features"][0]["properties"]["stationIdentifier"]
            return closest_station
        else:
            print("Failed to retrieve weather station data.")
    else:
        print("Failed to retrieve location data.")

# Prompt user for zip code
zip_code = get_zip_code()

curentLatitude = nomi.query_postal_code(zip_code).latitude

curentLongitude = nomi.query_postal_code(zip_code).longitude

print (f"Current location is: ", curentLatitude, curentLongitude)

closest_station = get_closest_weather_station(curentLatitude, curentLongitude)

print(f"The closest weather station is: {closest_station}")

def fetch_historical_weather_observations(station):
    url = f"https://api.weather.gov/stations/{station}/observations/latest "
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        observations = data["features"]
        return observations
    else:
        print("Failed to retrieve historical weather observations.")

# Rest of the code...

# Fetch historical weather observations
historical_observations = fetch_historical_weather_observations(closest_station)

# Process and use the historical observations as needed
# ...

#Print min and max temp for each day
#for observation in historical_observations:
#    print(observation["properties"]["minTemperature"], observation["properties"]["maxTemperature"])

weather_data = historical_observations[0]["properties"]

print(weather_data)