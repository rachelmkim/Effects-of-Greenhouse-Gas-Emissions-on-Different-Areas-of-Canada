"""CSC110 Fall 2020 Final Project, Data Reading

Description
===============================
This module reads the raw data from the csv and txt files and converts them into a usable format.
WARNING: IT TAKES QUITE A LONG TIME TO RUN

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of TA's and professors
teaching CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2020 Dana Alshekerchi, Nehchal Kalsi, Rachel Kim, Kathy Lee.
"""

from typing import List, Any, Dict, Tuple
import csv
import os


def read_ghg_emissions_for_maps(filename: str) -> Dict[Any, List[float]]:
    """Read and return the csv of the greenhouse gases dataset as a dictionary. The file is
    specified by the filename inputted. The keys of the returned dictionary are years from 1990 to
    2018 and the list associated with each key contains the CO2 equivalent emissions for each of the
    provinces in alphabetical order.

    Preconditions:
        - filename is in the format 'GHG_IPCC_Can_Prov_Terr.csv'
    """

    with open(filename) as file:
        reader = csv.reader(file)

        # Skip header row
        next(reader)

        data_so_far = {}
        for row in reader:
            if int(row[0]) >= 1990 and row[3] == 'TOTAL':
                if int(row[0]) not in data_so_far:
                    data_so_far[int(row[0])] = []
                list.append(data_so_far[int(row[0])], float(row[-2]))

        for year in range(1990, 1999):
            list.insert(data_so_far[year], 7, data_so_far[year][6])

        # remove the values that contain the total emissions for Canada
        for year in data_so_far:
            list.pop(data_so_far[year], 2)

        # make the Nunavut emission values the same as Northwest Territories before Nunavut was
        # founded in 1999 since it was a part of Northwest Territories

    return data_so_far


def read_ghg_emissions(filename: str) -> List[List[Any]]:
    """Read and return the csv of the greenhouse gases dataset as a nested list, with the inner list
    containing the year (an integer), province (a string), and CO2 equivalent of greenhouse gas
    emissions (a float) in that order. The file is specified by the filename inputted.

    Preconditions:
        - filename is in the format 'GHG_IPCC_Can_Prov_Terr.csv'
    """

    with open(filename) as file:
        reader = csv.reader(file)

        # Skip header row
        next(reader)

        data_so_far = []
        for row in reader:
            if row[3] == 'TOTAL':
                new_row = []
                list.append(new_row, int(row[0]))
                list.append(new_row, row[1])
                list.append(new_row, float(row[-2]))
                list.append(data_so_far, new_row)

    return data_so_far


def read_daily_mean_temps_all_files_for_maps(file_path: str, directory: str) -> \
        Dict[Tuple[str, str, str], Dict[int, List[float]]]:
    """Read and return the data in ALL of the text files that represent different locations in
    Canada. The location of the files is specified by file_path and directory.

    The key of the dictionary is a tuple, with the first element representing the station name and
    the second element representing the province or territory that the station is in.

    The value of the dictionary is another dictionary. The key of this inner dictionary is the year
    and the value of this inner dictionary is a list of all the temperatures for every day of that
    year.

    Preconditions:
        - file_path is in a format that resembles this:
            'C:/Users/Rachel Kim/Documents/University of Toronto/2020-2021
            /CSC110/miscellaneous/Final Project/daily_mean_temps/'
        - directory is in a format that resembles this:
            'C:\\Users\\Rachel Kim\\Documents\\University of Toronto\\2020-2021
            \\CSC110\\miscellaneous\\Final Project\\daily_mean_temps'
    """

    files = os.listdir(directory)

    data_so_far = {}
    for file_name in files:
        f = open(file_path + file_name, 'r')

        # get the station name and the province
        first_line = f.readline()
        first_line_list = str.split(first_line, ',')

        location_key = (str.strip(first_line_list[0]), str.strip(first_line_list[1]),
                        str.strip(first_line_list[2]))
        years_and_temps = read_daily_mean_temps_one_file(file_path + file_name)
        data_so_far[location_key] = years_and_temps

    return data_so_far


def read_daily_mean_temps_all_files(file_path: str, directory: str) -> \
        Dict[Tuple[str, str], Dict[int, List[float]]]:
    """Read and return the data in ALL of the text files that represent different locations in
    Canada. The location of the files is specified by file_path and directory.

    The key of the dictionary is a tuple, with the first element representing the station name and
    the second element representing the province or territory that the station is in.

    The value of the dictionary is another dictionary. The key of this inner dictionary is the year
    and the value of this inner dictionary is a list of all the temperatures for every day of that
    year.

    Preconditions:
        - file_path is in a format that resembles this:
            'C:/Users/Rachel Kim/Documents/University of Toronto/2020-2021
            /CSC110/miscellaneous/Final Project/daily_mean_temps/'
        - directory is in a format that resembles this:
            'C:\\Users\\Rachel Kim\\Documents\\University of Toronto\\2020-2021
            \\CSC110\\miscellaneous\\Final Project\\daily_mean_temps'
    """

    files = os.listdir(directory)

    data_so_far = {}
    for file_name in files:
        f = open(file_path + file_name, 'r')

        # get the station name and the province
        first_line = f.readline()
        first_line_list = str.split(first_line, ',')

        location_key = (str.strip(first_line_list[1], ' '), str.strip(first_line_list[2], ' '))
        years_and_temps = read_daily_mean_temps_one_file(file_path + file_name)
        data_so_far[location_key] = years_and_temps

    return data_so_far


###############################
# Helper Functions
###############################


def read_daily_mean_temps_one_file(filename: str) -> Dict[int, List[float]]:
    """Reads and returns the temperature data as a dictionary in the file called filename. The key
    of this dictionary is the year and the value of this dictionary is a list of all the
    temperatures for every day of that year.

    Preconditions:
        - file_name is a txt file with the same format as 'dm112FN0M.txt'
    """

    f = open(filename)
    lines = f.readlines()

    # get rid of the first four lines of the text file, they are headers for the table
    for _ in range(4):
        list.pop(lines, 0)

    row_data = convert_data_to_list(lines)

    # check that the data contains the appropriate range i.e. from January 1990 to December 2018.
    # If it doesnt, do a early return of an empty dictionary
    if not (row_data[1] and row_data[2]):
        return {}

    data_dictionary = make_data_dictionary(row_data[0])
    new_data = substitute_outliers(data_dictionary)

    return new_data


def convert_data_to_list(lines: List[str]) -> Tuple[List[List[float]], bool, bool]:
    """Return a tuple that contains lines as a nested list, a boolean that represents whether or not
    the start date of the range (January 1990) is in the list, and a boolean that represents whether
    or not the end date of the range (December 2018) is in the range.

    Preconditions:
        - the lines of the list are in the format of a line in 'dm112FN0M.txt'
    """

    contains_data_range_start = False
    contains_data_range_end = False

    data_as_list_so_far = []
    # by the end of this loop, there is a nested list that represents the text data
    for line in lines:
        if 1990 <= int(line[1:5]) <= 2018:
            # replace any character in the alphabet - the only ones that are in the files are the
            # ones below
            line = str.replace(line, 'M', ' ')
            line = str.replace(line, 'E', ' ')
            line = str.replace(line, 'a', ' ')

            # a list of all the numbers in a line of the text
            line_list = [float(num) for num in str.split(line) if num != '\n']
            list.append(data_as_list_so_far, line_list)

            # check that the start and the end of the range of dates is in the list
            if line_list[0] == 1990 and line_list[1] == 1:
                contains_data_range_start = True
            if line_list[0] == 2018 and line_list[1] == 12:
                contains_data_range_end = True

    return (data_as_list_so_far, contains_data_range_start, contains_data_range_end)


def make_data_dictionary(data_as_list: List[List[float]]) -> Dict[int, List[float]]:
    """Return a dictionary that represents data_as_list. The key of the returned dictionary will be
    an int representing the year. The corresponding value will be a list of all the average
    temperatures in that year, in chronological order, starting from January 1.

    Preconditions:
        - 1990 <= row[0] <= 2018
        - 1 <= row[1] <= 12
        - len(row) == 33
    """

    leap_years_since_1990 = [2000, 2004, 2008, 2012, 2016]
    months_with_30_days = [4, 6, 9, 11]

    data_as_dictionary_so_far = {}
    current_year = 1990 - 1
    for row in data_as_list:
        if row[0] != current_year:
            current_year = current_year + 1
            data_as_dictionary_so_far[current_year] = []

        month = row[1]

        # every month has 31 entries in it, regardless of if the month has 31 days.
        # remove the entries for non-existent days (such as April 31)
        if month in months_with_30_days:
            for i in range(2, len(row) - 1):
                list.append(data_as_dictionary_so_far[current_year], row[i])
        elif month == 2 and current_year in leap_years_since_1990:
            for i in range(2, len(row) - 2):
                list.append(data_as_dictionary_so_far[current_year], row[i])
        elif month == 2 and current_year not in leap_years_since_1990:
            for i in range(2, len(row) - 3):
                list.append(data_as_dictionary_so_far[current_year], row[i])
        else:
            for i in range(2, len(row)):
                list.append(data_as_dictionary_so_far[current_year], row[i])

    return data_as_dictionary_so_far


def substitute_outliers(data_as_dictionary: Dict[int, List[float]]) -> Dict[int, List[float]]:
    """Return a new dictionary with the outlier values in data_as_dicionary substituted. The key of
    the returned dictionary will be an int representing the year. The corresponding value will be a
    list of all the average temperatures in that year, in chronological order, starting from January
    1.

    Preconditions:
        - all(1990 <= year <= 2018 for year in data_as_dictionary)
        - the only outlier value is -9999.9
    """

    # make a comprehensive list that includes all the temperatures
    all_temperatures = []
    for year in range(1990, 2019):
        for temperature in data_as_dictionary[year]:
            list.append(all_temperatures, temperature)
        list.append(all_temperatures, 'YEAR CHANGE')

    # determine the indices of all_temperatures at which the outlier values are
    outlier_indices_and_avg_temp = find_outlier_indices(all_temperatures)

    # replace all the indices in the outlier indices with average temp
    replace_outlier_temps(all_temperatures, outlier_indices_and_avg_temp)

    # make the list into a dictionary format again
    new_data = convert_list_to_dictionary(all_temperatures)

    return new_data


def find_outlier_indices(all_temperatures: List[Any]) -> List[Tuple[List[int], float]]:
    """Return a list of tuples given all_temperatures. The first element of the tuple represents the
    list of consecutive indices at which there were outlier temperatures. The second element of the
    tuple represents the average temperature of the nearest non-outlier temperature before and after
    a particular outlier group.

    If the first element of the list is an outlier, take the closest true temperature recorded
    after. If the last element of the list is an outlier, take the closest true temperature recorded
    before.

    Preconditions:
        - the only outlier value is -9999.9
    """

    outlier_indices_and_avg_temp = []
    for temp_index in range(len(all_temperatures)):
        outlier_indices = []
        if all_temperatures[temp_index] == -9999.9:

            # find the first true temperature that comes after the outlier value
            first_true_temperature = -9999.9
            i = temp_index
            while first_true_temperature in (-9999.9, 'YEAR CHANGE') \
                    and i != len(all_temperatures) - 1:
                first_true_temperature = all_temperatures[i]
                list.append(outlier_indices, i)
                i = i + 1

            # find the last true temperature that comes before the outlier value
            last_true_temperature = -9999.9
            j = temp_index - 1
            while last_true_temperature in (-9999.9, 'YEAR CHANGE') and j != 0:
                last_true_temperature = all_temperatures[j]
                list.append(outlier_indices, j)
                j = j - 1

            list.sort(outlier_indices)

            # calculate the average temperature based on where the outlier value was
            if i != len(all_temperatures) - 1 and j != 0:
                average_temperature = (first_true_temperature + last_true_temperature) / 2
            elif i == len(all_temperatures) - 1 and j != 0:
                average_temperature = last_true_temperature
            else:
                average_temperature = first_true_temperature
            list.append(outlier_indices_and_avg_temp, (outlier_indices, average_temperature))

    return outlier_indices_and_avg_temp


def replace_outlier_temps(all_temperatures: List[Any],
                          outlier_indices_and_avg_temp: List[Tuple[List[int], float]]) -> None:
    """Mutate the list so that all the indices in all_temperatures that are outliers are replaced by
    the average temperature found in find_outlier_indices.
    """

    for outlier in outlier_indices_and_avg_temp:
        for index in outlier[0]:
            if all_temperatures[index] != 'YEAR CHANGE':
                all_temperatures[index] = outlier[1]


def convert_list_to_dictionary(all_temperatures: List[Any]) -> Dict[int, List[float]]:
    """Return a dictionary representing the data in all_temperatures. The key of the
    returned dictionary will be an int representing the year. The corresponding value will be a list
    of all the average temperatures in that year, in chronological order, starting from January 1.
    """

    data_as_dictionary_so_far = {}
    i = 0
    for year in range(1990, 2019):
        data_as_dictionary_so_far[year] = []
        while all_temperatures[i] != 'YEAR CHANGE':
            list.append(data_as_dictionary_so_far[year], all_temperatures[i])
            i = i + 1
        # skip over the 'YEAR CHANGE' placeholder in all_temperatures
        i = i + 1
    return data_as_dictionary_so_far


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        # the names (strs) of imported modules
        'extra-imports': ['os', 'csv', 'python_ta', 'python_ta.contracts'],
        # the names (strs) of functions that call print/open/input
        'allowed-io': ['read_ghg_emissions', 'read_daily_mean_temps_all_files',
                       'read_daily_mean_temps_one_file', 'read_ghg_emissions_for_maps',
                       'read_daily_mean_temps_all_files_for_maps'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()
