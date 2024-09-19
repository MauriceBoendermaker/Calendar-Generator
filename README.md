
# Holiday and Moon Phase Calendar Generator

This Python script scrapes holiday data for all countries and calculates moon phases for a specified year. It generates a CSV and an Excel file with holidays and moon phases organized by month, allowing users to dynamically regenerate a calendar for any given year.

## Features
- Scrapes holiday data for all countries from [timeanddate.com](https://www.timeanddate.com).
- Calculates moon phases (New Moon, Full Moon, etc.) for the specified year.
- Exports the data into both CSV and Excel files.
- Excel file is organized by month with a separate sheet for each month.
- Moon phases and holidays are displayed together, grouped by day.
- Automatically handles the generation of data for any year.

## Requirements

To run this project, you need to have the following installed:
- Python 3.6+
- Pip (Python package installer)

## Installation

### 1. Clone this repository
First, you need to clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/your-repository.git
cd your-repository
```

### 2. Install the required dependencies
To ensure all necessary Python libraries are installed, run:

```bash
pip install -r requirements.txt
```

## Usage

After you have installed the dependencies, you can run the script to generate the holiday and moon phase calendar for a specific year.

### Modify the year
In the Python script, update the `year` variable in the `__main__` block to the year for which you want to generate the calendar:

```python
if __name__ == "__main__":
    year = 2025  # Change this to the desired year
    regenerate_calendar_for_year(year)
```

### Run the script
To run the script, use the following command in your terminal or command prompt:

```bash
python script_name.py
```

The script will output two files:
- `holidays_<year>.csv` — A CSV file containing all holidays and moon phases.
- `holidays_<year>.xlsx` — An Excel file with a sheet for each month, showing holidays and moon phases.
