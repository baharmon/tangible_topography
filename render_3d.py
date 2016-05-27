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
render = os.path.join(gisdbase, location, 'results')
output = os.path.join(render, "3d_depth_5.tif")

gscript.run_command('m.nviz.image',
                    elevation_map="dem_5",
                    color_map="depth_5",
                    shininess_value=20,
                    resolution_fine=1,
                    height=2000,
                    perspective=20,
                    light_position=(0.68, -0.68 ,0.95),
                    light_ambient=60,
                    fringe="ne",
                    fringe_color=(192, 192, 192),
                    fringe_elevation=250,
                    arrow_position=(0, 0),
                    arrow_size=100,
                    output=output,
                    format="tif",
                    size=(1600, 1600),
                    #overwrite=True
                    )
