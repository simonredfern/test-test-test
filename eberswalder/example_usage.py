#!/usr/bin/env python3
"""
Example Usage Script for Brandenburg Weather Data Fetcher

This script demonstrates how to use the BrandenburgWeatherFetcher class
to get weather data for cities in Brandenburg, Germany.

Before running this script:
1. Get a free API key from https://openweathermap.org/api
2. Set the environment variable: export OPENWEATHER_API_KEY="your_key_here"
3. Install dependencies: pip install -r requirements.txt
4. Run: python example_usage.py
"""

import os
import json
from datetime import datetime
from weather_fetcher import BrandenburgWeatherFetcher
from config import WeatherConfig


def print_separator(title: str):
    """Print a formatted separator with title"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def example_current_weather():
    """Example: Get current weather for a specific city"""
    print_separator("Current Weather Example")
    
    # Initialize the fetcher
    fetcher = BrandenburgWeatherFetcher(WeatherConfig.OPENWEATHER_API_KEY)
    
    try:
        # Get current weather for Eberswalde
        weather = fetcher.get_current_weather("eberswalde")
        print(fetcher.format_current_weather(weather))
        
        # Also try Potsdam
        potsdam_weather = fetcher.get_current_weather("potsdam")
        print(fetcher.format_current_weather(potsdam_weather))
        
    except Exception as e:
        print(f"Error fetching current weather: {e}")


def example_forecast():
    """Example: Get weather forecast"""
    print_separator("Weather Forecast Example")
    
    fetcher = BrandenburgWeatherFetcher(WeatherConfig.OPENWEATHER_API_KEY)
    
    try:
        # Get 3-day forecast for Brandenburg an der Havel
        forecast = fetcher.get_forecast("brandenburg_havel", days=3)
        
        print(f"3-Day Forecast for {forecast['city_info']['name']}:")
        print("-" * 50)
        
        current_date = None
        for item in forecast["list"][:12]:  # Show first 12 entries (1.5 days)
            dt = datetime.fromtimestamp(item["dt"])
            date_str = dt.strftime("%Y-%m-%d")
            time_str = dt.strftime("%H:%M")
            
            # Print date header when date changes
            if current_date != date_str:
                if current_date is not None:
                    print()
                print(f"\n📅 {date_str}:")
                current_date = date_str
            
            temp = item["main"]["temp"]
            feels_like = item["main"]["feels_like"]
            description = item["weather"][0]["description"].title()
            humidity = item["main"]["humidity"]
            
            print(f"  {time_str}: {temp}°C (feels {feels_like}°C) - {description} - Humidity: {humidity}%")
            
    except Exception as e:
        print(f"Error fetching forecast: {e}")


def example_all_cities():
    """Example: Get weather for all Brandenburg cities"""
    print_separator("All Cities Weather Summary")
    
    fetcher = BrandenburgWeatherFetcher(WeatherConfig.OPENWEATHER_API_KEY)
    
    try:
        all_weather = fetcher.get_all_brandenburg_weather()
        
        print("Current weather across Brandenburg:")
        print("-" * 50)
        
        # Sort cities by temperature
        city_temps = []
        for city_key, weather_data in all_weather["cities"].items():
            if "error" not in weather_data:
                city_name = weather_data.get("city_info", {}).get("name", city_key)
                temp = weather_data["main"]["temp"]
                description = weather_data["weather"][0]["description"].title()
                city_temps.append((temp, city_name, description))
        
        city_temps.sort(reverse=True)  # Sort by temperature, highest first
        
        for temp, city_name, description in city_temps:
            print(f"  🌡️  {city_name:<20} {temp:>5.1f}°C - {description}")
        
        print(f"\nData fetched at: {all_weather['timestamp']}")
        
        # Save to file
        filename = f"brandenburg_weather_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        fetcher.save_weather_data(all_weather, filename)
        
    except Exception as e:
        print(f"Error fetching all cities weather: {e}")


def example_coordinates():
    """Example: Get weather for specific coordinates"""
    print_separator("Weather by Coordinates Example")
    
    fetcher = BrandenburgWeatherFetcher(WeatherConfig.OPENWEATHER_API_KEY)
    
    try:
        # Example coordinates for Sanssouci Palace in Potsdam
        lat, lon = 52.4040, 13.0396
        
        weather = fetcher.get_weather_for_coordinates(lat, lon)
        
        print(f"Weather at coordinates ({lat}, {lon}):")
        print(f"Location: {weather['name']}")
        print(f"Temperature: {weather['main']['temp']}°C")
        print(f"Condition: {weather['weather'][0]['description'].title()}")
        print(f"Humidity: {weather['main']['humidity']}%")
        print(f"Wind Speed: {weather['wind']['speed']} m/s")
        
    except Exception as e:
        print(f"Error fetching weather by coordinates: {e}")


def example_air_quality():
    """Example: Get air quality data"""
    print_separator("Air Quality Example")
    
    fetcher = BrandenburgWeatherFetcher(WeatherConfig.OPENWEATHER_API_KEY)
    
    try:
        # Get air quality for Cottbus
        air_quality = fetcher.get_air_quality("cottbus")
        
        city_name = air_quality["city_info"]["name"]
        aqi = air_quality["list"][0]["main"]["aqi"]
        components = air_quality["list"][0]["components"]
        
        # Air Quality Index meanings
        aqi_meanings = {
            1: "Good",
            2: "Fair", 
            3: "Moderate",
            4: "Poor",
            5: "Very Poor"
        }
        
        print(f"Air Quality in {city_name}:")
        print(f"Air Quality Index: {aqi} ({aqi_meanings.get(aqi, 'Unknown')})")
        print("Components (μg/m³):")
        print(f"  CO (Carbon Monoxide): {components.get('co', 'N/A')}")
        print(f"  NO₂ (Nitrogen Dioxide): {components.get('no2', 'N/A')}")
        print(f"  O₃ (Ozone): {components.get('o3', 'N/A')}")
        print(f"  PM2.5 (Fine Particulate Matter): {components.get('pm2_5', 'N/A')}")
        print(f"  PM10 (Particulate Matter): {components.get('pm10', 'N/A')}")
        
    except Exception as e:
        print(f"Error fetching air quality: {e}")


def example_data_processing():
    """Example: Process and analyze weather data"""
    print_separator("Data Processing Example")
    
    fetcher = BrandenburgWeatherFetcher(WeatherConfig.OPENWEATHER_API_KEY)
    
    try:
        # Get weather for multiple cities and analyze
        cities_to_check = ["eberswalde", "potsdam", "cottbus", "frankfurt_oder"]
        weather_data = {}
        
        for city in cities_to_check:
            weather_data[city] = fetcher.get_current_weather(city)
        
        # Find warmest and coldest cities
        temps = [(city, data["main"]["temp"]) for city, data in weather_data.items()]
        warmest = max(temps, key=lambda x: x[1])
        coldest = min(temps, key=lambda x: x[1])
        
        print("Temperature Analysis:")
        print(f"🔥 Warmest: {fetcher.brandenburg_cities[warmest[0]]['name']} at {warmest[1]}°C")
        print(f"❄️  Coldest: {fetcher.brandenburg_cities[coldest[0]]['name']} at {coldest[1]}°C")
        
        # Average temperature
        avg_temp = sum(temp for _, temp in temps) / len(temps)
        print(f"📊 Average temperature across selected cities: {avg_temp:.1f}°C")
        
        # Find cities with similar weather conditions
        conditions = {}
        for city, data in weather_data.items():
            condition = data["weather"][0]["main"]
            if condition not in conditions:
                conditions[condition] = []
            conditions[condition].append(fetcher.brandenburg_cities[city]["name"])
        
        print("\nWeather Conditions:")
        for condition, city_list in conditions.items():
            print(f"  {condition}: {', '.join(city_list)}")
        
    except Exception as e:
        print(f"Error processing weather data: {e}")


def main():
    """Main function to run all examples"""
    print("🌤️  Brandenburg Weather Data Fetcher Examples")
    print("Using OpenWeatherMap API")
    
    # Check if API key is configured
    if not WeatherConfig.validate_api_key():
        print("\n❌ Error: OpenWeatherMap API key not found!")
        print("Please set the OPENWEATHER_API_KEY environment variable.")
        print("Get your free API key from: https://openweathermap.org/api")
        print("\nExample:")
        print("  export OPENWEATHER_API_KEY='your_api_key_here'")
        return
    
    print(f"✅ API Key configured")
    print(f"📍 Default region: {WeatherConfig.REGION_NAME}")
    print(f"🏠 Default city: {WeatherConfig.DEFAULT_CITY}")
    
    try:
        # Run all examples
        example_current_weather()
        example_forecast()
        example_all_cities()
        example_coordinates()
        example_air_quality()
        example_data_processing()
        
        print_separator("Available Cities")
        fetcher = BrandenburgWeatherFetcher(WeatherConfig.OPENWEATHER_API_KEY)
        print("You can use any of these city keys with the fetcher:")
        for key, city in fetcher.brandenburg_cities.items():
            print(f"  '{key}' → {city['name']} ({city['lat']:.4f}, {city['lon']:.4f})")
        
        print_separator("Tips")
        print("💡 Tips for using the weather fetcher:")
        print("   • Free tier allows 1,000 API calls per day")
        print("   • Data is cached in JSON files for offline analysis")
        print("   • Use city keys (like 'eberswalde') for predefined locations")
        print("   • Or use get_weather_for_coordinates() for any location")
        print("   • All temperatures are in Celsius by default")
        print("   • Check the config.py file for customization options")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()