import gmapsdatalib as gmd
import restaurantManaging as rman
import pandas as pd
import numpy as np

# Function to get the number of ratings from a restaurant
def get_number_of_ratings(restaurant):
    if 'user_ratings_total' in restaurant.keys():
        return restaurant['user_ratings_total']
    else: 
        return -1

# Mean function for using after groupying by geo point
def number_of_ratings_average(nratings):
    n = 0
    sum = 0
    for m in nratings:
        if m >= 0:
            n += 1
            sum += m
    if n <= 0: return 0
    else: return sum/n

# Getting restaurant dictionaries from stored .pkl files
restaurants = gmd.pkl_files_to_list_of_dicts("ids_full_info")

# Filtering to have only restaurants in Barcelona
restaurants = rman.get_restaurants_in_barcelona(restaurants)

# Getting geo points and selections according to this geo points from stored .pkl files
selections, geo_points = rman.get_selections_from_pkl_files("filtering_grid")

# Filtering geo points and selections with postal codes in Barcelona
pcodes_filter = rman.get_barcelona_postalcodes()
df = pd.read_csv("grid_postalcodes.csv")
pcodes = df[df.columns[2]]
pcodes = [str(pc) for pc in pcodes.values]
postal_code_selection = rman.filter_by_postalcode(pcodes, pcodes_filter)
geo_points = list(np.array(geo_points)[postal_code_selection])
selections = list(np.array(selections)[postal_code_selection])

# Computing the average of number of ratings of each restaurant 
# around each geo point (250m aprox) and generating a CSV file
headers = ["latitude","longitude","average_number_of_ratings_of_each_restaurant_around(250m)_this_point"]
values = rman.grid_group_by(restaurants, selections, get_number_of_ratings, number_of_ratings_average)
file_name = "average_number_of_ratings_grid.csv"
rman.geopoints_values_to_csv(geo_points,values,headers=headers,file_name=file_name)