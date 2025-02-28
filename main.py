import argparse
import json
import urllib.request
import pandas as pd
#import duckdb
from geopy.distance import geodesic

# Function to download json data from a url provided to us by Dr.Grant
def fetchdata(url, isjson=True):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Referer': 'https://www.google.com/',
        'DNT': '1',  # Do Not Track request header
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
    }

    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        data = response.read().decode('utf-8')
        if isjson:
            return pd.DataFrame(json.loads(data))
        else:
            return pd.DataFrame(data)

#temporary for debugging
#def download_file(file):
#    if file is not None:
#        download = open(file)
#        return pd.DataFrame(json.load(download))
#    else:
#        return None

def data_cleaning(data):
    column_name = [col for col in data.columns if 'date' in col.lower()]
    for i in range(0,len(column_name)):
        data[column_name[i]] = data[column_name[i]].str.replace(r'T.*', '', regex=True)
    return data

def formatdate(year,month,day):
    if month<10:
        month = f"0{month}"
    else:
        month = f"{month}"
    if day<10:
        day = f"0{day}"
    else:
        day = f"{day}"
    return f"{year}-{month}-{day}"

def filterdates(data, date):
    column_name = [col for col in data.columns if 'date' in col.lower()]
    i = 1 if len(column_name)>1 else 0
    filtered_data = data[data[column_name[i]] == date]
    return filtered_data

def find_biggest_incident(data):
    if data.empty:
        return None
    biggest_crash = data.loc[[data['totalpeopleinvolved'].idxmax()]]
    return biggest_crash

def extract_location(data):
     longitude, latitude = data['longitude'], data['latitude']
     return latitude.iloc[0], longitude.iloc[0]

def compare_location(location, data):
    new_df = pd.DataFrame(columns=data.columns)
    for i in range(0, len(data)):
        latitude = data['latitude'].iloc[i]
        longitude = data['longitude'].iloc[i]
        distance = geodesic((latitude, longitude), location).kilometers
        if distance<1:
            new_df = pd.concat([new_df, data.iloc[[i]]], ignore_index=True)
    return new_df

def sort_print(data):
    data = data.sort_values(by='totalpeopleinvolved', ascending=False)
    for i in range(0, len(data)):
        print(f"{data['totalpeopleinvolved'].iloc[i]}\t{data['case_number'].iloc[i]}")

def main(year, month, day):
    #gather the data from the url, create data frames, and clean the data
    arrests = data_cleaning(fetchdata("https://data.cityofgainesville.org/resource/aum6-79zv.json"))
    traffic_incidents = data_cleaning(fetchdata("https://data.cityofgainesville.org/resource/iecn-3sxx.json"))
    crime_responses = data_cleaning(fetchdata("https://data.cityofgainesville.org/resource/gvua-xt9q.json"))

    #temporary for debugging
    #traffic_incidents = data_cleaning(download_file("filename.json"))

    #format the data for use
    date = formatdate(int(year), int(month), int(day))

    #filter all data frames for incidents that occurred on the given date
    arr_dates = filterdates(arrests, date)
    traffic_dates = filterdates(traffic_incidents, date)
    crime_dates = filterdates(crime_responses, date)

    #find the traffic incident that affected the most total people, assuming that there will never be 2 biggest crashes
    biggest_crash = find_biggest_incident(traffic_dates)
    if biggest_crash != None:

        #extract the location of that crash
        location = extract_location(biggest_crash)

        #compare the location of the crash to all other incidents and remove all incidents that are not within 1km
        new_data=compare_location(location,traffic_dates)

        #sort and print the data out
        sort_print(new_data)
    else:
        print("There is no crash on that date! In the given data!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=str, required=False, help="The year.")
    parser.add_argument("--month", type=str, required=False, help="The month.")
    parser.add_argument("--day", type=int, required=True, help="The day.")
    args = parser.parse_args()
    main(args.year, args.month, args.day)
