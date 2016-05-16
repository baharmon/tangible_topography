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

    # set rendering directory
    render = os.path.normpath("C:/Users/Brendan/Documents/grassdata/results/series/")
    
    # set paramters
    overwrite = True
    
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
            variance = x+"_variance_"+str(i)
            mean = x+"_mean_"+str(i)
            coeff = x+"_coeff_"+str(i)
    
            # list
            series = gscript.list_grouped('rast', pattern=pattern)['analysis']
    
            # set region
            gscript.run_command('g.region', rast=region)
    
            # driver settings
            info = gscript.parse_command('r.info', map=region, flags='g')
            width=int(info.cols)+int(info.cols)/2
            height=int(info.rows)
    
            # compute standard deviation
            gscript.run_command('r.series', input=series, output=stddev, method="stddev", overwrite=overwrite)
            gscript.run_command('r.colors', map=stddev, color="bcyr")
            gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,stddev+".png"), overwrite=overwrite)
            gscript.run_command('d.shade', shade=relief, color=stddev, brighten=75)
            gscript.run_command('d.vect', map=contour, display='shape')
            gscript.run_command('d.legend', raster=stddev, fontsize=10, at=(10,90,1,4))
            gscript.run_command('d.mon', stop=driver)
    
            # compute variance
            gscript.run_command('r.series', input=series, output=variance, method="variance", overwrite=overwrite)
            gscript.run_command('r.colors', map=variance, color="bcyr")
            gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,variance+".png"), overwrite=overwrite)
            gscript.run_command('d.shade', shade=relief, color=variance, brighten=75)
            gscript.run_command('d.vect', map=contour, display='shape')
            gscript.run_command('d.legend', raster=variance, fontsize=10, at=(10,90,1,4))
            gscript.run_command('d.mon', stop=driver)
    
            # compute coefficient of variation
            # stddev / mean * 100 = percentage of variation
            gscript.run_command('r.series', input=series, output=mean, method="average", overwrite=overwrite)
            gscript.run_command('r.mapcalc', expression='{coeff} = {stddev} / {mean} * 100'.format(coeff=coeff,stddev=stddev,mean=mean), overwrite=overwrite)
            gscript.run_command('r.colors', map=coeff, color="bcyr")
            gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,coeff+".png"), overwrite=overwrite)
            gscript.run_command('d.shade', shade=relief, color=coeff, brighten=75)
            gscript.run_command('d.vect', map=contour, display='shape')
            gscript.run_command('d.legend', raster=coeff, fontsize=10, at=(10,90,1,4))
            gscript.run_command('d.mon', stop=driver)

if __name__ == "__main__":
    atexit.register(cleanup)
    sys.exit(main())