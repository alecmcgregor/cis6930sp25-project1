import pytest
import main
import json
import pandas as pd

year = 2024
month = 12
day = 12

date = "2024-12-12"

url_traffic = "https://data.cityofgainesville.org/resource/iecn-3sxx.json"

url_crime = "https://data.cityofgainesville.org/resource/gvua-xt9q.json"

expected_traffic = f"https://data.cityofgainesville.org/resource/iecn-3sxx.json?$where=accident_date%20between%20%27{date}T00:00:00%27%20and%20%27{date}T23:59:59%27"

expected_crime = f"https://data.cityofgainesville.org/resource/gvua-xt9q.json?$where=report_date%20between%20%27{date}T00:00:00%27%20and%20%27{date}T23:59:59%27"

def test_formatdate():
    new_date = main.formatdate(year,month,day)
    assert new_date == "2024-12-12"

def test_formattraffic_url():
    url = main.format_traffic_url(url_traffic, date)
    assert url == expected_traffic

def test_formatcrime_url():
    url = main.format_crime_url(url_crime, date)
    assert url == expected_crime

def test_download_url():
    df_1 = main.fetchdata(expected_traffic)
    assert not df_1.empty

def test_correct_date():
    df = main.fetchdata(expected_traffic)
    df['accident_date'] = df['accident_date'].str.replace(r'T.*', '', regex=True)
    assert (df['accident_date'] == date).all()
