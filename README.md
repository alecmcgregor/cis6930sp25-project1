# cis6930sp25-project1

Name: Alec McGregor

## Assignment Description

In this assignment we gathered json data from the Gainesville crime API and found all incidents that corresponded to a given date. Then we found the location of the largest traffic incident on that day and compared it's location to all other traffic incidents that occured on that same day. If they were within 1km then the crime identifier and number of people involved were printed out.

## How to install

pipenv install -e .

## How to run

pipenv run python main.py --year 2025 --month 1 --day 1

## Example

![video](video)

## Features and functions

#### fetchdata() - fetches json data from a url.

#### data_cleaning() - removes time information from all of the date columns in the data.

#### formatdate() - will make sure that the date is in a 4 digit year, 2 digit month, and 2 digit day format in the order year-month-day.

#### filterdates() - filtered the data for all traffic incidents that occured on the given date.

#### find_biggest_incident() - finds the traffic incident where the most people were involved.

#### extract_location() - finds the coordinates of the traffic incident that involved the most people.

#### compare_location() - compares the coordinates of the traffic incident that involved the most people, with all other traffic incidents that occured on the given day.

#### sort_print() - sorts the data from most people involved to least number of people involved and prints the number of people involved on the left, then a tab, and then the crime identifier on the right.

#### main() - gathers all of the previous functions into one and runs them seemlessly

## Bugs and Assumptions
The largest assumption is that when we are finding the traffic incident that involves the most people, is that there will always be one traffic incident with more people involved. Also when trying to debug the data collected from the api was continuously changing so there needed to be a downloaded .json file to test on since the data there would be unchanging and we could precit what dates would be included in the 1000 events that are pulled. We are also assumming that people give valid dates when running the program, if a date is given that is not in the system or does not follow the proper format for the year, month, or day then it may cause a bug.
...
