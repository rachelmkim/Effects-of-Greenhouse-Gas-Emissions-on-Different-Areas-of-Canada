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
from typing import List, Any, Dict
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def combine_plots(gas_data: List[List[Any]], temp_data: Dict[str, List[float]], province: str) -> None:
    """
    Return a combined plot for carbon dioxide data and temperature data for the given province.

    The plot opens in a browser window.
    Carbon dioxide uses the primary y-axis and temperature uses the secondary y-axis.
    """
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    co2_return = values_for_co2_plot(gas_data, province)

    fig.add_trace(go.Scatter(x=co2_return[0], y=co2_return[1],
                             mode='lines+markers',
                             name='CO2', line=dict(color="#0E9CB3")),
                  secondary_y=False,
                  row=1, col=1)

    temp_return = values_for_temp_plot(temp_data)

    fig.add_trace(go.Scatter(x=temp_return[0], y=temp_return[1],
                             mode='lines+markers',
                             name='Temperatures', line=dict(color="#800000")),
                  secondary_y=True,
                  row=1, col=1)

    # set up axes names and title
    fig.update_layout(title_text=f"Carbon dioxide levels and anomaly temperatures for {province}",
                      paper_bgcolor='#FFE4AE',  # same colors
                      plot_bgcolor='rgb(255,228,174)'
                      )
    fig.update_xaxes(title_text="Years")
    fig.update_yaxes(title_text="Carbon dioxide levels", secondary_y=False)
    fig.update_yaxes(title_text="Temperatures in Celsius", secondary_y=True)
    fig.show()


###############################
# Helper Functions
###############################


def province_sort(given_data: List[List[Any]], province: str) -> List[List[Any]]:
    """
    Return a filtered list of all the lists that contain the province name.

    Precondition:
        - province in [x[1] for x in given_data]
    """
    new_data = [x for x in given_data if x[1] == province]
    return new_data


def values_for_co2_plot(given_data: List[List[Any]], province: str) -> List[List[Any]]:
    """
    Return the values required to plot carbon dioxide data.
    """
    data = province_sort(given_data, province)

    years = list(range(data[0][0], data[-1][0] + 1))
    values = [x[2] for x in data]
    return [years, values]


def temp_anomaly(temp_data: Dict[str, List[float]]) -> List[List[Any]]:
    """Transform the given temp_data into a list of years and calculated temperature anomaly.

    The returned list consists of lists of the year and its associated temperature anomaly.

    Preconditions:
        - temp_data != {}
        - temp_data is a dictionary with years as keys and list of daily temperatures for that year,
         in the returned format from data_reading.read_daily_mean_temps_one_file()
    """
    new_data = []
    for year in temp_data:
        total = 0
        for temp in temp_data[year]:
            total += temp
        average = total / len(temp_data[year])
        new_data.append([year, average])

    av = 0
    for day in new_data:
        av += day[1]
    av = av / len(new_data)

    for day in new_data:
        day[1] = day[1] - av

    return new_data


def values_for_temp_plot(temp_data: Dict[str, List[float]]) -> List[List[Any]]:
    """
    Return the values required to plot temperature data.
    """
    data = temp_anomaly(temp_data)

    years = list(range(int(data[0][0]), int(data[-1][0]) + 1))
    temps = [x[1] for x in data]
    return [years, temps]


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
