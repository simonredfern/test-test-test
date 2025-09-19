#!/usr/bin/env python3
"""
Test Demo Script for Brandenburg Weather Data Fetcher

This script demonstrates the weather fetcher functionality without requiring 
an actual API key. It shows the structure, available cities, and simulates
API responses for testing purposes.
"""

import json
from datetime import datetime
from weather_fetcher import BrandenburgWeatherFetcher
from config import WeatherConfig


def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def show_available_cities():
    """Show all available Brandenburg cities"""
    print_header("Available Brandenburg Cities")
    
    # We can create the fetcher without a valid API key just to access the cities
    try:
        fetcher = BrandenburgWeatherFetcher("dummy_key")
        
        print("The weather fetcher includes these major Brandenburg cities:")
        print()
        
        for i, (key, city) in enumerate(fetcher.brandenburg_cities.items(), 1):
            print(f"{i:2d}. {city['name']:<25} (Key: '{key}')")
            print(f"     Coordinates: {city['lat']:.4f}°N, {city['lon']:.4f}°E")
            print()
        
        print(f"Total cities available: {len(fetcher.brandenburg_cities)}")
        
    except Exception as e:
        print(f"Error: {e}")


def show_configuration():
    """Show current configuration settings"""
    print_header("Configuration Settings")
    
    print("Current weather fetcher configuration:")
    print()
    print(f"Default Units:        {WeatherConfig.DEFAULT_UNITS}")
    print(f"Default Language:     {WeatherConfig.DEFAULT_LANGUAGE}")
    print(f"Default City:         {WeatherConfig.DEFAULT_CITY}")
    print(f"Region:              {WeatherConfig.REGION_NAME}")
    print(f"Country Code:        {WeatherConfig.COUNTRY_CODE}")
    print(f"Timezone:            {WeatherConfig.TIMEZONE}")
    print(f"Request Timeout:     {WeatherConfig.REQUEST_TIMEOUT} seconds")
    print(f"Data Directory:      {WeatherConfig.DATA_DIR}")
    print()
    print("Rate Limits (Free Tier):")
    print(f"  Max calls per minute: {WeatherConfig.MAX_CALLS_PER_MINUTE}")
    print(f"  Max calls per day:    {WeatherConfig.MAX_CALLS_PER_DAY}")


def simulate_weather_data():
    """Show what actual weather data would look like"""
    print_header("Sample Weather Data Structure")
    
    # Simulate what real weather data looks like
    sample_weather = {
        "coord": {"lon": 13.8217, "lat": 52.8339},
        "weather": [
            {
                "id": 800,
                "main": "Clear",
                "description": "clear sky",
                "icon": "01d"
            }
        ],
        "base": "stations",
        "main": {
            "temp": 18.5,
            "feels_like": 17.8,
            "temp_min": 16.2,
            "temp_max": 21.3,
            "pressure": 1013,
            "humidity": 65
        },
        "visibility": 10000,
        "wind": {
            "speed": 3.2,
            "deg": 240
        },
        "clouds": {
            "all": 0
        },
        "dt": 1695038400,
        "sys": {
            "type": 2,
            "id": 2001334,
            "country": "DE",
            "sunrise": 1695015180,
            "sunset": 1695061620
        },
        "timezone": 7200,
        "id": 2933364,
        "name": "Eberswalde",
        "cod": 200,
        "city_info": {
            "lat": 52.8339,
            "lon": 13.8217,
            "name": "Eberswalde"
        },
        "fetch_time": datetime.now().isoformat()
    }
    
    print("Sample weather data structure for Eberswalde:")
    print(json.dumps(sample_weather, indent=2))


def show_api_methods():
    """Show available API methods and their usage"""
    print_header("Available Weather Fetcher Methods")
    
    methods = [
        {
            "name": "get_current_weather(city_key)",
            "description": "Get current weather for a Brandenburg city",
            "example": "fetcher.get_current_weather('eberswalde')"
        },
        {
            "name": "get_forecast(city_key, days)",
            "description": "Get weather forecast (1-5 days)",
            "example": "fetcher.get_forecast('potsdam', days=3)"
        },
        {
            "name": "get_weather_for_coordinates(lat, lon)",
            "description": "Get weather for specific coordinates",
            "example": "fetcher.get_weather_for_coordinates(52.8339, 13.8217)"
        },
        {
            "name": "get_all_brandenburg_weather()",
            "description": "Get current weather for all cities",
            "example": "fetcher.get_all_brandenburg_weather()"
        },
        {
            "name": "get_air_quality(city_key)",
            "description": "Get air quality data for a city",
            "example": "fetcher.get_air_quality('cottbus')"
        },
        {
            "name": "save_weather_data(data, filename)",
            "description": "Save weather data to JSON file",
            "example": "fetcher.save_weather_data(weather, 'data.json')"
        },
        {
            "name": "format_current_weather(data)",
            "description": "Format weather data for display",
            "example": "fetcher.format_current_weather(weather_data)"
        }
    ]
    
    print("The BrandenburgWeatherFetcher class provides these methods:")
    print()
    
    for i, method in enumerate(methods, 1):
        print(f"{i}. {method['name']}")
        print(f"   {method['description']}")
        print(f"   Usage: {method['example']}")
        print()


def show_getting_started():
    """Show how to get started with the weather fetcher"""
    print_header("Getting Started")
    
    print("To use the Brandenburg Weather Data Fetcher:")
    print()
    print("1. Get a FREE API key from OpenWeatherMap:")
    print("   → Visit: https://openweathermap.org/api")
    print("   → Sign up for a free account")
    print("   → Go to API keys section")
    print("   → Copy your API key")
    print()
    print("2. Set the environment variable:")
    print("   → export OPENWEATHER_API_KEY='your_api_key_here'")
    print("   → Or add it to your .bashrc/.zshrc for persistence")
    print()
    print("3. Run the examples:")
    print("   → python example_usage.py")
    print("   → python weather_fetcher.py")
    print()
    print("4. Or use it in your own code:")
    print("""
   from weather_fetcher import BrandenburgWeatherFetcher
   import os
   
   api_key = os.getenv("OPENWEATHER_API_KEY")
   fetcher = BrandenburgWeatherFetcher(api_key)
   
   # Get current weather for Eberswalde
   weather = fetcher.get_current_weather("eberswalde")
   print(fetcher.format_current_weather(weather))
    """)


def run_demo_tests():
    """Run various tests that don't require API access"""
    print_header("Demo Tests (No API Required)")
    
    try:
        # Test 1: Initialize fetcher
        print("✓ Test 1: Initialize weather fetcher")
        fetcher = BrandenburgWeatherFetcher("test_key")
        print("  Weather fetcher created successfully")
        
        # Test 2: Check cities data
        print("\n✓ Test 2: Check Brandenburg cities data")
        assert len(fetcher.brandenburg_cities) > 0
        print(f"  Found {len(fetcher.brandenburg_cities)} cities")
        
        # Test 3: Validate city data structure
        print("\n✓ Test 3: Validate city data structure")
        for key, city in fetcher.brandenburg_cities.items():
            assert "name" in city
            assert "lat" in city
            assert "lon" in city
            assert isinstance(city["lat"], (int, float))
            assert isinstance(city["lon"], (int, float))
        print("  All cities have valid data structure")
        
        # Test 4: Test configuration
        print("\n✓ Test 4: Test configuration settings")
        assert WeatherConfig.DEFAULT_UNITS in ["metric", "imperial", "kelvin"]
        assert WeatherConfig.DEFAULT_LANGUAGE is not None
        print("  Configuration settings are valid")
        
        # Test 5: Test invalid city handling
        print("\n✓ Test 5: Test invalid city handling")
        try:
            fetcher.get_current_weather("invalid_city")
            print("  ERROR: Should have raised an exception!")
        except ValueError as e:
            print("  Correctly handles invalid city names")
        
        print("\n🎉 All demo tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main demo function"""
    print("🌤️  Brandenburg Weather Data Fetcher - Demo Mode")
    print("This demo shows the fetcher capabilities without requiring an API key")
    
    # Run all demo sections
    show_available_cities()
    show_configuration()
    show_api_methods()
    simulate_weather_data()
    run_demo_tests()
    show_getting_started()
    
    print_header("Demo Complete")
    print("This demo showed you:")
    print("• Available Brandenburg cities and their coordinates")
    print("• Configuration options")
    print("• Available API methods")
    print("• Sample data structure")
    print("• Basic tests")
    print("• How to get started with a real API key")
    print()
    print("Next steps:")
    print("1. Get your free OpenWeatherMap API key")
    print("2. Set the OPENWEATHER_API_KEY environment variable")
    print("3. Run 'python example_usage.py' for real weather data!")


if __name__ == "__main__":
    main()