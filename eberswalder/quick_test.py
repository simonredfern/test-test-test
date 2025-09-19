#!/usr/bin/env python3
"""
Quick Test Script for Brandenburg Weather Data Fetcher

This is a simple script to quickly test the weather fetcher when you have
an OpenWeatherMap API key. It fetches weather for Eberswalde and shows
a basic formatted output.

Usage:
  1. Get API key from https://openweathermap.org/api
  2. export OPENWEATHER_API_KEY='your_key_here'
  3. python quick_test.py
"""

import os
import sys
from weather_fetcher import BrandenburgWeatherFetcher

def main():
    """Quick test of the weather fetcher"""
    
    # Check for API key
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        print("❌ No API key found!")
        print("Set your OpenWeatherMap API key with:")
        print("export OPENWEATHER_API_KEY='your_key_here'")
        print("\nGet a free key at: https://openweathermap.org/api")
        sys.exit(1)
    
    print("🌤️  Quick Weather Test for Brandenburg")
    print("=" * 40)
    
    try:
        # Initialize fetcher
        fetcher = BrandenburgWeatherFetcher(api_key)
        
        # Test 1: Get weather for Eberswalde
        print("\n📍 Current Weather in Eberswalde:")
        weather = fetcher.get_current_weather("eberswalde")
        print(fetcher.format_current_weather(weather))
        
        # Test 2: Get weather for Potsdam
        print("\n📍 Current Weather in Potsdam:")
        weather = fetcher.get_current_weather("potsdam")
        print(fetcher.format_current_weather(weather))
        
        # Test 3: Simple comparison
        print("\n🌡️  Temperature Comparison:")
        cities = ["eberswalde", "potsdam", "cottbus"]
        for city in cities:
            weather = fetcher.get_current_weather(city)
            city_name = weather["city_info"]["name"]
            temp = weather["main"]["temp"]
            condition = weather["weather"][0]["description"].title()
            print(f"  {city_name:<20} {temp:>5.1f}°C - {condition}")
        
        print("\n✅ Quick test completed successfully!")
        print("For more examples, run: python example_usage.py")
        
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        print("Make sure your API key is valid and you have internet connection.")

if __name__ == "__main__":
    main()