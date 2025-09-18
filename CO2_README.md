# Mauna Loa CO2 Data Programs

This directory contains Python programs to fetch and display atmospheric CO2 concentration data from the Mauna Loa Observatory in Hawaii - the famous Keeling Curve dataset.

## Programs

### 1. Interactive CO2 Data Viewer (`co2_data_viewer.py`)

A full-featured interactive program with a menu system that allows you to:
- View data summaries and statistics
- Browse recent measurements
- Calculate yearly averages
- Search by specific dates
- Refresh data from NOAA servers

**Usage:**
```bash
python co2_data_viewer.py
```

**Features:**
- Interactive menu system
- Real-time data fetching from NOAA
- Statistical analysis (trends, averages, growth rates)
- Date range filtering
- Search functionality
- Data validation and error handling

### 2. Simple CO2 Data Printer (`simple_co2_printer.py`)

A straightforward script that fetches the data and prints it in a clean table format.

**Usage:**
```bash
python simple_co2_printer.py
```

**Output includes:**
- Complete data table with all measurements
- Summary statistics
- Growth rate calculations
- Recent trends

## Data Source

Both programs fetch data from:
- **Source**: NOAA Global Monitoring Laboratory
- **URL**: https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.txt
- **Coverage**: March 1958 to present
- **Frequency**: Monthly measurements
- **Units**: Parts per million (ppm)

## Data Format

The data includes the following columns:
- **Year/Month**: Date of measurement
- **Decimal Date**: Year as decimal (e.g., 2024.5 = July 2024)
- **Monthly Average**: Raw CO2 concentration in ppm
- **Deseasonalized**: CO2 with seasonal variations removed
- **Days**: Number of measurement days (negative = interpolated)
- **StdDev**: Standard deviation of daily measurements
- **Uncertainty**: Measurement uncertainty

## Requirements

- Python 3.6 or higher
- Internet connection to fetch data
- No external packages required (uses standard library only)

## Example Output

```
MAUNA LOA OBSERVATORY - ATMOSPHERIC CO2 CONCENTRATIONS
================================================================================
Source: NOAA Global Monitoring Laboratory
Units: parts per million (ppm)

Year  Month    Date     CO2(ppm)  Deseason.  Days  StdDev  Uncert.
--------------------------------------------------------------------------------
1958     3   1958.2027   315.71    314.44    -1   -9.99   -0.99*
1958     4   1958.2877   317.45    315.16    -1   -9.99   -0.99*
...
2025     7   2025.5417   427.87    427.45    24    0.28    0.11
--------------------------------------------------------------------------------

SUMMARY STATISTICS:
Time period: 1958-03 to 2025-07
Total records: 809
First measurement: 315.71 ppm
Latest measurement: 427.87 ppm
Total increase: 112.16 ppm over 67.3 years
Average rate: 1.67 ppm/year
Recent 10-year trend: 2.31 ppm/year
```

## Historical Context

This dataset represents one of the most important climate records in history:

- **Started by**: Charles David Keeling (Scripps Institution) in 1958
- **Location**: Mauna Loa Observatory, Hawaii (11,500 ft elevation)
- **Significance**: First continuous record showing rising atmospheric CO2
- **Scientific Impact**: Key evidence for human-caused climate change

The characteristic sawtooth pattern shows:
- **Seasonal cycle**: ~6 ppm annual variation due to Northern Hemisphere vegetation
- **Long-term trend**: Steady increase from human fossil fuel emissions
- **Recent acceleration**: Faster growth rates in recent decades

## Notes

- Records marked with `*` contain interpolated data
- Measurements were temporarily relocated during Mauna Loa volcanic activity (2022-2023)
- Early data (1958-1974) from Scripps; later data from NOAA
- The "deseasonalized" values remove the natural seasonal CO2 cycle to show the underlying trend

## License

These programs are provided for educational and research purposes. The CO2 data is freely available from NOAA Global Monitoring Laboratory.