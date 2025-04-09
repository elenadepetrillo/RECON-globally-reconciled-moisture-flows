# Created by Elena De Petrillo (elena.depetrillo@polito.it) & Luca Monaco (luca.monaco@polito.it)

# Script to retrieve and plot the reconciled moisture flow of evaporation at the source from precipitation at the
# sink based on NetCDF moisture flow data (RECON).  


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

#Example usage with specific latitude and longitude values of the source (location of evaporation)
# Set a location of evaporation (point coordinates) and get its evaporation shed, i.e., the precipitation flows in downind cells (sinks) originating from its annual evaporation.


# Modify these coordinates to analyze different points.
lon = 7.7
lat = 45.1

# Get the evaporation shed, which need to be converted in cubic meters

evaporation_shed = dataset["moisture_flow"].sel(sourcelat=lat, sourcelon=lon,method="nearest").values
# Convert to cubic meters
evaporation_shed = np.where(
        evaporation_shed== 0,
        0,
        10**(((evaporation_shed- 1) / 254) * (np.log10(ymax) - np.log10(ymin)) + np.log10(ymin))
    )

# Optional: Plotting results (customize as needed)
lats = np.arange(90, -90, -0.5)
lons = np.arange(0, 360, 0.5)
plt.figure(figsize=(10, 6))
plt.imshow(evaporation_shed, extent=[lons.min(), lons.max(), lats.min(), lats.max()])
plt.colorbar(label="moisture flow [m$^3$]")
plt.title(f"Annual precipitation originating from evaporation at location (Lat: {lat}, Lon: {lon})")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()
