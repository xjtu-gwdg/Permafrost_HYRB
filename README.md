# Permafrost_HYRB

## Overview
This project is an example implementation of the GIPL2 permafrost model ([GIPL](https://github.com/Elchin/GIPL))  for the Headwater of the Yellow River Basin (HYRB). This project provides a demonstration of running the GIPL2 model with input data from 2010 to 2012. The temporal resolution of the simulation is 1 month, and the spatial resolution is 1 km.

## Project Structure
```
GIPL_HYRB/
│-- data/
│   │-- tas_2010_2012.nc        # Temperature data (2010-2012)
│   │-- pr_2010_2012.nc         # Precipitation data (2010-2012)
│   │-- SOIL.tif                # Soil classification data
│   │-- Tsoil_200912.nc         # (Optional) Initial soil temperature data (December 2009)
│-- scripts/
│   │-- GIPL_HYRB.py            # Main script for running the GIPL2 model
│   │-- utils/                  # Utility functions for model execution
│-- temp/                       # Temporary files generated during model execution
│-- output/
│   │-- Tsoil_2010_2012.nc      # Model output containing simulated soil temperature
│-- requirements.txt            # Required dependencies for the project
│-- README.md                   # Project documentation
```

## Installation
Ensure that you have Python installed on your system. To install the required dependencies, run the following command:
```sh
pip install -r requirements.txt
```

## Running the Model
To execute the GIPL2 model, run the following command:
```sh
python scripts/GIPL_HYRB.py
```

## Model Input Data
The model requires the following input data, which are stored in the `data/` directory:
- **tas_2010_2012.nc**: Temperature data from 2010 to 2012.
- **pr_2010_2012.nc**: Precipitation data from 2010 to 2012.
- **SOIL.tif**: Soil classification data.
- **Tsoil_200912.nc** *(optional)*: Initial soil temperature data from December 2009.

## Model Output
The output of the model is stored in the `output/` directory. The primary output file is:
- **Tsoil_2010_2012.nc**: A NetCDF file containing simulated soil temperature data with four dimensions:
  - **time** (monthly resolution from 2010 to 2012)
  - **depth**
  - **y** (spatial dimension)
  - **x** (spatial dimension)

## Temporary Files
The `temp/` directory is used to store temporary files generated during model execution. It can be deleted after the model run to free up storage space.


