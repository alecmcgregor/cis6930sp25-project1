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

dates_df = pd.DataFrame(dates)

def test_compare_remove():
    testing = main.compare_location(location, dates_df)
    assert testing.equals(dates_df)
    
def test_printing():
    statement = io.StringIO()
    sys.stdout = statement
    main.sort_print(dates_df)
    expectation = ("4\t224010123\n" + "3\t224010436\n")
    sys.stdout = sys.__stdout__
    assert statment.getValue() == expectation
