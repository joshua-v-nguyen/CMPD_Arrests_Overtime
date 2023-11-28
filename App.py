import geopandas as gpd
import pandas as pd
import streamlit as st

canopy_shp = gpd.read_file('Tree_Canopy-polygon.shp')
