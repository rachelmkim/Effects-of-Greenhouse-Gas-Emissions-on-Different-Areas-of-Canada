import data_reading
import maps

PROVINCE_GEOJSON_FILE_NAME = 'canada_provinces.geojson'
WEATHER_STATIONS_GEOJSON_FILE_NAME = 'weather_stations.geojson'
DAILY_TEMPS_GEOJSON_FILE_NAME = 'data_for_maps_since_1990.json'
EMISSIONS_CSV_FILE_NAME = 'GHG_IPCC_Can_Prov_Terr.csv'

province_id_map = maps.format_province_id_map(PROVINCE_GEOJSON_FILE_NAME)

emissions_data_frame = data_reading.read_ghg_emissions_for_maps(EMISSIONS_CSV_FILE_NAME)
emissions_difference_data_frame = maps.calculate_emissions_difference(emissions_data_frame)
temperatures_difference_data_frame = maps.calculate_temp_difference(
    maps.format_temps(WEATHER_STATIONS_GEOJSON_FILE_NAME, DAILY_TEMPS_GEOJSON_FILE_NAME)
)

year = int(input('Enter a year between 1991 and 2018: '))

maps.plot_emissions_map(PROVINCE_GEOJSON_FILE_NAME, 'raw_data', emissions_data_frame,
                        province_id_map, year)
maps.plot_emissions_map(PROVINCE_GEOJSON_FILE_NAME, 'difference', emissions_difference_data_frame,
                        province_id_map, year)
maps.plot_temperatures_map(PROVINCE_GEOJSON_FILE_NAME, 'difference',
                           temperatures_difference_data_frame, year)
