#!/usr/bin/env python3
"""
Simple Mauna Loa CO2 Data Printer
=================================

A straightforward script that fetches and prints CO2 data from Mauna Loa Observatory.
This creates a simple table showing the atmospheric CO2 measurements over time.

Data source: NOAA Global Monitoring Laboratory
"""

import urllib.request
import sys


def fetch_co2_data():
    """Fetch CO2 data from NOAA website and return as text."""
    url = "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.txt"
    
    try:
        print("Fetching CO2 data from NOAA Global Monitoring Laboratory...")
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


def parse_and_print_data(raw_data):
    """Parse the raw data and print in a formatted table."""
    lines = raw_data.strip().split('\n')
    
    # Find where the actual data starts (after header comments)
    data_start = 0
    for i, line in enumerate(lines):
        if not line.strip().startswith('#') and not line.strip().startswith('-') and line.strip():
            data_start = i
            break
    
    # Print header
    print("\n" + "=" * 80)
    print("MAUNA LOA OBSERVATORY - ATMOSPHERIC CO2 CONCENTRATIONS")
    print("=" * 80)
    print("Source: NOAA Global Monitoring Laboratory")
    print("Units: parts per million (ppm)")
    print()
    print("Year  Month    Date     CO2(ppm)  Deseason.  Days  StdDev  Uncert.")
    print("-" * 80)
    
    records = []
    
    # Parse and print each data line
    for line in lines[data_start:]:
        line = line.strip()
        if not line:
            continue
            
        try:
            parts = line.split()
            if len(parts) >= 8:
                year = int(parts[0])
                month = int(parts[1])
                decimal_date = float(parts[2])
                monthly_avg = float(parts[3])
                deseasonalized = float(parts[4])
                num_days = int(parts[5])
                std_dev = float(parts[6])
                uncertainty = float(parts[7])
                
                # Format the output line
                interpolated = "*" if num_days < 0 else " "
                print(f"{year:4d}    {month:2d}   {decimal_date:8.4f}  {monthly_avg:7.2f}   "
                      f"{deseasonalized:7.2f}   {num_days:3d}   {std_dev:5.2f}   "
                      f"{uncertainty:5.2f}{interpolated}")
                
                records.append({
                    'year': year, 'month': month, 'co2': monthly_avg,
                    'deseasonalized': deseasonalized
                })
                
        except (ValueError, IndexError):
            continue
    
    print("-" * 80)
    print("* = interpolated data")
    
    # Print summary statistics
    if records:
        first_record = records[0]
        last_record = records[-1]
        
        print(f"\nSUMMARY STATISTICS:")
        print(f"Time period: {first_record['year']}-{first_record['month']:02d} to {last_record['year']}-{last_record['month']:02d}")
        print(f"Total records: {len(records)}")
        print(f"First measurement: {first_record['co2']:.2f} ppm")
        print(f"Latest measurement: {last_record['co2']:.2f} ppm")
        
        increase = last_record['co2'] - first_record['co2']
        years = (last_record['year'] - first_record['year']) + (last_record['month'] - first_record['month']) / 12
        avg_increase = increase / years if years > 0 else 0
        
        print(f"Total increase: {increase:.2f} ppm over {years:.1f} years")
        print(f"Average rate: {avg_increase:.2f} ppm/year")
        
        # Show recent trend (last 10 years if available)
        recent_records = [r for r in records if r['year'] >= last_record['year'] - 10]
        if len(recent_records) >= 2:
            recent_increase = recent_records[-1]['co2'] - recent_records[0]['co2']
            recent_years = len(recent_records) / 12  # approximate years
            recent_trend = recent_increase / recent_years if recent_years > 0 else 0
            print(f"Recent 10-year trend: {recent_trend:.2f} ppm/year")


def main():
    """Main function to run the CO2 data printer."""
    print("Mauna Loa CO2 Data Printer")
    print("=" * 30)
    
    # Fetch the data
    raw_data = fetch_co2_data()
    if raw_data is None:
        print("Failed to fetch data. Please check your internet connection.")
        return 1
    
    # Parse and display the data
    parse_and_print_data(raw_data)
    
    print("\nData fetched successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(main())