# RECON Moisture Flows Dataset  

This repository provides a usage tutorial for the **RECON dataset**, a global atmospheric moisture connections NetCDF dataset. The RECON dataset is a post-processed version of the Lagrangian (forward trajectory-based) tracking model **UTrack** dataset (DOI UTrack dataset: [10.1594/PANGAEA.912710](https://doi.pangaea.de/10.1594/PANGAEA.912710), DOI UTrack support paper: [10.5194/essd-12-3177-2020](https://doi.org/10.5194/essd-12-3177-2020)).

---

## Data Overview  

The **RECON dataset** provides moisture flow volumes, in cubic meters, from evaporation sources to precipitation targets and vice versa. It offers global coverage at a resolution of 0.5° for an average year based on the period **2008–2017**.
The RECON dataset is available at [10.5281/zenodo.14191920](https://doi.org/10.5281/zenodo.14191920) in a compressed .7z format, along with a data download and treatment guide. Instead, this repository provides basic Python scripts to retrieve moisture flow volumes from sources of evaporation to targets of precipitation.  

---

## Data Handling  

- The dataset supports the retrieval of **source-to-target** and **target-to-source sheds** using a 4-tuple of coordinates `(source_lat, source_lon, target_lat, target_lon)`:  
  - **Latitudes (lats)** are in the range `[90, -90]`.  
  - **Longitudes (lons)** are in the range `[0, 360]`.

- To retrieve **evaporation sheds** (downwind region receiving precipitation) from an evapotranspiration point, users must specify the **source coordinates**. Conversely, to retrieve **precipitation sheds** (upwind region contributing to precipitation), users must specify the **target coordinates**.

- **Data Format**: Moisture flow volumes in the dataset are stored as integers `[0, 255]` and must be converted to cubic meters.  The data conversion formula
    
    $y = 10^{\frac{z-1}{254}\cdot[log_{10}(y_{max})-log_{10}(y_{min})]+log_{10}(y_{min})}$

    is included in the scripts described in the next section. $y$ is the converted volume in $m^3$, $z$ is the volume retrieved from RECON, $y_{max}\approx 122079329\ m^3$ is the maximum volume in $m^3$ contained in RECON and $y_{min}=10^{-3}\ m^3$ is the minimum threshold we chose to considering a moisture volume.

---

## Repository contents

### Scripts  

1. **Rec_precipitation_shed.py**  
   - This script retrieves and plots the reconciled moisture flows contributing to precipitation at the sink of interest from upwind evaporation sources based on the RECON NetCDF data.  

2. **Rec_evaporation_shed.py**  
   - This script retrieves and plots the reconciled moisture flows originating precipitation in a downwind area from the source of interest based on the RECON NetCDF data.  

### Requirements  

- A **requirements.txt** file is provided to install the necessary dependencies via `pip`.  
`pip install -r requirements.txt`
- The dependencies include essential Python libraries needed to run the provided scripts. Versions are specified as used by the authors, but they're not mandatory.

---

## How to Use the Scripts  

1. **Set Up the Environment**:  
   - Ensure you have a Python environment with the required packages as pointed out in the subsection **Requirements**.

2. **Run the Scripts**:  
   - Use the scripts to retrieve and analyze reconciled moisture flows. You can specify either source or target coordinates based on whether you want precipitation or evapotranspiration sheds.  

3. **Visualization**:  
   - The scripts also generate plots that visualize global moisture flows, focusing on evaporation-to-precipitation or precipitation-to-evaporation pathways.  

---

## Data generation process

1. **Monthly Averages**:  
   We calculated the monthly averaged (2008–2017) moisture flow volumes from the **UTrack dataset**, using a customized version of ERA5 monthly average data.
   In this preprocessing step, we ensured that:
     - Negative evapotranspiration values were set to zero.
     - The global hydrological cycle was balanced, ensuring global evapotranspiration equals global precipitation.  

2. **Yearly Averages**:  
   The monthly averaged moisture flows were integrated to obtain yearly averages.  

3. **Reconciliation**:  
   - The yearly averaged moisture flows were reconciled with our processed version of ERA5 yearly average data.  
   - This reconciliation was performed using the Iterative Proportional Fitting (IPF) method to ensure consistency.  
   Here follows an animated gif showing the IPF correction coefficient at every iteration at global scale
   ![IPF correction coefficients by iteration](images/IPF_1sec.gif)
4. **Data conversion**:
   To ensure continuity with the Utrack dataset data format and reduce the RECON dataset weight, we converted the moisture volumes into integer values `[0, 255]` using the following formula
   
   ![Integer conversion formula](images/zfromy.png)

   where $z$ is the RECON integer converted volume, $rint$ is the nearest integer convertion function, $y$ is the initial volume in $m^3$, $y_{max}\approx 122079329\ m^3$ is the maximum volume in $m^3$ contained in RECON and $y_{min}=10^{-3}\ m^3$ is the minimum threshold we chose to considering a moisture volume.
