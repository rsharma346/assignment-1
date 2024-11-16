#!/usr/bin/env python3

import sys
from datetime import datetime

def parse_date(date: str) -> (int, int, int):
    """Parses a date string in DD/MM/YYYY or YYYY-MM-DD format"""
    try:
        if '/' in date:
            # DD/MM/YYYY format
            day, month, year = (int(x) for x in date.split('/'))
        elif '-' in date:
            # YYYY-MM-DD format
            year, month, day = (int(x) for x in date.split('-'))
        else:
            raise ValueError("Invalid date format")
        return day, month, year
    except ValueError as e:
        raise ValueError("Date parsing error: Invalid format or data") from e

def leap_year(year: int) -> bool:
    """Return True if the year is a leap year, otherwise False"""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def mon_max(month: int, year: int) -> int:
    """Returns the maximum number of days for a given month"""
    if month == 2:
        return 29 if leap_year(year) else 28
    elif month in [4, 6, 9, 11]:
        return 30
    else:
        return 31

def valid_date(date: str) -> bool:
    """Check if a given date is valid"""
    try:
        # Attempt to parse the date
        day, month, year = parse_date(date)

        # Check if the month is in the valid range (1 to 12)
        if month < 1 or month > 12:
            return False

        # Check if the day is valid for the given month and year
        if day < 1 or day > mon_max(month, year):
            return False

        return True
    except ValueError:
        # Catch any parsing errors and return False for invalid date formats
        return False

def usage():
    """Prints a usage message to the user"""
    print(f"Usage: {sys.argv[0]} <start_date> <end_date>")
    print("\nExample:")
    print(f"  {sys.argv[0]} 31/12/2023 05/01/2024")
    print("Ensure the dates are in the correct format (DD/MM/YYYY or YYYY-MM-DD).")
    sys.exit()

def day_of_week(date: str) -> str:
    """Returns the day of the week for a given date (DD/MM/YYYY format)"""
    day, month, year = parse_date(date)
    days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    offset = {1: 0, 2: 3, 3: 2, 4: 5, 5: 0, 6: 3, 7: 5, 8: 1, 9: 4, 10: 6, 11: 2, 12: 4}
    if month < 3:
        year -= 1
    num = (year + year // 4 - year // 100 + year // 400 + offset[month] + day) % 7
    return days[num]

def after(date: str) -> str:
    """Returns the next day's date in YYYY-MM-DD format"""
    day, month, year = parse_date(date)
    day += 1

    if day > mon_max(month, year):
        day = 1
        month += 1
        if month > 12:
            month = 1
            year += 1
    return f"{year}-{month:02}-{day:02}"

def before(date: str) -> str:
    """Returns the previous day's date in YYYY-MM-DD format"""
    day, month, year = parse_date(date)
    day -= 1

    if day < 1:
        month -= 1
        if month < 1:
            month = 12
            year -= 1
        day = mon_max(month, year)
    return f"{year}-{month:02}-{day:02}"

def date_compare(start_date: str, end_date: str) -> bool:
    """Compares if start_date is earlier than end_date"""
    start_day, start_month, start_year = parse_date(start_date)
    end_day, end_month, end_year = parse_date(end_date)
    
    start_date_obj = datetime(start_year, start_month, start_day)
    end_date_obj = datetime(end_year, end_month, end_day)

    return start_date_obj < end_date_obj

def day_count(start_date: str, end_date: str) -> int:
    """Counts the number of Saturdays and Sundays between the start and end date"""
    count = 0
    date = start_date
    while date != end_date:
        if day_of_week(date) in ['Sat', 'Sun']:
            count += 1
        date = after(date)
    # Include the end date in the count
    if day_of_week(end_date) in ['Sat', 'Sun']:
        count += 1
    return count

if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage()

    start_date = sys.argv[1]
    end_date = sys.argv[2]

    # Validate both dates
    if not valid_date(start_date) or not valid_date(end_date):
        usage()

    # Swap start and end dates if in reversed order
    if not date_compare(start_date, end_date):
        start_date, end_date = end_date, start_date

    weekend_days = day_count(start_date, end_date)

    # Updated output to match the expected format
    print(f"The period between {start_date} and {end_date} includes {weekend_days} weekend days.")

