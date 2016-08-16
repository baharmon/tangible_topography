#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@brief: 3D rendering for the tangible topography experiment

This program is free software under the GNU General Public License
(>=v2). Read the file COPYING that comes with GRASS for details.

@author: Brendan Harmon (brendanharmon@gmail.com)
"""

import os
import grass.script as gscript

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

# set path
render_3d = os.path.join(gisdbase, location, 'render_3d')

# set variables
res = 3 # resolution of the region

# 3d variables
color_3d = "192:192:192"
res_3d = 1
height_3d = 2000
perspective = 25
light_position = (0.68, -0.68, 0.95)
fringe = "ne"
fringe_elevation = 250
format_3d = "tif"
size_3d = (1000, 1000)
vpoint_size = 4
vpoint_marker = "x"
vpoint_color = "red"
vline_width = 2
vline_color = "black"
# arrow_position = (100, 100)
# arrow_size = 100

url="http://soliton.vm.bytemark.co.uk/pub/cpt-city/mpl/viridis.cpt" # http://soliton.vm.bytemark.co.uk/pub/cpt-city/mpl/inferno.cpt

# list scanned DEMs
dems = gscript.list_grouped('rast',
                            pattern='dem_*')['PERMANENT']

# iterate through scanned DEMs
for dem in dems:

    # reference variables
    region = dem
    dem_difference = dem.replace("dem", "dem_difference")

    # mean variables
    mean_dem = dem.replace("dem", "mean_dem")

    # stdev variables
    stdev_dem = dem.replace("dem", "stdev_dem")
    stdev_regression_difference_series = dem.replace("dem", "stdev_regression_difference_series")

    # set region
    gscript.run_command('g.region',
                        rast=region,
                        res=res)

    # 3D render stdev elevation
    gscript.run_command('r.cpt2grass',
        map=stdev_dem,
        url=url,
        flags="s")

    gscript.run_command('m.nviz.image',
        elevation_map=mean_dem,
        color_map=stdev_dem,
        resolution_fine=res_3d,
        height=height_3d,
        perspective=perspective,
        light_position=light_position,
        fringe=fringe,
        fringe_color=color_3d,
        fringe_elevation=fringe_elevation,
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
        output=os.path.join(render_3d, stdev_dem),
        format=format_3d,
        size=size_3d,
        errors='ignore'
        )

    # 3D render stdev of regressed difference series
    gscript.run_command('r.cpt2grass',
        map=stdev_regression_difference_series,
        url=url,
        flags="s")

    gscript.run_command('m.nviz.image',
        elevation_map=mean_dem,
        color_map=stdev_regression_difference_series,
        resolution_fine=res_3d,
        height=height_3d,
        perspective=perspective,
        light_position=light_position,
        fringe=fringe,
        fringe_color=color_3d,
        fringe_elevation=fringe_elevation,
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
        output=os.path.join(render_3d,stdev_regression_difference_series),
        format=format_3d,
        size=size_3d,
        errors='ignore'
        )
