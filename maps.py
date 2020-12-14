"""CSC110 Fall 2020 Final Project, Maps

Description
===============================
This module plots the maps that serve as a part of the visualization component for our project, and
also includes some helper functions that format the data in a more usable form so that plotly can
read it.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of TA's and professors
teaching CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2020 Dana Alshekerchi, Nehchal Kalsi, Rachel Kim, Kathy Lee.
"""

from typing import Dict, Any, List
import json
import ast
import plotly.express as px

PROVINCE_LIST = ['Alberta', 'British Columbia', 'Manitoba', 'New Brunswick',
                 'Newfoundland and Labrador', 'Northwest Territories', 'Nova Scotia', 'Nunavut',
                 'Ontario', 'Prince Edward Island', 'Quebec', 'Saskatchewan', 'Yukon']


def plot_emissions_map(geojson_map_file_name: str, type_of_map: str, dataframe: dict,
                       province_id_map: dict, year: int) -> None:
    """Plot a map that shows the CO2 equivalent emissions in different provinces and territories in
    Canada.

    geojson_map_file_name a file containing the borders of each of the provinces. The type_of_map
    indicates whether the program is plotting the raw data or if it is plotting the differences. The
    dataframe is the dictionary that is read to plot the map. The province_id_map maps each of the
    provinces and territories in Canada to their id that is specified in the geojson file. The
    function will take data from the year specified.

    Preconditions:
        - geojson_map_file_name is in the form 'canada_provinces.geojson'
        - 1990 < year <= 2018
    """

    province_borders = json.load(open(geojson_map_file_name, 'r'))
    # dataframe is in alphabetical order because of the way the file is structured
    fig = px.choropleth(dataframe,
                        locations=[province_id_map[province] for province in PROVINCE_LIST],
                        geojson=province_borders,
                        color=year,
                        scope='north america',
                        title='CO2 Emissions ' + type_of_map + ' (Units: kilotons)')
    fig.update_geos(fitbounds='geojson', visible=False)
    fig.show()
    # fig.write_image('emissions_map_' + type_of_map + '.png', width=1000)


def plot_temperatures_map(geojson_map_file_name: str, type_of_map: str, dataframe: dict,
                          year: int) -> None:
    """Plot a map that shows the daily mean temperatures in different provinces and territories in
    Canada.

    geojson_map_file_name a file containing the borders of each of the provinces. The type_of_map
    indicates whether the program is plotting the raw data or if it is plotting the differences. The
    dataframe is the dictionary that is read to plot the map. The function will take data from the
    year specified.
    """
    province_borders = json.load(open(geojson_map_file_name, 'r'))
    fig = px.scatter_geo(dataframe,
                         lat='latitudes',
                         lon='longitudes',
                         geojson=province_borders,
                         # locations='id',
                         locationmode='country names',
                         color=year,
                         scope='north america',
                         size_max=100,
                         center=dict(lon=-96.4835, lat=62.2400),
                         title='Daily Mean Temperatures ' + type_of_map + ' (Units: Celsius)')
    fig.update_geos(fitbounds='geojson', visible=True)
    fig.show()
    # fig.write_image('daily_temperatures_map_' + type_of_map + '.png', width=1000)


###############################
# Helper Functions
###############################

def format_province_id_map(geojson_map_file_name: str) -> Dict[str, int]:
    """Return the formatted version of the emissions data given geojson_map_file_name which refers
    to the name of the raw geojson file containing the information about province and territory
    borders. The keys of the returned dictionary will be the name of the province or territory, and
    the values will be the ids associated with each province in geojson_file_name.

    Preconditions:
        - geojson_map_file_name refers to a file in the format 'canada_provinces_geojson'
    """

    province_borders = json.load(open(geojson_map_file_name, 'r'))
    province_id_map = {}
    for feature in province_borders['features']:
        # creating a dictionary that maps the province name to the id
        province_id_map[feature['properties']['PRENAME']] = feature['id']
    return province_id_map


def format_temps(geojson_stations_file_name: str, json_temp_file_name: str) -> Dict[Any, List[Any]]:
    """Return the formatted version of the daily temperatures data given geojson_stations_file_name,
    containing the information on the geographical locations of each of the weather stations, and
    json_temp_file_name, containing the information about the daily mean temperatures at each of the
    weather stations.

    The keys of the returned dictionary will be the years in which the data was recorded as well as
    'id', 'latitudes', and 'longitudes'. The values will be the average annual temperatures recorded
    at each station, along with the order of the stations (as represented by the list for 'id') and
    the latitude and longitude coordinates for that station.

    Preconditions:
        - geojson_stations_file_name is in the format of 'weather_stations.geojson'
        - json_temp_file_name is in the format of 'INSERT NAME!!!!!'
    """

    daily_temps = json.load(open(json_temp_file_name, 'r'))
    weather_stations = json.load(open(geojson_stations_file_name, 'r'))
    # keys are ids, coordinates are values
    weather_station_id_map = {}
    for feature in weather_stations['features']:
        # creating a dictionary that maps the province name to the id
        weather_station_id_map[feature['id']] = feature['geometry']['coordinates']

    # remove all of the stations with an empty dictionary, convert the keys back into tuples
    daily_temps_dict = {ast.literal_eval(key): daily_temps[key] for key in daily_temps
                        if daily_temps[key] != {}}
    daily_temps_dict = {key[0]: {
        inner_key: sum(daily_temps_dict[key][inner_key]) / len(daily_temps_dict[key][inner_key]) for
        inner_key in daily_temps_dict[key]} for key in daily_temps_dict}

    remove_unusable_values(weather_station_id_map, daily_temps_dict)
    formatted_emissions = reformat_daily_temps_data(weather_station_id_map, daily_temps_dict)
    return formatted_emissions


def calculate_emissions_difference(raw_data: Dict[int, List[float]]) -> Dict[Any, List[float]]:
    """Return a dictionary containing the difference between emissions in each year from 1990 to
    2018 compared to 1990 given raw_data. The keys of the returned dictionary will be the same as
    the keys of raw_data; the list associated with each year will be the difference in mean
    temperatures between the year and 1990.

    Preconditions:
        - all(year in raw_data for year in range(1990, 2019))
        - all(len(raw_data[year]) == len(raw_data[1990]) for year in range(1990, 2019))
    """

    difference_dict_so_far = {}
    for year in range(1990, 2019):
        difference_dict_so_far[year] = [raw_data[year][i] - raw_data[1990][i] for i in
                                        range(len(raw_data[1990]))]
    return difference_dict_so_far


def calculate_temp_difference(raw_data: Dict[Any, List[Any]]) -> Dict[Any, List[Any]]:
    """Return a dictionary containing the difference between daily mean temperatures in each year
    from 1990 to 2018 compared to 1990 given raw_data. The keys of the returned dictionary will be
    the same as the keys of raw_data; the list associated with each year will be the difference in
    mean temperatures between the year and 1990. The values associated with 'id', 'latitudes', and
    'longitudes' will remain the same.

    Preconditions:
        - all(year in raw_data for year in range(1990, 2019))
        - all(len(raw_data[key]) == len(raw_data[1990]) for key in raw_data)
    """

    difference_dict_so_far = {'id': raw_data['id'], 'latitudes': raw_data['latitudes'],
                              'longitudes': raw_data['longitudes']}
    for year in range(1990, 2019):
        difference_dict_so_far[year] = [raw_data[year][i] - raw_data[1990][i] for i in
                                        range(len(raw_data[1990]))]
    return difference_dict_so_far


def remove_unusable_values(id_to_coords: Dict[str, List[float]],
                           temp_data: Dict[str, Dict[str, float]]) -> None:
    """Remove the key and the value associated to it in both id_to_coords and temp_data that are
    not in both dictionaries.

    Preconditions:
        - all(len(id_to_coords[key]) == 2 for key in id_to_coords)
        - the keys of both dictionaries must be the weather station ids
    """

    keys_to_remove_id_to_coords = []
    keys_to_remove_temp_data = []

    # collects the station names that are in weather_station_id_map but not in
    # station_ids_in_daily_temps
    for station_id in id_to_coords:
        if station_id not in temp_data:
            list.append(keys_to_remove_id_to_coords, station_id)

    # collects the station names that are in daily_temperature_dict but not in
    # weather_station_id_map
    for station_id in temp_data:
        if station_id not in id_to_coords:
            list.append(keys_to_remove_temp_data, station_id)

    # remove all the values corresponding to keys that are not in both dictionaries
    for key in keys_to_remove_id_to_coords:
        dict.pop(id_to_coords, key)
    for key in keys_to_remove_temp_data:
        dict.pop(temp_data, key)


def reformat_daily_temps_data(id_to_coords: Dict[str, List[float]],
                              temp_data: Dict[str, Dict[str, float]]) -> Dict[Any, List[Any]]:
    """Return the formatted version of the daily temperatures data given id_to_coords and temp_data.
    The keys of the new dictionary will contain the years between 1990 and 2018 inclusive, as well
    as 'id', 'latitudes', and 'longitudes'. The values will be the average annual temperatures
    recorded at each station, along with the order of the stations (as represented by the list for
    'id') and the latitude and longitude coordinates for that station.

    Preconditions:
        - all(len(id_to_coords[key]) == 2 for key in id_to_coords)
        - the keys of both dictionaries must be the weather station ids
    """
    reformatted_dict_so_far = {'id': [], 'latitudes': [], 'longitudes': []}
    for station_id in id_to_coords:
        list.append(reformatted_dict_so_far['id'], station_id)
        list.append(reformatted_dict_so_far['latitudes'], id_to_coords[station_id][1])
        list.append(reformatted_dict_so_far['longitudes'], id_to_coords[station_id][0])
        for year in temp_data[station_id]:  # inner keys are years
            if int(year) not in reformatted_dict_so_far:
                reformatted_dict_so_far[int(year)] = []
            list.append(reformatted_dict_so_far[int(year)], temp_data[station_id][year])
    return reformatted_dict_so_far


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        # the names (strs) of imported modules
        'extra-imports': ['json', 'plotly.express', 'python_ta', 'python_ta.contracts', 'ast'],
        # the names (strs) of functions that call print/open/input
        'allowed-io': ['plot_emissions_map', 'plot_temperatures_map', 'format_province_id_map',
                       'format_temps'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()
