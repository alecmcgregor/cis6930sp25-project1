import pytest
import main
import io
import sys
import pandas as pd

location = ('79.67545', '-82.34557')

dates = [
    {
        "case_number": "224010123",
        "accident_date": "2024-02-15",
        "totalpeopleinvolved": "4",
        "longitude": "-82.34012",
        "latitude": "79.67545"
    },
    {
        "case_number": "224010436",
        "accident_date": "2024-02-15",
        "totalpeopleinvolved": "3",
        "longitude": "-82.34557",
        "latitude": "79.67890"
    }
]

new_dates = [
    {
        "id": "224010123",
        "totalpeopleinvolved": "4"
    },
    {
        "id": "224010436",
        "totalpeopleinvolved": "3"
    }
]

crime_dates = [
    {
        "id": "224010123",
        "accident_date": "2024-02-15",
        "longitude": "-82.34012",
        "latitude": "79.67545",
    },
    {
        "id": "224010436",
        "accident_date": "2024-02-15",
        "longitude": "-82.34557",
        "latitude": "79.67890"
    }
]

expected_crime_dates = [
    {
        "id": "224010123",
        "totalpeopleinvolved": "1"
    },
    {
        "id": "224010436",
        "totalpeopleinvolved": "1"
    }
]

dates_df = pd.DataFrame(dates)
new_dates_df = pd.DataFrame(new_dates)
crime_dates_df = pd.DataFrame(crime_dates)
expected_crime_dates_df = pd.DataFrame(expected_crime_dates)

def test_compare_remove():
    testing = main.compare_location(location, dates_df)
    assert testing.equals(dates_df)

def test_clean_crimes():
    new_df = main.clean_crimes(crime_dates_df)
    new_df.reset_index(drop=True, inplace=True)
    assert new_df.equals(expected_crime_dates_df)

def test_clean_traffic():
    new_df = main.clean_traffic(dates_df)
    assert new_df.equals(new_dates_df)
    
def test_printing():
    statement = io.StringIO()
    sys.stdout = statement
    main.sort_print(new_dates_df)
    expectation = ("4\t224010123\n" + "3\t224010436\n")
    sys.stdout = sys.__stdout__
    assert statement.getvalue() == expectation
