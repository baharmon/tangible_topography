#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue May 24 16:21:34 2016

@author: Brendan
"""

import os
import grass.script as gscript

# set environment
env = gscript.gisenv()

overwrite = True
env['GRASS_OVERWRITE'] = overwrite
env['GRASS_VERBOSE'] = False
env['GRASS_MESSAGE_FORMAT'] = 'standard'
gisdbase = env['GISDBASE']
location = env['LOCATION_NAME']
mapset = env['MAPSET']

# set rendering directory
render = os.path.join(gisdbase, location, 'results')

# import seaborn as sns
#
# sns.set(style="whitegrid")
#
# cells = sns.load_dataset(os.path.join(render,'cells.csv'))
#
# g = sns.factorplot(x="flow_cells", data=cells, kind="count",
#                    palette="BuPu", size=6, aspect=1.5)
# g.set_xticklabels(step=2)
#


import numpy as np
import seaborn as sns
sns.set(style="white")

# Load the example planets dataset
planets = sns.load_dataset(os.path.join(render,'planets'))

# Make a range of years to show categories with no observations
years = np.arange(2000, 2015)

# Draw a count plot to show the number of planets discovered each year
g = sns.factorplot(x="year", data=planets, kind="count",
                   palette="BuPu", size=6, aspect=1.5, order=years)
g.set_xticklabels(step=2)



# # Draw a nested barplot to show survival for class and sex
# g = sns.factorplot(x="ref_flow_cells", y="survived", hue="sex", data=cells,
#                    size=6, kind="bar", palette="muted")
# g.despine(left=True)
# g.set_ylabels("survival probability")
#
#



# import numpy as np
# import seaborn as sns
# sns.set(style="white")
#
# # Load the example planets dataset
# planets = sns.load_dataset("planets")
#
# # Make a range of years to show categories with no observations
# years = np.arange(2000, 2015)
#
# # Draw a count plot to show the number of planets discovered each year
# g = sns.factorplot(x="year", data=planets, kind="count",
#                    palette="BuPu", size=6, aspect=1.5, order=years)
# g.set_xticklabels(step=2)
