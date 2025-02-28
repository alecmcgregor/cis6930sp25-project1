import pytest
import main
import pandas as pd

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

def test_location_finder():
    location = main.extract_location(expected_df)
    assert location == ('79.67545', '-82.34557')
