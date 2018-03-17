import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import folium
import json
import geopandas
from branca.colormap import linear

def draw_function_pie():
    # Draw the pie chart for each function
    print('Inside pie chart function.')
    function_df = data_df.groupby("function")["ip"].count().reset_index(name="count").set_index("function")
    ax = function_df.plot(subplots=True, kind = "pie",title='function ratio', figsize=(10.3, 10.3))
    fig = ax[0].get_figure()
    fig.savefig(os.path.join(dir_name, 'function_pie.pdf'))
    print('Finish drawing')

def draw_year_month_bar():
    # Draw the bar chart for connection time each month
    print('Inside bar chart function.')
    data_sort_time_country_df = data_df.groupby(['year', 'month'])["ip"].count().reset_index(name="count").sort_values(["year", "month"])
    append_column = []
    for i in range(4):
        append_column.append(str(data_sort_time_country_df["year"][i]) + '/' + str(data_sort_time_country_df["month"][i]))
    data_sort_time_country_df["Year/Month"] = append_column
    year_month_df = data_sort_time_country_df.set_index("Year/Month").drop(columns = ["year", "month"])
    ax = year_month_df.plot(subplots=True, lw=2,kind = "bar",title='connection numbers each month', figsize=(10.3, 10.3))
    # ax.set_xlabel("numbers")
    # ax.set_ylabel("Year/Month")
    fig = ax[0].get_figure()
    fig.savefig(os.path.join(dir_name, 'year_month_bar.pdf'))
    print('Finish drawing')

def draw_map():
    # Draw the map !!
    print('Inside map drawing function.')
    data_sort_country = data_df.groupby(['country'])["ip"].count().reset_index(name="count")
    connect_count = 0
    for index, row in data_sort_country.iterrows():
        connect_count += row['count']
    data_sort_country.at[14, 'country'] = 'Others'
    ## ration for string (for showing), ratio(%) float(precision 2) (for computing)
    data_sort_country['ratio'] = (round(data_sort_country['count'] / connect_count*100, 2)).astype(str) + '%'
    data_sort_country['ratio(%)'] = round(data_sort_country['count'] / connect_count*100, 2)
    data_sort_country['ratio'] = data_sort_country['ratio'].astype(str)

    ## reading the json file( can change to low, medium, high)
    world_json = 'custom.geo_low.json'
    geo_json_data = json.load(open(world_json))
    kw = {'location': [48, -102], 'zoom_start': 3}
    gdf = geopandas.read_file(world_json)

    ## colormapping for the map
    colormap = linear.YlGn.scale(0, data_sort_country['ratio(%)'].max())

    world_country_df = gdf['name'].to_frame(name = 'country')
    merge_map_df = pd.merge(world_country_df, data_sort_country, how = 'left', on = ['country'])

    for index, row in merge_map_df.iterrows():
        if(np.isnan(row['ratio(%)'])):
            merge_map_df.at[index, 'ratio(%)'] = 0

    ratio_dictionary = merge_map_df.set_index('country')['ratio(%)']

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

    # Can change to choropleth
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
    m.save(os.path.join(dir_name, 'map.html'))
    print('Finish drawing')


if __name__ == '__main__':
    print("Remember to put 'ip_log.jpg' and 'custom.geo_low.json' in the current folder!!!!! ")
    print("")
    dir_name = input('Please enter the absolute folder that you want to store data: ')

    data = pickle.load(open("ip_log.jpg", "rb"))
    # Storing data
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
    draw_function_pie()
    draw_year_month_bar()
    draw_map()
