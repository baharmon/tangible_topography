# -*- coding: utf-8 -*-

"""
@brief: digital elevation model re-interpolation for the tangible topography experiment

This program is free software under the GNU General Public License
(>=v2). Read the file COPYING that comes with GRASS for details.

@author: Brendan Harmon (brendanharmon@gmail.com)
"""

import grass.script as gscript

# temporary region
gscript.use_temp_region()

# list scanned DEMs for experiment 1
dems = gscript.list_grouped('rast', pattern='*dem_1')['reinterpolation']

# iterate through scanned DEMs
for dem in dems:

    print dem

    # set region
    region = "dem_1@PERMANENT"

    # reinterpolate DEM from random points using regularized spline with tension
    gscript.run_command('g.region', raster=region)
    info = gscript.raster_info(dem)
    #resolution = int(info.cols) * int(info.rows) / 10
    resolution = 4000
    gscript.run_command('r.random', input=dem, npoints=resolution, vector=dem.replace("dem","points"), flags='bd', overwrite=True)
    gscript.run_command('v.surf.rst', input=dem.replace("dem","points"), elevation=dem,  tension=50, smooth=5, overwrite=True)
    gscript.run_command('r.colors', map=dem, color="elevation")
    gscript.run_command('g.remove', type='raster', pattern='*points*', flags='f')


# list scanned DEMs for experiment 2
dems = gscript.list_grouped('rast', pattern='*dem_2')['reinterpolation']

# iterate through scanned DEMs
for dem in dems:

    print dem

    # set region
    region = "dem_1@PERMANENT"

    # reinterpolate DEM from random points using regularized spline with tension
    gscript.run_command('g.region', raster=region)
    info = gscript.raster_info(dem)
    #resolution = int(info.cols) * int(info.rows) / 10
    resolution = 4000
    gscript.run_command('r.random', input=dem, npoints=resolution, vector=dem.replace("dem","points"), flags='bd', overwrite=True)
    gscript.run_command('v.surf.rst', input=dem.replace("dem","points"), elevation=dem,  tension=50, smooth=5,  overwrite=True)
    gscript.run_command('r.colors', map=dem, color="elevation")
    gscript.run_command('g.remove', type='raster', pattern='*points*', flags='f')

# list scanned DEMs for experiment 3
dems = gscript.list_grouped('rast', pattern='*dem_3')['reinterpolation']

# iterate through scanned DEMs
for dem in dems:

    print dem

    # set region
    region = "dem_2@PERMANENT"

    # reinterpolate DEM from random points using regularized spline with tension
    gscript.run_command('g.region', raster=region)
    info = gscript.raster_info(dem)
    #resolution = int(info.cols) * int(info.rows) / 10
    resolution = 4000
    gscript.run_command('r.random', input=dem, npoints=resolution, vector=dem.replace("dem","points"), flags='bd', overwrite=True)
    gscript.run_command('v.surf.rst', input=dem.replace("dem","points"), elevation=dem,  tension=50, smooth=5,  overwrite=True)
    gscript.run_command('r.colors', map=dem, color="elevation")
    gscript.run_command('g.remove', type='raster', pattern='*points*', flags='f')

# list scanned DEMs for experiment 4
dems = gscript.list_grouped('rast', pattern='*dem_4')['reinterpolation']

# iterate through scanned DEMs
for dem in dems:

    print dem

    # set region
    region = "dem_3@PERMANENT"

    # reinterpolate DEM from random points using regularized spline with tension
    gscript.run_command('g.region', raster=region)
    info = gscript.raster_info(dem)
    #resolution = int(info.cols) * int(info.rows) / 10
    resolution = 4000
    gscript.run_command('r.random', input=dem, npoints=resolution, vector=dem.replace("dem","points"), flags='bd', overwrite=True)
    gscript.run_command('v.surf.rst', input=dem.replace("dem","points"), elevation=dem,  tension=50, smooth=5,  overwrite=True)
    gscript.run_command('r.colors', map=dem, color="elevation")
    gscript.run_command('g.remove', type='raster', pattern='*points*', flags='f')

# list scanned DEMs for experiment 5
dems = gscript.list_grouped('rast', pattern='*dem_5')['reinterpolation']

# iterate through scanned DEMs
for dem in dems:

    print dem

    # set region
    region = "dem_4@PERMANENT"

    # reinterpolate DEM from random points using regularized spline with tension
    gscript.run_command('g.region', raster=region)
    info = gscript.raster_info(dem)
    #resolution = int(info.cols) * int(info.rows) / 10
    resolution = 4000
    gscript.run_command('r.random', input=dem, npoints=resolution, vector=dem.replace("dem","points"), flags='bd', overwrite=True)
    gscript.run_command('v.surf.rst', input=dem.replace("dem","points"), elevation=dem,  tension=50, smooth=5,  overwrite=True)
    gscript.run_command('r.colors', map=dem, color="elevation")
    gscript.run_command('g.remove', type='raster', pattern='*points*', flags='f')

# list scanned DEMs for experiment 6
dems = gscript.list_grouped('rast', pattern='*dem_6')['reinterpolation']

# iterate through scanned DEMs
for dem in dems:

    print dem

    # set region
    region = "dem_1@PERMANENT"

    # reinterpolate DEM from random points using regularized spline with tension
    gscript.run_command('g.region', raster=region)
    info = gscript.raster_info(dem)
    #resolution = int(info.cols) * int(info.rows) / 10
    resolution = 4000
    gscript.run_command('r.random', input=dem, npoints=resolution, vector=dem.replace("dem","points"), flags='bd', overwrite=True)
    gscript.run_command('v.surf.rst', input=dem.replace("dem","points"), elevation=dem,  tension=50, smooth=5,  overwrite=True)
    gscript.run_command('r.colors', map=dem, color="elevation")
    gscript.run_command('g.remove', type='raster', pattern='*points*', flags='f')

# list scanned DEMs for experiment 7
dems = gscript.list_grouped('rast', pattern='*dem_7')['reinterpolation']

# iterate through scanned DEMs
for dem in dems:

    print dem

    # set region
    region = "dem_4@PERMANENT"

    # reinterpolate DEM from random points using regularized spline with tension
    gscript.run_command('g.region', raster=region)
    info = gscript.raster_info(dem)
    #resolution = int(info.cols) * int(info.rows) / 10
    resolution = 4000
    gscript.run_command('r.random', input=dem, npoints=resolution, vector=dem.replace("dem","points"), flags='bd', overwrite=True)
    gscript.run_command('v.surf.rst', input=dem.replace("dem","points"), elevation=dem,  tension=50, smooth=5,  overwrite=True)
    gscript.run_command('r.colors', map=dem, color="elevation")
    gscript.run_command('g.remove', type='raster', pattern='*points*', flags='f')
