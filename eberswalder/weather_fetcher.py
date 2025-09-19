"""
Weather Data Fetcher for Brandenburg using OpenWeatherMap API

This module provides functionality to fetch current weather data, forecasts,
and historical data for locations in Brandenburg, Germany using the OpenWeatherMap API.
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import os


class BrandenburgWeatherFetcher:
    """
    A class to fetch weather data for Brandenburg locations using OpenWeatherMap API.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the weather fetcher with OpenWeatherMap API key.
        
        Args:
            api_key (str): Your OpenWeatherMap API key
        """
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.onecall_url = "https://api.openweathermap.org/data/3.0/onecall"
        
        # Major Brandenburg cities with coordinates
        self.brandenburg_cities = {
            "potsdam": {"lat": 52.3906, "lon": 13.0645, "name": "Potsdam"},
            "cottbus": {"lat": 51.7606, "lon": 14.3349, "name": "Cottbus"},
            "brandenburg_havel": {"lat": 52.4125, "lon": 12.5492, "name": "Brandenburg an der Havel"},
            "frankfurt_oder": {"lat": 52.3481, "lon": 14.5507, "name": "Frankfurt (Oder)"},
            "eberswalde": {"lat": 52.8339, "lon": 13.8217, "name": "Eberswalde"},
            "oranienburg": {"lat": 52.7545, "lon": 13.2369, "name": "Oranienburg"},
            "rathenow": {"lat": 52.6047, "lon": 12.3367, "name": "Rathenow"},
            "senftenberg": {"lat": 51.5255, "lon": 14.0025, "name": "Senftenberg"},
            "neuruppin": {"lat": 52.9245, "lon": 12.8012, "name": "Neuruppin"},
            "schwedt": {"lat": 53.0606, "lon": 14.2825, "name": "Schwedt/Oder"}
        }
    
    def get_current_weather(self, city_key: str = "potsdam") -> Dict[str, Any]:
        """
        Get current weather for a Brandenburg city.
        
        Args:
            city_key (str): Key for the city (default: "potsdam")
            
        Returns:
            Dict containing current weather data
        """
        if city_key not in self.brandenburg_cities:
            raise ValueError(f"City '{city_key}' not found. Available cities: {list(self.brandenburg_cities.keys())}")
        
        city = self.brandenburg_cities[city_key]
        url = f"{self.base_url}/weather"
        
        params = {
            "lat": city["lat"],
            "lon": city["lon"],
            "appid": self.api_key,
            "units": "metric",
            "lang": "en"
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Add city info to response
        data["city_info"] = city
        data["fetch_time"] = datetime.now().isoformat()
        
        return data
    
    def get_forecast(self, city_key: str = "potsdam", days: int = 5) -> Dict[str, Any]:
        """
        Get weather forecast for a Brandenburg city.
        
        Args:
            city_key (str): Key for the city (default: "potsdam")
            days (int): Number of days to forecast (1-5, default: 5)
            
        Returns:
            Dict containing forecast data
        """
        if city_key not in self.brandenburg_cities:
            raise ValueError(f"City '{city_key}' not found. Available cities: {list(self.brandenburg_cities.keys())}")
        
        if not 1 <= days <= 5:
            raise ValueError("Days must be between 1 and 5 for the free tier")
        
        city = self.brandenburg_cities[city_key]
        url = f"{self.base_url}/forecast"
        
        params = {
            "lat": city["lat"],
            "lon": city["lon"],
            "appid": self.api_key,
            "units": "metric",
            "lang": "en",
            "cnt": days * 8  # 8 forecasts per day (3-hour intervals)
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Add city info to response
        data["city_info"] = city
        data["fetch_time"] = datetime.now().isoformat()
        
        return data
    
    def get_weather_for_coordinates(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Get current weather for specific coordinates in Brandenburg.
        
        Args:
            lat (float): Latitude
            lon (float): Longitude
            
        Returns:
            Dict containing current weather data
        """
        url = f"{self.base_url}/weather"
        
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric",
            "lang": "en"
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        data["fetch_time"] = datetime.now().isoformat()
        
        return data
    
    def get_all_brandenburg_weather(self) -> Dict[str, Any]:
        """
        Get current weather for all major Brandenburg cities.
        
        Returns:
            Dict with weather data for all cities
        """
        all_weather = {}
        
        for city_key in self.brandenburg_cities:
            try:
                all_weather[city_key] = self.get_current_weather(city_key)
            except Exception as e:
                all_weather[city_key] = {"error": str(e)}
        
        return {
            "timestamp": datetime.now().isoformat(),
            "cities": all_weather
        }
    
    def get_air_quality(self, city_key: str = "potsdam") -> Dict[str, Any]:
        """
        Get air quality data for a Brandenburg city.
        
        Args:
            city_key (str): Key for the city (default: "potsdam")
            
        Returns:
            Dict containing air quality data
        """
        if city_key not in self.brandenburg_cities:
            raise ValueError(f"City '{city_key}' not found. Available cities: {list(self.brandenburg_cities.keys())}")
        
        city = self.brandenburg_cities[city_key]
        url = f"{self.base_url}/air_pollution"
        
        params = {
            "lat": city["lat"],
            "lon": city["lon"],
            "appid": self.api_key
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        data["city_info"] = city
        data["fetch_time"] = datetime.now().isoformat()
        
        return data
    
    def save_weather_data(self, data: Dict[str, Any], filename: str):
        """
        Save weather data to a JSON file.
        
        Args:
            data (Dict): Weather data to save
            filename (str): Name of the file to save to
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Weather data saved to {filename}")
    
    def format_current_weather(self, weather_data: Dict[str, Any]) -> str:
        """
        Format current weather data into a readable string.
        
        Args:
            weather_data (Dict): Weather data from API
            
        Returns:
            Formatted weather string
        """
        if "error" in weather_data:
            return f"Error: {weather_data['error']}"
        
        city_name = weather_data.get("city_info", {}).get("name", weather_data.get("name", "Unknown"))
        temp = weather_data["main"]["temp"]
        feels_like = weather_data["main"]["feels_like"]
        humidity = weather_data["main"]["humidity"]
        pressure = weather_data["main"]["pressure"]
        description = weather_data["weather"][0]["description"].title()
        wind_speed = weather_data["wind"]["speed"]
        
        return f"""
Weather in {city_name}:
  Temperature: {temp}°C (feels like {feels_like}°C)
  Condition: {description}
  Humidity: {humidity}%
  Pressure: {pressure} hPa
  Wind Speed: {wind_speed} m/s
  Fetched: {weather_data.get('fetch_time', 'Unknown')}
        """.strip()


def main():
    """
    Example usage of the BrandenburgWeatherFetcher class.
    
    To use this script:
    1. Get a free API key from https://openweathermap.org/api
    2. Set the API key as an environment variable: export OPENWEATHER_API_KEY="your_key_here"
    3. Run this script
    """
    
    # Get API key from environment variable
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not api_key:
        print("Please set the OPENWEATHER_API_KEY environment variable with your OpenWeatherMap API key.")
        print("You can get a free API key from: https://openweathermap.org/api")
        print("Then run: export OPENWEATHER_API_KEY='your_key_here'")
        return
    
    # Initialize the weather fetcher
    fetcher = BrandenburgWeatherFetcher(api_key)
    
    print("Brandenburg Weather Data Fetcher")
    print("=" * 40)
    
    # Get current weather for Eberswalde (since you created the eberswalder folder)
    try:
        print("\n1. Current Weather in Eberswalde:")
        eberswalde_weather = fetcher.get_current_weather("eberswalde")
        print(fetcher.format_current_weather(eberswalde_weather))
        
        # Save the data
        fetcher.save_weather_data(eberswalde_weather, "eberswalde_current_weather.json")
        
    except Exception as e:
        print(f"Error getting Eberswalde weather: {e}")
    
    # Get weather for all Brandenburg cities
    try:
        print("\n2. Weather Summary for All Brandenburg Cities:")
        all_weather = fetcher.get_all_brandenburg_weather()
        
        for city_key, weather_data in all_weather["cities"].items():
            if "error" not in weather_data:
                city_name = weather_data.get("city_info", {}).get("name", city_key)
                temp = weather_data["main"]["temp"]
                description = weather_data["weather"][0]["description"]
                print(f"  {city_name}: {temp}°C, {description}")
        
        # Save all weather data
        fetcher.save_weather_data(all_weather, "brandenburg_all_weather.json")
        
    except Exception as e:
        print(f"Error getting all Brandenburg weather: {e}")
    
    # Get 5-day forecast for Potsdam
    try:
        print("\n3. 5-Day Forecast for Potsdam:")
        forecast = fetcher.get_forecast("potsdam", 3)  # 3 days to stay within free limits
        
        for item in forecast["list"][:5]:  # Show first 5 forecasts
            dt = datetime.fromtimestamp(item["dt"])
            temp = item["main"]["temp"]
            description = item["weather"][0]["description"]
            print(f"  {dt.strftime('%Y-%m-%d %H:%M')}: {temp}°C, {description}")
        
        # Save forecast data
        fetcher.save_weather_data(forecast, "potsdam_forecast.json")
        
    except Exception as e:
        print(f"Error getting forecast: {e}")
    
    print("\n" + "=" * 40)
    print("Available Brandenburg cities:")
    for key, city in fetcher.brandenburg_cities.items():
        print(f"  {key}: {city['name']}")


if __name__ == "__main__":
    main()