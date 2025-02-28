import pytest
import main
import pandas as pd

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

expected = [
    {
        "case_number": "224010123",
        "accident_date": "2024-02-15",
        "totalpeopleinvolved": "4",
        "longitude": "-82.34012",
        "latitude": "79.67545"
    }
]

expected_df = pd.DataFrame(expected)

def test_most_affected():
    biggest = main.find_biggest_incident(dates_df)
    data.loc[:, "totalpeopleinvolved"] = biggest["totalpeopleinvolved"].astype(str)
    assert biggest.equals(expected_df)
