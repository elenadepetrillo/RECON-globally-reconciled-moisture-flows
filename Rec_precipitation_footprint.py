# Script to retrieve and plot the reconciled moisture flow of precipiation from evaporation from target to source based on NetCDF moisture flow data (Recon_Diati).

#Created by Elena De Petrillo (elena.depetrillo@polito.it) & Luca Monaco (luca.monaco@polito.it)

# Released 11 November 2024

# Required Libraries
import numpy as np
import xarray as xr
import pandas as pd
import netCDF4 as nc
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy.ma as ma
import geopandas as gpd
from shapely.geometry import box

# Input Configuration - Change paths according to your directory structure
input_file = "/DiatiTrack_0.5_AVERAGE_final.nc"

# Constants for calculation
ymax = 122079329.40990189  # Maximum moisture flow value
ymin = 10**-3  # Minimum moisture flow value

# Load dataset
dataset = xr.open_dataset(input_file)


lats = np.arange(90, -90, -0.5)
lons = np.arange(0, 360, 0.5)


# Helper function to get the closest index for a given latitude/longitude
def get_closest_index(lat_array, target_lat):
    """
    Find the index in `lat_array` closest to `target_lat`.
    
    Parameters:
        lat_array (np.array): Array of latitude values to search within.
        target_lat (float): Target latitude value.
    
    Returns:
        int: Index of the closest latitude in `lat_array`.
    """
    import operator
    lat_index, min_value = min(enumerate(abs(lat_array - target_lat)), key=operator.itemgetter(1))
    return lat_index

# Function to calculate footprint moisture flow volume at a specific location
def get_footprints(latitude, longitude):
    """
    Calculate the moisture flow footprint at a specified latitude and longitude.
    
    Parameters:
        latitude (float): Latitude of the point to analyze.
        longitude (float): Longitude of the point to analyze.
    
    Returns:
        np.array: Moisture flow footprint volume for the specified location.
    """
    # Find closest grid cell indices for latitude and longitude
    latidx = get_closest_index(lats, latitude)
    lonidx = get_closest_index(lons, longitude)

    # Retrieve the moisture flow (cubic meters) associated to the precipitation footprint for the specified target cell
    flow = dataset.variables['moisture_flow'][:, :, latidx, lonidx]

    # Calculate moisture flow volume using a scaling transformation
    flow_volume = np.where(
        flow == 0,
        0,
        10**(((flow - 1) / 254) * (np.log10(ymax) - np.log10(ymin)) + np.log10(ymin))
    )
    
    return flow_volume

# Example usage with specific latitude and longitude values of the source cell
# Modify these coordinates to analyze different points.
lon = 7.7
lat = 45.1

# Initialize the footprint array and compute footprint for the specified location
precipitation_footprint = np.zeros((360, 720))
precipitation_footprint = get_footprints(lat, lon)

# Optional: Plotting results (customize as needed)
plt.figure(figsize=(10, 6))
plt.imshow(precipitation_footprint, extent=[lons.min(), lons.max(), lats.min(), lats.max()])
plt.colorbar(label="Moisture Flow Volume [m$^3$]")
plt.title(f"Origin of Precipiation for Location (Lat: {lat}, Lon: {lon})")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()
