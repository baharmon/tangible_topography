#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@brief: spatial analysis for the tangible topography experiment

This program is free software under the GNU General Public License (>=v2).
"""

import os
import sys
import csv
import atexit
import grass.script as gscript
from grass.exceptions import CalledModuleError
# import matplotlib.pyplot as plt

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

# set rendering directories
render = os.path.join(gisdbase, location, "render", mapset)
render_3d = os.path.join(gisdbase, location, "render_3d", mapset)

# csv path
cells = os.path.join(render, 'cells.csv')

# set variables
res = 3  # resolution of the region
npoints = "100%"  # percent of points for random resampling
rain_value = 300  # rain in mm/hr for r.sim.water
niterations = 4  # number of iterations for r.sim.water
nwalkers = 5000  # number of walkers for r.sim.water
step = 5  # contour interval
search = 9  # search size for r.geomorphon
skip = 6  # skip distance for r.geomorphon
size = 9  # moving window size for r.param.scale
brighten = 75  # percent brightness of shaded relief
render_multiplier = 3  # multiplier for rendering size
whitespace = 3
fontsize = 9 * render_multiplier  # legend font size
legend_coord = (10, 50, 1, 4)  # legend display coordinates

# 3d variables
color_3d = "192:192:192"
res_3d = 1
height_3d = 2000
perspective = 25
light_position = (0.68, -0.68, 0.95)
fringe = "ne"
fringe_elevation = 250
format_3d = "tif"
size_3d = (1000, 1000)
vpoint_size = 4
vpoint_marker = "x"
vpoint_color = "red"
vline_width = 2
vline_color = "black"
# arrow_position = (100, 100)
# arrow_size = 100

# set color rules
depressions_colors = """\
0% aqua
100% blue
nv white
default white
"""

depth_colors = """\
0 255:255:255
0.001 255:255:0
0.05 0:255:255
0.1 0:127:255
0.5 0:0:255
100% 0:0:0
nv white
default white
"""

dem_difference_colors = """\
-36 red
0 white
36 blue
nv white
default white
"""

flow_difference_colors = """\
-0.5 red
0 192:192:192
0.5 blue
nv white
default white
"""

slope_difference_colors = """\
30 blue
0 192:192:192
-30 red
nv 192:192:192
default 192:192:192
"""

forms_difference_colors = """\
10 blue
0 192:192:192
-10 red
nv 192:192:192
default 192:192:192
"""

stdev_dem_difference_colors = """\
nv 192:192:192
default 192:192:192
0 247:252:253
4 224:236:244
8 191:211:230
12 158:188:218
16 140:150:198
20 140:107:177
24 136:65:157
28 129:15:124
32 77:0:75
"""

stdev_dem_regression_difference_colors = """\
nv 192:192:192
default 192:192:192
0 247:252:253
3 224:236:244
6 191:211:230
9 158:188:218
12 140:150:198
15 140:107:177
18 136:65:157
21 129:15:124
24 77:0:75
"""

stdev_slope_difference_colors = """\
45 blue
0 white
-45 red
nv white
default white
"""

# 3d color rules with null values and default set to light gray
dem_colors_3d = """\
0% 0:191:191
20% 0:255:0
40% 255:255:0
60% 255:127:0
80% 191:127:63
100% 200:200:200
nv 192:192:192
default 192:192:192
"""

slope_colors_3d = """\
0 192:192:192
2 255:255:0
5 0:255:0
10 0:255:255
15 0:0:255
30 255:0:255
50 255:0:0
90 0:0:0
nv 192:192:192
default 192:192:192
"""

depressions_colors_3d = """\
0% aqua
100% blue
nv 192:192:192
default 192:192:192
"""

depth_colors_3d = """\
0 192:192:192
0.001 255:255:0
0.05 0:255:255
0.1 0:127:255
0.5 0:0:255
100% 0:0:0
nv 192:192:192
default 192:192:192
"""

forms_colors_3d = """\
0 192:192:192
1 220:220:220
2 56:0:0
3 200:0:0
4 255:80:20
5 250:210:60
6 255:255:60
7 180:230:20
8 60:250:150
9 0:0:255
10 0:0:56
11 255:0:255
nv 192:192:192
default 192:192:192
"""

dem_difference_colors_3d = """\
42 blue
0 192:192:192
-42 red
nv 192:192:192
default 192:192:192
"""

dem_regression_difference_colors_3d = """\
36 blue
0 192:192:192
-36 red
nv 192:192:192
default 192:192:192
"""

flow_difference_colors_3d = """\
0.5 blue
0 192:192:192
-0.5 red
nv 192:192:192
default 192:192:192
"""

slope_difference_colors_3d = """\
30 blue
0 192:192:192
-30 red
nv 192:192:192
default 192:192:192
"""

forms_difference_colors_3d = """\
10 blue
0 192:192:192
-10 red
nv 192:192:192
default 192:192:192
"""

stdev_colors_3d = """\
nv 192:192:192
default 192:192:192
0 247:252:253
4 224:236:244
8 191:211:230
12 158:188:218
16 140:150:198
20 140:107:177
24 136:65:157
28 129:15:124
32 77:0:75
"""

stdev_diff_colors_3d = """\
nv 192:192:192
default 192:192:192
0 247:252:253
3 224:236:244
6 191:211:230
9 158:188:218
12 140:150:198
15 140:107:177
18 136:65:157
21 129:15:124
24 77:0:75
"""

def main():

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

    reference(ref_flow_cells,
        ref_depression_cells,
        ref_peak_cells,
        ref_pit_cells,
        ref_ridge_cells,
        ref_valley_cells)

    mean_analysis(flow_cells,
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

    stdev_analysis()

    render_3d_images()

    write_results(ref_flow_cells,
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
            name=['depressionless_dem', 'flow_dir', 'dx', 'dy', 'a', 'b', 'regression'],
            flags='f')
    except CalledModuleError:
        pass

    try:
        # remove mask
        gscript.run_command('r.mask', raster='MASK', flags='r')
    except CalledModuleError:
        pass

def reference(ref_flow_cells, ref_depression_cells, ref_peak_cells, ref_pit_cells, ref_ridge_cells, ref_valley_cells):
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

        # render elevation
        info = gscript.parse_command('r.info',
            map=dem,
            flags='g')
        width = int(info.cols)+int(info.cols)/2*render_multiplier*whitespace
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
        gscript.run_command('r.contour',
            input=dem,
            output=contour,
            step=step,
            overwrite=overwrite)
        gscript.run_command('d.shade',
            shade=relief,
            color=dem,
            brighten=brighten)
        gscript.run_command('d.vect', map=contour, display="shape")
        gscript.run_command('d.legend',
            raster=dem,
            fontsize=fontsize,
            at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # compute the difference between the modeled and reference elevation
        gscript.run_command('d.mon',
            start=driver,
            width=width,
            height=height,
            output=os.path.join(render, dem_difference+".png"),
            overwrite=overwrite)
        gscript.run_command('r.mapcalc',
            expression='{difference} = {before} - {after}'.format(before=dem_before,
                after=dem_after,
                difference=dem_difference),
            overwrite=overwrite)
        gscript.write_command('r.colors',
            map=dem_difference,
            rules='-',
            stdin=dem_difference_colors)
        gscript.run_command('d.vect', map=contour, display='shape')
        gscript.run_command('d.legend',
            raster=dem_difference,
            fontsize=fontsize,
            at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # compute the difference between the modeled and reference elevation with linear regression
        gscript.run_command('d.mon',
            start=driver,
            width=width,
            height=height,
            output=os.path.join(render, dem_regression_difference+".png"),
            overwrite=overwrite)
        regression_params = gscript.parse_command('r.regression.line',
            flags='g',
            mapx=dem_before,
            mapy=dem_after,
            overwrite=overwrite)
        gscript.run_command('r.mapcalc',
            expression='{regression} = {a} + {b} * {before}'.format(a=regression_params['a'],
                b=regression_params['b'],
                before=dem_before,
                regression=dem_regression),
            overwrite=overwrite)
        gscript.run_command('r.mapcalc',
            expression='{difference} = {regression} - {after}'.format(regression=dem_regression,
                after=dem_after,
                difference=dem_regression_difference),
            overwrite=overwrite)
        gscript.write_command('r.colors',
            map=dem_regression_difference,
            rules='-',
            stdin=dem_difference_colors)
        gscript.run_command('d.vect', map=contour, display='shape')
        gscript.run_command('d.legend',
            raster=dem_regression_difference,
            fontsize=fontsize,
            at=legend_coord)
        gscript.run_command('d.mon',
            stop=driver)

        # check if mask needed
        find_mask = gscript.find_file(mask,
            element='cell')
        if find_mask['name']:
            gscript.run_command('r.mask',
                raster=mask,
                overwrite=overwrite)

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

        # compute the difference between the modeled and reference slope
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render, slope_difference+".png"), overwrite=overwrite)
        gscript.run_command('r.mapcalc', expression='{difference} = {before} - {after}'.format(before=slope_before, after=slope_after, difference=slope_difference), overwrite=overwrite)
        gscript.write_command('r.colors', map=slope_difference, rules='-', stdin=slope_difference_colors)
        gscript.run_command('d.vect', map=contour, display='shape')
        gscript.run_command('d.legend', raster=slope_difference, fontsize=fontsize, at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        #compute landforms
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
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render, depressions+".png"), overwrite=overwrite)
        gscript.run_command('r.fill.dir', input=dem, output='depressionless_dem', direction='flow_dir', overwrite=overwrite)
        gscript.run_command('r.mapcalc', expression='{depressions} = if({depressionless_dem} - {dem} > {depth}, {depressionless_dem} - {dem}, null())'.format(depressions=depressions, depressionless_dem='depressionless_dem', dem=dem, depth=0), overwrite=overwrite)
        gscript.write_command('r.colors', map=depressions, rules='-', stdin=depressions_colors)
        gscript.run_command('d.shade', shade=relief, color=depressions, brighten=brighten)
        gscript.run_command('d.vect', map=contour, display='shape')
        gscript.run_command('d.legend', raster=depressions, fontsize=fontsize, at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # compute the difference between the modeled and reference landorms
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render, forms_difference+".png"), overwrite=overwrite)
        gscript.run_command('r.mapcalc', expression='{difference} = {before} - {after}'.format(before=forms_before, after=forms_after, difference=forms_difference), overwrite=overwrite)
        gscript.write_command('r.colors', map=forms_difference, rules='-', stdin=forms_difference_colors)
        gscript.run_command('d.vect', map=contour, display='shape')
        gscript.run_command('d.legend', raster=forms_difference, fontsize=fontsize, at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # compute the difference between the modeled and reference flow depth
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render, depth_difference+".png"), overwrite=overwrite)
        gscript.run_command('r.mapcalc', expression='{difference} = {before} - {after}'.format(before=depth_before, after=depth_after, difference=depth_difference), overwrite=overwrite)
        gscript.write_command('r.colors', map=depth_difference, rules='-', stdin=flow_difference_colors)
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
            gscript.run_command('d.vect', map=contour, display='shape')
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
            gscript.run_command('d.vect', map=contour, display='shape')
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
            gscript.run_command('d.vect', map=contour, display='shape')
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
            gscript.run_command('d.vect', map=contour, display='shape')
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
            gscript.run_command('d.vect', map=contour, display='shape')
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
            gscript.run_command('r.mask', flags='r')
        except CalledModuleError:
            pass

def mean_analysis(flow_cells, depression_cells, peak_cells, pit_cells, ridge_cells, valley_cells, flow_distance, peak_distance, pit_distance, ridge_distance, valley_distance):
    """compute the difference, water flow, depressions, and concentrated flow for each series of models"""

    # list reference DEMs
    dems = gscript.list_grouped('rast', pattern='dem_*')['PERMANENT']

    # iterate through reference DEMs
    for dem in dems:

        # list scanned DEMs
        dem_list = gscript.list_grouped('rast', pattern='*'+dem)[mapset]

        # variables
        region = dem
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

        # compute mean elevation
        gscript.run_command('r.series',
            input=dem_list,
            output=mean_dem,
            method="average",
            overwrite=overwrite)
        gscript.run_command('r.colors',
            map=mean_dem, color="elevation")
        gscript.run_command('r.relief',
            input=mean_dem,
            output=mean_relief,
            altitude=90,
            azimuth=45,
            zscale=1,
            units="intl",
            overwrite=overwrite)
        gscript.run_command('r.contour',
            input=mean_dem,
            output=mean_contour,
            step=step,
            overwrite=overwrite)
        info = gscript.parse_command('r.info', map=dem, flags='g')
        width=int(info.cols)+int(info.cols)/2*render_multiplier*whitespace
        height=int(info.rows)*render_multiplier
        gscript.run_command('d.mon',
            start=driver,
            width=width,
            height=height,
            output=os.path.join(render,mean_dem+".png"),
            overwrite=overwrite)
        gscript.run_command('d.shade',
            shade=mean_relief,
            color=mean_dem,
            brighten=brighten)
        gscript.run_command('d.vect', map=mean_contour, display="shape")
        gscript.run_command('d.legend',
            raster=mean_dem,
            fontsize=fontsize,
            at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # check if mask needed
        find_mask = gscript.find_file(mask, element = 'cell')
        if find_mask['name']:
            gscript.run_command('r.mask', raster=mask, overwrite=overwrite)

        # compute the difference between the mean and reference elevation
        gscript.run_command('d.mon',
            start=driver,
            width=width,
            height=height,
            output=os.path.join(render,mean_dem_difference+".png"),
            overwrite=overwrite)
        gscript.run_command('r.mapcalc',
            expression='{difference} = {before} - {after}'.format(before=mean_dem_before,
                after=mean_dem_after,
                difference=mean_dem_difference),
            overwrite=overwrite)
        gscript.write_command('r.colors',
            map=mean_dem_difference,
            rules='-', stdin=dem_difference_colors)
        gscript.run_command('d.rast', map=mean_dem_difference)
        gscript.run_command('d.vect', map=mean_contour, display='shape')
        gscript.run_command('d.legend',
            raster=mean_dem_difference,
            fontsize=fontsize,
            at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # linear regression
        regression_params = gscript.parse_command('r.regression.line',
            flags='g',
            mapx=mean_dem_before,
            mapy=mean_dem_after,
            overwrite=overwrite)
        gscript.run_command('r.mapcalc',
            expression='{regression} = {a} + {b} * {before}'.format(a=regression_params['a'],
            b=regression_params['b'],
            before=mean_dem_before,
            regression=mean_dem_regression),
            overwrite=overwrite)
        gscript.run_command('r.colors',
            map=mean_dem_regression,
            color="elevation")
        gscript.run_command('d.mon',
            start=driver,
            width=width,
            height=height,
            output=os.path.join(render,mean_dem_regression+".png"),
            overwrite=overwrite)
        gscript.run_command('d.rast',
            map=mean_dem_regression)
        gscript.run_command('d.legend',
            raster=mean_dem_regression,
            fontsize=fontsize,
            at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # compute the difference between the modeled and reference elevation with linear regression
        gscript.run_command('d.mon',
            start=driver,
            width=width,
            height=height,
            output=os.path.join(render, mean_dem_regression_difference+".png"),
            overwrite=overwrite)
        gscript.run_command('r.mapcalc',
            expression='{difference} = {regression} - {after}'.format(regression=mean_dem_regression,
                after=mean_dem_after,
                difference=mean_dem_regression_difference),
            overwrite=overwrite)
        gscript.write_command('r.colors',
            map=mean_dem_regression_difference,
            rules='-',
            stdin=dem_difference_colors)
        gscript.run_command('d.rast', map=mean_dem_regression_difference)
        gscript.run_command('d.vect', map=mean_contour, display='shape')
        gscript.run_command('d.legend',
            raster=mean_dem_regression_difference,
            fontsize=fontsize,
            at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # compute mean slope
        gscript.run_command('d.mon', start=driver, width=width, height=height,  output=os.path.join(render,mean_slope+".png"), overwrite=overwrite)
        gscript.run_command('r.param.scale', input=mean_dem, output=mean_slope, size=size, method="slope", overwrite=overwrite)
        gscript.run_command('r.colors', map=mean_slope, color="slope")
        gscript.run_command('d.shade', shade=mean_relief, color=mean_slope, brighten=brighten)
        gscript.run_command('d.vect', map=mean_contour, display='shape')
        gscript.run_command('d.legend', raster=mean_slope, fontsize=fontsize, at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        #compute mean landforms
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

        # identify mean depressions
        gscript.run_command('r.fill.dir', input=mean_dem, output='depressionless_dem', direction='flow_dir',overwrite=overwrite)
        gscript.run_command('r.mapcalc', expression='{depressions} = if({depressionless_dem} - {dem} > {depth}, {depressionless_dem} - {dem}, null())'.format(depressions=mean_depressions, depressionless_dem='depressionless_dem', dem=mean_dem, depth=0), overwrite=overwrite)
        gscript.write_command('r.colors', map=mean_depressions, rules='-', stdin=depressions_colors)
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,mean_depressions+".png"), overwrite=overwrite)
        gscript.run_command('d.rast', map=mean_depressions)
        gscript.run_command('d.vect', map=mean_contour, display='shape')
        gscript.run_command('d.legend', raster=mean_depressions, fontsize=fontsize, at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # compute the difference between the mean and reference slope
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render, mean_slope_difference+".png"), overwrite=overwrite)
        gscript.run_command('r.mapcalc', expression='{difference} = {before} - {after}'.format(before=mean_slope_before,after=mean_slope_after,difference=mean_slope_difference), overwrite=overwrite)
        gscript.write_command('r.colors', map=mean_slope_difference, rules='-', stdin=slope_difference_colors)
        gscript.run_command('d.rast', map=mean_slope_difference)
        gscript.run_command('d.vect', map=mean_contour, display='shape')
        gscript.run_command('d.legend', raster=mean_slope_difference, fontsize=fontsize, at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # compute the difference between the mean and reference landorms
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render, mean_forms_difference+".png"), overwrite=overwrite)
        gscript.run_command('r.mapcalc', expression='{difference} = {before} - {after}'.format(before=mean_forms_before,after=mean_forms_after,difference=mean_forms_difference), overwrite=overwrite)
        gscript.write_command('r.colors', map=mean_forms_difference, rules='-', stdin=forms_difference_colors)
        gscript.run_command('d.rast', map=mean_forms_difference)
        gscript.run_command('d.vect', map=mean_contour, display='shape')
        gscript.run_command('d.legend', raster=mean_forms_difference, fontsize=fontsize, at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # compute the difference between the mean and reference flow depth
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render, mean_depth_difference+".png"), overwrite=overwrite)
        gscript.run_command('r.mapcalc', expression='{difference} = {before} - {after}'.format(before=mean_depth_before,after=mean_depth_after,difference=mean_depth_difference), overwrite=overwrite)
        gscript.write_command('r.colors', map=mean_depth_difference, rules='-', stdin=flow_difference_colors)
        gscript.run_command('d.rast', map=mean_depth_difference)
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
            gscript.run_command('d.rast', map=mean_depth_difference)
            gscript.run_command('d.vect', map=mean_contour, display='shape')
            gscript.run_command('d.vect', map=concentrated_points, display='shape', color='blue')
            gscript.run_command('d.vect', map=mean_concentrated_points, display='shape', color='red')
            gscript.run_command('d.vect', map=flow_lines, display='shape')
            gscript.run_command('d.legend', raster=mean_depth_difference, fontsize=fontsize, at=legend_coord)
            gscript.run_command('d.mon', stop=driver)
        except CalledModuleError:
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
            gscript.run_command('d.rast', map=mean_peaks)
            gscript.run_command('d.vect', map=mean_contour, display='shape')
            gscript.run_command('d.vect', map=peak_points, display='shape', color='blue')
            gscript.run_command('d.vect', map=mean_peak_points, display='shape', color='red')
            gscript.run_command('d.vect', map=peak_lines, display='shape')
            gscript.run_command('d.legend', raster=mean_forms, fontsize=fontsize, at=legend_coord)
            gscript.run_command('d.mon', stop=driver)
        except CalledModuleError:
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
            gscript.run_command('d.rast', map=mean_pits)
            gscript.run_command('d.vect', map=contour, display='shape')
            gscript.run_command('d.vect', map=pit_points, display='shape', color='blue')
            gscript.run_command('d.vect', map=mean_pit_points, display='shape', color='red')
            gscript.run_command('d.vect', map=pit_lines, display='shape')
            gscript.run_command('d.legend', raster=mean_forms, fontsize=fontsize, at=legend_coord)
            gscript.run_command('d.mon', stop=driver)
        except CalledModuleError:
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
            gscript.run_command('d.rast', map=mean_ridges)
            gscript.run_command('d.vect', map=mean_contour, display='shape')
            gscript.run_command('d.vect', map=ridge_points, display='shape', color='blue')
            gscript.run_command('d.vect', map=mean_ridge_points, display='shape', color='red')
            gscript.run_command('d.vect', map=ridge_lines, display='shape')
            gscript.run_command('d.legend', raster=mean_forms, fontsize=fontsize, at=legend_coord)
            gscript.run_command('d.mon', stop=driver)
        except CalledModuleError:
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
            gscript.run_command('d.rast', map=mean_valleys)
            gscript.run_command('d.vect', map=mean_contour, display='shape')
            gscript.run_command('d.vect', map=valley_points, display='shape', color='blue')
            gscript.run_command('d.vect', map=mean_valley_points, display='shape', color='red')
            gscript.run_command('d.vect', map=valley_lines, display='shape')
            gscript.run_command('d.legend', raster=mean_forms, fontsize=fontsize, at=legend_coord)
            gscript.run_command('d.mon', stop=driver)
        except CalledModuleError:
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
            ridge_cells.append(0)
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
            gscript.run_command('r.mask', flags='r')
        except CalledModuleError:
            pass

def stdev_analysis():
    """compute the difference, water flow, depressions, and concentrated flow for each series of models"""

    # list reference DEMs
    dems = gscript.list_grouped('rast', pattern='dem_*')['PERMANENT']

    # iterate through reference DEMs
    for dem in dems:

        # list scanned DEMs
        dem_list = gscript.list_grouped('rast', pattern='*'+dem)[mapset]

        # variables
        region = dem
        mask = dem.replace("dem","mask")
        stdev_dem = dem.replace("dem","stdev_dem")
        stdev_contour = dem.replace("dem","stdev_contour")
        stdev_difference_series = dem.replace("dem","stdev_difference_series")
        stdev_regression_difference_series = dem.replace("dem","stdev_regression_difference_series")

        # set region
        gscript.run_command('g.region', rast=region, res=res)

        # check if mask needed
        find_mask = gscript.find_file(mask, element = 'cell')
        if find_mask['name']:
            gscript.run_command('r.mask', raster=mask, overwrite=overwrite)

        # compute stdev elevation
        gscript.run_command('r.series',
            input=dem_list,
            output=stdev_dem,
            method="stddev",
            overwrite=overwrite)
        gscript.write_command('r.colors',
            map=stdev_dem,
            rules='-',
            stdin=stdev_colors_3d)
        gscript.run_command('r.contour',
            input=stdev_dem,
            output=stdev_contour,
            step=step,
            overwrite=overwrite)
        info = gscript.parse_command('r.info', map=dem, flags='g')
        width=int(info.cols)+int(info.cols)/2*render_multiplier*whitespace
        height=int(info.rows)*render_multiplier
        gscript.run_command('d.mon',
            start=driver,
            width=width,
            height=height,
            output=os.path.join(render,stdev_dem+".png"),
            overwrite=overwrite)
        gscript.run_command('d.rast', map=stdev_dem)
        gscript.run_command('d.legend',
            raster=stdev_dem,
            fontsize=fontsize,
            at=legend_coord)
        gscript.run_command('d.vect', map=stdev_contour, display="shape")
        gscript.run_command('d.legend',
            raster=stdev_dem,
            fontsize=fontsize,
            at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # compute difference series
        j = 0
        for elev in dem_list:
            j = j + 1
            diff = 'diff_' + str(j) + dem.replace("dem","")
            regress_diff = 'regress_diff_' + str(j) + dem.replace("dem","")

            # difference
            gscript.run_command('r.mapcalc',
                expression='{difference} = {before} - {after}'.format(before=dem,
                    after=elev,
                    difference=diff),
                overwrite=overwrite)

            # difference with linear regression
            regression_params = gscript.parse_command('r.regression.line',
                flags='g',
                mapx=dem,
                mapy=elev,
                overwrite=overwrite)
            gscript.run_command('r.mapcalc',
                expression='{regression} = {a} + {b} * {before}'.format(a=regression_params['a'],
                b=regression_params['b'],
                before=dem,
                regression='regression'),
                overwrite=overwrite)
            # difference
            gscript.run_command('r.mapcalc',
                expression='{difference} = {regression} - {after}'.format(regression='regression',
                    after=elev,
                    difference=regress_diff),
                overwrite=overwrite)

        # compute stdev of difference series
        diff_list = gscript.list_grouped('rast',
            pattern='diff_*')[mapset]
        gscript.run_command('r.series',
            input=diff_list,
            output=stdev_difference_series,
            method="stddev",
            overwrite=overwrite)
        gscript.write_command('r.colors',
            map=stdev_difference_series,
            rules='-',
            stdin=stdev_colors_3d)
        gscript.run_command('d.mon',
            start=driver,
            width=width,
            height=height,
            output=os.path.join(render,stdev_difference_series+".png"),
            overwrite=overwrite)
        gscript.run_command('d.rast', map=stdev_difference_series)
        gscript.run_command('d.legend',
            raster=stdev_difference_series,
            fontsize=fontsize,
            at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # compute stdev of regressed difference series
        regress_diff_list = gscript.list_grouped('rast',
            pattern='regress_diff_*')[mapset]
        gscript.run_command('r.series',
            input=regress_diff_list,
            output=stdev_regression_difference_series,
            method="stddev",
            overwrite=overwrite)
        gscript.write_command('r.colors',
            map=stdev_regression_difference_series,
            rules='-',
            stdin=stdev_colors_3d)
        gscript.run_command('d.mon',
            start=driver,
            width=width,
            height=height,
            output=os.path.join(render,stdev_regression_difference_series+".png"),
            overwrite=overwrite)
        gscript.run_command('d.rast', map=stdev_regression_difference_series)
        gscript.run_command('d.legend',
            raster=stdev_regression_difference_series,
            fontsize=fontsize,
            at=legend_coord)
        gscript.run_command('d.mon', stop=driver)

        # try to remove mask
        try:
            gscript.run_command('r.mask', flags='r')
        except CalledModuleError:
            pass

        try:
            # remove temporary maps
            gscript.run_command('g.remove',
                type='raster',
                pattern='*diff_*',
                flags='f')
        except CalledModuleError:
            pass

def render_3d_images():
    """3D rendering with nviz"""

    # list scanned DEMs
    dems = gscript.list_grouped('rast',
                                pattern='dem_*')['PERMANENT']

    # iterate through scanned DEMs
    for dem in dems:

        # reference variables
        region = dem
        slope = dem.replace("dem", "slope")
        forms = dem.replace("dem", "forms")
        depth = dem.replace("dem", "depth")
        dem_difference = dem.replace("dem", "dem_difference")
        depressions = dem.replace("dem", "depressions")
        concentrated_flow = dem.replace("dem", "concentrated_flow")
        peaks = dem.replace("dem", "peaks")
        ridges = dem.replace("dem", "ridges")
        valleys = dem.replace("dem", "valleys")

        # mean variables
        mean_dem = dem.replace("dem", "mean_dem")
        mean_slope = dem.replace("dem", "mean_slope")
        mean_forms = dem.replace("dem", "mean_forms")
        mean_depth = dem.replace("dem", "mean_depth")
        mean_dem_difference = dem.replace("dem", "mean_dem_difference")
        mean_dem_regression = dem.replace("dem", "mean_dem_regression")
        mean_dem_regression_difference = dem.replace("dem", "mean_dem_regression_difference")
        mean_forms_difference = dem.replace("dem", "mean_forms_difference")
        mean_depth_difference = dem.replace("dem", "mean_depth_difference")

        # stdev variables
        stdev_dem = dem.replace("dem", "stdev_dem")
        stdev_difference_series = dem.replace("dem", "stdev_difference_series")
        stdev_regression_difference_series = dem.replace("dem", "stdev_regression_difference_series")

        # set region
        gscript.run_command('g.region',
                            rast=region,
                            res=res)

        # 3D render elevation
        gscript.write_command('r.colors',
            map=dem,
            rules='-',
            stdin=dem_colors_3d)
        gscript.run_command('m.nviz.image',
            elevation_map=dem,
            color_map=dem,
            resolution_fine=res_3d,
            height=height_3d,
            perspective=perspective,
            light_position=light_position,
            fringe=fringe,
            fringe_color=color_3d,
            fringe_elevation=fringe_elevation,
            output=os.path.join(render_3d, dem),
            format=format_3d,
            size=size_3d,
            errors='ignore'
            )

        # 3D render slope
        gscript.write_command('r.colors',
            map=slope,
            rules='-',
            stdin=slope_colors_3d)
        gscript.run_command('m.nviz.image',
            elevation_map=dem,
            color_map=slope,
            resolution_fine=res_3d,
            height=height_3d,
            perspective=perspective,
            light_position=light_position,
            fringe=fringe,
            fringe_color=color_3d,
            fringe_elevation=fringe_elevation,
            output=os.path.join(render_3d, slope),
            format=format_3d,
            size=size_3d,
            errors='ignore'
            )

        # 3D render landforms
        gscript.write_command('r.colors',
            map=forms,
            rules='-',
            stdin=forms_colors_3d)
        gscript.run_command('m.nviz.image',
            elevation_map=dem,
            color_map=forms,
            resolution_fine=res_3d,
            height=height_3d,
            perspective=perspective,
            light_position=light_position,
            fringe=fringe,
            fringe_color=color_3d,
            fringe_elevation=fringe_elevation,
            output=os.path.join(render_3d, forms),
            format=format_3d,
            size=size_3d,
            errors='ignore'
            )

        # 3D render water flow
        gscript.write_command('r.colors',
            map=depth,
            rules='-',
            stdin=depth_colors_3d)
        gscript.run_command('m.nviz.image',
            elevation_map=dem,
            color_map=depth,
            resolution_fine=res_3d,
            height=height_3d,
            perspective=perspective,
            light_position=light_position,
            fringe=fringe,
            fringe_color=color_3d,
            fringe_elevation=fringe_elevation,
            output=os.path.join(render_3d, depth),
            format=format_3d,
            size=size_3d,
            errors='ignore'
            )

        # 3D render difference
        gscript.run_command('m.nviz.image',
            elevation_map=dem,
            color=color_3d,
            resolution_fine=res_3d,
            height=height_3d,
            perspective=perspective,
            light_position=light_position,
            fringe=fringe,
            fringe_color=color_3d,
            fringe_elevation=fringe_elevation,
            output=os.path.join(render_3d, dem_difference),
            format=format_3d,
            size=size_3d,
            errors='ignore'
            )

        # 3D render mean elevation
        gscript.write_command('r.colors',
            map=mean_dem,
            rules='-',
            stdin=dem_colors_3d)
        gscript.run_command('m.nviz.image',
            elevation_map=mean_dem,
            color_map=mean_dem,
            resolution_fine=res_3d,
            height=height_3d,
            perspective=perspective,
            light_position=light_position,
            fringe=fringe,
            fringe_color=color_3d,
            fringe_elevation=fringe_elevation,
            output=os.path.join(render_3d, mean_dem),
            format=format_3d,
            size=size_3d,
            errors='ignore'
            )

        # 3D render mean slope
        gscript.write_command('r.colors',
            map=mean_slope,
            rules='-',
            stdin=slope_colors_3d)
        gscript.run_command('m.nviz.image',
            elevation_map=mean_dem,
            color_map=mean_slope,
            resolution_fine=res_3d,
            height=height_3d,
            perspective=perspective,
            light_position=light_position,
            fringe=fringe,
            fringe_color=color_3d,
            fringe_elevation=fringe_elevation,
            output=os.path.join(render_3d, mean_slope),
            format=format_3d,
            size=size_3d,
            errors='ignore'
            )

        # 3D render mean landforms
        gscript.write_command('r.colors',
            map=mean_forms,
            rules='-',
            stdin=forms_colors_3d)
        gscript.run_command('m.nviz.image',
            elevation_map=mean_dem,
            color_map=mean_forms,
            resolution_fine=res_3d,
            height=height_3d,
            perspective=perspective,
            light_position=light_position,
            fringe=fringe,
            fringe_color=color_3d,
            fringe_elevation=fringe_elevation,
            output=os.path.join(render_3d, mean_forms),
            format=format_3d,
            size=size_3d,
            errors='ignore'
            )

        # 3D render mean water flow
        gscript.write_command('r.colors',
            map=mean_depth,
            rules='-',
            stdin=depth_colors_3d)
        gscript.run_command('m.nviz.image',
            elevation_map=mean_dem,
            color_map=mean_depth,
            resolution_fine=res_3d,
            height=height_3d,
            perspective=perspective,
            light_position=light_position,
            fringe=fringe,
            fringe_color=color_3d,
            fringe_elevation=fringe_elevation,
            output=os.path.join(render_3d, mean_depth),
            format=format_3d,
            size=size_3d,
            errors='ignore'
            )

        # 3D render mean elevation difference
        gscript.write_command('r.colors',
            map=mean_dem_difference,
            rules='-',
            stdin=dem_difference_colors_3d)
        gscript.run_command('m.nviz.image',
            elevation_map=mean_dem,
            color_map=mean_dem_difference,
            resolution_fine=res_3d,
            height=height_3d,
            perspective=perspective,
            light_position=light_position,
            fringe=fringe,
            fringe_color=color_3d,
            fringe_elevation=fringe_elevation,
            output=os.path.join(render_3d, mean_dem_difference),
            format=format_3d,
            size=size_3d,
            errors='ignore'
            )

        # 3D render mean forms difference
        gscript.write_command('r.colors',
            map=mean_forms_difference,
            rules='-',
            stdin=forms_difference_colors_3d)
        gscript.run_command('m.nviz.image',
            elevation_map=mean_dem,
            color_map=mean_forms_difference,
            resolution_fine=res_3d,
            height=height_3d,
            perspective=perspective,
            light_position=light_position,
            fringe=fringe,
            fringe_color=color_3d,
            fringe_elevation=fringe_elevation,
            output=os.path.join(render_3d, mean_forms_difference),
            format=format_3d,
            size=size_3d,
            errors='ignore'
            )

        # 3D render mean regressed elevation difference
        gscript.write_command('r.colors',
            map=mean_dem_regression_difference,
            rules='-',
            stdin=dem_regression_difference_colors_3d)
        gscript.run_command('m.nviz.image',
            elevation_map=mean_dem,
            color_map=mean_dem_regression_difference,
            resolution_fine=res_3d,
            height=height_3d,
            perspective=perspective,
            light_position=light_position,
            fringe=fringe,
            fringe_color=color_3d,
            fringe_elevation=fringe_elevation,
            output=os.path.join(render_3d, mean_dem_regression_difference),
            format=format_3d,
            size=size_3d,
            errors='ignore'
            )

        # 3D render mean flow difference
        gscript.write_command('r.colors',
            map=mean_depth_difference,
            rules='-',
            stdin=flow_difference_colors_3d)
        gscript.run_command('m.nviz.image',
            elevation_map=mean_dem,
            color_map=mean_depth_difference,
            resolution_fine=res_3d,
            height=height_3d,
            perspective=perspective,
            light_position=light_position,
            fringe=fringe,
            fringe_color=color_3d,
            fringe_elevation=fringe_elevation,
            output=os.path.join(render_3d, mean_depth_difference),
            format=format_3d,
            size=size_3d,
            errors='ignore'
            )

        # 3D render stdev elevation
        gscript.write_command('r.colors',
            map=stdev_dem,
            rules='-',
            stdin=stdev_colors_3d)

        gscript.run_command('m.nviz.image',
            elevation_map=mean_dem,
            color_map=stdev_dem,
            resolution_fine=res_3d,
            height=height_3d,
            perspective=perspective,
            light_position=light_position,
            fringe=fringe,
            fringe_color=color_3d,
            fringe_elevation=fringe_elevation,
            output=os.path.join(render_3d, stdev_dem),
            format=format_3d,
            size=size_3d,
            errors='ignore'
            )

        # 3D render stdev of regressed difference series
        gscript.write_command('r.colors',
            map=stdev_regression_difference_series,
            rules='-',
            stdin=stdev_diff_colors_3d)

        gscript.run_command('m.nviz.image',
            elevation_map=mean_dem,
            color_map=stdev_regression_difference_series,
            resolution_fine=res_3d,
            height=height_3d,
            perspective=perspective,
            light_position=light_position,
            fringe=fringe,
            fringe_color=color_3d,
            fringe_elevation=fringe_elevation,
            output=os.path.join(render_3d,stdev_regression_difference_series),
            format=format_3d,
            size=size_3d,
            errors='ignore'
            )

def write_results(ref_flow_cells,
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

    # count number of dems
    i = 0
    dems = gscript.list_grouped('rast',
                                pattern='dem_*')['PERMANENT']
    for dem in dems:
        i = i + 1

    # print
    for x in xrange(i):
        print x
        # reference cells
        print 'ref flow cells: ' + str(ref_flow_cells[x])
        print 'ref depression cells: ' + str(ref_depression_cells[x])
        print 'ref peak cells: ' + str(ref_peak_cells[x])
        print 'ref pit cells: ' + str(ref_pit_cells[x])
        print 'ref ridge cells: ' + str(ref_ridge_cells[x])
        print 'ref valley cells: ' + str(ref_valley_cells[x])
        # mean cells
        print 'mean flow cells: ' + str(flow_cells[x])
        print 'mean depression cells: ' + str(depression_cells[x])
        print 'mean peak cells: ' + str(peak_cells[x])
        print 'mean pit cells: ' + str(pit_cells[x])
        print 'mean ridge cells: ' + str(ridge_cells[x])
        print 'mean valley cells: ' + str(valley_cells[x])
        # mean distance
        print 'flow distance: ' + str(flow_distance[x])
        print 'peak distance: ' + str(peak_distance[x])
        print 'pit distance: ' + str(pit_distance[x])
        print 'ridge distance: ' + str(ridge_distance[x])
        print 'valley distance: ' + str(valley_distance[x])

    # write to csv file
    with open(cells, 'wb') as csvfile:
        cells_writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

        cells_writer.writerow(['ref_flow_cells', 'ref_depression_cells', 'ref_peak_cells', 'ref_pit_cells', 'ref_ridge_cells', 'ref_valley_cells', 'flow_cells', 'depression_cells', 'peak_cells', 'pit_cells', 'ridge_cells', 'valley_cells', 'flow_distance', 'peak_distance', 'pit_distance', 'ridge_distance', 'valley_distance'])

        for x in xrange(i):
            cells_writer.writerow([ref_flow_cells[x], ref_depression_cells[x], ref_peak_cells[x], ref_pit_cells[x], ref_ridge_cells[x], ref_valley_cells[x], flow_cells[x], depression_cells[x], peak_cells[x], pit_cells[x], ridge_cells[x], valley_cells[x], flow_distance[x], peak_distance[x], pit_distance[x], ridge_distance[x], valley_distance[x]])


if __name__ == "__main__":
    atexit.register(cleanup)
    sys.exit(main())
