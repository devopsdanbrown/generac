'''This module will prompt the user for their zip code and start and stop dates/times
and pull and display NWS data for that location and timespan.
'''

from datetime import datetime
from array import array

import requests
import pgeocode

nomi = pgeocode.Nominatim('us')

def check_valid_date(date_str: str):
    '''Checks if the date string is a valid ISO date.'''
    try:
        iso_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        return iso_date
    except ValueError:
        return None

def get_zip_code() -> str:
    '''Prompt user for zip code.'''
    zip_code = input("Enter zip code: ")
    while not (zip_code.isdigit()) and len(zip_code) != 5:
        print("Invalid zip code. Please enter a valid zip code.")
        zip_code = input("Enter zip code: ")
    return zip_code

def get_start_date_time():
    '''Prompt user for start date.'''
    start_date_time = input("Enter start date (YYYY-MM-DDThh:mm): ")
    while not (iso_date := check_valid_date(start_date_time)):
        print("Invalid start date. Please enter a valid start date.")
        start_date_time = input("Enter start date (YYYY-MM-DDThh:mm): ")
    return iso_date

def get_end_date_time():
    '''Prompt user for end date.'''
    end_date_time = input("Enter end date (YYYY-MM-DDThh:mm): ")
    while not (iso_date := check_valid_date(end_date_time)):
        print("Invalid start date. Please enter a valid start date.")
        end_date_time = input("Enter end date (YYYY-MM-DDThh:mm): ")
    return iso_date

def get_closest_weather_station(latitude, longitude):
    '''Queries the NWS API and returns the closest weather station.'''
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

def fetch_historical_weather_observations(
    station, start_time_object, end_time_object
    ):
    start_time = start_time_object.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_time = end_time_object.strftime("%Y-%m-%dT%H:%M:%SZ")
    url = f"https://api.weather.gov/stations/{station}/observations?start={start_time}&end={end_time}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        observations = data.get("features")
        return observations
    else:
        error_messages = response.json().get("parameterErrors")
        print("Failed to retrieve historical weather observations:")
        print(*error_messages, sep="\n")

# Prompt user for zip code
zip_code = get_zip_code()

# start_daterange = get_start_date_time()
# end_daterange = get_end_date_time()

start_daterange = datetime.strptime("2023-12-01T00:00", '%Y-%m-%dT%H:%M')
end_daterange = datetime.strptime("2023-12-06T23:59", '%Y-%m-%dT%H:%M')

curentLatitude = nomi.query_postal_code(zip_code).latitude

curentLongitude = nomi.query_postal_code(zip_code).longitude

print (f"Current location is: ", curentLatitude, curentLongitude)

print (f"Start date/time: {start_daterange}")
print (f"End date/time: {end_daterange}")

closest_station = get_closest_weather_station(curentLatitude, curentLongitude)

print(f"The closest weather station is: {closest_station}")

# Rest of the code...

# Fetch historical weather observations
historical_observations = fetch_historical_weather_observations(
    closest_station, start_daterange, end_daterange)

# Process and use the historical observations as needed
# ...

#Print min and max temp for each day
#for observation in historical_observations:
#    print(observation["properties"]["minTemperature"], observation["properties"]["maxTemperature"])

temp_dates = [line.get("properties").get("timestamp") for line in historical_observations]
temp_data = [line.get("properties").get("temperature").get("value") for line in historical_observations]

#print(len(temp_dates), " dates:  ", temp_dates)
#print(len(temp_data), " temps:  ", temp_data)

#Print min and max temp for each day
for observation in historical_observations:
    print(observation["properties"]["timestamp"], observation["properties"]["temperature"]["value"])
   
