import netCDF4 as nC
from cftime import date2num, num2date
from datetime import datetime

def out2nc(image_width, image_height, total_month, soillayernum, geotransform, OUTdatas, filename):
    dep_lst = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 30, 40, 50, 60, 70, 80,
               90, 100, 110, 120]

    nc_name = filename
    curnc = nC.Dataset(nc_name, "w", format="NETCDF3_CLASSIC")
    curnc.set_fill_off()

    nc_x = curnc.createDimension("x", image_width)
    nc_y = curnc.createDimension("y", image_height)
    nc_time = curnc.createDimension("time", total_month)
    nc_depth = curnc.createDimension("depth", soillayernum)


    nc_v_proj = curnc.createVariable("EPSG:32646", "f8")
    nc_v_x = curnc.createVariable("x", "float32", dimensions=("x",))
    nc_v_y = curnc.createVariable("y", "float32", dimensions=("y",))
    nc_v_time = curnc.createVariable("time", "float32", dimensions=("time",))
    nc_v_depth = curnc.createVariable("depth", "float32", dimensions=("depth",))
    nc_v_data = curnc.createVariable("Tsoil", "f4", dimensions=("time", "depth", "y", "x"), fill_value=-32768)


    curnc.description = "Temperature of soil Data (2010-2012)"
    curnc.start_year = "2010"


    nc_v_x.units = "m"
    nc_v_x.long_name = "x coordinate of projection"
    nc_v_x.standard_name = "projection_x_coordinate"
    nc_v_y.units = "m"
    nc_v_y.long_name = "y coordinate of projection"
    nc_v_y.standard_name = "projection_y_coordinate"

    nc_v_time.long_name = "time"
    nc_v_time.units = "months since 2010-01-01"
    nc_v_time.calendar = "360_day"  # 这里修改为 360 天日历

    nc_v_depth.long_name = "depth"
    nc_v_depth.units = "meter"

    nc_v_data.long_name = "Temperature of soil"
    nc_v_data.units = "Celsius"
    nc_v_data.grid_mapping = "EPSG:32646"
    nc_v_data.missing_value = -32768


    for d in range(soillayernum):
        nc_v_depth[d] = dep_lst[d]


    date0 = datetime(2010, 1, 1)
    date_num0 = date2num(date0, units="months since 2010-01-01", calendar="360_day")


    for t in range(total_month):
        nc_v_time[t] = date_num0 + t  # 每次增加 1 个月
        for i in range(image_width):
            nc_v_x[i] = round(geotransform[0] + 1000 * i + 500, 5)
        for j in range(image_height):
            nc_v_y[j] = round(geotransform[3] - 1000 * j - 500, 5)
        nc_v_data[t, :, :, :] = OUTdatas[t, :, :, :]

    curnc.close()

    print("The model run has been completed!")

