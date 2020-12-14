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

from tkinter import Button, Entry, Label, StringVar, mainloop, Tk
from tkinter import ttk
import json
import ast
from PIL import ImageTk, Image
import data_reading
import combine
import maps

ROOT = Tk()


def read_temp_data(file: str) -> dict:
    """Return a dictionary mapping course codes to course data from the data in the given file.

    In the returned dictionary:
        - each key is a string representing the course code
        - each corresponding value is a tuple representing a course value, in the format
          descried in Part 3 of the assignment handout.

    Note that the implementation of this function provided to you is INCOMPLETE since it just
    returns a dictionary in the same format as the raw JSON file. It's your job to implement
    the functions below, and then modify this function body to get the returned data
    in the right format.

    Preconditions:
        - file is the path to a JSON file containing course data using the same format as
          the data in data/course_data_small.json.
    file is the name (or path) of a JSON file containing course data using the format in
    the sample file course_data_small.json.
    """
    with open(file) as json_file:
        data_input = json.load(json_file)
    return data_input


# Map
PROVINCE_GEOJSON_FILE_NAME = 'canada_provinces.geojson'
WEATHER_STATIONS_GEOJSON_FILE_NAME = 'weather_stations.geojson'
DAILY_TEMPS_GEOJSON_FILE_NAME = 'data_for_maps_since_1990.json'
EMISSIONS_CSV_FILE_NAME = 'GHG_IPCC_Can_Prov_Terr.csv'

PROVINCE_ID_MAP = maps.format_province_id_map(PROVINCE_GEOJSON_FILE_NAME)

EMISSIONS_DATA_FRAME = data_reading.read_ghg_emissions_for_maps(EMISSIONS_CSV_FILE_NAME)
EMISSIONS_DIFFERENCE_DATA_FRAME = maps.calculate_emissions_difference(EMISSIONS_DATA_FRAME)
TEMPERATURES_DIFFERENCE_DATA_FRAME = maps.calculate_temp_difference(
    maps.format_temps(WEATHER_STATIONS_GEOJSON_FILE_NAME, DAILY_TEMPS_GEOJSON_FILE_NAME)
)


def map_open() -> None:
    """
    Opens
    """
    try:
        year = int(YEAR_SELECT.get())
        if 1991 <= year <= 2018:
            maps.plot_emissions_map(PROVINCE_GEOJSON_FILE_NAME, 'raw_data', EMISSIONS_DATA_FRAME,
                                    PROVINCE_ID_MAP, year)
            maps.plot_emissions_map(PROVINCE_GEOJSON_FILE_NAME,
                                    'difference', EMISSIONS_DIFFERENCE_DATA_FRAME,
                                    PROVINCE_ID_MAP, year)
            maps.plot_temperatures_map(PROVINCE_GEOJSON_FILE_NAME, 'difference',
                                       TEMPERATURES_DIFFERENCE_DATA_FRAME, year)
        raise ValueError
    except ValueError:
        YEAR_RANGE_LABEL.config(text='Wrong input. \n Please input a year \nbetween 1991 to 2018')


MAP_BUTTON = Button(ROOT, text='Map', command=map_open)
MAP_BUTTON.grid(row=5, column=3, padx=15)

YEAR_SELECT = Entry(ROOT, width=7)
YEAR_SELECT.grid(row=5, column=2)

YEAR_RANGE_LABEL = Label(ROOT, text='Input year \nbetween 1991 to 2018', bg='#FFE4AE')
YEAR_RANGE_LABEL.grid(row=4, column=2)

# Opens the image
TITLE_IMAGE = Image.open("TITLE_IMAGE.png")
# Resizes the image
SMALLER = TITLE_IMAGE.resize((300, 300), Image.ANTIALIAS)  # (300, 255)
NEW_TITLE = ImageTk.PhotoImage(SMALLER)
# Displays the image as a label
TITLE_LABEL = Label(ROOT, image=NEW_TITLE, borderwidth=0)
TITLE_LABEL.grid(row=1, column=1, columnspan=12)

# Labels for everything
PROVINCE_LABEL = Label(ROOT, text='Province', bg='#FFE4AE')
PROVINCE_LABEL.grid(row=4, column=4, padx=15)

STATION_LABEL = Label(ROOT, text='Station', bg='#FFE4AE')
STATION_LABEL.grid(row=4, column=7, padx=15)

SEARCH_LABEL = Label(ROOT, text='Station Search', bg='#FFE4AE')
SEARCH_LABEL.grid(row=4, column=5, padx=15)


def window(main) -> None:
    """
    This function sets the main window up to be in the middle of
    the screen as well as determines the size of the screen
    """
    main.title('Effects of Greenhouse Gases in Canada')
    main.update_idletasks()
    width = 750
    height = 450
    x = (main.winfo_screenwidth() // 2) - (width // 2)
    y = (main.winfo_screenheight() // 2) - (height // 2)
    main.geometry('{}x{}+{}+{}'.format(width, height, x, y))


# Background colour
ROOT.config(bg='#FFE4AE')

DIRTY_DATA = read_temp_data('data.json')
DATA = {x: DIRTY_DATA[x] for x in DIRTY_DATA if DIRTY_DATA[x] != {}}
CITIES = [ast.literal_eval(x)[0] for x in DATA.keys()]
PROVINCE = [ast.literal_eval(x)[1] for x in DATA.keys()]
ABB_TO_PROVINCE = {'BC': 'British Columbia', 'MAN': 'Manitoba', 'ALTA': 'Alberta',
                   'NFLD': 'Newfoundland and Labrador', 'PEI': 'Prince Edward Island',
                   'YT': 'Yukon', 'NB': 'New Brunswick', 'SASK': 'Saskatchewan',
                   'NU': 'Nunavut', 'ONT': 'Ontario', 'NS': 'Nova Scotia',
                   'NWT': 'Northwest Territories', 'QUE': 'Quebec'}


def province_filter(event) -> None:
    """
    idk
    """
    SEARCH_BUTTON['state'] = 'normal'
    cities_in_province = [ast.literal_eval(x)[0] for x in DATA.keys()
                          if ABB_TO_PROVINCE[ast.literal_eval(x)[1]] == PROVINCE_DROP.get()]
    CITY_COMBO['values'] = [x.replace('_', ' ').title() for x in cities_in_province]


# Province combobox
PROVINCE_OPTIONS = [ABB_TO_PROVINCE[x] for x in ABB_TO_PROVINCE]
PROVINCE_DROP = ttk.Combobox(ROOT, value=PROVINCE_OPTIONS)
PROVINCE_DROP.current(0)
PROVINCE_DROP.bind("<<ComboboxSelected>>", province_filter)
PROVINCE_DROP.grid(row=5, column=4)


def selected(event) -> None:
    """
    Opens a new browser with the plotly graph
    """
    province = ''
    city_choosen = CITY_COMBO.get().upper().replace(" ", "_")
    # Gets the province in which the city is located in
    for item in CITIES:
        if city_choosen == item:
            province = PROVINCE[CITIES.index(item)]
            break
    ghg_data = data_reading.read_ghg_emissions('GHG_IPCC_Can_Prov_Terr.csv')
    key = "('" + city_choosen + "', '" + province + "')"
    combine.combine_plots(ghg_data, DATA[key], ABB_TO_PROVINCE[province])


def search() -> None:
    """
    Searches for the city needed
    """
    search_values = CITY_TYPE.get().lower()
    cities_in_province = [ast.literal_eval(x)[0] for x in DATA.keys()
                          if ABB_TO_PROVINCE[ast.literal_eval(x)[1]] == PROVINCE_DROP.get()]
    if search_values in ('', ' '):
        CITY_COMBO['values'] = [x.replace('_', ' ').title() for x in cities_in_province]
    else:
        display_values = []
        for value in [x.replace('_', ' ').title() for x in cities_in_province]:
            if search_values in value.lower():
                display_values.append(value)
        CITY_COMBO['values'] = display_values


CITY_OPTIONS = CITIES
# CITY_OPTIONS = [x[0] for x in test.keys() if x[1] == PROVINCE_DROP.get()]

CITY_COMBO = ttk.Combobox(ROOT, value=[x.replace('_', ' ').title() for x in CITY_OPTIONS])
CITY_COMBO.bind('<<ComboboxSelected>>', selected)
CITY_COMBO.grid(row=5, column=7, padx=15)

CITY_TYPE = StringVar()
SEARCH_TEXT = Entry(ROOT, text=CITY_TYPE)
SEARCH_TEXT.grid(row=5, column=5, padx=15)

SEARCH_BUTTON = Button(ROOT, text="Search", command=search)
SEARCH_BUTTON['state'] = 'disabled'
SEARCH_BUTTON.grid(row=5, column=6, padx=15)

window(ROOT)
mainloop()

if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        # the names (strs) of imported modules
        'extra-imports': ['tkinter', 'json', 'python_ta', 'python_ta.contracts',
                          'ast', 'PIL', 'data_reading', 'combine', 'maps'],
        # the names (strs) of functions that call print/open/input
        'allowed-io': ['read_temp_data'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()
