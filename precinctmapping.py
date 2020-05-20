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


class Chloropleth(object):
    """
    Make Chloropleth maps to help visualize demographic/electoral data by precinct.
    Creates interactive figures using bokeh in Jupyter Notebooks, hoverable to see exact data values for each precinct

    Parameters:
    --json_data (JSON-formatted str): input data, consisting of merged geopandas shapefile data
        and pandas input data
    --varname (str): Name of the column in the input data that you want to map
    --palette (bokeh palette): Color scheme for the map. Great tool for picking palettes is here -
        https://colorbrewer2.org/#type=sequential&scheme=BuGn&n=3
    --figtitle (str): What you want the displayed title of the map to be
    --mapscale (tuple): Tuple in the form (min,max) where min, max are the highest and lowest data values
        scaled to the color palette

    Functions:
        create(): builds the map and displays it using bokeh in a Jupyter notebook
    """
    def __init__(self, json_data, varname, figtitle, palette, mapscale): #eg. palette = brewer['YlGnBu'][8][::-1]
        self.json_data = json_data
        self.varname = varname
        self.palette = palette
        self.figtitle = figtitle
        self.mapscale = mapscale

    def create(self):
        # Input GeoJSON source that contains features for plotting.
        geosource = GeoJSONDataSource(geojson=self.json_data)
        # Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
        color_mapper = LinearColorMapper(palette=self.palette, low=self.mapscale[0], high=self.mapscale[1],nan_color = '#d9d9d9')
        tick_labels = {str(self.mapscale[0]): '<' + str(self.mapscale[0]), str(self.mapscale[1]):'>' + str(self.mapscale[1])}
        color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8, width=int(400*1.5), height=20,
                                 border_line_color=None, location=(0, 0), orientation='horizontal',major_label_overrides=tick_labels)
        # Add hover tool
        hover = HoverTool(tooltips=[('County', '@CNTY'), ('Precinct', '@Precinct'),(self.varname,'@'+self.varname)])
        # Create figure object.
        p = figure(title=self.figtitle, plot_height=int(600*1.5), plot_width=int(500*1.5),
                   toolbar_location=None, tools=[hover])
        p.xgrid.grid_line_color = None
        p.ygrid.grid_line_color = None

        # Add patch renderer to figure.
        p.patches('xs', 'ys', source=geosource, fill_color={'field': self.varname , 'transform': color_mapper},
                  line_color='black', line_width=0.25, fill_alpha=1)
        # Specify figure layout.
        p.add_layout(color_bar, 'below')
        # Display figure inline in Jupyter Notebook.
        output_notebook()
        # Display figure.
        show(p)


