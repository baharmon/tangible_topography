#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@brief: spatial analysis for the tangible topography experiment

This program is free software under the GNU General Public License
(>=v2). Read the file COPYING that comes with GRASS for details.

@author: Brendan Harmon (brendanharmon@gmail.com)
"""

import os
import sys
import csv
import atexit
import grass.script as gscript
from grass.exceptions import CalledModuleError
# import matplotlib.pyplot as plt

# set graphics driver
driver = "cairo"

# temporary region
gscript.use_temp_region()

# set environment
env = gscript.gisenv()

overwrite = True
env['GRASS_OVERWRITE'] = overwrite
env['GRASS_VERBOSE'] = False
env['GRASS_MESSAGE_FORMAT'] = 'standard'
gisdbase = env['GISDBASE']
location = env['LOCATION_NAME']
mapset = env['MAPSET']

# set rendering directories
render = os.path.join(gisdbase, location, 'results')
render_3d = os.path.join(gisdbase, location, 'render_3d')

# csv path
cells = os.path.join(render, 'cells.csv')

# set variables
res = 3  # resolution of the region
npoints = "100%"  # percent of points for random resampling
rain_value = 300  # rain in mm/hr for r.sim.water
niterations = 4  # number of iterations for r.sim.water
nwalkers = 5000  # number of walkers for r.sim.water
step = 5  # contour interval
search = 9  # search size for r.geomorphon
skip = 6  # skip distance for r.geomorphon
size = 9  # moving window size for r.param.scale
brighten = 75  # percent brightness of shaded relief
render_multiplier = 3  # multiplier for rendering size
whitespace = 3
fontsize = 9 * render_multiplier  # legend font size
legend_coord = (10, 50, 1, 4)  # legend display coordinates

dem_difference_colors = '-40 blue\n0 white\n40 red' # '0% blue\n0 white\n100% red'
flow_difference_colors = '-0.5 blue\n0 white\n0.5 red'

def main():

    legend()
    atexit.register(cleanup)
    sys.exit(0)

def cleanup():

    try:
        # remove temporary maps
        gscript.run_command('g.remove',
            type='raster',
            name=['random', 'random_2'],
            flags='f')
    except CalledModuleError:
        pass

    try:
        # remove mask
        gscript.run_command('r.mask', raster='MASK', flags='r')
    except CalledModuleError:
        pass

def legend():
    """Draw legend"""

    dem="dem_1"

    # set region
    gscript.run_command('g.region',
        rast=dem,
        res=res)

    # start monitor
    info = gscript.parse_command('r.info',
        map=dem,
        flags='g')
    width = int(info.cols)+int(info.cols)/2*render_multiplier*whitespace
    height = int(info.rows)*render_multiplier
    gscript.run_command('d.mon',
        start=driver,
        width=width,
        height=height,
        output=os.path.join(render, "legend"+".png"),
        overwrite=overwrite)

    random = "random"
    random_2 = "random_2"

    gscript.run_command('r.random.surface',
        output=random,
        high=2,
        overwrite=overwrite)

    gscript.run_command('r.mapcalc',
        expression='{random_2} = ({random}/2) - 0.5'.format(random_2=random_2,
            random=random),
        overwrite=overwrite)

    gscript.write_command('r.colors',
        map=random_2,
        rules='-',
        stdin=flow_difference_colors)

    # render legend
    gscript.run_command('d.legend',
        raster=random_2,
        fontsize=fontsize,
        at=legend_coord,
        flags='vcs')
    gscript.run_command('d.mon', stop=driver)

if __name__ == "__main__":
    atexit.register(cleanup)
    sys.exit(main())
