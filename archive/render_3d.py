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
output_3d = os.path.join(render_3d, "dem_1")

# temporary region
gscript.use_temp_region()
gscript.run_command('g.region', rast='dem_1')

# 3D rendering
gscript.run_command('m.nviz.image',
                    elevation_map="dem_1",
                    #color_map="dem_1",
                    color="192:192:192",
                    resolution_fine=1,
                    height=2000,
                    perspective=25,
                    light_position=(0.68, -0.68 ,0.95),
                    fringe="ne",
                    fringe_color="192:192:192",
                    fringe_elevation=250,
                    #arrow_position=(100, 100),
                    #arrow_size=100,
                    output=output_3d,
                    format="tif",
                    size=(1000, 1000),
                    )
