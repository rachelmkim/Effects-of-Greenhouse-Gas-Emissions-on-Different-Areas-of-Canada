"""CSC110 Fall 2020 Final Project, Main

Description
===============================
This module is the graphical user interface that allows the user to access all the components of
our project. To display a map, the interface prompts the user to enter a valid year, which creates
three maps. To display a graph, the user needs to select a station that could be filtered out by
province as well as by the search bar.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of TA's and professors
teaching CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2020 Dana Alshekerchi, Nehchal Kalsi, Rachel Kim, Kathy Lee.
"""

from tkinter import Button, Entry, Label, StringVar, mainloop, Tk, Toplevel
from tkinter import ttk
import json
import ast
from PIL import ImageTk, Image
import data_reading
import combine
import maps

# Creates the main window
ROOT = Tk()

# Opens the image for the title
TITLE_IMAGE = Image.open('title_image.png')
# Resizes the image
SMALLER = TITLE_IMAGE.resize((300, 300), Image.ANTIALIAS)  # (300, 255)
NEW_TITLE = ImageTk.PhotoImage(SMALLER)
# Displays the image as a label
TITLE_LABEL = Label(ROOT, image=NEW_TITLE, borderwidth=0)
TITLE_LABEL.grid(row=1, column=1, columnspan=4)


def window(main) -> None:
    """
    Sets the main window up to be in the middle of
    the screen as well as determines the size of the screen
    """
    main.title('Effects of Greenhouse Gases in Canada')
    main.update_idletasks()
    width = 575
    height = 550
    x = (main.winfo_screenwidth() // 2) - (width // 2)
    y = (main.winfo_screenheight() // 2) - (height // 2)
    main.geometry('{}x{}+{}+{}'.format(width, height, x, y))


# Creates an icon
ROOT.iconbitmap('leaf.ico')

# Background colour
ROOT.config(bg='#FFE4AE')


# From Assignment 2 Part 4
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


# Retrieving data needed

UNFILTERED_DATA = read_temp_data('data.json')
DATA = {x: UNFILTERED_DATA[x] for x in UNFILTERED_DATA if UNFILTERED_DATA[x] != {}}
CITIES = [ast.literal_eval(x)[0] for x in DATA.keys()]
PROVINCE = [ast.literal_eval(x)[1] for x in DATA.keys()]
ABB_TO_PROVINCE = {'BC': 'British Columbia', 'MAN': 'Manitoba', 'ALTA': 'Alberta',
                   'NFLD': 'Newfoundland and Labrador', 'PEI': 'Prince Edward Island',
                   'YT': 'Yukon', 'NB': 'New Brunswick', 'SASK': 'Saskatchewan',
                   'NU': 'Nunavut', 'ONT': 'Ontario', 'NS': 'Nova Scotia',
                   'NWT': 'Northwest Territories', 'QUE': 'Quebec'}


def map_open() -> None:
    """
    Opens three maps on different browsers based on the year inputted when the map button is clicked

    Precondition:
        - 1990 < YEAR_SELECT.get() <= 2018
    """
    # Retrieves data needed from files
    province_geojson_file_name = 'canada_provinces.geojson'
    weather_stations_geojson = 'weather_stations.geojson'
    daily_temps_geojson = 'data_for_maps_since_1990.json'
    emissions_csv_file_name = 'GHG_IPCC_Can_Prov_Terr.csv'

    province_id_map = maps.format_province_id_map(province_geojson_file_name)

    emissions_data_frame = data_reading.read_ghg_emissions_for_maps(emissions_csv_file_name)
    emissions_difference_data_frame = maps.calculate_emissions_difference(emissions_data_frame)
    temperatures_difference_data_frame = maps.calculate_temp_difference(
        maps.format_temps(weather_stations_geojson, daily_temps_geojson))

    # This occurs when the the correct input (a year between 1991-2018)
    try:
        year = int(YEAR_SELECT.get())
        if 1991 <= year <= 2018:
            maps.plot_emissions_map(province_geojson_file_name, 'raw_data', emissions_data_frame,
                                    province_id_map, year)
            maps.plot_emissions_map(province_geojson_file_name,
                                    'difference', emissions_difference_data_frame,
                                    province_id_map, year)
            maps.plot_temperatures_map(province_geojson_file_name, 'difference',
                                       temperatures_difference_data_frame, year)
            # If the year is not between 1991 and 2018
        raise ValueError
    except ValueError:
        YEAR_RANGE_LABEL.config(text='Wrong input. \n Enter year \n(1991 - 2018)',
                                bg='#FFE4AE', fg='#800000')


def province_filter(event) -> None:
    """
    Enables the search button when the province is selected
    Filters out stations, only those in the province chosen appear
    """
    SEARCH_BUTTON['state'] = 'normal'
    cities_in_province = [ast.literal_eval(x)[0] for x in DATA.keys()
                          if ABB_TO_PROVINCE[ast.literal_eval(x)[1]] == PROVINCE_COMBO.get()]
    # Changes the city back to its original format
    sorted_cities = [x.replace('_', ' ').title() for x in cities_in_province]
    sorted_cities.sort()
    CITY_COMBO['values'] = sorted_cities


def selected(event) -> None:
    """
    Opens a new browser with the plotly graph of the station selected
    Graph compares temperature anomaly of station and CO2 emission of the province
    """
    province = ''
    city_chosen = CITY_COMBO.get().upper().replace(' ', '_')
    # Gets the province in which the city is located in
    for item in CITIES:
        if city_chosen == item:
            province = PROVINCE[CITIES.index(item)]
            break
    ghg_data = data_reading.read_ghg_emissions('GHG_IPCC_Can_Prov_Terr.csv')
    key = "('" + city_chosen + "', '" + province + "')"
    combine.combine_plots(ghg_data, DATA[key], ABB_TO_PROVINCE[province], CITY_COMBO.get())


def search() -> None:
    """
    Searches for the station located in the province selected based
    on the characters written in the search entry box
    """
    search_values = CITY_TYPE.get().lower()
    cities_in_province = [ast.literal_eval(x)[0] for x in DATA.keys()
                          if ABB_TO_PROVINCE[ast.literal_eval(x)[1]] == PROVINCE_COMBO.get()]
    if search_values in ('', ' '):
        CITY_COMBO['values'] = [x.replace('_', ' ').title() for x in cities_in_province]
    else:
        display_values = []
        for value in [x.replace('_', ' ').title() for x in cities_in_province]:
            if search_values in value.lower():
                display_values.append(value)
                display_values.sort()
        CITY_COMBO['values'] = display_values


def creators_page() -> None:
    """
    Opens another window which showcases a picture of the creators
    """
    creators_window = Toplevel(ROOT)
    creators_window.title('Creators')
    creators_window.update_idletasks()
    width = 575
    height = 450
    x = (creators_window.winfo_screenwidth() // 2) - (width // 2)
    y = (creators_window.winfo_screenheight() // 2) - (height // 2)
    creators_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    creators_window.iconbitmap('leaf.ico')
    creators_window.config(bg='#FFE4AE')
    introduction_label = Label(creators_window, text='This project was created by...',
                               font=('Helvetica', 10, 'bold'),
                               bg='#FFE4AE', fg='#800000', borderwidth=0)
    introduction_label.grid(row=1, column=1, columnspan=4, pady=(10, 20))
    # Opens the image for the title
    creator_image = Image.open('creator_image.png')
    # Resizes the image
    resized = creator_image.resize((600, 350), Image.ANTIALIAS)
    new_creator = ImageTk.PhotoImage(resized)
    # Displays the image as a label
    creator_label = Label(creators_window, image=new_creator, borderwidth=0)
    creator_label.photo = new_creator
    creator_label.grid(row=2, column=1, columnspan=4)
    why_label = Label(creators_window, text='for the CSC110 Final Project',
                      font=('Helvetica', 10, 'bold'),
                      bg='#FFE4AE', fg='#800000', borderwidth=0)
    why_label.grid(row=3, column=1, columnspan=4, pady=(10, 0))


def instructions_page() -> None:
    """
    Opens a new window on to of the original window to display further instructions as to what
    the user should expect when the buttons are clicked
    """
    instructions_window = Toplevel(ROOT)
    instructions_window.title('Instructions')
    instructions_window.update_idletasks()
    width = 575
    height = 250
    x = (instructions_window.winfo_screenwidth() // 2) - (width // 2)
    y = (instructions_window.winfo_screenheight() // 2) - (height // 2)
    instructions_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    instructions_window.iconbitmap('leaf.ico')
    instructions_window.config(bg='#FFE4AE')
    map_instructions_title = Label(instructions_window, text='Map Instructions',
                                   font=('Helvetica', 10, 'bold', 'underline'),
                                   bg='#FFE4AE',
                                   fg='#800000',
                                   borderwidth=0)
    map_instructions_title.pack()
    map_instructions = Label(instructions_window, text='1. Enter a year between 1991 and 2018.\n'
                                                       ' 2. Upon '
                                                       'clicking Map with a valid year, following '
                                                       'three maps appear, '
                                                       'displaying:\n a. CO2 equivalent of GHG '
                                                       'emissions across '
                                                       'Canada for the given year \n b. '
                                                       'Difference in CO2 equivalent output '
                                                       'across Canada, for the given year '
                                                       'and 1990\n c. Difference in mean '
                                                       'temperatures for each weather station, '
                                                       'for a given year compared to 1990 ',
                             bg='#FFE4AE', fg='#800000', borderwidth=0)
    map_instructions.pack()
    graph_instructions_title = Label(instructions_window, text='Graph Instructions',
                                     font=('Helvetica', 10, 'bold', 'underline'),
                                     bg='#FFE4AE',
                                     fg='#800000',
                                     borderwidth=0)
    graph_instructions_title.pack(pady=(15, 0))
    graph_instructions = Label(instructions_window, text='1. Select a province or territory'
                                                         ' in the Province/Territory dropdown '
                                                         'menu.\n 2. Enter keywords of the '
                                                         'weather station under Search '
                                                         'Station and click Search. \n Select '
                                                         'the station in the Station dropdown '
                                                         'menu.\n '
                                                         '3. Once a weather station selected,'
                                                         ' a graph will display in '
                                                         'your browser.This displays\n the '
                                                         'temperature anomaly and CO2 '
                                                         'equivalent of GHG emissions for\n '
                                                         'your selected weather '
                                                         'station. ',
                               bg='#FFE4AE', fg='#800000', borderwidth=0)
    graph_instructions.pack()


# Labels for all the buttons and entry boxes for user friendliness

# Map Widgets
VIEW_MAP_LABEL = Label(ROOT, text='View Map', font=('Helvetica', 10,
                                                    'bold', 'underline'), bg='#FFE4AE',
                       fg='#800000', borderwidth=0)
VIEW_MAP_LABEL.grid(row=2, column=1, columnspan=4)

YEAR_RANGE_LABEL = Label(ROOT, text='Enter year\n(1991 - 2018)', bg='#FFE4AE', fg='#800000')
YEAR_RANGE_LABEL.grid(row=3, column=2)

YEAR_SELECT = Entry(ROOT, width=7)
YEAR_SELECT.grid(row=4, column=2)

MAP_BUTTON = Button(ROOT, text='Map', command=map_open, bg='#800000', fg='#FFE4AE')
MAP_BUTTON.grid(row=4, column=3, padx=15)

# Graph Widgets

VIEW_GRAPH_LABEL = Label(ROOT, text='View Graph', font=('Helvetica', 10, 'bold',
                                                        'underline'), bg='#FFE4AE', fg='#800000',
                         borderwidth=0)
VIEW_GRAPH_LABEL.grid(row=5, column=1, columnspan=4, pady=(15, 0))

PROVINCE_LABEL = Label(ROOT, text='1. Province/Territory', bg='#FFE4AE', fg='#800000')
PROVINCE_LABEL.grid(row=6, column=1, padx=15)

PROVINCE_OPTIONS = [ABB_TO_PROVINCE[x] for x in ABB_TO_PROVINCE]
PROVINCE_OPTIONS.sort()
PROVINCE_COMBO = ttk.Combobox(ROOT, value=PROVINCE_OPTIONS)
PROVINCE_COMBO.current(0)
PROVINCE_COMBO.bind('<<ComboboxSelected>>', province_filter)
PROVINCE_COMBO.grid(row=7, column=1, padx=15)

SEARCH_LABEL = Label(ROOT, text='2. Station Search', bg='#FFE4AE', fg='#800000')
SEARCH_LABEL.grid(row=6, column=2, padx=15)

CITY_TYPE = StringVar()
SEARCH_TEXT = Entry(ROOT, text=CITY_TYPE)
SEARCH_TEXT.grid(row=7, column=2, padx=15)

SEARCH_BUTTON = Button(ROOT, text='Search', command=search, bg='#800000', fg='#FFE4AE')
SEARCH_BUTTON['state'] = 'disabled'
SEARCH_BUTTON.grid(row=7, column=3, padx=15)

STATION_LABEL = Label(ROOT, text='3. Station', bg='#FFE4AE', fg='#800000')
STATION_LABEL.grid(row=6, column=4, padx=15)

CITY_OPTIONS = [x.replace('_', ' ').title() for x in CITIES]
CITY_OPTIONS.sort()
CITY_COMBO = ttk.Combobox(ROOT, value=[x.replace('_', ' ').title() for x in CITY_OPTIONS])
CITY_COMBO.bind('<<ComboboxSelected>>', selected)
CITY_COMBO.grid(row=7, column=4, padx=15)

INSTRUCTIONS_BUTTON = Button(ROOT, text='Instructions', command=instructions_page,
                             bg='#800000', fg='#FFE4AE')
INSTRUCTIONS_BUTTON.grid(row=8, column=1, pady=(30, 0))

CREATORS_BUTTON = Button(ROOT, text='Creators', command=creators_page, bg='#800000', fg='#FFE4AE')
CREATORS_BUTTON.grid(row=8, column=4, pady=(30, 0))

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
