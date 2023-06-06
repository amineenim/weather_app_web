import datetime
import requests
from django.shortcuts import render


# Create your views here.

def home(request) : 
    # read the API KEY 
    #API_KEY = open('API_KEY', 'r').read()
    # the url to request to get weather data about now
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    forecast_url = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}'
    
    # check for the request verb 
    if request.method == "GET" :
        return render(request, 'weather_app/home.html')
    elif request.method == "POST" :
        # get the city submitted by user
        city = request.POST['city']
        # call the function that handles the data fetch 
        weather_data, forecast_data, error = fetch_weather_and_forecast(city, API_KEY, current_weather_url, forecast_url)
        context = {
            'weather_data' : weather_data,
            'forecast_data' : forecast_data,
            'error' : error
        }
        return render(request, 'weather_app/home.html', context)       


# function that fetches weather and forecast data 
def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url) :
    # fetch the endpoint after formating the url with necessary params values
    response = requests.get(current_weather_url.format(city, api_key)).json()
    # check if the return code from api is not 404 which corresponds to city not found
    if response['cod'] == '404':
        weather_data, daily_forecast = None, None
        error = True
        return weather_data, daily_forecast, error  
    # extract coordinates from the response object 
    longitude = response['coord']['lon']
    latitude = response['coord']['lat']
    # fetch for the forecast data 
    forecast_response = requests.get(forecast_url.format(latitude, longitude, api_key)).json()
    # prepare dictionnary of wanted data
    weather_data = {
        "city" : city,
        "temperature" : round(response['main']['temp'] - 273.15, 2),
        "description" : response['weather'][0]['description'],
        "icon" : response['weather'][0]['icon']
    }
    daily_forecast = []
    for daily_data in forecast_response['list'][:5] :
        daily_forecast.append({
            "day" : datetime.datetime.fromtimestamp(daily_data['dt']).strftime("%A"),
            "min_temp" : round(daily_data['main']['temp_min'] -273.15, 2),
            "max_temp" : round(daily_data['main']['temp_max'] -273.15, 2),
            "time" : daily_data['dt_txt'],
            "description" : daily_data['weather'][0]['description'],
            "icon" : daily_data['weather'][0]['icon']
        })
    error = False 
    return weather_data, daily_forecast, error



















