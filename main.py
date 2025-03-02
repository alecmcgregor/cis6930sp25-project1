import argparse
import json
import urllib.request
import pandas as pd
from geopy.distance import geodesic

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

def format_traffic_url(url,date):
    ending = f"?$where=accident_date%20between%20%27{date}T00:00:00%27%20and%20%27{date}T23:59:59%27"
    url = url + ending
    return url

def format_crime_url(url,date):
    #could need  report_date instead or could need both report and offense date = same day, check
    ending = f"?$where=report_date%20between%20%27{date}T00:00:00%27%20and%20%27{date}T23:59:59%27"
    url = url + ending
    return url

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
# def download_file(file):
#    if file is not None:
#        download = open(file)
#        return pd.DataFrame(json.load(download))
#    else:
#        return None

# def data_cleaning(data):
#     column_name = [col for col in data.columns if 'date' in col.lower()]
#     for i in range(0,len(column_name)):
#         data[column_name[i]] = data[column_name[i]].str.replace(r'T.*', '', regex=True)
#     return data



# def filterdates(data, date):
#     column_name = [col for col in data.columns if 'date' in col.lower()]
#     i = 1 if len(column_name)>1 else 0
#     filtered_data = data[data[column_name[i]] == date]
#     return filtered_data

def find_biggest_incident(data):
    #if no data was passed in return an empty df
    if data.empty:
        return pd.DataFrame()
    #convert totalpeopleinvolved into ints for comparison
    data.loc[:, "totalpeopleinvolved"] = data["totalpeopleinvolved"].astype(int)
    #extract the largest crash on the list
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
        if distance<=1:
            new_df = pd.concat([new_df, data.iloc[[i]]], ignore_index=True)
    return new_df

def clean_crimes(data):
    data.insert(1, 'totalpeopleinvolved', 1)
    selected_data = data[['id', 'totalpeopleinvolved']]
    return selected_data

def clean_traffic(data):
    selected_data = data[['case_number', 'totalpeopleinvolved']]
    selected_data = selected_data.copy()
    selected_data.rename(columns={'case_number':'id'}, inplace = True)
    return selected_data

def sort_print(data):
    data = data.sort_values(by='totalpeopleinvolved', ascending=False)
    for i in range(0, len(data)-1):
        if data['totalpeopleinvolved'].iloc[i] == data['totalpeopleinvolved'].iloc[i+1]:
            counter = i
            while data['totalpeopleinvolved'].iloc[counter] == data['totalpeopleinvolved'].iloc[counter+1] and counter<=len(data)-1:
                if data['id'].iloc[counter] < data['id'].iloc[counter+1]:
                    data.iloc[[counter, counter+1]] = data.iloc[[counter+1, counter]].values
                    counter=i
                else:
                    counter+=1
    for i in range(0, len(data)):
        print(f"{data['totalpeopleinvolved'].iloc[i]}\t{data['id'].iloc[i]}")

def main(year, month, day):
    #format the data for use
    date = formatdate(int(year), int(month), int(day))

    #fetch data from a formatted url to only return incidents on the provided day
    traffic_incidents = fetchdata(format_traffic_url("https://data.cityofgainesville.org/resource/iecn-3sxx.json", date))
    crime_incidents = fetchdata(format_crime_url("https://data.cityofgainesville.org/resource/gvua-xt9q.json", date))

    #gather the data from the url, create data frames, and clean the data
    # arrests = data_cleaning(fetchdata("https://data.cityofgainesville.org/resource/aum6-79zv.json"))
    # #traffic_incidents = data_cleaning(fetchdata("https://data.cityofgainesville.org/resource/iecn-3sxx.json"))
    # crime_responses = data_cleaning(fetchdata("https://data.cityofgainesville.org/resource/gvua-xt9q.json"))

    #temporary for debugging
    # traffic_incidents = data_cleaning(download_file("filename.json"))

    #filter all data frames for incidents that occurred on the given date
    # arr_dates = filterdates(arrests, date)
    # traffic_dates = filterdates(traffic_incidents, date)
    # crime_dates = filterdates(crime_responses, date)

    #find the traffic incident that affected the most total people, assuming that there will never be 2 biggest crashes
    biggest_crash = find_biggest_incident(traffic_incidents)
    if not biggest_crash.empty:

        #extract the location of that crash
        location = extract_location(biggest_crash)

        #compare the location of the crash to all other incidents and remove all incidents that are not within 1km
        new_traffic_data = compare_location(location,traffic_incidents)
        new_crime_data = compare_location(location, crime_incidents)

        #clean data for combination
        clean_traffic_data = clean_traffic(new_traffic_data)
        clean_crime_data = clean_crimes(new_crime_data)
        combined_data = pd.concat([clean_traffic_data, clean_crime_data], axis=0, ignore_index=True)

        #sort and print the data out
        sort_print(combined_data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=str, required=False, help="The year.")
    parser.add_argument("--month", type=str, required=False, help="The month.")
    parser.add_argument("--day", type=str, required=True, help="The day.")
    args = parser.parse_args()
    if not args.year:
        parser.print_help(sys.stderr)
    elif not args.month:
        parser.print_help(sys.stderr)
    elif not args.day:
        parser.print_help(sys.stderr)
    else:
        main(args.year, args.month, args.day)
