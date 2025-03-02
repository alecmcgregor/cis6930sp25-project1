# cis6930sp25-project1

Name: Alec McGregor

## Assignment Description

In this assignment we gathered json data from the Gainesville crime API and found all traffic and crime incidents that corresponded to a given date. Then we found the location of the largest traffic incident on that day and compared it's location to all other crime and traffic incidents that occured on that same day. If they were within 1km then the crime identifier and number of people involved were printed out being sorted from the largest amout of people involved to the least.

## How to install

pipenv install -e .

## How to run

pipenv run python main.py --year 2025 --month 1 --day 1

## Example

https://youtu.be/COgKMKECBFk

## Features and functions

#### formatdate() - will make sure that the date is in a 4 digit year, 2 digit month, and 2 digit day format in the order year-month-day.

#### format_traffic_url() - formats the url to make sure that only incidents on the correct date are being pulled from the traffic api.

#### format_crime_url() - formats the url to make sure that only incidents on the correct date are being pulled from the crime api.

#### fetchdata() - fetches the data from the provided api urls and turns it into a pandas data frame.

#### find_biggest_incident() - finds the traffic incident where the most people were involved.

#### extract_location() - finds the coordinates of the traffic incident that involved the most people.

#### compare_location() - compares the coordinates of the traffic incident that involved the most people, with all other traffic incidents that occured on the given day.

#### clean_crimes() - cleans up the crime data to make sure that it can be combined with traffic data.

#### clean_traffic() - cleans up the traffic data to make sure that it can be combined with crime data.

#### sort_print() - sorts the data from most people involved to least number of people involved and sorts by crime identifier. Then prints the number of people involved on the left, then a tab, and then the crime identifier on the right.

#### main() - gathers all of the previous functions into one and runs them seemlessly.

## Bugs and Assumptions
The following assumptions are based off of the "Running Example" that was provided in the project instructions. The arrest API was ignored since the example showed that we were concerned with all traffic incidents on a given day, not just those that resulted in arrests. Secondly, the crime data was filtered based on report date instead of crime date, this was also based on the running example which I found out filtered by report date. Third, is that the data downloaded will be in .json format for the fetch data function.
