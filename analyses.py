# -*- coding: utf-8 -*-

"""
@brief: spatial analysis for the tangible topography experiment

This program is free software under the GNU General Public License
(>=v2). Read the file COPYING that comes with GRASS for details.

@author: Brendan Harmon (brendanharmon@gmail.com)
"""

import os
import grass.script as gscript

# switch between png and cairo driver

# temporary region
gscript.use_temp_region()

# remove temporary maps
gscript.run_command('g.remove', flags='f', type='raster', pattern='*stddev*')
gscript.run_command('g.remove', flags='f', type='raster', pattern='*variance*')
gscript.run_command('g.remove', flags='f', type='raster', pattern='*coeff*')
gscript.run_command('g.remove', flags='f', type='raster', pattern='*mean*')
gscript.run_command('g.remove', flags='f', type='raster', pattern='*mean*')

# set graphics driver
driver = "cairo"

# set statistics directory
stats = os.path.normpath("C:/Users/Brendan/Documents/grassdata/results/stats/")

# set rendering directory
render = os.path.normpath("C:/Users/Brendan/Documents/grassdata/results/render/")

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

    # set region
    gscript.run_command('g.region', rast=region, res=3)

    # render DEM
    info = gscript.parse_command('r.info', map=dem, flags='g')
    gscript.run_command('d.mon', start=driver, width=info.cols, height=info.rows, output=os.path.join(render,dem+".png"), overwrite=True)
    gscript.run_command('r.relief', input=dem, output=relief, zscale=0.5, overwrite=True)
    gscript.run_command('r.contour', input=dem, output=contour, step=5, overwrite=True)
    gscript.run_command('r.colors', map=dem, color="elevation")
    gscript.run_command('d.shade', shade=relief, color=dem, brighten=75)
    gscript.run_command('d.vect', map=contour, display='shape')
    gscript.run_command('d.legend', raster=dem)
    gscript.run_command('d.mon', stop=driver)

    # compute slope
    gscript.run_command('d.mon', start=driver, width=info.cols, height=info.rows, output=os.path.join(render,slope+".png"), overwrite=True)
    gscript.run_command('r.slope.aspect', elevation=dem, slope=slope, overwrite=True)
    gscript.run_command('d.shade', shade=relief, color=slope, brighten=75)
    gscript.run_command('d.vect', map=contour, display='shape')
    gscript.run_command('d.legend', raster=slope)
    gscript.run_command('d.mon', stop=driver)

    #compute geomorphon
    gscript.run_command('d.mon', start=driver, width=info.cols, height=info.rows, output=os.path.join(render,forms+".png"), overwrite=True)
    gscript.run_command('r.geomorphon', dem=dem, forms=forms, search=9, skip=6, overwrite=True)
    gscript.run_command('d.shade', shade=relief, color=forms, brighten=75)
    gscript.run_command('d.vect', map=contour, display='shape')
    #gscript.run_command('d.legend', raster=forms)
    gscript.run_command('d.mon', stop=driver)

    # simulate water flow
    gscript.run_command('d.mon', start=driver, width=info.cols, height=info.rows, output=os.path.join(render,depth+".png"), overwrite=True)
    gscript.run_command('r.slope.aspect', elevation=dem, dx='dx', dy='dy', overwrite=True)
    gscript.run_command('r.sim.water', elevation=dem, dx='dx', dy='dy', rain_value=300, depth=depth, nwalkers=5000, niterations=4, overwrite=True)
    gscript.run_command('g.remove', flags='f', type='raster', name=['dx', 'dy'])
    gscript.run_command('d.shade', shade=relief, color=depth, brighten=75)
    gscript.run_command('d.vect', map=contour, display='shape')
    gscript.run_command('d.legend', raster=depth)
    gscript.run_command('d.mon', stop=driver)

    # compute difference
    gscript.run_command('d.mon', start=driver, width=info.cols, height=info.rows, output=os.path.join(render,difference+".png"), overwrite=True)
    regression_params = gscript.parse_command('r.regression.line', flags='g', mapx=before, mapy=after, overwrite=True)
    gscript.run_command('r.mapcalc', expression='{regression} = {a} + {b} * {before}'.format(a=regression_params['a'], b=regression_params['b'],before=before,regression=regression), overwrite=True)
    gscript.run_command('r.mapcalc', expression='{difference} = {regression} - {after}'.format(regression=regression,after=after,difference=difference), overwrite=True)
    gscript.run_command('r.colors', map=difference, color="differences")
    gscript.run_command('d.shade', shade=relief, color=difference, brighten=75)
    gscript.run_command('d.vect', map=contour, display='shape')
    gscript.run_command('d.legend', raster=difference)
    gscript.run_command('d.mon', stop=driver)
    gscript.run_command('g.remove', flags='f', type='raster', name=regression)
