#Created by Elena De Petrillo (elena.depetrillo@polito.it) & Luca Monaco (luca.monaco@polito.it). November 2024

RECON_moisture_flows_0.5.nc: This file contains a dataset of moisture flow volumes (in cubic meters) from sources of evaporation to targets of precipitation at 0.5° with global coverage and centred over 2008-2017, which aligns coherently with annual precipitation and evaporation volumes from ERA5 reanalysis,  obtained from the processing of the Lagrangian (forward trajectory-based) tracking model UTrack reconciled with ERA5 reanalysis through a reconciliation framework based on the Iterative Proportional Fitting procedure and on ERA5 preprocessing. Data are collected in integers that need to be transformed into cubic meters. Instructions for users are contained in the file description. The file also contains information on the generation of the dataset, authors of the dataset, and input variable information.

To handle the database users can use a Python environment with the required packages described in the following sample scripts. 
An in-depth data-processing workflow through Python code is available in the sample codes. 

# Rec_precipitation_footprint.py: Script to retrieve and plot the reconciled moisture flow of precipiation from evaporation from target to source based on NetCDF moisture flow data (RECON).
# Rec_evaporation_footprint.py: Script to retrieve and plot the reconciled moisture flow of evaporation to precipiation from source to target based on NetCDF moisture flow data (RECON).  


RECON_ERA5_avgYear_0.5_volumes.nc: This file contains ERA5 processed volumes of total precipitation and evaporation centred over 2008-2017 which ensure the closure of the hydrological balance for the average year. Data are available at a spatial resolution of 0.5° and have a global coverage. Condensation values are excluded.
