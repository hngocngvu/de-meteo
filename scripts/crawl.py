import openmeteo_requests
import pandas as pd 
import requests_cache
from retry_requests import retry
from config.config import URL, MAX_CALLS_DAILY
from config.meteo_params import params


cache_session= requests_cache.CachedSession('.cache', expire_after= 3600) # in seconds

retry_session= retry(cache_session, retries=3, backoff_factor= 2)

openmeteo= openmeteo_requests.Client(session= retry_session)

responses= openmeteo.weather_api(URL, params= params)

response= responses[0]

#current data
current = response.Current()
current_temperature_2m = current.Variables(0).Value()
current_relative_humidity_2m = current.Variables(1).Value()
current_apparent_temperature = current.Variables(2).Value()
current_wind_speed_10m = current.Variables(3).Value()
current_wind_gusts_10m = current.Variables(4).Value()
current_wind_direction_10m = current.Variables(5).Value()
current_rain = current.Variables(6).Value()
current_showers = current.Variables(7).Value()
current_weather_code = current.Variables(8).Value()
current_cloud_cover = current.Variables(9).Value()
current_precipitation = current.Variables(10).Value()

# add [] -> pandas can indentify the data as a list and create a dataframe with one row
current_data= pd.DataFrame({
    'date': [pd.to_datetime(current.Time(), unit= 's', utc= True).tz_convert('Asia/Ho_Chi_Minh')],
    'temperature_2m': [current_temperature_2m],
    'relative_humidity_2m': [current_relative_humidity_2m],
    'apparent_temperature': [current_apparent_temperature],
    'wind_speed_10m': [current_wind_speed_10m],
    'wind_gusts_10m': [current_wind_gusts_10m],
    'wind_direction_10m': [current_wind_direction_10m],
    'rain': [current_rain],
    'showers': [current_showers],
    'weather_code': [current_weather_code],
    'cloud_cover': [current_cloud_cover],
    'precipitation': [current_precipitation]
})

# hourly data
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
hourly_apparent_temperature = hourly.Variables(2).ValuesAsNumpy()
hourly_precipitation = hourly.Variables(3).ValuesAsNumpy()
hourly_rain = hourly.Variables(4).ValuesAsNumpy()
hourly_showers = hourly.Variables(5).ValuesAsNumpy()
hourly_weather_code = hourly.Variables(6).ValuesAsNumpy()
hourly_cloud_cover = hourly.Variables(7).ValuesAsNumpy()
hourly_visibility = hourly.Variables(8).ValuesAsNumpy()
hourly_wind_speed_10m = hourly.Variables(9).ValuesAsNumpy()
hourly_wind_direction_10m = hourly.Variables(10).ValuesAsNumpy()
hourly_wind_gusts_10m = hourly.Variables(11).ValuesAsNumpy()
hourly_uv_index = hourly.Variables(12).ValuesAsNumpy()


hourly_data = pd.DataFrame({
	"date": pd.date_range(
		start = pd.to_datetime(hourly.Time(), unit = "s", utc = True).tz_convert('Asia/Ho_Chi_Minh'),
		end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True).tz_convert('Asia/Ho_Chi_Minh'),
		freq = pd.Timedelta(seconds = hourly.Interval()),
		inclusive = "left"
	),
    'temperature_2m': hourly_temperature_2m,
    'relative_humidity_2m': hourly_relative_humidity_2m,
    'apparent_temperature': hourly_apparent_temperature,
    'precipitation': hourly_precipitation,
    'rain': hourly_rain,    
    'showers': hourly_showers,
    'weather_code': hourly_weather_code,
    'cloud_cover': hourly_cloud_cover,
    'visibility': hourly_visibility,
    'wind_speed_10m': hourly_wind_speed_10m,
    'wind_direction_10m': hourly_wind_direction_10m,
    'wind_gusts_10m': hourly_wind_gusts_10m,
    'uv_index': hourly_uv_index
})

if __name__=="__main__":
    print(f"\nCurrent data:\n{current_data.head(5)}")
    print(f"\nHourly data:\n{hourly_data.head(5)}")

