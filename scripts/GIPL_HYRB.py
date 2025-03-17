# -*- coding: utf-8 -*-
# Main program for GIPL_HYRB


import threading
import os
import gdal
import numpy as np
import time
from utils import out2nc, run_gipl
from netCDF4 import Dataset


def read_out(index, x, y):
    # Read GIPL output data
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    outdata = np.loadtxt(os.path.join(BASE_DIR, '../temp/GIPL-master-{}\out\\result.txt'.format(index + 101)),
                         usecols=(4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                                  18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                                  30, 31, 32, 33, 34))
    OUTdatas[:, :, y, x] = outdata



start = time.time()

# Read air temperature data
filename = "../data/tas_2010_2012.nc"
nc = Dataset(filename)
tas_all = np.array(nc.variables['tas'])
tas_all[tas_all < -1000] = np.nan

# Initialize snow data
snow = np.full(tas_all.shape, 0.0)

# Read precipitation data
filename = "../data/pr_2010_2012.nc"
nc = Dataset(filename)
pr_all = np.array(nc.variables['pr'])
pr_all[pr_all < -1000] = np.nan

# Read Initial data
filename = "../data/Tsoil_200912.nc"
nc = Dataset(filename)
Tsoil = np.array(nc.variables['Tsoil'])
Tsoil[Tsoil < -1000] = np.nan

# Read soil data
SOIL = np.full((294, 382), np.nan)
SOIL_path = "../data/SOIL.tif"
SOIL_tif = gdal.Open(SOIL_path, gdal.GA_ReadOnly)
SOIL2 = SOIL_tif.ReadAsArray()
SOIL[:291, :] = SOIL2[:, :]
SOIL[SOIL == -999] = 2

# Initialize output data storage
OUTdatas = np.full((tas_all.shape[0], 31, tas_all.shape[1], tas_all.shape[2]), np.nan)
k = 0
p = 0
m = 0
process_lst = list()

for x in range(tas_all.shape[2]):
    for y in range(tas_all.shape[1]):
        m = m + 1
        if ~np.isnan(tas_all[0, y, x]):
            if p != 15:
                process_lst.append([x, y])
                p = p + 1
            else:
                process_lst.append([x, y])
                threads = []
                for index in range(16):
                    t = threading.Thread(target=run_gipl.run_gipl, args=(index, process_lst[index][0], process_lst[index][1],
                                                                         tas_all, pr_all, SOIL, Tsoil))
                    t.start()
                    time.sleep(0.1)
                    threads.append(t)
                for thread in threads:
                    thread.join()
                for index in range(16):
                    read_out(index, process_lst[index][0], process_lst[index][1])

                p = 0
                k = k + 1
                process_lst = list()
    print( 'Processing... {:.2f}% done'.format(m * 100 / (tas_all.shape[1] * tas_all.shape[2])))

# Output as NetCDF
geotransform = tuple([760320.4834019323, 1000.0, 0.0, 3950305.3179288693, 0.0, -1000.0])
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(BASE_DIR, '../out/Tsoil_2010_2012.nc')
out2nc.out2nc(tas_all.shape[2], tas_all.shape[1], tas_all.shape[0], 31, geotransform, OUTdatas, filename)
