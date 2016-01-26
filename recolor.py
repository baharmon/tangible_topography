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

# set graphics driver
driver = "cairo"

# set grass data directory
grassdata = os.path.normpath("C:/Users/Brendan/Documents/grassdata/")

# set rendering directory
render_dir = os.path.normpath("results/render/")
render = os.path.join(grassdata,render_dir)

# set color rule directory
diff_dir = os.path.normpath("experiment_ncspf/difference_rule.txt")
difference_rule = os.path.join(grassdata,diff_dir)

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

    # set region
    gscript.run_command('g.region', rast=region, res=3)

    # render DEM
    info = gscript.parse_command('r.info', map=dem, flags='g')
    width=int(info.cols)+int(info.cols)/2
    height=int(info.rows)

    # compute slope
    gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,slope+".png"), overwrite=overwrite)
#    gscript.run_command('r.param.scale', input=dem, output=slope, size=9, method="slope", overwrite=overwrite)
    gscript.run_command('r.colors', map=slope, color="slope")
    gscript.run_command('d.shade', shade=relief, color=slope, brighten=75)
    gscript.run_command('d.vect', map=contour, display='shape')
    gscript.run_command('d.legend', raster=slope, fontsize=10, at=(10,80,1,4))
    gscript.run_command('d.mon', stop=driver)

