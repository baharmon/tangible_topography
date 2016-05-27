#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grass.script as gscript
import os
import csv

# set environment
env = gscript.gisenv()

overwrite = True
env['GRASS_OVERWRITE'] = overwrite
env['GRASS_VERBOSE'] = False
env['GRASS_MESSAGE_FORMAT'] = 'standard'
gisdbase = env['GISDBASE']
location = env['LOCATION_NAME']
mapset = env['MAPSET']


# temporary variable
i = 5

# temporary data
ref_flow_cells = [1.1604560776584574, 1.1604560776584574, 1.1604560776584574, 1.937777450312218, 3.284274899150841]
flow_cells = [1.5970086021109249, 0.9117869181602166, 0.9523107811895595, 1.0315165134741844, 2.4922175763045917]

# csv path
cells = os.path.join(gisdbase, location, 'results','cells.csv')

# write to csv file
with open(cells, 'wb') as csvfile:
    cells_writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    cells_writer.writerow(['reference_flow_cells','flow_cells'])

    for x in xrange(i):
        cells_writer.writerow(ref_flow_cells[x],flow_cells[x]])
