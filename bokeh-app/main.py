import gspread
from oauth2client.service_account import ServiceAccountCredentials

import geopandas as gpd
import pandas as pd
import numpy as np
from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.transform import factor_cmap
from bokeh.palettes import brewer, Spectral6
import json
from bokeh.io import curdoc, output_notebook
from bokeh.models import Slider, HoverTool
from bokeh.layouts import widgetbox, row, column
from bokeh.io import export_png
from precinctmapping import Chloropleth

#This shapefile contains all Texas election precincts, not just TX31
shapefile = 'texasprecincts/Precincts.shp'
# Read shapefile using Geopandas
gdf = gpd.read_file(shapefile)
gdf = gdf[gdf['CNTY'].isin(['27', '491'])] #Filters for Bell and Williamson Counties, which make up TX31

#connect to the google sheet
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open("TX 31 Precinct Tracker ")
# Extract and print all of the values
worksheets = sheet.worksheets()
worksheets = [w.title for w in worksheets]
worksheets.remove('Template')

datafile = pd.DataFrame({'Precinct': worksheets, 'Turf Cut':[1 for i in range(len(worksheets))]})


#I think at one point the precinct column was giving me trouble so I put this here, it may or may not be necessary
for i in range(len(datafile)):
    datafile['Precinct'].iloc[i] = str(datafile['Precinct'].iloc[i])
    if len(datafile['Precinct'].iloc[i]) == 3:
        datafile['Precinct'].iloc[i] = '0' + datafile['Precinct'].iloc[i]
print(datafile.head())

#merge geodata and data, convert to json
merged = gdf.merge(datafile, 'left', left_on='PREC', right_on='Precinct')
#print(merged.head)
merged_json = json.loads(merged.to_json())
jsondata = json.dumps(merged_json)
mapscale = (0,datafile['Turf Cut'].max())
print(mapscale)

#Instantiate Chloropleth object and create map
my_map = Chloropleth(json_data = jsondata, 
                     varname = 'Turf Cut',
                     figtitle = 'TX31 Precincts with Turfs Cut', 
                     palette = brewer['Spectral'][5][::-1],
                     mapscale = mapscale)
my_map.create(qualitative=True)
