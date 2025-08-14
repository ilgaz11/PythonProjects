from requests import get
import json

KEY = "qKUX2jstVey2CBXRYvlR6VGjFlPUDcm0"

def search_city(apikey: str):
    city_name = input("Enter a city: ")
    url = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={apikey}&q={city_name}"
    data = get(url)
    result= json.loads(data.content)
    if len(result) == 0:
        print("City not found")
        return False
    else:
        city_data = result[0]
        city_key = city_data["Key"]
        city = city_data["EnglishName"]
        country = city_data["Country"]["EnglishName"]
        coords = (city_data["GeoPosition"]["Latitude"], city_data["GeoPosition"]["Longitude"])
        city_info = [city_key, city, country, coords]
        print(f"{city_info[2]}, {city_info[1]}   Coords: {city_info[3]}\n")
        return city_info
        


def get_forecast(city_key, apikey: str):
    url = f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{city_key}?apikey={apikey}"
    data = get(url)
    result = json.loads(data.content)
    for day in result["DailyForecasts"]:
        date = day["Date"][:10]
        min_temp = (day["Temperature"]["Minimum"]["Value"] - 32) * 5/9
        max_temp = (day["Temperature"]["Maximum"]["Value"] - 32) * 5/9
        weather_condition = day["Day"]["IconPhrase"]
        has_rain = day["Day"]["HasPrecipitation"]
        if has_rain:
            precipitation = f"{day["Day"]["PrecipitationType"]} - {day["Day"]["PrecipitationIntensity"]}"
        else:
            precipitation = "None"
        print(f"{date:12}   Minimum: {round(min_temp)} °C     Maximum: {round(max_temp)} °C")
        print(f"Weather: {weather_condition:14} Precipitation: {precipitation}\n")

    

if __name__ == "__main__":
    while True:
        city_info = search_city(KEY)
        if not city_info:
            break
        else:
            get_forecast(city_info[0], KEY)