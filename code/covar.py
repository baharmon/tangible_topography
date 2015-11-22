# -*- coding: utf-8 -*-

"""
@brief: plot univariate statistics for the tangible topography experiment

This program is free software under the GNU General Public License
(>=v2). Read the file COPYING that comes with GRASS for details.

@author: Brendan Harmon (brendanharmon@gmail.com)
"""

import os
import grass.script as gscript
import matplotlib.pyplot as plt

# temporary region
gscript.use_temp_region()

# remove temporary maps
gscript.run_command('g.remove', flags='f', type='raster', pattern='*stddev*')
gscript.run_command('g.remove', flags='f', type='raster', pattern='*variance*')
gscript.run_command('g.remove', flags='f', type='raster', pattern='*coeff*')
gscript.run_command('g.remove', flags='f', type='raster', pattern='*mean*')

# set rendering directory
render = os.path.normpath("C:/Users/Brendan/Documents/grassdata/results/univar/")

# set paramters
overwrite = True

# assign regions
regions = ["dem_1","dem_1","dem_2","dem_3","dem_4","dem_1","dem_4"]

covar = []

# loop through the differences
categories = ["dem"]
for x in categories:
    for i in range(1,8):

        # variables
        pattern = "*"+x+"_"+str(i)
        key_value=i-1
        region=regions[key_value]


        save_covar = os.path.join(render,"covar_"+str(i)+".png")

        # list
        series = gscript.list_grouped('rast', pattern=pattern)['analysis']

        # set region
        gscript.run_command('g.region', rast=region)

        """ compute covariance """
        # compute covariance of DEMs
        covariance = gscript.read_command('r.covar', map=series, flags='r')
        covar = covariance.split(os.linesep)[1].split()

        # plot means
        plt.plot(range(len(covar)) , covar)
        plt.savefig(save_covar, transparent=overwrite)
        plt.close()
