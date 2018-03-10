import pickle
import pandas as pd
import numpy as np
import os
import folium
import json
import geopandas
from branca.colormap import linear
# from altair import *     use for drawing

data = pickle.load(open("ip_log.jpg", "rb"))

ip_list = []
country_list = []
function_list = []
time_list = []
year_list = []
month_list = []

for i in range(len(data)):
    for j in range(len(data[i])):
        if(j%4 == 0):
            ip_list.append(data[i][j])
        elif(j%4 == 1):
            country_list.append(data[i][j])
        elif(j%4 == 2):
            function_list.append(data[i][j])
        elif(j%4 == 3):
            time_list.append(data[i][j])
            year_list.append(data[i][j].year)
            month_list.append(data[i][j].month)
            
df_ip = pd.DataFrame(ip_list, columns=['ip'])
df_country = pd.DataFrame(country_list, columns=['country'])
df_function = pd.DataFrame(function_list, columns=['function'])
df_year = pd.DataFrame(year_list, columns=['year'])
df_month = pd.DataFrame(month_list, columns=['month'])

data_df = pd.concat([df_ip, df_country, df_function, df_year, df_month], axis = 1)
# This is for month rate flow 
data_sort_time_country = data_df.groupby(['country', 'year', 'month'])["ip"].count().reset_index(name="count")
# This is for map drawing
data_sort_country = data_df.groupby(['country'])["ip"].count().reset_index(name="count")

# all the connection
connect_count = 0
for index, row in data_sort_country.iterrows():
    connect_count += row['count']
    
# Na data are added as "Others"
data_sort_country.at[14, 'country'] = 'Others'

# store ratio(%)(numeric) for computing and ratio (string) for showing
data_sort_country['ratio'] = (round(data_sort_country['count'] / connect_count*100, 2)).astype(str) + '%'
data_sort_country['ratio(%)'] = round(data_sort_country['count'] / connect_count*100, 2)
data_sort_country['ratio'] = data_sort_country['ratio'].astype(str)

### Map section
world_json = os.path.join('/Users/Kuan-Hao/Documents/大二下/專題研究-莊曜宇/hw_2', 'custom.geo_high.json')
geo_json_data = json.load(open(world_json))
kw = {'location': [48, -102], 'zoom_start': 3}
gdf = geopandas.read_file(world_json)

# Color scale
colormap = linear.YlGn.scale(0, data_sort_country['ratio(%)'].max())
print(colormap(7.0))
colormap

world_country_df = gdf['name'].to_frame(name = 'country')
merge_map_df = pd.merge(world_country_df, data_sort_country, how = 'left', on = ['country'])
for index, row in merge_map_df.iterrows():
    if(np.isnan(row['ratio(%)'])):
        merge_map_df.at[index, 'ratio(%)'] = 0

# for geojson to find data
ratio_dictionary = merge_map_df.set_index('country')['ratio(%)']
#merge_map_df[~np.isnan(merge_map_df['count'])].sort_values('country')


m = folium.Map(
    [43, -100], 
    zoom_start=4,
    world_copy_jump=True,
    no_wrap=False,)

geojson = folium.GeoJson(
    geo_json_data,
    name = 'ratio of usage',
    highlight_function=lambda feature: {
        'fillColor': colormap(ratio_dictionary[feature['properties']['name']]),
        'color': 'black',
        'weight': 2,
        'fillOpacity': 1.5,
    },
    style_function=lambda feature: {
        'fillColor': colormap(ratio_dictionary[feature['properties']['name']]),
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.7
    }
)
geojson.add_to(m)

# m.choropleth(
#     geo_data=geopandas.read_file(world_json),
# #     data=state_data,
# #     columns=['State', 'Unemployment'],
# #     key_on='feature.id',
#     fill_color='grey',
#     fill_opacity=0.7,
#     line_opacity=0.2,
# #     legend_name='Unemployment Rate (%)',
#     highlight=True
# )

colormap.caption = 'Flow rate color scale'
colormap.add_to(m)
m.save(os.path.join('/Users/Kuan-Hao/Desktop', 'GeoJSON_and_choropleth_3.html'))