# -*- coding: utf-8 -*-

"""
@brief: histograms for the tangible topography experiment

This program is free software under the GNU General Public License
(>=v2). Read the file COPYING that comes with GRASS for details.

@author: Brendan Harmon (brendanharmon@gmail.com)
"""

import os
import grass.script as gscript

# temporary region
gscript.use_temp_region()

# set graphics driver
driver = "cairo"

# set rendering directory
histogram_dir = os.path.normpath("C:/Users/Brendan/Documents/grassdata/results/histogram/")

# assign regions
regions = ["dem_1","dem_1","dem_2","dem_3","dem_4","dem_1","dem_4"]

# list differences
diffs = gscript.list_grouped('rast', pattern='*diff*')['analysis']

# iterate through differences
for diff in diffs:

    # variable
    histogram = diff.replace("diff","diff_hist")

    # set graphics output
    gscript.run_command('d.mon', start=driver, output=os.path.join(histogram_dir,histogram+".png"), overwrite=True)

    # set region
    key_value=int(diff[-1:])-1
    region=regions[key_value]
    gscript.run_command('g.region', rast=region)

    #histogram
    gscript.run_command('d.histogram', map=diff, bgcolor="none")

    # stop graphics
    gscript.run_command('d.mon', stop=driver)

# list DEMs
dems = gscript.list_grouped('rast', pattern='*dem*')['analysis']

# iterate through DEMs
for dem in dems:

    # variable
    histogram = dem.replace("dem","dem_hist")

    # set graphics output
    gscript.run_command('d.mon', start=driver, output=os.path.join(histogram_dir,histogram+".png"), overwrite=True)

    # set region
    key_value=int(dem[-1:])-1
    region=regions[key_value]
    gscript.run_command('g.region', rast=region)

    #histogram
    gscript.run_command('d.histogram', map=dem, bgcolor="none")

    # stop graphics
    gscript.run_command('d.mon', stop=driver)
