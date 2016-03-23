# -*- coding: utf-8 -*-

"""
@brief: spatial analysis for the tangible topography experiment

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
    render_dir = os.path.normpath("results/render/")
    render = os.path.join(grassdata,render_dir)

    # color rules
    depressions_colors = '0% aqua\n100% blue'
    depth_colors = '0 255:255:255\n0.001 255:255:0\n0.05 0:255:255\n0.1 0:127:255\n0.5 0:0:255\n100% 0:0:0'
    difference_colors = '-100 red\n-20 orange\n0 white\n20 aqua\n100 blue'

    # set paramters
    overwrite = True

    # assign regions
    regions = ["dem_1","dem_1","dem_2","dem_3","dem_4","dem_1","dem_4"]

    # list scanned DEMs
    dems = gscript.list_grouped('rast', pattern='*dem*')['analysis']

    # iterate through scanned DEMs
    for dem in dems:

        # variables
        key_value=int(dem[-1:])-1
        region=regions[key_value]
        relief=dem.replace("dem","relief")
        contour=dem.replace("dem","contour")
        slope=dem.replace("dem","slope")
        forms=dem.replace("dem","form")
        depth=dem.replace("dem","depth")
        before=region
        after=dem
        regression=dem.replace("dem","regress")
        difference=dem.replace("dem","diff")
        depth_before=region.replace("dem","depth")
        depth_after=depth
        depth_difference=dem.replace("dem","depth_diff")
        depressions=dem.replace("dem","depressions")

        # set region
        gscript.run_command('g.region', rast=region, res=3)

        # render DEM
        info = gscript.parse_command('r.info', map=dem, flags='g')
        width=int(info.cols)+int(info.cols)/2
        height=int(info.rows)
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,dem+".png"), overwrite=overwrite)
        gscript.run_command('r.colors', map=dem, color="elevation")
        gscript.run_command('r.relief', input=dem, output=relief, altitude=60, azimuth=45, zscale=1, units="intl", overwrite=overwrite)
        gscript.run_command('r.contour', input=dem, output=contour, step=5, overwrite=overwrite)
        gscript.run_command('d.shade', shade=relief, color=dem, brighten=75)
        gscript.run_command('d.vect', map=contour, display='shape')
        gscript.run_command('d.legend', raster=dem, fontsize=10, at=(10,90,1,4))
        gscript.run_command('d.mon', stop=driver)

        # compute slope
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,slope+".png"), overwrite=overwrite)
        gscript.run_command('r.param.scale', input=dem, output=slope, size=9, method="slope", overwrite=overwrite)
        gscript.run_command('r.colors', map=slope, color="slope")
        gscript.run_command('d.shade', shade=relief, color=slope, brighten=75)
        gscript.run_command('d.vect', map=contour, display='shape')
        gscript.run_command('d.legend', raster=slope, fontsize=10, at=(10,70,1,4))
        gscript.run_command('d.mon', stop=driver)

        #compute geomorphon
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,forms+".png"), overwrite=overwrite)
        gscript.run_command('r.geomorphon', dem=dem, forms=forms, search=9, skip=6, overwrite=overwrite)
        gscript.run_command('d.shade', shade=relief, color=forms, brighten=75)
        gscript.run_command('d.vect', map=contour, display='shape')
        gscript.run_command('d.legend', raster=forms)
        gscript.run_command('d.mon', stop=driver)

        # compute difference
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,difference+".png"), overwrite=overwrite)
        regression_params = gscript.parse_command('r.regression.line', flags='g', mapx=before, mapy=after, overwrite=overwrite)
        gscript.run_command('r.mapcalc', expression='{regression} = {a} + {b} * {before}'.format(a=regression_params['a'], b=regression_params['b'],before=before,regression=regression), overwrite=overwrite)
        gscript.run_command('r.mapcalc', expression='{difference} = {regression} - {after}'.format(regression=regression,after=after,difference=difference), overwrite=overwrite)
        gscript.write_command('r.colors', map=difference, rules='-', stdin=difference_colors)
        gscript.run_command('d.shade', shade=relief, color=difference, brighten=75)
        gscript.run_command('d.vect', map=contour, display='shape')
        gscript.run_command('d.legend', raster=difference, fontsize=10, at=(10,90,1,4))
        gscript.run_command('d.mon', stop=driver)
        gscript.run_command('g.remove', flags='f', type='raster', name=regression)

        # simulate water flow
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,depth+".png"), overwrite=overwrite)
        gscript.run_command('r.slope.aspect', elevation=dem, dx='dx', dy='dy', overwrite=overwrite)
        gscript.run_command('r.sim.water', elevation=dem, dx='dx', dy='dy', rain_value=300, depth=depth, nwalkers=5000, niterations=4, overwrite=overwrite)
        gscript.run_command('g.remove', flags='f', type='raster', name=['dx', 'dy'])
        gscript.run_command('d.shade', shade=relief, color=depth, brighten=75)
        gscript.run_command('d.vect', map=contour, display='shape')
        gscript.run_command('d.legend', raster=depth, fontsize=10, at=(10,90,1,4))
        gscript.run_command('d.mon', stop=driver)

        # identify depressions
        gscript.run_command('r.fill.dir', input=dem, output='depressionless_dem', direction='flow_dir',overwrite=overwrite)
        gscript.run_command('r.mapcalc', expression='{depressions} = if({depressionless_dem} - {dem} > {depth}, {depressionless_dem} - {dem}, null())'.format(depressions=depressions, depressionless_dem='depressionless_dem', dem=dem, depth=0), overwrite=overwrite)
        gscript.write_command('r.colors', map=depressions, rules='-', stdin=depressions_colors)
        gscript.run_command('g.remove', flags='f', type='raster', name=['depressionless_dem','flow_dir'])
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,depressions+".png"), overwrite=overwrite)
        gscript.run_command('d.shade', shade=relief, color=depressions, brighten=75)
        gscript.run_command('d.vect', map=contour, display='shape')
        gscript.run_command('d.legend', raster=depressions, fontsize=10, at=(10,90,1,4))
        gscript.run_command('d.mon', stop=driver)

        # compute the difference between the modeled and reference flow depth
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,difference+".png"), overwrite=overwrite)
        gscript.run_command('r.mapcalc', expression='{difference} = {before} - {after}'.format(before=depth_before,after=depth_after,difference=depth_difference), overwrite=overwrite)
        gscript.run_command('r.colors', map=depth_difference, color="differences")
        gscript.run_command('d.shade', shade=relief, color=depth_difference, brighten=75)
        gscript.run_command('d.vect', map=contour, display='shape')
        gscript.run_command('d.legend', raster=depth_difference, fontsize=10, at=(10,90,1,4))
        gscript.run_command('d.mon', stop=driver)

if __name__ == "__main__":
    atexit.register(cleanup)
    sys.exit(main())
