#!/usr/bin/env python3
"""
Mauna Loa CO2 Data Viewer
=========================

This program fetches and displays atmospheric CO2 concentration data
from the Mauna Loa Observatory, Hawaii - the famous Keeling Curve dataset.

Data source: NOAA Global Monitoring Laboratory
URL: https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.txt
"""

import urllib.request
import urllib.error
import sys
from datetime import datetime
from typing import List, Tuple, Optional


class CO2DataRecord:
    """Represents a single monthly CO2 measurement record."""
    
    def __init__(self, year: int, month: int, decimal_date: float, 
                 monthly_avg: float, deseasonalized: float, 
                 num_days: int, std_dev: float, uncertainty: float):
        self.year = year
        self.month = month
        self.decimal_date = decimal_date
        self.monthly_avg = monthly_avg
        self.deseasonalized = deseasonalized
        self.num_days = num_days
        self.std_dev = std_dev
        self.uncertainty = uncertainty
    
    def __str__(self) -> str:
        return (f"{self.year:4d}-{self.month:02d}: {self.monthly_avg:7.2f} ppm "
                f"(deseasonalized: {self.deseasonalized:7.2f} ppm)")
    
    def is_interpolated(self) -> bool:
        """Returns True if this record contains interpolated data."""
        return self.num_days < 0


class MaunaLoaCO2Data:
    """Handler for Mauna Loa CO2 data fetching and processing."""
    
    DATA_URL = "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.txt"
    
    def __init__(self):
        self.records: List[CO2DataRecord] = []
        self.header_info: List[str] = []
    
    def fetch_data(self) -> bool:
        """
        Fetch CO2 data from NOAA website.
        Returns True if successful, False otherwise.
        """
        try:
            print("Fetching CO2 data from NOAA...")
            with urllib.request.urlopen(self.DATA_URL) as response:
                content = response.read().decode('utf-8')
            
            self._parse_data(content)
            print(f"Successfully loaded {len(self.records)} records")
            return True
            
        except urllib.error.URLError as e:
            print(f"Error fetching data: {e}")
            return False
        except Exception as e:
            print(f"Error processing data: {e}")
            return False
    
    def _parse_data(self, content: str) -> None:
        """Parse the raw data content into records."""
        lines = content.strip().split('\n')
        
        # Extract header information (comments starting with #)
        self.header_info = []
        data_lines = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('#') or line.startswith('-'):
                self.header_info.append(line)
            elif line and not line.startswith('#'):
                data_lines.append(line)
        
        # Parse data records
        self.records = []
        for line in data_lines:
            try:
                parts = line.split()
                if len(parts) >= 8:
                    record = CO2DataRecord(
                        year=int(parts[0]),
                        month=int(parts[1]),
                        decimal_date=float(parts[2]),
                        monthly_avg=float(parts[3]),
                        deseasonalized=float(parts[4]),
                        num_days=int(parts[5]),
                        std_dev=float(parts[6]),
                        uncertainty=float(parts[7])
                    )
                    self.records.append(record)
            except (ValueError, IndexError):
                continue  # Skip malformed lines
    
    def print_summary(self) -> None:
        """Print a summary of the dataset."""
        if not self.records:
            print("No data available")
            return
        
        first_record = self.records[0]
        last_record = self.records[-1]
        
        print("\n" + "="*60)
        print("MAUNA LOA ATMOSPHERIC CO2 DATA SUMMARY")
        print("="*60)
        print(f"Data source: {self.DATA_URL}")
        print(f"Time period: {first_record.year}-{first_record.month:02d} to {last_record.year}-{last_record.month:02d}")
        print(f"Total records: {len(self.records)}")
        print(f"First measurement: {first_record.monthly_avg:.2f} ppm ({first_record.year}-{first_record.month:02d})")
        print(f"Latest measurement: {last_record.monthly_avg:.2f} ppm ({last_record.year}-{last_record.month:02d})")
        
        # Calculate increase
        increase = last_record.monthly_avg - first_record.monthly_avg
        years = last_record.decimal_date - first_record.decimal_date
        avg_increase_per_year = increase / years if years > 0 else 0
        
        print(f"Total increase: {increase:.2f} ppm over {years:.1f} years")
        print(f"Average increase: {avg_increase_per_year:.2f} ppm/year")
        
        # Find recent trend (last 10 years)
        recent_records = [r for r in self.records if r.year >= last_record.year - 10]
        if len(recent_records) >= 2:
            recent_increase = recent_records[-1].monthly_avg - recent_records[0].monthly_avg
            recent_years = recent_records[-1].decimal_date - recent_records[0].decimal_date
            recent_trend = recent_increase / recent_years if recent_years > 0 else 0
            print(f"Recent trend (last 10 years): {recent_trend:.2f} ppm/year")
    
    def print_recent_data(self, num_records: int = 12) -> None:
        """Print the most recent data records."""
        if not self.records:
            print("No data available")
            return
        
        print(f"\n{'-'*50}")
        print(f"MOST RECENT {num_records} MONTHS OF CO2 DATA")
        print(f"{'-'*50}")
        print("Date       CO2 (ppm)  Deseasonalized  Days  Uncertainty")
        print("-" * 50)
        
        recent_records = self.records[-num_records:] if len(self.records) >= num_records else self.records
        
        for record in recent_records:
            interpolated_mark = "*" if record.is_interpolated() else " "
            print(f"{record.year}-{record.month:02d}    {record.monthly_avg:8.2f}    "
                  f"{record.deseasonalized:8.2f}     {record.num_days:3d}    "
                  f"{record.uncertainty:6.2f}{interpolated_mark}")
        
        print("\n* = interpolated data")
    
    def print_yearly_averages(self, start_year: Optional[int] = None, end_year: Optional[int] = None) -> None:
        """Print yearly average CO2 concentrations."""
        if not self.records:
            print("No data available")
            return
        
        # Group records by year
        yearly_data = {}
        for record in self.records:
            if start_year and record.year < start_year:
                continue
            if end_year and record.year > end_year:
                continue
            
            if record.year not in yearly_data:
                yearly_data[record.year] = []
            yearly_data[record.year].append(record.monthly_avg)
        
        print(f"\n{'-'*40}")
        print("YEARLY AVERAGE CO2 CONCENTRATIONS")
        print(f"{'-'*40}")
        print("Year    Average (ppm)   Change")
        print("-" * 40)
        
        prev_avg = None
        for year in sorted(yearly_data.keys()):
            if yearly_data[year]:  # Only if we have data for this year
                avg = sum(yearly_data[year]) / len(yearly_data[year])
                change_str = ""
                if prev_avg is not None:
                    change = avg - prev_avg
                    change_str = f"  {change:+5.2f}"
                
                print(f"{year}    {avg:10.2f}{change_str}")
                prev_avg = avg
    
    def search_by_date(self, year: int, month: Optional[int] = None) -> None:
        """Search for data by specific date."""
        matches = []
        
        for record in self.records:
            if record.year == year and (month is None or record.month == month):
                matches.append(record)
        
        if not matches:
            date_str = f"{year}" if month is None else f"{year}-{month:02d}"
            print(f"No data found for {date_str}")
            return
        
        print(f"\n{'-'*50}")
        if month is None:
            print(f"CO2 DATA FOR YEAR {year}")
        else:
            print(f"CO2 DATA FOR {year}-{month:02d}")
        print(f"{'-'*50}")
        
        for record in matches:
            print(record)


def print_menu():
    """Print the interactive menu."""
    print("\n" + "="*50)
    print("MAUNA LOA CO2 DATA VIEWER - MENU")
    print("="*50)
    print("1. Show data summary")
    print("2. Show recent data (last 12 months)")
    print("3. Show yearly averages")
    print("4. Show yearly averages for date range")
    print("5. Search by specific year")
    print("6. Search by specific month/year")
    print("7. Refresh data")
    print("8. Show dataset info")
    print("0. Exit")
    print("-" * 50)


def main():
    """Main program function."""
    print("Mauna Loa CO2 Data Viewer")
    print("=" * 30)
    
    co2_data = MaunaLoaCO2Data()
    
    # Initial data fetch
    if not co2_data.fetch_data():
        print("Failed to fetch initial data. Exiting.")
        return 1
    
    while True:
        print_menu()
        try:
            choice = input("Enter your choice (0-8): ").strip()
            
            if choice == '0':
                print("Thank you for using CO2 Data Viewer!")
                break
                
            elif choice == '1':
                co2_data.print_summary()
                
            elif choice == '2':
                co2_data.print_recent_data()
                
            elif choice == '3':
                co2_data.print_yearly_averages()
                
            elif choice == '4':
                try:
                    start_year = int(input("Enter start year (or press Enter for beginning): ").strip() or "0") or None
                    end_year = int(input("Enter end year (or press Enter for end): ").strip() or "0") or None
                    co2_data.print_yearly_averages(start_year, end_year)
                except ValueError:
                    print("Invalid year format. Please enter a valid year.")
                    
            elif choice == '5':
                try:
                    year = int(input("Enter year: ").strip())
                    co2_data.search_by_date(year)
                except ValueError:
                    print("Invalid year format. Please enter a valid year.")
                    
            elif choice == '6':
                try:
                    year = int(input("Enter year: ").strip())
                    month = int(input("Enter month (1-12): ").strip())
                    co2_data.search_by_date(year, month)
                except ValueError:
                    print("Invalid date format. Please enter valid year and month.")
                    
            elif choice == '7':
                if co2_data.fetch_data():
                    print("Data refreshed successfully!")
                else:
                    print("Failed to refresh data.")
                    
            elif choice == '8':
                print(f"\n{'-'*60}")
                print("DATASET INFORMATION")
                print(f"{'-'*60}")
                for line in co2_data.header_info[:20]:  # Show first 20 lines of header
                    print(line)
                if len(co2_data.header_info) > 20:
                    print(f"... and {len(co2_data.header_info) - 20} more header lines")
                    
            else:
                print("Invalid choice. Please enter a number between 0 and 8.")
                
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
        
        input("\nPress Enter to continue...")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())