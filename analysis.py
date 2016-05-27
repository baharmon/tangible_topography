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
import csv
import atexit
import grass.script as gscript
from grass.exceptions import CalledModuleError
import matplotlib.pyplot as plt

# set graphics driver
driver = "cairo"

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

# set rendering directory
render = os.path.join(gisdbase, location, 'results')

# csv path
cells = os.path.join(render,'cells.csv')

# set variables
res = 3 # resolution of the region
npoints = "100%" # percent of points for random resampling
rain_value = 300 # rain in mm/hr for r.sim.water
niterations = 4 # number of iterations for r.sim.water
nwalkers = 5000 # number of walkers for r.sim.water
step = 5 # contour interval
search = 9 # search size for r.geomorphon
skip = 6 # skip distance for r.geomorphon
size = 9 # moving window size for r.param.scale
brighten = 75 # percent brightness of shaded relief
render_multiplier = 3 # multiplier for rendering size
fontsize = 9 * render_multiplier # legend font size
legend_coord = (10, 50, 1, 4) # legend display coordinates


# set color rules
depressions_colors = '0% aqua\n100% blue'
depth_colors = '0 255:255:255\n0.001 255:255:0\n0.05 0:255:255\n0.1 0:127:255\n0.5 0:0:255\n100% 0:0:0'
dem_difference_colors = '-40 blue\n0 white\n40 red' # '0% blue\n0 white\n100% red'
flow_difference_colors = '-0.5 blue\n0 white\n0.5 red'
slope_difference_colors = '-30 blue\n0 white\n30 red' # '0% blue\n0 white\n100% red'
forms_difference_colors = '-10 blue\n0 white\n10 red'

# set region
# region = "dem@PERMANENT"
# gscript.run_command('g.region', rast=region, res=res)

# driver settings
# info = gscript.parse_command('r.info', map=region, flags='g')
# width = int(info.cols)+int(info.cols)/2
# height = int(info.rows)

def main():

    # set counter
    i = 0

    # initialize list
    ref_flow_cells = []
    ref_depression_cells = []
    ref_peak_cells = []
    ref_pit_cells = []
    ref_ridge_cells = []
    ref_valley_cells = []
    flow_cells = []
    depression_cells = []
    peak_cells = []
    pit_cells = []
    ridge_cells = []
    valley_cells = []
    flow_distance = []
    peak_distance = []
    pit_distance = []
    ridge_distance = []
    valley_distance = []

    # run functions
    i = reference(i,
              ref_flow_cells,
              ref_depression_cells,
              ref_peak_cells,
              ref_pit_cells,
              ref_ridge_cells,
              ref_valley_cells)

    analysis(flow_cells,
             depression_cells,
             peak_cells,
             pit_cells,
             ridge_cells,
             valley_cells,
             flow_distance,
             peak_distance,
             pit_distance,
             ridge_distance,
             valley_distance)

    write_results(i,
         ref_flow_cells,
         ref_depression_cells,
         ref_peak_cells,
         ref_pit_cells,
         ref_ridge_cells,
         ref_valley_cells,
         flow_cells,
         depression_cells,
         peak_cells,
         pit_cells,
         ridge_cells,
         valley_cells,
         flow_distance,
         peak_distance,
         pit_distance,
         ridge_distance,
         valley_distance)

    atexit.register(cleanup)
    sys.exit(0)

def cleanup():

    try:
        # remove temporary maps
        gscript.run_command('g.remove',
                            type='raster',
                            name=['depressionless_dem', 'flow_dir', 'dx', 'dy'],
                            flags='f')

    except CalledModuleError:
        pass

def reference(i, ref_flow_cells, ref_depression_cells, ref_peak_cells, ref_pit_cells, ref_ridge_cells, ref_valley_cells):
    """Spatial analyses of the reference maps"""

    # compute shaded relief
    relief = 'relief'
    gscript.run_command('g.region',
                        rast='dem@PERMANENT',
                        res=res)
    gscript.run_command('r.relief',
                        input='dem@PERMANENT',
                        output=relief,
                        altitude=90,
                        azimuth=45,
                        zscale=1,
                        units="intl",
                        overwrite=overwrite)

    # list scanned DEMs
    dems = gscript.list_grouped('rast',
                                pattern='dem_*')['PERMANENT']

    # iterate through scanned DEMs
    for dem in dems:

        # variables
        region = dem
        #relief = dem.replace("dem","relief")
        mask = dem.replace("dem","mask")
        contour = dem.replace("dem", "contour")
        slope = dem.replace("dem", "slope")
        forms = dem.replace("dem", "forms")
        depth = dem.replace("dem", "depth")
        dem_before = dem
        dem_after = dem
        dem_difference = dem.replace("dem", "dem_difference")
        dem_regression = dem.replace("dem", "dem_regression")
        dem_regression_difference = dem.replace("dem", "dem_regression_difference")
        slope_before = slope
        slope_after = slope
        slope_difference = dem.replace("dem", "slope_difference")
        slope_regression = dem.replace("dem", "slope_regression")
        slope_regression_difference = dem.replace("dem", "slope_regression_difference")
        forms_before = forms
        forms_after = forms
        forms_difference = dem.replace("dem", "forms_difference")
        depth_before = depth
        depth_after = depth
        depth_difference = dem.replace("dem", "depth_difference")
        depressions = dem.replace("dem", "depressions")
        concentrated_flow = dem.replace("dem", "concentrated_flow")
        concentrated_points = dem.replace("dem", "concentrated_points")
        peaks = dem.replace("dem", "peaks")
        peak_points = dem.replace("dem", "peak_points")
        pits = dem.replace("dem", "pits")
        pit_points = dem.replace("dem", "pit_points")
        ridges = dem.replace("dem", "ridges")
        ridge_points = dem.replace("dem", "ridge_points")
        valleys = dem.replace("dem", "valleys")
        valley_points = dem.replace("dem", "valley_points")

        # set region
        gscript.run_command('g.region',
                            rast=region,
                            res=res)

        # check if mask needed
        find_mask = gscript.find_file(mask,
                                      element='cell')
        if find_mask['name']:
            gscript.run_command('r.mask',
                                raster=mask,
                                overwrite=overwrite)

        # render DEM
        info = gscript.parse_command('r.info',
                                     map=dem,
                                     flags='g')
        width = int(info.cols)+int(info.cols)/2*render_multiplier
        height = int(info.rows)*render_multiplier
        gscript.run_command('d.mon',
                            start=driver,
                            width=width,
                            height=height,
                            output=os.path.join(render, dem+".png"),
                            overwrite=overwrite)
        gscript.run_command('r.colors',
                            map=dem,
                            color="elevation")
        #gscript.run_command('r.relief', input=dem, output=relief, altitude=90, azimuth=45, zscale=1, units="intl", overwrite=overwrite)
        gscript.run_command('r.contour',
                            input=dem,
                            output=contour,
                            step=step,
                            overwrite=overwrite)
        gscript.run_command('d.shade',
                            shade=relief,
                            color=dem,
                            brighten=brighten)
        gscript.run_command('d.vect',
                            map=contour,
                            display="shape")
        gscript.run_command('d.legend',
                            raster=dem,
                            fontsize=fontsize,
                            at=legend_coord)
        gscript.run_command('d.mon',
                            stop=driver)

        # compute slope
        gscript.run_command('d.mon',
                            start=driver,
                            width=width,
                            height=height,
                            output=os.path.join(render, slope+".png"),
                            overwrite=overwrite)
        gscript.run_command('r.param.scale',
                            input=dem, output=slope,
                            size=size,
                            method="slope",
                            overwrite=overwrite)
        gscript.run_command('r.colors',
                            map=slope,
                            color="slope")
        gscript.run_command('d.shade',
                            shade=relief,
                            color=slope,
                            brighten=brighten)
        gscript.run_command('d.vect',
                            map=contour,
                            display='shape')
        gscript.run_command('d.legend',
                            raster=slope,
                            fontsize=fontsize,
                            at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        #compute geomorphon
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render, forms+".png"), overwrite=overwrite)
        gscript.run_command('r.geomorphon', dem=dem, forms=forms, search=search, skip=skip, overwrite=overwrite)
        gscript.run_command('d.shade', shade=relief, color=forms, brighten=brighten)
        gscript.run_command('d.vect', map=contour, display='shape')
        gscript.run_command('d.legend', raster=forms, fontsize=fontsize, at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # simulate water flow
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render, depth+".png"), overwrite=overwrite)
        gscript.run_command('r.slope.aspect', elevation=dem, dx='dx', dy='dy', overwrite=overwrite)
        gscript.run_command('r.sim.water', elevation=dem, dx='dx', dy='dy', rain_value=rain_value, depth=depth, nwalkers=nwalkers, niterations=niterations, overwrite=overwrite)
        gscript.run_command('g.remove', flags='f', type='raster', name=['dx', 'dy'])
        gscript.run_command('d.shade', shade=relief, color=depth, brighten=brighten)
        gscript.run_command('d.vect', map=contour, display='shape')
        gscript.run_command('d.legend', raster=depth, fontsize=fontsize, at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # identify depressions
        gscript.run_command('r.fill.dir', input=dem, output='depressionless_dem', direction='flow_dir', overwrite=overwrite)
        gscript.run_command('r.mapcalc', expression='{depressions} = if({depressionless_dem} - {dem} > {depth}, {depressionless_dem} - {dem}, null())'.format(depressions=depressions, depressionless_dem='depressionless_dem', dem=dem, depth=0), overwrite=overwrite)
        gscript.write_command('r.colors', map=depressions, rules='-', stdin=depressions_colors)
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render, depressions+".png"), overwrite=overwrite)
        gscript.run_command('d.shade', shade=relief, color=depressions, brighten=brighten)
        gscript.run_command('d.vect', map=contour, display='shape')
        gscript.run_command('d.legend', raster=depressions, fontsize=fontsize, at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # compute the difference between the modeled and reference elevation
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render, dem_difference+".png"), overwrite=overwrite)
        gscript.run_command('r.mapcalc', expression='{difference} = {before} - {after}'.format(before=dem_before, after=dem_after, difference=dem_difference), overwrite=overwrite)
        gscript.write_command('r.colors', map=dem_difference, rules='-', stdin=dem_difference_colors)
        gscript.run_command('d.shade', shade=relief, color=dem_difference, brighten=brighten)
        gscript.run_command('d.vect', map=contour, display='shape')
        gscript.run_command('d.legend', raster=dem_difference, fontsize=fontsize, at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # compute the linearly regressed difference between the modeled and reference elevation
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render, dem_regression_difference+".png"), overwrite=overwrite)
        regression_params = gscript.parse_command('r.regression.line', flags='g', mapx=dem_before, mapy=dem_after, overwrite=overwrite)
        gscript.run_command('r.mapcalc', expression='{regression} = {a} + {b} * {before}'.format(a=regression_params['a'], b=regression_params['b'], before=dem_before, regression=dem_regression), overwrite=overwrite)
        gscript.run_command('r.mapcalc', expression='{difference} = {regression} - {after}'.format(regression=dem_regression, after=dem_after, difference=dem_regression_difference), overwrite=overwrite)
        gscript.write_command('r.colors', map=dem_regression_difference, rules='-', stdin=dem_difference_colors)
        gscript.run_command('d.shade', shade=relief, color=dem_regression_difference, brighten=brighten)
        gscript.run_command('d.vect', map=contour, display='shape')
        gscript.run_command('d.legend', raster=dem_regression_difference, fontsize=fontsize, at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # compute the difference between the modeled and reference slope
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render, slope_difference+".png"), overwrite=overwrite)
        gscript.run_command('r.mapcalc', expression='{difference} = {before} - {after}'.format(before=slope_before, after=slope_after, difference=slope_difference), overwrite=overwrite)
        gscript.write_command('r.colors', map=slope_difference, rules='-', stdin=slope_difference_colors)
        gscript.run_command('d.shade', shade=relief, color=slope_difference, brighten=brighten)
        gscript.run_command('d.vect', map=contour, display='shape')
        gscript.run_command('d.legend', raster=slope_difference, fontsize=fontsize, at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # compute the difference between the modeled and reference slope of the regressed elevation
        gscript.run_command('r.param.scale',
                            input=dem_regression, output=slope_regression,
                            size=size,
                            method="slope",
                            overwrite=overwrite)
        gscript.run_command('r.colors',
                            map=slope_regression,
                            color="slope")
        gscript.run_command('d.mon',
                            start=driver,
                            width=width,
                            height=height,
                            output=os.path.join(render, slope_regression_difference+".png"),
                            overwrite=overwrite)
        gscript.run_command('r.mapcalc',
                            expression='{difference} = {before} - {after}'.format(
                            before=slope_before,
                            after=slope_regression,
                            difference=slope_regression_difference),
                            overwrite=overwrite)
        gscript.write_command('r.colors',
                              map=slope_regression_difference,
                              rules='-',
                              stdin=slope_difference_colors)
        gscript.run_command('d.shade',
                            shade=relief,
                            color=slope_regression_difference,
                            brighten=brighten)
        gscript.run_command('d.vect',
                            map=contour,
                            display='shape')
        gscript.run_command('d.legend',
                            raster=slope_regression_difference,
                            fontsize=fontsize,
                            at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # compute the linearly regressed difference between the modeled and reference slope
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render, slope_regression_difference+".png"), overwrite=overwrite)
        regression_params = gscript.parse_command('r.regression.line', flags='g', mapx=slope_before, mapy=slope_after, overwrite=overwrite)
        gscript.run_command('r.mapcalc', expression='{regression} = {a} + {b} * {before}'.format(a=regression_params['a'], b=regression_params['b'], before=slope_before, regression=slope_regression), overwrite=overwrite)
        gscript.run_command('r.mapcalc', expression='{difference} = {regression} - {after}'.format(regression=slope_regression, after=slope_after, difference=slope_regression_difference), overwrite=overwrite)
        gscript.write_command('r.colors', map=slope_regression_difference, rules='-', stdin=slope_difference_colors)
        gscript.run_command('d.shade', shade=relief, color=slope_regression_difference, brighten=brighten)
        gscript.run_command('d.vect', map=contour, display='shape')
        gscript.run_command('d.legend', raster=slope_regression_difference, fontsize=fontsize, at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # compute the difference between the modeled and reference landorms
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render, forms_difference+".png"), overwrite=overwrite)
        gscript.run_command('r.mapcalc', expression='{difference} = {before} - {after}'.format(before=forms_before, after=forms_after, difference=forms_difference), overwrite=overwrite)
        gscript.write_command('r.colors', map=forms_difference, rules='-', stdin=forms_difference_colors)
        gscript.run_command('d.shade', shade=relief, color=forms_difference, brighten=brighten)
        gscript.run_command('d.vect', map=contour, display='shape')
        gscript.run_command('d.legend', raster=forms_difference, fontsize=fontsize, at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # compute the difference between the modeled and reference flow depth
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render, depth_difference+".png"), overwrite=overwrite)
        gscript.run_command('r.mapcalc', expression='{difference} = {before} - {after}'.format(before=depth_before, after=depth_after, difference=depth_difference), overwrite=overwrite)
        gscript.write_command('r.colors', map=depth_difference, rules='-', stdin=flow_difference_colors)
        gscript.run_command('d.shade', shade=relief, color=depth_difference, brighten=brighten)
        gscript.run_command('d.vect', map=contour, display='shape')
        gscript.run_command('d.legend', raster=depth_difference, fontsize=fontsize, at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # concentrated flow
        try:
            # extract concentrated flow
            gscript.run_command('r.mapcalc', expression='{concentrated_flow} = if({depth}>=0.05,{depth},null())'.format(depth=depth,concentrated_flow=concentrated_flow), overwrite=overwrite)
            gscript.write_command('r.colors', map=concentrated_flow, rules='-', stdin=depth_colors)
            gscript.run_command('r.random', input=concentrated_flow, npoints=npoints, vector=concentrated_points, overwrite=overwrite)
            gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,concentrated_flow+".png"), overwrite=overwrite)
            gscript.run_command('d.shade', shade=relief, color=concentrated_flow, brighten=brighten)
            #gscript.run_command('d.vect', map=concentrated_points, display='shape')
            gscript.run_command('d.legend', raster=concentrated_flow, fontsize=fontsize, at=legend_coord)
            gscript.run_command('d.mon', stop=driver)
        except CalledModuleError:
            print "no valleys exist in " + dem

        # peaks
        try:
            # extract peaks
            gscript.run_command('r.mapcalc', expression='{peaks} = if({forms}==2,2,null())'.format(peaks=peaks,forms=forms), overwrite=overwrite)
            gscript.run_command('r.colors', map=peaks, raster=forms)
            gscript.run_command('r.random', input=peaks, npoints=npoints, vector=peak_points, overwrite=overwrite)
            gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,peaks+".png"), overwrite=overwrite)
            gscript.run_command('d.shade', shade=relief, color=peaks, brighten=brighten)
            gscript.run_command('d.vect', map=peak_points, display='shape')
            gscript.run_command('d.legend', raster=forms, fontsize=fontsize, at=legend_coord)
            gscript.run_command('d.mon', stop=driver)
        except CalledModuleError:
            print "no peaks exist in " + dem

        # pits
        try:
            # extract pits
            gscript.run_command('r.mapcalc', expression='{pits} = if({forms}==10,10,null())'.format(pits=pits,forms=forms), overwrite=overwrite)
            gscript.run_command('r.colors', map=pits, raster=forms)
            gscript.run_command('r.random', input=pits, npoints=npoints, vector=pit_points, overwrite=overwrite)
            gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,pits+".png"), overwrite=overwrite)
            gscript.run_command('d.shade', shade=relief, color=pits, brighten=brighten)
            gscript.run_command('d.vect', map=pit_points, display='shape')
            gscript.run_command('d.legend', raster=forms, fontsize=fontsize, at=legend_coord)
            gscript.run_command('d.mon', stop=driver)
        except CalledModuleError:
            print "no pits exist in " + dem

        # ridges
        try:
            # extract ridges
            gscript.run_command('r.mapcalc', expression='{ridges} = if({forms}==3,3,null())'.format(ridges=ridges,forms=forms), overwrite=overwrite)
            gscript.run_command('r.colors', map=ridges, raster=forms)
            gscript.run_command('r.random', input=ridges, npoints=npoints, vector=ridge_points, overwrite=overwrite)
            gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,ridges+".png"), overwrite=overwrite)
            gscript.run_command('d.shade', shade=relief, color=ridges, brighten=brighten)
            gscript.run_command('d.vect', map=ridge_points, display='shape')
            gscript.run_command('d.legend', raster=forms, fontsize=fontsize, at=legend_coord)
            gscript.run_command('d.mon', stop=driver)
        except CalledModuleError:
            print "no ridges exist in " + dem

        #valleys
        try:
            # extract valleys
            gscript.run_command('r.mapcalc', expression='{valleys} = if({forms}==9,9,null())'.format(valleys=valleys,forms=forms), overwrite=overwrite)
            gscript.run_command('r.colors', map=valleys, raster=forms)
            gscript.run_command('r.random', input=valleys, npoints=npoints, vector=valley_points, overwrite=overwrite)
            gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,valleys+".png"), overwrite=overwrite)
            gscript.run_command('d.shade', shade=relief, color=valleys, brighten=brighten)
            gscript.run_command('d.vect', map=valley_points, display='shape')
            gscript.run_command('d.legend', raster=forms, fontsize=fontsize, at=legend_coord)
            gscript.run_command('d.mon', stop=driver)
        except CalledModuleError:
            print "no valleys exist in " + dem

        # print total number of cells
        univar = gscript.parse_command('r.univar', map=dem, separator='newline', flags='g')
        if 'cells' in univar:
            total_count = float(univar['cells'])
            print 'number of cell in' + dem + ': ' + str(total_count)
        else:
            print 'no non null cells exist in ' + dem

        # compute number of cells with depressions
        univar = gscript.parse_command('r.univar', map=depressions, separator='newline', flags='g')
        if 'cells' in univar:
            total_count = float(univar['cells'])
            null_count = float(univar['null_cells'])
            non_null_count = total_count - null_count
            percent = non_null_count/total_count*100
            ref_depression_cells.append(percent)
            print 'cells with depressions in ' + dem + ': ' + str(non_null_count)
            print 'percent cells with depressions in ' + dem + ': ' + str(percent)
        else:
            ref_depression_cells.append(0)
            print 'no cells with depressions exist in ' + dem

        # compute number of cells with concentrated flow
        univar = gscript.parse_command('r.univar', map=concentrated_flow, separator='newline', flags='g')
        if 'cells' in univar:
            total_count = float(univar['cells'])
            null_count = float(univar['null_cells'])
            non_null_count = total_count - null_count
            percent = non_null_count/total_count*100
            ref_flow_cells.append(percent)
            print 'cells with concentrated flow in ' + dem + ': ' + str(non_null_count)
            print 'percent cells with concentrated flow in ' + dem + ': ' + str(percent)
        else:
            ref_flow_cells.append(0)
            print 'no cells with concentrated flow exist in ' + dem

        # compute number of cells with peaks
        univar = gscript.parse_command('r.univar', map=peaks, separator='newline', flags='g')
        if 'cells' in univar:
            total_count = float(univar['cells'])
            null_count = float(univar['null_cells'])
            non_null_count = total_count - null_count
            percent = non_null_count/total_count*100
            ref_peak_cells.append(percent)
            print 'cells with peaks in ' + dem + ': ' + str(non_null_count)
            print 'percent cells with peaks in ' + dem + ': ' + str(percent)
        else:
            ref_peak_cells.append(0)
            print 'no cells with peaks exist in ' + dem

        # compute number of cells with pits
        univar = gscript.parse_command('r.univar', map=pits, separator='newline', flags='g')
        if 'cells' in univar:
            total_count = float(univar['cells'])
            null_count = float(univar['null_cells'])
            non_null_count = total_count - null_count
            percent = non_null_count/total_count*100
            ref_pit_cells.append(percent)
            print 'cells with pits in ' + dem + ': ' + str(non_null_count)
            print 'percent cells with pits in ' + dem + ': ' + str(percent)
        else:
            ref_pit_cells.append(0)
            print 'no cells with pits exist in ' + dem

        # compute number of cells with ridges
        univar = gscript.parse_command('r.univar', map=ridges, separator='newline', flags='g')
        if 'cells' in univar:
            total_count = float(univar['cells'])
            null_count = float(univar['null_cells'])
            non_null_count = total_count - null_count
            percent = non_null_count/total_count*100
            ref_ridge_cells.append(percent)
            print 'cells with ridges in ' + dem + ': ' + str(non_null_count)
            print 'percent cells with ridges in ' + dem + ': ' + str(percent)
        else:
            ref_ridge_cells.append(0)
            print 'no cells with ridges exist in ' + dem

        # compute number of cells with valleys
        univar = gscript.parse_command('r.univar', map=valleys, separator='newline', flags='g')
        if 'cells' in univar:
            total_count = float(univar['cells'])
            null_count = float(univar['null_cells'])
            non_null_count = total_count - null_count
            percent = non_null_count/total_count*100
            ref_valley_cells.append(percent)
            print 'cells with valleys in ' + dem + ': ' + str(non_null_count)
            print 'percent cells with valleys in ' + dem + ': ' + str(percent)
        else:
            ref_valley_cells.append(0)
            print 'no cells with valleys exist in ' + dem

        # try to remove mask
        try:
            gscript.run_command('r.mask', raster=mask, flags='r')
        except CalledModuleError:
            pass

        i = i + 1
        return i

def analysis(flow_cells, depression_cells, peak_cells, pit_cells, ridge_cells, valley_cells, flow_distance, peak_distance, pit_distance, ridge_distance, valley_distance):
    """compute the difference, water flow, depressions, and concentrated flow for each series of models"""

    # list reference DEMs
    dems = gscript.list_grouped('rast', pattern='dem_*')['PERMANENT']

    # iterate through reference DEMs
    for dem in dems:

        # list scanned DEMs
        dem_list = gscript.list_grouped('rast', pattern='*'+dem)[mapset]

        # variables
        region = dem
        relief = "relief"
        mask = dem.replace("dem","mask")
        contour = dem.replace("dem","contour")
        slope = dem.replace("dem","slope")
        forms = dem.replace("dem","forms")
        depth = dem.replace("dem","depth")
        mean_dem = dem.replace("dem","mean_dem")
        mean_relief = dem.replace("dem","mean_relief")
        mean_contour = dem.replace("dem","mean_contour")
        mean_slope = dem.replace("dem","mean_slope")
        mean_forms = dem.replace("dem","mean_forms")
        mean_depth = dem.replace("dem","mean_depth")
        mean_dem_before = dem
        mean_dem_after = mean_dem
        mean_dem_difference = dem.replace("dem","mean_dem_difference")
        mean_dem_regression = dem.replace("dem", "mean_dem_regression")
        mean_dem_regression_difference = dem.replace("dem", "mean_dem_regression_difference")
        mean_slope_before = slope
        mean_slope_after = mean_slope
        mean_slope_difference = dem.replace("dem","mean_slope_difference")
        mean_slope_regression = dem.replace("dem", "mean_slope_regression")
        mean_slope_regression_difference = dem.replace("dem", "mean_slope_regression_difference")
        mean_forms_before = forms
        mean_forms_after = mean_forms
        mean_forms_difference = dem.replace("dem","mean_forms_difference")
        mean_depth_before = depth
        mean_depth_after = mean_depth
        mean_depth_difference = dem.replace("dem","mean_depth_difference")
        mean_depressions = dem.replace("dem","mean_depressions")
        mean_concentrated_flow = dem.replace("dem","mean_concentrated_flow")
        mean_concentrated_points = dem.replace("dem","mean_concentrated_points")
        concentrated_points = dem.replace("dem","concentrated_points")
        copied_concentrated_points = dem.replace("dem","copied_concentrated_points")
        flow_lines = dem.replace("dem","flow_lines")
        mean_peaks = dem.replace("dem","mean_peaks")
        mean_peak_points = dem.replace("dem","mean_peak_points")
        peak_points = dem.replace("dem","peak_points")
        copied_peak_points = dem.replace("dem","copied_peak_points")
        peak_lines= dem.replace("dem","peak_lines")
        mean_pits = dem.replace("dem","mean_pits")
        mean_pit_points = dem.replace("dem","mean_pit_points")
        pit_points = dem.replace("dem","pit_points")
        copied_pit_points = dem.replace("dem","copied_pit_points")
        pit_lines = dem.replace("dem","pit_lines")
        mean_ridges = dem.replace("dem","mean_ridges")
        mean_ridge_points = dem.replace("dem","mean_ridge_points")
        ridge_points = dem.replace("dem","ridge_points")
        copied_ridge_points = dem.replace("dem","copied_ridge_points")
        ridge_lines = dem.replace("dem","ridge_lines")
        mean_valleys = dem.replace("dem","mean_valleys")
        mean_valley_points = dem.replace("dem","mean_valley_points")
        valley_points = dem.replace("dem","valley_points")
        copied_valley_points = dem.replace("dem","copied_valley_points")
        valley_lines = dem.replace("dem","valley_lines")

        # set region
        gscript.run_command('g.region', rast=region, res=res)

        # compute mean DEM
        gscript.run_command('r.series', input=dem_list, output=mean_dem, method="average", overwrite=overwrite)
        gscript.run_command('r.colors', map=mean_dem, color="elevation")
        gscript.run_command('r.relief', input=mean_dem, output=mean_relief, altitude=90, azimuth=45, zscale=1, units="intl", overwrite=overwrite)
        gscript.run_command('r.contour', input=mean_dem, output=mean_contour, step=step, overwrite=overwrite)
        info = gscript.parse_command('r.info', map=dem, flags='g')
        width=int(info.cols)+int(info.cols)/2*render_multiplier
        height=int(info.rows)*render_multiplier
        gscript.run_command('d.mon', start=driver, width=width, height=height,  output=os.path.join(render,mean_dem+".png"), overwrite=overwrite)
        gscript.run_command('d.shade', shade=mean_relief, color=mean_dem, brighten=brighten)
        gscript.run_command('d.vect', map=mean_contour, display="shape")
        gscript.run_command('d.legend', raster=mean_dem, fontsize=fontsize, at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # compute mean slope
        gscript.run_command('d.mon', start=driver, width=width, height=height,  output=os.path.join(render,mean_slope+".png"), overwrite=overwrite)
        gscript.run_command('r.param.scale', input=mean_dem, output=mean_slope, size=size, method="slope", overwrite=overwrite)
        gscript.run_command('r.colors', map=mean_slope, color="slope")
        gscript.run_command('d.shade', shade=mean_relief, color=mean_slope, brighten=brighten)
        gscript.run_command('d.vect', map=mean_contour, display='shape')
        gscript.run_command('d.legend', raster=mean_slope, fontsize=fontsize, at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        #compute mean geomorphon
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,mean_forms+".png"), overwrite=overwrite)
        gscript.run_command('r.geomorphon', dem=mean_dem, forms=mean_forms, search=search, skip=skip, overwrite=overwrite)
        gscript.run_command('d.shade', shade=mean_relief, color=mean_forms, brighten=brighten)
        gscript.run_command('d.vect', map=mean_contour, display='shape')
        gscript.run_command('d.legend', raster=mean_forms, fontsize=fontsize, at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # simulate water flow
        gscript.run_command('d.mon', start=driver, width=width, height=height,  output=os.path.join(render,mean_depth+".png"), overwrite=overwrite)
        gscript.run_command('r.slope.aspect', elevation=mean_dem, dx='dx', dy='dy', overwrite=overwrite)
        gscript.run_command('r.sim.water', elevation=mean_dem, dx='dx', dy='dy', rain_value=rain_value, depth=mean_depth, nwalkers=nwalkers, niterations=niterations, overwrite=overwrite)
        gscript.run_command('g.remove', flags='f', type='raster', name=['dx', 'dy'])
        gscript.run_command('d.shade', shade=mean_relief, color=mean_depth, brighten=brighten)
        gscript.run_command('d.vect', map=mean_contour, display='shape')
        gscript.run_command('d.legend', raster=mean_depth, fontsize=fontsize, at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # check if mask needed
        find_mask = gscript.find_file(mask, element = 'cell')
        if find_mask['name']:
            gscript.run_command('r.mask', raster=mask, overwrite=overwrite)

        # identify mean depressions
        gscript.run_command('r.fill.dir', input=mean_dem, output='depressionless_dem', direction='flow_dir',overwrite=overwrite)
        gscript.run_command('r.mapcalc', expression='{depressions} = if({depressionless_dem} - {dem} > {depth}, {depressionless_dem} - {dem}, null())'.format(depressions=mean_depressions, depressionless_dem='depressionless_dem', dem=mean_dem, depth=0), overwrite=overwrite)
        gscript.write_command('r.colors', map=mean_depressions, rules='-', stdin=depressions_colors)
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,mean_depressions+".png"), overwrite=overwrite)
        gscript.run_command('d.shade', shade=mean_relief, color=mean_depressions, brighten=brighten)
        gscript.run_command('d.vect', map=mean_contour, display='shape')
        gscript.run_command('d.legend', raster=mean_depressions, fontsize=fontsize, at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # compute the difference between the mean and reference elevation
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,mean_dem_difference+".png"), overwrite=overwrite)
        gscript.run_command('r.mapcalc', expression='{difference} = {before} - {after}'.format(before=mean_dem_before,after=mean_dem_after,difference=mean_dem_difference), overwrite=overwrite)
        gscript.write_command('r.colors', map=mean_dem_difference, rules='-', stdin=dem_difference_colors)
        gscript.run_command('d.shade', shade=mean_relief, color=mean_dem_difference, brighten=brighten)
        gscript.run_command('d.vect', map=mean_contour, display='shape')
        gscript.run_command('d.legend', raster=mean_dem_difference, fontsize=fontsize, at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # compute the linearly regressed difference between the modeled and reference elevation
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render, mean_dem_regression_difference+".png"), overwrite=overwrite)
        regression_params = gscript.parse_command('r.regression.line', flags='g', mapx=mean_dem_before, mapy=mean_dem_after, overwrite=overwrite)
        gscript.run_command('r.mapcalc', expression='{regression} = {a} + {b} * {before}'.format(a=regression_params['a'], b=regression_params['b'], before=mean_dem_before, regression=mean_dem_regression), overwrite=overwrite)
        gscript.run_command('r.mapcalc', expression='{difference} = {regression} - {after}'.format(regression=mean_dem_regression, after=mean_dem_after, difference=mean_dem_regression_difference), overwrite=overwrite)
        gscript.write_command('r.colors', map=mean_dem_regression_difference, rules='-', stdin=dem_difference_colors)
        gscript.run_command('d.shade', shade=relief, color=mean_dem_regression_difference, brighten=brighten)
        gscript.run_command('d.vect', map=contour, display='shape')
        gscript.run_command('d.legend', raster=mean_dem_regression_difference, fontsize=fontsize, at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # compute the difference between the mean and reference slope
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render, mean_slope_difference+".png"), overwrite=overwrite)
        gscript.run_command('r.mapcalc', expression='{difference} = {before} - {after}'.format(before=mean_slope_before,after=mean_slope_after,difference=mean_slope_difference), overwrite=overwrite)
        gscript.write_command('r.colors', map=mean_slope_difference, rules='-', stdin=slope_difference_colors)
        gscript.run_command('d.shade', shade=mean_relief, color=mean_slope_difference, brighten=brighten)
        gscript.run_command('d.vect', map=mean_contour, display='shape')
        gscript.run_command('d.legend', raster=mean_slope_difference, fontsize=fontsize, at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # compute the difference between the modeled and reference slope of the regressed mean elevation
        gscript.run_command('r.param.scale',
                            input=mean_dem_regression, output=mean_slope_regression,
                            size=size,
                            method="slope",
                            overwrite=overwrite)
        gscript.run_command('r.colors',
                            map=mean_slope_regression,
                            color="slope")
        gscript.run_command('d.mon',
                            start=driver,
                            width=width,
                            height=height,
                            output=os.path.join(render, mean_slope_regression_difference+".png"),
                            overwrite=overwrite)
        gscript.run_command('r.mapcalc',
                            expression='{difference} = {before} - {after}'.format(
                            before=mean_slope_before,
                            after=mean_slope_regression,
                            difference=mean_slope_regression_difference),
                            overwrite=overwrite)
        gscript.write_command('r.colors',
                              map=mean_slope_regression_difference,
                              rules='-',
                              stdin=slope_difference_colors)
        gscript.run_command('d.shade',
                            shade=relief,
                            color=mean_slope_regression_difference,
                            brighten=brighten)
        gscript.run_command('d.vect',
                            map=contour,
                            display='shape')
        gscript.run_command('d.legend',
                            raster=mean_slope_regression_difference,
                            fontsize=fontsize,
                            at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # compute the difference between the mean and reference landorms
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render, mean_forms_difference+".png"), overwrite=overwrite)
        gscript.run_command('r.mapcalc', expression='{difference} = {before} - {after}'.format(before=mean_forms_before,after=mean_forms_after,difference=mean_forms_difference), overwrite=overwrite)
        gscript.write_command('r.colors', map=mean_forms_difference, rules='-', stdin=forms_difference_colors)
        gscript.run_command('d.shade', shade=mean_relief, color=mean_forms_difference, brighten=brighten)
        gscript.run_command('d.vect', map=mean_contour, display='shape')
        gscript.run_command('d.legend', raster=mean_forms_difference, fontsize=fontsize, at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # compute the difference between the mean and reference flow depth
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render, mean_depth_difference+".png"), overwrite=overwrite)
        gscript.run_command('r.mapcalc', expression='{difference} = {before} - {after}'.format(before=mean_depth_before,after=mean_depth_after,difference=mean_depth_difference), overwrite=overwrite)
        gscript.write_command('r.colors', map=mean_depth_difference, rules='-', stdin=flow_difference_colors)
        gscript.run_command('d.shade', shade=mean_relief, color=mean_depth_difference, brighten=brighten)
        gscript.run_command('d.vect', map=mean_contour, display='shape')
        gscript.run_command('d.legend', raster=mean_depth_difference, fontsize=fontsize, at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # mean concentrated flow
        try:
            # extract mean concentrated flow
            gscript.run_command('r.mapcalc', expression='{concentrated_flow} = if({depth}>=0.05,{depth},null())'.format(depth=mean_depth,concentrated_flow=mean_concentrated_flow), overwrite=overwrite)
            gscript.write_command('r.colors', map=mean_concentrated_flow, rules='-', stdin=depth_colors)
            gscript.run_command('r.random', input=mean_concentrated_flow, npoints=npoints, vector=mean_concentrated_points, overwrite=overwrite)
            # distance from reference
            gscript.run_command('g.copy', vector=[concentrated_points, copied_concentrated_points], overwrite=overwrite)
            gscript.run_command('v.db.addcolumn', map=copied_concentrated_points, columns='distance INTEGER', overwrite=overwrite)
            gscript.run_command('v.distance', from_=copied_concentrated_points, to=mean_concentrated_points, upload='dist', column='distance', output=flow_lines, separator='newline', overwrite=overwrite)
            univar_distance = gscript.parse_command('v.db.univar', map=copied_concentrated_points, column='distance', flags='g', overwrite=overwrite)
            # collect stats
            dist = float(univar_distance['sum'])
            flow_distance.append(dist)
            print 'sum of min flow distance in ' + dem + ': ' + str(dist)
            mean_dist = float(univar_distance['mean'])
            print 'mean of min flow distance in ' + dem +': ' + str(mean_dist)
            # render
            gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,mean_concentrated_flow+".png"), overwrite=overwrite)
            gscript.run_command('d.shade', shade=relief, color=mean_depth_difference, brighten=brighten)
            gscript.run_command('d.vect', map=contour, display='shape')
            gscript.run_command('d.vect', map=concentrated_points, display='shape', color='blue')
            gscript.run_command('d.vect', map=mean_concentrated_points, display='shape', color='red')
            gscript.run_command('d.vect', map=flow_lines, display='shape')
            gscript.run_command('d.legend', raster=mean_depth_difference, fontsize=fontsize, at=legend_coord)
            gscript.run_command('d.mon', stop=driver)
        except CalledModuleError:
            gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,mean_concentrated_flow+".png"), overwrite=overwrite)
            gscript.run_command('d.shade', shade=relief, color=mean_depth_difference, brighten=brighten)
            gscript.run_command('d.vect', map=contour, display='shape')
            gscript.run_command('d.legend', raster=mean_depth_difference, fontsize=fontsize, at=legend_coord)
            gscript.run_command('d.mon', stop=driver)
            flow_distance.append(0)
            print "no concentrated flow exist in " + dem

        # mean peaks
        try:
            # extract mean peaks
            gscript.run_command('r.mapcalc', expression='{peaks} = if({forms}==2,2,null())'.format(peaks=mean_peaks,forms=mean_forms), overwrite=overwrite)
            gscript.run_command('r.colors', map=mean_peaks, raster=mean_forms)
            gscript.run_command('r.random', input=mean_peaks, npoints=npoints, vector=mean_peak_points, overwrite=overwrite)
            # distance from reference
            gscript.run_command('g.copy', vector=[peak_points, copied_peak_points], overwrite=overwrite)
            gscript.run_command('v.db.addcolumn', map=copied_peak_points, columns='distance INTEGER', overwrite=overwrite)
            gscript.run_command('v.distance', from_=copied_peak_points, to=mean_peak_points, upload='dist', column='distance', output=peak_lines, separator='newline', overwrite=overwrite)
            univar_distance = gscript.parse_command('v.db.univar', map=copied_peak_points, column='distance', flags='g', overwrite=overwrite)
            # collect stats
            dist = float(univar_distance['sum'])
            peak_distance.append(dist)
            print 'sum of min peak distance in ' + dem + ': ' + str(dist)
            mean_dist = float(univar_distance['mean'])
            print 'mean of min peak distance in ' + dem + ': ' + str(mean_dist)
            # render
            gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,mean_peaks+".png"), overwrite=overwrite)
            gscript.run_command('d.shade', shade=relief, color=mean_forms_difference, brighten=brighten)
            gscript.run_command('d.vect', map=contour, display='shape')
            gscript.run_command('d.vect', map=peak_points, display='shape', color='blue')
            gscript.run_command('d.vect', map=mean_peak_points, display='shape', color='red')
            gscript.run_command('d.vect', map=peak_lines, display='shape')
            gscript.run_command('d.legend', raster=mean_forms_difference, fontsize=fontsize, at=legend_coord)
            gscript.run_command('d.mon', stop=driver)
        except CalledModuleError:
            gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,mean_peaks+".png"), overwrite=overwrite)
            gscript.run_command('d.shade', shade=relief, color=mean_forms_difference, brighten=brighten)
            gscript.run_command('d.vect', map=contour, display='shape')
            gscript.run_command('d.legend', raster=mean_forms_difference, fontsize=fontsize, at=legend_coord)
            gscript.run_command('d.mon', stop=driver)
            peak_distance.append(0)
            print "no peaks exist in " + dem

        # mean pits
        try:
            #extract mean pits
            gscript.run_command('r.mapcalc', expression='{pits} = if({forms}==10,10,null())'.format(pits=mean_pits,forms=mean_forms), overwrite=overwrite)
            gscript.run_command('r.colors', map=mean_pits, raster=mean_forms)
            gscript.run_command('r.random', input=mean_pits, npoints=npoints, vector=mean_pit_points, overwrite=overwrite)
            # distance from reference
            gscript.run_command('g.copy', vector=[pit_points, copied_pit_points], overwrite=overwrite)
            gscript.run_command('v.db.addcolumn', map=copied_pit_points, columns='distance INTEGER', overwrite=overwrite)
            gscript.run_command('v.distance', from_=copied_pit_points, to=mean_pit_points, upload='dist', column='distance', output=pit_lines, separator='newline', overwrite=overwrite)
            univar_distance = gscript.parse_command('v.db.univar', map=copied_pit_points, column='distance', flags='g', overwrite=overwrite)
            # collect stats
            dist = float(univar_distance['sum'])
            pit_distance.append(dist)
            print 'sum of min pit distance in ' + dem + ': ' + str(dist)
            mean_dist = float(univar_distance['mean'])
            print 'mean of min pit distance in ' + dem + ': ' + str(mean_dist)
            # render
            gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,mean_pits+".png"), overwrite=overwrite)
            gscript.run_command('d.shade', shade=relief, color=mean_forms_difference, brighten=brighten)
            gscript.run_command('d.vect', map=contour, display='shape')
            gscript.run_command('d.vect', map=pit_points, display='shape', color='blue')
            gscript.run_command('d.vect', map=mean_pit_points, display='shape', color='red')
            gscript.run_command('d.vect', map=pit_lines, display='shape')
            gscript.run_command('d.legend', raster=mean_forms_difference, fontsize=fontsize, at=legend_coord)
            gscript.run_command('d.mon', stop=driver)
        except CalledModuleError:
            gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,mean_pits+".png"), overwrite=overwrite)
            gscript.run_command('d.shade', shade=relief, color=mean_forms_difference, brighten=brighten)
            gscript.run_command('d.vect', map=contour, display='shape')
            gscript.run_command('d.legend', raster=mean_forms_difference, fontsize=fontsize, at=legend_coord)
            gscript.run_command('d.mon', stop=driver)
            pit_distance.append(0)
            print "no pits exist in " + dem

        # mean ridges
        try:
            # extract mean ridges
            gscript.run_command('r.mapcalc', expression='{ridges} = if({forms}==3,3,null())'.format(ridges=mean_ridges,forms=mean_forms), overwrite=overwrite)
            gscript.run_command('r.colors', map=mean_ridges, raster=mean_forms)
            gscript.run_command('r.random', input=mean_ridges, npoints=npoints, vector=mean_ridge_points, overwrite=overwrite)
            # distance from reference
            gscript.run_command('g.copy', vector=[ridge_points, copied_ridge_points], overwrite=overwrite)
            gscript.run_command('v.db.addcolumn', map=copied_ridge_points, columns='distance INTEGER', overwrite=overwrite)
            gscript.run_command('v.distance', from_=copied_ridge_points, to=mean_ridge_points, upload='dist', column='distance', output=ridge_lines, separator='newline', overwrite=overwrite)
            univar_distance = gscript.parse_command('v.db.univar', map=copied_ridge_points, column='distance', flags='g', overwrite=overwrite)
            # collect stats
            dist = float(univar_distance['sum'])
            ridge_distance.append(dist)
            print 'sum of min ridge distance in ' + dem + ': ' + str(dist)
            mean_dist = float(univar_distance['mean'])
            print 'mean of min ridge distance in ' + dem + ': ' + str(mean_dist)
            # render
            gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,mean_ridges+".png"), overwrite=overwrite)
            gscript.run_command('d.shade', shade=relief, color=mean_forms_difference, brighten=brighten)
            gscript.run_command('d.vect', map=contour, display='shape')
            gscript.run_command('d.vect', map=ridge_points, display='shape', color='blue')
            gscript.run_command('d.vect', map=mean_ridge_points, display='shape', color='red')
            gscript.run_command('d.vect', map=ridge_lines, display='shape')
            gscript.run_command('d.legend', raster=mean_forms_difference, fontsize=fontsize, at=legend_coord)
            gscript.run_command('d.mon', stop=driver)
        except CalledModuleError:
            gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,mean_ridges+".png"), overwrite=overwrite)
            gscript.run_command('d.shade', shade=relief, color=mean_forms_difference, brighten=brighten)
            gscript.run_command('d.vect', map=contour, display='shape')
            gscript.run_command('d.legend', raster=mean_forms_difference, fontsize=fontsize, at=legend_coord)
            gscript.run_command('d.mon', stop=driver)
            ridge_distance.append(0)
            print "no ridges exist in " + dem

        # mean valleys
        try:
            # extract mean valleys
            gscript.run_command('r.mapcalc', expression='{valleys} = if({forms}==9,9,null())'.format(valleys=mean_valleys,forms=mean_forms), overwrite=overwrite)
            gscript.run_command('r.colors', map=mean_valleys, raster=mean_forms)
            gscript.run_command('r.random', input=mean_valleys, npoints=npoints, vector=mean_valley_points, overwrite=overwrite)
            # distance from reference
            gscript.run_command('g.copy', vector=[valley_points, copied_valley_points], overwrite=overwrite)
            gscript.run_command('v.db.addcolumn', map=copied_valley_points, columns='distance INTEGER', overwrite=overwrite)
            gscript.run_command('v.distance', from_=copied_valley_points, to=mean_valley_points, upload='dist', column='distance', output=valley_lines, separator='newline', overwrite=overwrite)
            univar_distance = gscript.parse_command('v.db.univar', map=copied_valley_points, column='distance', flags='g', overwrite=overwrite)
            # collect stats
            dist = float(univar_distance['sum'])
            valley_distance.append(dist)
            print 'sum of min valley distance in ' + dem + ': ' + str(dist)
            mean_dist = float(univar_distance['mean'])
            print 'mean of min valley distance in ' + dem + ': ' + str(mean_dist)
            # render
            gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,mean_valleys+".png"), overwrite=overwrite)
            gscript.run_command('d.shade', shade=relief, color=mean_forms_difference, brighten=brighten)
            gscript.run_command('d.vect', map=contour, display='shape')
            gscript.run_command('d.vect', map=valley_points, display='shape', color='blue')
            gscript.run_command('d.vect', map=mean_valley_points, display='shape', color='red')
            gscript.run_command('d.vect', map=valley_lines, display='shape')
            gscript.run_command('d.legend', raster=mean_forms_difference, fontsize=fontsize, at=legend_coord)
            gscript.run_command('d.mon', stop=driver)
        except CalledModuleError:
            gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,mean_valleys+".png"), overwrite=overwrite)
            gscript.run_command('d.shade', shade=relief, color=mean_forms_difference, brighten=brighten)
            gscript.run_command('d.vect', map=contour, display='shape')
            gscript.run_command('d.legend', raster=mean_forms_difference, fontsize=fontsize, at=legend_coord)
            gscript.run_command('d.mon', stop=driver)
            valley_distance.append(0)
            print "no valleys exist in " + dem

        # compute number of cells with mean depressions
        univar = gscript.parse_command('r.univar', map=mean_depressions, separator='newline', flags='g')
        if 'cells' in univar:
            total_count = float(univar['cells'])
            null_count = float(univar['null_cells'])
            non_null_count = total_count - null_count
            percent = non_null_count/total_count*100
            depression_cells.append(percent)
            print 'cells in ' + dem + ' with depressions: ' + str(non_null_count)
            print 'percent cells in ' + dem + ' with depressions: ' + str(percent)
        else:
            depression_cells.append(0)
            print 'no cells in ' + dem

        # compute number of cells with concentrated flow
        univar = gscript.parse_command('r.univar', map=mean_concentrated_flow, separator='newline', flags='g')
        if 'cells' in univar:
            total_count = float(univar['cells'])
            null_count = float(univar['null_cells'])
            non_null_count = total_count - null_count
            percent = non_null_count/total_count*100
            flow_cells.append(percent)
            print 'cells in ' + dem + ' with concentrated flow: ' + str(non_null_count)
            print 'percent cells in ' + dem + ' with concentrated flow: ' + str(percent)
        else:
            flow_cells.append(0)
            print 'no cells in ' + dem

        # compute number of cells with mean peaks
        univar = gscript.parse_command('r.univar', map=mean_peaks, separator='newline', flags='g')
        if 'cells' in univar:
            total_count = float(univar['cells'])
            null_count = float(univar['null_cells'])
            non_null_count = total_count - null_count
            percent = non_null_count/total_count*100
            peak_cells.append(percent)
            print 'cells with peaks in ' + dem + ': ' + str(non_null_count)
            print 'percent cells with peaks in ' + dem + ': ' + str(percent)
        else:
            peak_cells.append(0)
            print 'no cells with peaks exist in ' + dem

        # compute number of cells with mean pits
        univar = gscript.parse_command('r.univar', map=mean_pits, separator='newline', flags='g')
        if 'cells' in univar:
            total_count = float(univar['cells'])
            null_count = float(univar['null_cells'])
            non_null_count = total_count - null_count
            percent = non_null_count/total_count*100
            pit_cells.append(percent)
            print 'cells with pits in ' + dem + ': ' + str(non_null_count)
            print 'percent cells with pits in ' + dem + ': ' + str(percent)
        else:
            pit_cells.append(0)
            print 'no cells with pits exist in ' + dem

        # compute number of cells with mean ridges
        univar = gscript.parse_command('r.univar', map=mean_ridges, separator='newline', flags='g')
        if 'cells' in univar:
            total_count = float(univar['cells'])
            null_count = float(univar['null_cells'])
            non_null_count = total_count - null_count
            percent = non_null_count/total_count*100
            ridge_cells.append(percent)
            print 'cells with ridges in ' + dem + ': ' + str(non_null_count)
            print 'percent cells with ridges in ' + dem + ': ' + str(percent)
        else:
            print 'no cells with ridges exist in ' + dem

        # compute number of cells with mean valleys
        univar = gscript.parse_command('r.univar', map=mean_valleys, separator='newline', flags='g')
        if 'cells' in univar:
            total_count = float(univar['cells'])
            null_count = float(univar['null_cells'])
            non_null_count = total_count - null_count
            percent = non_null_count/total_count*100
            valley_cells.append(percent)
            print 'cells with valleys in ' + dem + ': ' + str(non_null_count)
            print 'percent cells with valleys in ' + dem + ': ' + str(percent)
        else:
            valley_cells.append(0)
            print 'no cells with valleys exist in ' + dem

        # try to remove mask
        try:
            gscript.run_command('r.mask', raster=mask, flags='r')
        except CalledModuleError:
            pass

def write_results(i,
                  ref_flow_cells,
                  ref_depression_cells,
                  ref_peak_cells,
                  ref_pit_cells,
                  ref_ridge_cells,
                  ref_valley_cells,
                  flow_cells,
                  depression_cells,
                  peak_cells,
                  pit_cells,
                  ridge_cells,
                  valley_cells,
                  flow_distance,
                  peak_distance,
                  pit_distance,
                  ridge_distance,
                  valley_distance):
    """plot the percent of cells with depressions and the minumum distance of mean concentrated flow points from the reference for each experiment"""

    # write to csv file
    with open(cells, 'wb') as csvfile:
        cells_writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

        cells_writer.writerow(['ref_flow_cells', 'ref_depression_cells', 'ref_peak_cells', 'ref_pit_cells', 'ref_ridge_cells', 'ref_valley_cells', 'flow_cells', 'depression_cells', 'peak_cells', 'pit_cells', 'ridge_cells', 'valley_cells'])

        for x in xrange(i):
            cells_writer.writerow([ref_flow_cells[x], ref_depression_cells[x], ref_peak_cells[x], ref_pit_cells[x], ref_ridge_cells[x], ref_valley_cells[x], flow_cells[x], depression_cells[x], peak_cells[x], pit_cells[x], ridge_cells[x], valley_cells[x]])


if __name__ == "__main__":
    atexit.register(cleanup)
    sys.exit(main())
