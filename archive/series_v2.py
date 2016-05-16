# -*- coding: utf-8 -*-

"""
@brief: spatial statistics for the tangible topography experiment

This program is free software under the GNU General Public License
(>=v2). Read the file COPYING that comes with GRASS for details.

@author: Brendan Harmon (brendanharmon@gmail.com)
"""

import os
import sys
import atexit
import grass.script as gscript
from grass.exceptions import CalledModuleError

# set graphics driver
driver = "cairo"

def cleanup():
    try:
        gscript.run_command('d.mon', stop=driver)
    except CalledModuleError:
        pass

def main():

    # temporary region
    gscript.use_temp_region()

    # set grass data directory
    grassdata = os.path.normpath("C:/Users/Brendan/Documents/grassdata/")

    # set rendering directory
    render_dir = os.path.normpath("results/series/")
    render = os.path.join(grassdata,render_dir)

    # set paramters
    overwrite = True

    # color rules
    depressions_colors = '0% aqua\n100% blue'
    depth_colors = '0 255:255:255\n0.001 255:255:0\n0.05 0:255:255\n0.1 0:127:255\n0.5 0:0:255\n100% 0:0:0'
    difference_colors = '-100 red\n-20 orange\n0 white\n20 aqua\n100 blue'
    dem_coeff_colors = '15 red\n10 yellow\n5 cyan\n0 blue'
    dem_mean_colors = '410 red\n360 yellow\n315 cyan\n270 blue'
    dem_stddev_colors = '50 purple\n30 red\n15 yellow\n5 cyan\n0 blue'
    diff_coeff_colors = '15 red\n10 yellow\n5 cyan\n0 blue'
    diff_mean_colors = '410 red\n360 yellow\n315 cyan\n270 blue'
    diff_stddev_colors = '50 purple\n30 red\n15 yellow\n5 cyan\n0 blue'
    form_coeff_colors = '130 red\n50 yellow\n25 cyan\n0 blue'
    form_mean_colors = '1 220:220:220\n2 56:0:0\n3 200:0:0\n4 255:80:20\n5 250:210:60\n6 255:255:60\n7 180:230:20\n8 60:250:150\n9 0:0:255\n10 0:0:56'
    form_stddev_colors = '4 red\n2.6 yellow\n1.3 cyan\n0 blue'

    # assign regions
    regions = ["dem_1","dem_1","dem_2","dem_3","dem_4","dem_1","dem_4"]

    # loop through the DEMs, differences, and landforms
    categories = ["dem","diff","form"]
    for x in categories:
        for i in range(1,8):

            # variables
            pattern = "*"+x+"_"+str(i)
            key_value=i-1
            region=regions[key_value]
            contour = "contour_"+region[-1:]
            relief = "relief_"+region[-1:]+"@PERMANENT"
            stddev = x+"_stddev_"+str(i)
            mean = x+"_mean_"+str(i)
            coeff = x+"_coeff_"+str(i)

            # list
            series = gscript.list_grouped('rast', pattern=pattern)['analysis']

            # set region
            gscript.run_command('g.region', rast=region+"@PERMANENT")

            # driver settings
            info = gscript.parse_command('r.info', map=region+"@PERMANENT", flags='g')
            width=int(info.cols)+int(info.cols)/2
            height=int(info.rows)

            # compute standard deviation
            gscript.run_command('r.series', input=series, output=stddev, method="stddev", overwrite=overwrite)
            gscript.write_command('r.colors', map=stddev, rules='-', stdin=x+'_stddev_colors')
            gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,stddev+".png"), overwrite=overwrite)
            gscript.run_command('d.shade', shade=relief, color=stddev, brighten=75)
            gscript.run_command('d.vect', map=contour, display='shape')
            gscript.run_command('d.legend', raster=stddev, fontsize=10, at=(10,90,1,4))
            gscript.run_command('d.mon', stop=driver)

            # compute mean
            gscript.run_command('r.series', input=series, output=mean, method="average", overwrite=overwrite)
            gscript.write_command('r.colors', map=mean, rules='-', stdin=x+'_mean_colors')
            gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,mean+".png"), overwrite=overwrite)
            gscript.run_command('d.shade', shade=relief, color=mean, brighten=75)
            gscript.run_command('d.vect', map=contour, display='shape')
            gscript.run_command('d.legend', raster=mean, fontsize=10, at=(10,90,1,4))
            gscript.run_command('d.mon', stop=driver)

            # compute coefficient of variation
            # stddev / mean * 100 = percentage of variation
            gscript.run_command('r.series', input=series, output=mean, method="average", overwrite=overwrite)
            gscript.run_command('r.mapcalc', expression='{coeff} = {stddev} / {mean} * 100'.format(coeff=coeff,stddev=stddev,mean=mean), overwrite=overwrite)
            gscript.write_command('r.colors', map=coeff, rules='-', stdin=x+'_coeff_colors')
            gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,coeff+".png"), overwrite=overwrite)
            gscript.run_command('d.shade', shade=relief, color=coeff, brighten=75)
            gscript.run_command('d.vect', map=contour, display='shape')
            gscript.run_command('d.legend', raster=coeff, fontsize=10, at=(10,90,1,4))
            gscript.run_command('d.mon', stop=driver)

    # # difference series
    # for i in range(1,8):
    #
    #     # variables
    #     key_value=i-1
    #     region=regions[key_value]
    #     contour = "contour_"+region[-1:]
    #     relief = "relief_"+region[-1:]+"@PERMANENT"
    #     difference_pattern = "*diff_"+str(i)
    #     reference_contour = "contour_"+region[-1:]+"@PERMANENT"
    #     reference_relief = "relief_"+region[-1:]+"@PERMANENT"
    #     mean_diff = "mean_diff_"+str(i)
    #     sum_diff = "sum_diff_"+str(i)
    #
    #     # set region
    #     gscript.run_command('g.region', rast=region+"@PERMANENT", res=3)
    #
    #     # driver settings
    #     info = gscript.parse_command('r.info', map=region+"@PERMANENT", flags='g')
    #     width=int(info.cols)+int(info.cols)/2
    #     height=int(info.rows)
    #
    #     # list differences
    #     difference_list = gscript.list_grouped('rast', pattern=difference_pattern)['analysis']
    #
    #     # compute mean of differences of depths
    #     gscript.run_command('r.series', input=diff_list, output=mean_diff, method="average", overwrite=overwrite)
    #     gscript.run_command('r.colors', map=mean_diff, color="differences")
    #     gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(series,mean_diff+".png"), overwrite=overwrite)
    #     gscript.run_command('d.shade', shade=reference_relief, color=mean_diff, brighten=75)
    #     gscript.run_command('d.vect', map=reference_contour, display='shape')
    #     gscript.run_command('d.legend', raster=mean_diff, fontsize=10, at=(10,90,1,4))
    #     gscript.run_command('d.mon', stop=driver)


if __name__ == "__main__":
    atexit.register(cleanup)
    sys.exit(main())
