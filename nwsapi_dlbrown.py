'''This module will prompt the user for their zip code
and pull and display recent NWS data for that location.
'''

import requests
import pgeocode

nomi = pgeocode.Nominatim('us')

def get_zip_code() -> str:
    '''Prompt user for zip code.'''
    zip_code = input("Enter zip code: ")
    while not (zip_code.isdigit()) and len(zip_code) != 5:
        print("Invalid zip code. Please enter a valid zip code.")
        zip_code = input("Enter zip code: ")
    return zip_code

def get_closest_weather_station(latitude, longitude) -> str | None:
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

def fetch_historical_weather_observations(station: str) -> list | None:
    start_time = start_time_object.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_time = end_time_object.strftime("%Y-%m-%dT%H:%M:%SZ")
    url = f"https://api.weather.gov/stations/{station}/observations"
    print(url)
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

curentLatitude = nomi.query_postal_code(zip_code).latitude
curentLongitude = nomi.query_postal_code(zip_code).longitude
print (f"Current location is: ", curentLatitude, curentLongitude)

closest_station = get_closest_weather_station(curentLatitude, curentLongitude)
print(f"The closest weather station is: {closest_station}")

# Fetch historical weather observations
historical_observations = fetch_historical_weather_observations(closest_station)

# Retrieve the time and temperature returned from the API
temp_dates = [line.get("properties").get("timestamp") for line in historical_observations]
temp_data = [line.get("properties").get("temperature").get("value") for line in historical_observations]

# Remove instances of null temperature from the data while keeping them correlated
historical_temp_data = zip(temp_dates, temp_data)
historical_temp_data = filter(lambda data: data[1] is not None,
                              historical_temp_data)

# Group the data by days
final = {}
for time, temp in historical_temp_data:
    date = time.split("T")[0]
    if final.get(date) is None:
        final[date] = []
    final[date].append(temp)

for key in final:
    final[key] = (max(final[key]), min(final[key]))

# Print min and max temp for each day
for date, (max_temp, min_temp) in final.items():
    print(f"{date}: Max temperature: {max_temp}°C, Min temperature: {min_temp}°C")
