"""This script takes in two city names as input and outputs the differences in
weather between the cities over the next 5 days.

Usage example:

    python compare_forecasts.py Toronto Cleveland

Output example:

    Weather forecast comparison between Toronto and Cleveland:

    Day 1:
    Toronto (18C) will be 3C cooler than Cleveland (21C).
    Toronto will have clear sky, but Cleveland will have rain.

    Day 2:
    Toronto (21C) will be 3C warmer than Cleveland (18C).
    Toronto will have scattered clouds, but Cleveland will have light rain.

    Day 3:
    Toronto and Cleveland will both have the same temperature (20C).
    Toronto and Cleveland will both have light rain.

    Day 4:
    Toronto (18C) will be 3C cooler than Cleveland (21C).
    Toronto and Cleveland will both have light rain.

    Day 5:
    Toronto and Cleveland will both have the same temperature (17C).
    Toronto will have scattered clouds, but Cleveland will have light rain.
"""

import argparse
import os
import sys
import json

""" Importing the 'requests' library by adding vendor directory to module search path """
parent_dir = os.path.abspath(os.path.dirname(__file__))
vendor_dir = os.path.join(parent_dir, 'vendor')
sys.path.append(vendor_dir)
import requests

def main():
    """ Parse the input parameters."""

    parser = argparse.ArgumentParser(description="Compare weather forecasts between two cities.")
    parser.add_argument("city1", type=str, help="The first city.")
    parser.add_argument("city2", type=str, help="The second city.")
    args = parser.parse_args()
    compare_forecasts(args.city1, args.city2)

def compare_forecasts(city1, city2):
    """ Print out the 5-day comparison in weather between city1 and city2. """

    print("Weather forecast comparison between {} and {}:".format(city1, city2) + '\n')

    for day in range(1, 6, 1):
        city1_info = get_temp_and_desc(city1, day)
        city2_info = get_temp_and_desc(city2, day)

        print 'Day ' + str(day) + ':'
        print(temp_output(city1, city1_info['temperature'], city2, city2_info['temperature']))
        print(desc_output(city1, city1_info['description'], city2, city2_info['description']) + '\n')

def get_temp_and_desc(city, day):
    """ Get the temperature and the weather description of a 'city' at a 'day' within the next 5 days.

    Arguments:
        city - - The city to retrieve the weather information for
        day  - - An integer between 1-5 that represents a day within the next 5 days

    Return:
        Dictionary:
        {
            'temperature': The temprature of the 'city' at a 'day'
            'description': The weather description of the 'city' at a 'day'
        }

    """
    try:
        # Make the API call using the provided city.
        # Note: the country is set to 'ca' in the call. We could add the country as a parameter to
        # retrieve global weather information.
        # Note: the unit is set to metric (Celsius) in the API call.
        req = requests.get('http://api.openweathermap.org/data/2.5/forecast?q=' + city + ',ca&APPID=fe9c5cddb7e01d747b4611c3fc9eaf2c&units=metric')
        city_json_data = json.loads(req.text)
        temp = city_json_data['list'][day]['main']['temp']
        desc = city_json_data['list'][day]['weather'][0]['description']
        return{'temperature': int(temp), 'description': desc}
    except Exception:
        print("Failure to call the API")

def temp_output(city1, city1_temp, city2, city2_temp):
    """ The temperature comparison between city1 and city2's temperature for a day.

    Arguments:
        city1      - - City #1
        city1_temp - - City 1's temperature in Celsius
        city2      - - City #2
        city2_temp - - City 2's temperature in Celsius

    Return:
        String of the temperature comparison between city1 and city2
    """

    if (city1_temp == city2_temp):
        return city1 + ' and ' + city2 + ' will both have the same temperature (' + str(city1_temp) + 'C).'
    elif (city1_temp < city2_temp):
        return city1 + ' (' + str(city1_temp) + 'C) will be ' + str(city2_temp - city1_temp) \
               + 'C cooler than ' + city2 + ' (' + str(city2_temp) + 'C).'
    else:
        return city1 + ' (' + str(city1_temp) + 'C) will be ' + str(city1_temp - city2_temp) \
               + 'C warmer than ' + city2 + ' (' + str(city2_temp) + 'C).'

def desc_output(city1, city1_desc, city2, city2_desc):
    """ The weather description comparison between city1 and city2's for a day.

    Arguments:
        city1      - - City #1
        city1_temp - - City 1's weather status
        city2      - - City #2
        city2_temp - - City 2's weather status

    Return:
        String of the weather description comparison between city1 and city2.
    """

    if (city1_desc == city2_desc):
        return city1 + ' and ' + city2 + ' will both have ' + city1_desc + '.'
    else:
        return city1 + ' will have ' + city1_desc + ', but ' + city2 + ' will have ' + city2_desc + '.'


if __name__ == "__main__":
    main()
