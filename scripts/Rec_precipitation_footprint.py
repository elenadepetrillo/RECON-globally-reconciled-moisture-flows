# Created by Elena De Petrillo (elena.depetrillo@polito.it) & Luca Monaco (luca.monaco@polito.it)

# Script to retrieve and plot the reconciled moisture flow of precipitation from evaporation 
# from target to source based on NetCDF moisture flow data (RECON).  

# Required Libraries
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

# Input Configuration - Change paths according to your directory structure
input_file = "/RECON_moisture_flows_0.5.nc"

# Constants for calculation
ymax = 122079329.40990189  # Maximum moisture flow value
ymin = 10**-3  # Minimum moisture flow value

# Load dataset
dataset = xr.open_dataset(input_file)

# Example usage with specific latitude and longitude values of the target cell
# i.e. Set a precipitation point coordinates, get where that point-wise moisture evapotranspirates from globally
# Modify these coordinates to analyze different points.
lon = 7.7
lat = 45.1

# Get precipitation field, which must be converted to m**3
evapotranspiration_sheds = dataset["moisture_flow"].sel(targetlat=lat, targetlon=lon,method="nearest").values
# Convert to m**3
evapotranspiration_sheds = np.where(
        evapotranspiration_sheds== 0,
        0,
        10**(((evapotranspiration_sheds- 1) / 254) * (np.log10(ymax) - np.log10(ymin)) + np.log10(ymin))
    )

# Optional: Plotting results (customize as needed)
lats = np.arange(90, -90, -0.5)
lons = np.arange(0, 360, 0.5)
plt.figure(figsize=(10, 6))
plt.imshow(evapotranspiration_sheds, extent=[lons.min(), lons.max(), lats.min(), lats.max()])
plt.colorbar(label="Moisture Flow Volume [m$^3$]")
plt.title(f"Evapotranspiration to location (Lat: {lat}, Lon: {lon})")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()
