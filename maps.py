"""CSC110 Fall 2020 Final Project, Plotting Maps

Description
===============================
ADD DESCRIPTION

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
import plotly.express as px


PROVINCE_LIST = ['Alberta', 'British Columbia', 'Manitoba', 'New Brunswick',
                 'Newfoundland and Labrador', 'Northwest Territories', 'Nova Scotia', 'Nunavut',
                 'Ontario', 'Prince Edward Island', 'Quebec', 'Saskatchewan', 'Yukon']


def plot_emissions_map(geojson_map_file_name: str, dataframe: dict, province_id_map: dict, year: int) -> None:
    """DOCSTRING"""
    province_borders = json.load(open(geojson_map_file_name, 'r'))
    # dataframe is in alphabetical order because of the way the file is structured
    fig = px.choropleth(dataframe,
                        locations=[province_id_map[province] for province in PROVINCE_LIST],
                        geojson=province_borders,
                        color=year,
                        scope='north america')
    fig.update_geos(fitbounds='geojson', visible=False)
    # fig.show()
    fig.write_image('emissions_map.png', width=1000)


def plot_temperatures_map(geojson_map_file_name: str, dataframe: dict, year: int) -> None:
    """DOCSTRING"""
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
                         center=dict(lon=-96.4835, lat=62.2400))
    fig.update_geos(fitbounds='geojson', visible=True)
    # fig.show()
    fig.write_image('daily_temperatures_map.png', width=1000)


###############################
# Helper Functions
###############################

def format_emissions(geojson_map_file_name: str) -> Dict[int, List[str]]:
    """DOCSTRING"""
    province_borders = json.load(open(geojson_map_file_name, 'r'))
    province_id_map = {}
    for feature in province_borders['features']:
        # creating a dictionary that maps the province name to the id
        province_id_map[feature['properties']['PRENAME']] = feature['id']
    return province_id_map


def format_temps(geojson_stations_file_name: str, json_temp_file_name: str) -> Dict[Any, List[Any]]:
    """DOCSTRING"""
    # keys are ids, coordinates are values
    daily_temps = json.load(open(json_temp_file_name, 'r'))
    weather_stations = json.load(open(geojson_stations_file_name, 'r'))
    weather_station_id_map = {}
    for feature in weather_stations['features']:
        # creating a dictionary that maps the province name to the id
        weather_station_id_map[feature['id']] = feature['geometry']['coordinates']

    # remove all of the stations with an empty dictionary, convert the keys back into tuples
    daily_temps_dict = {eval(key): daily_temps[key] for key in daily_temps
                        if daily_temps[key] != {}}
    daily_temps_dict = {key[0]: {inner_key: sum(daily_temps_dict[key][inner_key]) /
                                            len(daily_temps_dict[key][inner_key])
                                 for inner_key in daily_temps_dict[key]}
                        for key in daily_temps_dict}

    remove_unusable_values(weather_station_id_map, daily_temps_dict)
    formatted_emissions = reformat_daily_temps_data(weather_station_id_map, daily_temps_dict)
    return formatted_emissions


def calculate_emissions_difference(raw_data: Dict[Any, List[float]]) -> Dict[Any, List[float]]:
    """DOCSTRING"""
    difference_dict_so_far = {}
    for year in range(1999, 2019):
        difference_dict_so_far[year] = [raw_data[year][i] - raw_data[1999][i] for i in
                                        range(len(raw_data[1999]))]
    return difference_dict_so_far


def calculate_temperature_difference(raw_data: Dict[Any, List[Any]]) -> Dict[Any, List[Any]]:
    """DOCSTRING"""
    difference_dict_so_far = {'id': raw_data['id'], 'latitudes': raw_data['latitudes'],
                              'longitudes': raw_data['longitudes']}
    for year in range(1999, 2019):
        difference_dict_so_far[year] = [raw_data[year][i] - raw_data[1999][i] for i in
                                        range(len(raw_data[1999]))]
    return difference_dict_so_far


def remove_unusable_values(id_to_coords: Dict[str, List[float]],
                           temp_data: Dict[str, Dict[int, float]]) -> None:
    """DOCSTRING"""
    # after this we will only use the id map!
    keys_to_remove_from_id_to_coords = []
    keys_to_remove_from_temp_data = []

    # collects the station names that are in weather_station_id_map but not in
    # station_ids_in_daily_temps
    for station_id in id_to_coords:
        if station_id not in temp_data:
            list.append(keys_to_remove_from_id_to_coords, station_id)

    # collects the station names that are in daily_temperature_dict but not in
    # weather_station_id_map
    for station_id in temp_data:
        if station_id not in id_to_coords:
            list.append(keys_to_remove_from_temp_data, station_id)

    # remove all the values corresponding to keys that are not in both dictionaries
    for key in keys_to_remove_from_id_to_coords:
        dict.pop(id_to_coords, key)
    for key in keys_to_remove_from_temp_data:
        dict.pop(temp_data, key)


def reformat_daily_temps_data(id_to_coords: Dict[str, List[float]],
                              temp_data: Dict[str, Dict[int, float]]) -> Dict[Any, List[Any]]:
    """DOCSTRING"""
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
