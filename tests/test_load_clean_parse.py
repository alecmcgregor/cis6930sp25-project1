import pytest
import main
import json
import pandas as pd

url = "https://data.cityofgainesville.org/resource/iecn-3sxx.json"

data = [
    {
        "case_number": "224010123",
        "accident_date": "2024-02-15T14:35:22.000",
        "totalpeopleinvolved": "4",
        "longitude": "-82.34012",
        "latitude": "79.67545"
    },
    {
        "case_number": "224010456",
        "accident_date": "2024-02-18T09:12:48.000",
        "totalpeopleinvolved": "2",
        "longitude": "-82.34567",
        "latitude": "29.67890"
    },
    {
        "case_number": "224010436",
        "accident_date": "2024-02-28T09:12:48.000",
        "totalpeopleinvolved": "1",
        "longitude": "-12.34567",
        "latitude": "79.67890"
    },
    {
        "case_number": "224010436",
        "accident_date": "2024-02-15T09:12:48.000",
        "totalpeopleinvolved": "3",
        "longitude": "-82.34557",
        "latitude": "79.67890"
    }
]

df = pd.DataFrame(data)

cleaned = [
    {
        "case_number": "224010123",
        "accident_date": "2024-02-15",
        "totalpeopleinvolved": "4",
        "longitude": "-82.34012",
        "latitude": "79.67545"
    },
    {
        "case_number": "224010456",
        "accident_date": "2024-02-18",
        "totalpeopleinvolved": "2",
        "longitude": "-82.34567",
        "latitude": "29.67890"
    },
    {
        "case_number": "224010436",
        "accident_date": "2024-02-28",
        "totalpeopleinvolved": "1",
        "longitude": "-12.34567",
        "latitude": "79.67890"
    },
    {
        "case_number": "224010436",
        "accident_date": "2024-02-15",
        "totalpeopleinvolved": "3",
        "longitude": "-82.34557",
        "latitude": "79.67890"
    }
]

clean_df = pd.DataFrame(cleaned)

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

dates_df = pd.DataFrame(dates)

def test_download_url():
    df_1 = main.fetchdata(url)
    assert not df_1.empty

def test_clean_data():
    clean_data = main.data_cleaning(df)
    assert clean_data.equals(clean_df)

def test_date_filtering():
    just_dates = main.filterdates(clean_df, "2024-02-15")
    assert just_dates.equals(dates_df)
