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
import atexit
import grass.script as gscript
from grass.exceptions import CalledModuleError


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
res = 3



# list scanned DEMs
dems = gscript.list_grouped('rast', pattern='dem_*')['masked_data']

# iterate through scanned DEMs
for dem in dems:

    # variables
    masked_dem = dem.replace("dem","mask")

    # mask lake
    gscript.run_command('r.mapcalc', expression='{masked_dem} = if({dem} < 280, null(), {dem})'.format(masked_dem=masked_dem, dem=dem), overwrite=overwrite)

    # colors
    gscript.run_command('r.colors', map=masked_dem, color="elevation")
