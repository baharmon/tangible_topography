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
save_means = os.path.join(render,"mean.png")
save_absmeans = os.path.join(render,"asbvalmean.png")

# set paramters
overwrite = True

# assign regions
regions = ["dem_1","dem_1","dem_2","dem_3","dem_4","dem_1","dem_4"]

means = []
absmeans= []

# loop through the differences
categories = ["diff"]
for x in categories:
    for i in range(1,8):

        # variables
        pattern = "*"+x+"_"+str(i)
        key_value=i-1
        region=regions[key_value]

        # list
        series = gscript.list_grouped('rast', pattern=pattern)['analysis']

        # set region
        gscript.run_command('g.region', rast=region)

        """ compute univariate statistics """
        # compute the mean and the absolute value of the differences
        univar = gscript.parse_command('r.univar', map=series, separator='newline', flags='g')
        u =  float(univar['mean'])
        v =  float(univar['mean_of_abs'])
        means.append(u)
        absmeans.append(v)

# plot means
plt.plot(range(len(means)) , means)
plt.savefig(save_means, transparent=overwrite)
plt.close()

# plot absolute value of means
plt.plot(range(len(absmeans)) , absmeans)
plt.savefig(save_absmeans, transparent=overwrite)
plt.close()
