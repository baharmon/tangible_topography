#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Wed Nov 25 12:44:36 2015

@author: Brendan
"""

import grass.script as gscript
from collections import defaultdict

# initialize a dictionary for each name
d = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))

# initialize a list for participants' names
name_list = []

# initialize a list of categories
categories = ["dem"]

# get list of rasters
rasters = gscript.list_strings('raster', pattern="*")

for raster in rasters:

    raster_name, separator, mapset = raster.partition('@')

    name, separator, cat_number = raster_name.partition('_')

    cat, separator, number = cat_number.partition('_')

    name_list.append(name)

    # add values to dictionary
    d[name][number][cat] = raster

# remove duplicates
name_list = set(name_list)

# anonymize list of participants
participants = {v: k for k,v in enumerate(name_list)}
# participants = dict((v,k) for k,v in enumerate(name_list))

# loop through experiments
max_experiments=7
for n in range(max_experiments):
    # loop through participants
    for name in name_list:

        # loop through categories
        for cat in categories:

            raster = d[name][str(n+1)][cat]
            if not raster:
                continue

            raster_name, separator, mapset = raster.partition('@')
            new_raster = "participant_" + raster_name.replace(name,str(participants[name]+1))
            print "original raster: " + raster
            print "new raster: " + new_raster
            gscript.run_command('g.rename',raster="{map_1},{map_2}".format(map_1=raster ,map_2=new_raster),overwrite=True)
