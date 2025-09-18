#!/usr/bin/env python3
"""
CO2 Data Summary Demo
====================

Simple demo that shows just the key summary statistics from the Mauna Loa CO2 data.
"""

import urllib.request


def fetch_and_summarize():
    """Fetch CO2 data and show key summary statistics."""
    url = "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.txt"
    
    try:
        print("Fetching CO2 data from NOAA Global Monitoring Laboratory...")
        with urllib.request.urlopen(url) as response:
            content = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching data: {e}")
        return
    
    # Parse the data
    lines = content.strip().split('\n')
    records = []
    
    for line in lines:
        line = line.strip()
        if line.startswith('#') or line.startswith('-') or not line:
            continue
            
        try:
            parts = line.split()
            if len(parts) >= 8:
                year = int(parts[0])
                month = int(parts[1])
                co2_ppm = float(parts[3])
                records.append({'year': year, 'month': month, 'co2': co2_ppm})
        except (ValueError, IndexError):
            continue
    
    if not records:
        print("No data found!")
        return
    
    # Summary statistics
    first = records[0]
    last = records[-1]
    
    print("\n" + "="*60)
    print("MAUNA LOA CO2 DATA SUMMARY")
    print("="*60)
    print(f"📅 Time period: {first['year']}-{first['month']:02d} to {last['year']}-{last['month']:02d}")
    print(f"📊 Total records: {len(records)}")
    print(f"🌍 First measurement: {first['co2']:.2f} ppm ({first['year']})")
    print(f"🌍 Latest measurement: {last['co2']:.2f} ppm ({last['year']})")
    
    # Calculate trends
    increase = last['co2'] - first['co2']
    years = (last['year'] - first['year']) + (last['month'] - first['month']) / 12
    avg_rate = increase / years if years > 0 else 0
    
    print(f"📈 Total increase: {increase:.2f} ppm over {years:.1f} years")
    print(f"📈 Average rate: {avg_rate:.2f} ppm/year")
    
    # Recent trend (last 10 years)
    recent_records = [r for r in records if r['year'] >= last['year'] - 10]
    if len(recent_records) >= 2:
        recent_increase = recent_records[-1]['co2'] - recent_records[0]['co2']
        recent_years = len(recent_records) / 12
        recent_rate = recent_increase / recent_years if recent_years > 0 else 0
        print(f"🚨 Recent 10-year trend: {recent_rate:.2f} ppm/year")
    
    # Some key milestones
    milestones = [350, 400, 420]
    print(f"\n{'Key Milestones:':>20}")
    print("-" * 30)
    
    for milestone in milestones:
        for record in records:
            if record['co2'] >= milestone:
                print(f"{milestone:>15} ppm: {record['year']}-{record['month']:02d}")
                break
    
    # Show recent 12 months
    print(f"\n{'Recent 12 Months:':>20}")
    print("-" * 30)
    recent_12 = records[-12:]
    for record in recent_12:
        print(f"{record['year']}-{record['month']:02d}: {record['co2']:7.2f} ppm")
    
    print(f"\n🔬 Data source: NOAA Global Monitoring Laboratory")
    print(f"🏔️  Location: Mauna Loa Observatory, Hawaii")
    print(f"📏 Started by: Charles David Keeling (1958)")


if __name__ == "__main__":
    fetch_and_summarize()