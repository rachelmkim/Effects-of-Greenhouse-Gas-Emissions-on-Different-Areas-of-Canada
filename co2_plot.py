"""CSC110 Fall 2020 Final Project, Plotting Carbon Dioxide Emissions

Description
===============================
This module uses the input data to plot carbon dioxide emissions.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of TA's and professors
teaching CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2020 Dana Alshekerchi, Nehchal Kalsi, Rachel Kim, Kathy Lee.
"""
from typing import List, Any
import plotly.graph_objects as go

from plotly.subplots import make_subplots
import data_reading

# you can use this for testing
ghg_data = data_reading.read_ghg_emissions('GHG_IPCC_Can_Prov_Terr.csv')


def plot_co2_emissions(given_data: List[List[Any]], province: str) -> None:
    """Plot carbon dioxide emissions for the given province.

    Preconditions:
        - province in [x[1] for x in given_data]
    """
    data = province_sort(given_data, province)

    years = list(range(data[0][0], data[-1][0] + 1))
    values = [x[2] for x in data]

    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Scatter(x=years, y=values,
                             mode='lines+markers',
                             name='CO2'),
                  row=1, col=1)
    fig.update_layout(title=f'{province} CO2 Emissions from '
                            f'{data[0][0]} to {data[-1][0]}', xaxis_title='Years')
    fig.show()


# def plot_all_provinces(given_data: List[List[Any]]) -> None:
#     """sdfklj"""
#     provinces = list(set([x[1] for x in given_data]))
#     fig = make_subplots(rows=len(provinces), cols=1)
#
#     for i in provinces:
#         # plot_co2_emissions(given_data, i)
#
#         data = province_sort(given_data, i)
#
#         years = list(range(data[0][0], data[-1][0] + 1))
#         values = [x[2] for x in data]
#
#         fig.add_trace(go.Scatter(x=years, y=values,
#                                  mode='lines+markers',
#                                  name='CO2'),
#                       row=provinces.index(i) + 1, col=1)
#
#     fig.update_layout(title='CO2 Emissions', xaxis_title='Years')
#     fig.show()


###############################
# Helper Functions
###############################


def province_sort(given_data: List[List[Any]], province: str) -> List[List[Any]]:
    """
    Return a list of all the lists relevant to the province.

    Precondition:
        - province in [x[1] for x in given_data]
    """
    new_data = [x for x in given_data if x[1] == province]
    return new_data


def stuff_that_we_require(given_data: List[List[Any]], province: str) -> List[List[Any]]:
    """
    dfs
    """
    data = province_sort(given_data, province)

    years = list(range(data[0][0], data[-1][0] + 1))
    values = [x[2] for x in data]
    return [years, values]


if __name__ == '__main__':
    # import python_ta
    #
    # python_ta.check_all(config={
    #     # the names (strs) of imported modules
    #     'extra-imports': ['os', 'csv', 'python_ta', 'python_ta.contracts'],
    #     # the names (strs) of functions that call print/open/input
    #     'allowed-io': ['read_ghg_emissions', 'read_daily_mean_temps_all_files',
    #                    'read_daily_mean_temps_one_file'],
    #     'max-line-length': 100,
    #     'disable': ['R1705', 'C0200']
    # })
    #
    # import python_ta.contracts
    #
    # python_ta.contracts.DEBUG_CONTRACTS = False
    # python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()
