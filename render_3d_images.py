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
render_3d = os.path.join(gisdbase, location, 'render_3d')

# set variables
res = 3 # resolution of the region

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
slope_colors_3d = '0 192:192:192\n2 255:255:0\n5 0:255:0\n10 0:255:255\n15 0:0:255\n30 255:0:255\n50 255:0:0\n90 0:0:0\nnv 192:192:192\ndefault 192:192:192'
depressions_colors_3d = '0% aqua\n100% blue\nnv 192:192:192\ndefault 192:192:192'
depth_colors_3d = '0 192:192:192\n0.001 255:255:0\n0.05 0:255:255\n0.1 0:127:255\n0.5 0:0:255\n100% 0:0:0\nnv 192:192:192\ndefault 192:192:192'
forms_colors_3d = '0 192:192:192\n1 220:220:220\n2 56:0:0\n3 200:0:0\n4 255:80:20\n5 250:210:60\n6 255:255:60\n7 180:230:20\n8 60:250:150\n9 0:0:255\n10 0:0:56\n11 255:0:255\nnv 192:192:192\ndefault 192:192:192'
dem_difference_colors_3d = '-40 blue\n0 192:192:192\n40 red\nnv 192:192:192\ndefault 192:192:192'
flow_difference_colors_3d = '-0.5 blue\n0 192:192:192\n0.5 red\nnv 192:192:192\ndefault 192:192:192'
slope_difference_colors_3d = '-30 blue\n0 192:192:192\n30 red\nnv 192:192:192\ndefault 192:192:192'
forms_difference_colors_3d = '-10 blue\n0 192:192:192\n10 red\nnv 192:192:192\ndefault 192:192:192'
# stdev_dem_difference_colors_3d = '250 blue\n0 white\n350 red\nnv 192:192:192\ndefault 192:192:192'
# stdev_dem_regression_difference_colors_3d = '-11 blue\n0 white\n11 red\nnv 192:192:192\ndefault 192:192:192'
# stdev_slope_difference_colors_3d = '-40 blue\n0 white\n40 red\nnv 192:192:192\ndefault 192:192:192'
url="http://soliton.vm.bytemark.co.uk/pub/cpt-city/mpl/viridis.cpt" # http://soliton.vm.bytemark.co.uk/pub/cpt-city/mpl/inferno.cpt

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
    pits = dem.replace("dem", "pits")
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
    mean_slope_difference = dem.replace("dem", "mean_slope_difference")
    mean_slope_regression = dem.replace("dem", "mean_slope_regression")
    mean_slope_regression_difference = dem.replace("dem", "mean_slope_regression_difference")
    mean_forms_difference = dem.replace("dem", "mean_forms_difference")
    mean_depth_difference = dem.replace("dem", "mean_depth_difference")
    mean_depressions = dem.replace("dem", "mean_depressions")
    mean_concentrated_flow = dem.replace("dem", "mean_concentrated_flow")
    mean_concentrated_points = dem.replace("dem", "mean_concentrated_points")
    flow_lines = dem.replace("dem", "flow_lines")
    mean_peaks = dem.replace("dem", "mean_peaks")
    mean_peak_points = dem.replace("dem", "mean_peak_points")
    peak_lines = dem.replace("dem", "peak_lines")
    mean_pits = dem.replace("dem", "mean_pits")
    mean_pit_points = dem.replace("dem", "mean_pit_points")
    pit_lines = dem.replace("dem", "pit_lines")
    mean_ridges = dem.replace("dem", "mean_ridges")
    mean_ridge_points = dem.replace("dem", "mean_ridge_points")
    ridge_lines = dem.replace("dem", "ridge_lines")
    mean_valleys = dem.replace("dem", "mean_valleys")
    mean_valley_points = dem.replace("dem", "mean_valley_points")
    valley_lines = dem.replace("dem", "valley_lines")
    mean_forms_regression = dem.replace("dem","mean_forms_regression")
    mean_depth_regression = dem.replace("dem","mean_depth_regression")

    # stdev variables
    stdev_dem = dem.replace("dem", "stdev_dem")
    stdev_slope = dem.replace("dem", "stdev_slope")
    stdev_forms = dem.replace("dem", "stdev_forms")
    stdev_depth = dem.replace("dem", "stdev_depth")
    stdev_dem_difference = dem.replace("dem", "stdev_dem_difference")
    stdev_dem_regression = dem.replace("dem", "stdev_dem_regression")
    stdev_dem_regression_difference = dem.replace("dem", "stdev_dem_regression_difference")
    stdev_slope_difference = dem.replace("dem", "stdev_slope_difference")
    stdev_slope_regression = dem.replace("dem", "stdev_slope_regression")
    stdev_slope_regression_difference = dem.replace("dem", "stdev_slope_regression_difference")
    stdev_forms_difference = dem.replace("dem", "stdev_forms_difference")
    stdev_depth_difference = dem.replace("dem", "stdev_depth_difference")
    stdev_depressions = dem.replace("dem", "stdev_depressions")

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
        #color=color_3d,
        resolution_fine=res_3d,
        height=height_3d,
        perspective=perspective,
        light_position=light_position,
        fringe=fringe,
        fringe_color=color_3d,
        fringe_elevation=fringe_elevation,
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
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
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
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
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
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
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
        output=os.path.join(render_3d, depth),
        format=format_3d,
        size=size_3d,
        errors='ignore'
        )

    # 3D render depressions
    gscript.write_command('r.colors',
        map=depressions,
        rules='-',
        stdin=depressions_colors_3d)
    gscript.run_command('m.nviz.image',
        elevation_map=dem,
        color_map=depressions,
        resolution_fine=res_3d,
        height=height_3d,
        perspective=perspective,
        light_position=light_position,
        fringe=fringe,
        fringe_color=color_3d,
        fringe_elevation=fringe_elevation,
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
        output=os.path.join(render_3d, depressions),
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
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
        output=os.path.join(render_3d, dem_difference),
        format=format_3d,
        size=size_3d,
        errors='ignore'
        )

    # 3D render concentrated flow
    gscript.write_command('r.colors',
        map=concentrated_flow,
        rules='-',
        stdin=depth_colors_3d)
    gscript.run_command('m.nviz.image',
        elevation_map=dem,
        color_map=concentrated_flow,
        resolution_fine=res_3d,
        height=height_3d,
        perspective=perspective,
        light_position=light_position,
        fringe=fringe,
        fringe_color=color_3d,
        fringe_elevation=fringe_elevation,
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
        output=os.path.join(render_3d, concentrated_flow),
        format=format_3d,
        size=size_3d,
        errors='ignore'
        )

    # 3D render peaks
    gscript.write_command('r.colors',
        map=peaks,
        rules='-',
        stdin=forms_colors_3d)
    gscript.run_command('m.nviz.image',
        elevation_map=dem,
        color_map=peaks,
        resolution_fine=res_3d,
        height=height_3d,
        perspective=perspective,
        light_position=light_position,
        fringe=fringe,
        fringe_color=color_3d,
        fringe_elevation=fringe_elevation,
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
        output=os.path.join(render_3d, peaks),
        format=format_3d,
        size=size_3d,
        errors='ignore'
        )

    # 3D render pits
    gscript.write_command('r.colors',
        map=pits,
        rules='-',
        stdin=forms_colors_3d)
    gscript.run_command('m.nviz.image',
        elevation_map=dem,
        color_map=pits,
        resolution_fine=res_3d,
        height=height_3d,
        perspective=perspective,
        light_position=light_position,
        fringe=fringe,
        fringe_color=color_3d,
        fringe_elevation=fringe_elevation,
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
        output=os.path.join(render_3d, pits),
        format=format_3d,
        size=size_3d,
        errors='ignore'
        )

    # 3D render ridges
    gscript.write_command('r.colors',
        map=ridges,
        rules='-',
        stdin=forms_colors_3d)
    gscript.run_command('m.nviz.image',
        elevation_map=dem,
        color_map=ridges,
        resolution_fine=res_3d,
        height=height_3d,
        perspective=perspective,
        light_position=light_position,
        fringe=fringe,
        fringe_color=color_3d,
        fringe_elevation=fringe_elevation,
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
        output=os.path.join(render_3d, ridges),
        format=format_3d,
        size=size_3d,
        errors='ignore'
        )

    # 3D render valleys
    gscript.write_command('r.colors',
        map=valleys,
        rules='-',
        stdin=forms_colors_3d)
    gscript.run_command('m.nviz.image',
        elevation_map=dem,
        color_map=valleys,
        resolution_fine=res_3d,
        height=height_3d,
        perspective=perspective,
        light_position=light_position,
        fringe=fringe,
        fringe_color=color_3d,
        fringe_elevation=fringe_elevation,
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
        output=os.path.join(render_3d, valleys),
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
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
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
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
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
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
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
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
        output=os.path.join(render_3d, mean_depth),
        format=format_3d,
        size=size_3d,
        errors='ignore'
        )

    # 3D render mean depressions
    gscript.write_command('r.colors',
        map=mean_depressions,
        rules='-',
        stdin=depressions_colors_3d)
    gscript.run_command('m.nviz.image',
        elevation_map=mean_dem,
        color_map=mean_depressions,
        resolution_fine=res_3d,
        height=height_3d,
        perspective=perspective,
        light_position=light_position,
        fringe=fringe,
        fringe_color=color_3d,
        fringe_elevation=fringe_elevation,
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
        output=os.path.join(render_3d, mean_depressions),
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
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
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
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
        output=os.path.join(render_3d, mean_forms_difference),
        format=format_3d,
        size=size_3d,
        errors='ignore'
        )

    # 3D render mean regressed elevation
    gscript.write_command('r.colors',
        map=mean_dem_regression,
        rules='-',
        stdin=dem_colors_3d)
    gscript.run_command('m.nviz.image',
        elevation_map=mean_dem_regression,
        color_map=mean_dem_regression,
        resolution_fine=res_3d,
        height=height_3d,
        perspective=perspective,
        light_position=light_position,
        fringe=fringe,
        fringe_color=color_3d,
        fringe_elevation=fringe_elevation,
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
        output=os.path.join(render_3d, mean_dem_regression),
        format=format_3d,
        size=size_3d,
        errors='ignore'
        )

    # 3D render mean regressed elevation difference
    gscript.write_command('r.colors',
        map=mean_dem_regression_difference,
        rules='-',
        stdin=dem_difference_colors_3d)
    gscript.run_command('m.nviz.image',
        elevation_map=mean_dem_regression,
        color_map=mean_dem_regression_difference,
        resolution_fine=res_3d,
        height=height_3d,
        perspective=perspective,
        light_position=light_position,
        fringe=fringe,
        fringe_color=color_3d,
        fringe_elevation=fringe_elevation,
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
        output=os.path.join(render_3d, mean_dem_regression_difference),
        format=format_3d,
        size=size_3d,
        errors='ignore'
        )

    # 3D render mean slope difference
    gscript.write_command('r.colors',
        map=mean_slope_difference,
        rules='-',
        stdin=slope_difference_colors_3d)
    gscript.run_command('m.nviz.image',
        elevation_map=mean_dem,
        color_map=mean_slope_difference,
        resolution_fine=res_3d,
        height=height_3d,
        perspective=perspective,
        light_position=light_position,
        fringe=fringe,
        fringe_color=color_3d,
        fringe_elevation=fringe_elevation,
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
        output=os.path.join(render_3d, mean_slope_difference),
        format=format_3d,
        size=size_3d,
        errors='ignore'
        )

    # 3D render mean regressed slope
    gscript.write_command('r.colors',
        map=mean_slope_regression,
        rules='-',
        stdin=slope_colors_3d)
    gscript.run_command('m.nviz.image',
        elevation_map=mean_dem_regression,
        color_map=mean_slope_regression,
        resolution_fine=res_3d,
        height=height_3d,
        perspective=perspective,
        light_position=light_position,
        fringe=fringe,
        fringe_color=color_3d,
        fringe_elevation=fringe_elevation,
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
        output=os.path.join(render_3d, mean_slope_regression),
        format=format_3d,
        size=size_3d,
        errors='ignore'
        )

    # 3D render mean regressed slope difference
    gscript.write_command('r.colors',
        map=mean_slope_regression_difference,
        rules='-',
        stdin=slope_difference_colors_3d)
    gscript.run_command('m.nviz.image',
        elevation_map=mean_dem_regression,
        color_map=mean_slope_regression_difference,
        resolution_fine=res_3d,
        height=height_3d,
        perspective=perspective,
        light_position=light_position,
        fringe=fringe,
        fringe_color=color_3d,
        fringe_elevation=fringe_elevation,
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
        output=os.path.join(render_3d, mean_slope_regression_difference),
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
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
        output=os.path.join(render_3d, mean_depth_difference),
        format=format_3d,
        size=size_3d,
        errors='ignore'
        )

    # 3D render mean flow distance
    gscript.run_command('m.nviz.image',
        elevation_map=mean_dem,
        color_map=mean_depth_difference,
        vpoint=mean_concentrated_points,
        vpoint_size=vpoint_size,
        vpoint_marker=vpoint_marker,
        vpoint_color=vpoint_color,
        vline=flow_lines,
        vline_width=vline_width,
        vline_color=vline_color,
        resolution_fine=res_3d,
        height=height_3d,
        perspective=perspective,
        light_position=light_position,
        fringe=fringe,
        fringe_color=color_3d,
        fringe_elevation=fringe_elevation,
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
        output=os.path.join(render_3d, mean_concentrated_flow),
        format=format_3d,
        size=size_3d,
        errors='ignore'
        )

    # 3D render mean peak distance
    gscript.run_command('m.nviz.image',
        elevation_map=mean_dem,
        color=color_3d,
        vpoint=mean_peak_points,
        vpoint_size=vpoint_size,
        vpoint_marker=vpoint_marker,
        vpoint_color=vpoint_color,
        vline=peak_lines,
        vline_width=vline_width,
        vline_color=vline_color,
        resolution_fine=res_3d,
        height=height_3d,
        perspective=perspective,
        light_position=light_position,
        fringe=fringe,
        fringe_color=color_3d,
        fringe_elevation=fringe_elevation,
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
        output=os.path.join(render_3d, mean_peaks),
        format=format_3d,
        size=size_3d,
        errors='ignore'
        )

    # 3D render mean pit distance
    gscript.run_command('m.nviz.image',
        elevation_map=mean_dem,
        color=color_3d,
        vpoint=mean_pit_points,
        vpoint_size=vpoint_size,
        vpoint_marker=vpoint_marker,
        vpoint_color=vpoint_color,
        vline=pit_lines,
        vline_width=vline_width,
        vline_color=vline_color,
        resolution_fine=res_3d,
        height=height_3d,
        perspective=perspective,
        light_position=light_position,
        fringe=fringe,
        fringe_color=color_3d,
        fringe_elevation=fringe_elevation,
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
        output=os.path.join(render_3d, mean_pits),
        format=format_3d,
        size=size_3d,
        errors='ignore'
        )

    # 3D render mean ridge distance
    gscript.run_command('m.nviz.image',
        elevation_map=mean_dem,
        color=color_3d,
        vpoint=mean_ridge_points,
        vpoint_size=vpoint_size,
        vpoint_marker=vpoint_marker,
        vpoint_color=vpoint_color,
        vline=ridge_lines,
        vline_width=vline_width,
        vline_color=vline_color,
        resolution_fine=res_3d,
        height=height_3d,
        perspective=perspective,
        light_position=light_position,
        fringe=fringe,
        fringe_color=color_3d,
        fringe_elevation=fringe_elevation,
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
        output=os.path.join(render_3d, mean_ridges),
        format=format_3d,
        size=size_3d,
        errors='ignore'
        )

    # 3D render mean valley distance
    gscript.run_command('m.nviz.image',
        elevation_map=mean_dem,
        color=color_3d,
        vpoint=mean_valley_points,
        vpoint_size=vpoint_size,
        vpoint_marker=vpoint_marker,
        vpoint_color=vpoint_color,
        vline=valley_lines,
        vline_width=vline_width,
        vline_color=vline_color,
        resolution_fine=res_3d,
        height=height_3d,
        perspective=perspective,
        light_position=light_position,
        fringe=fringe,
        fringe_color=color_3d,
        fringe_elevation=fringe_elevation,
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
        output=os.path.join(render_3d, mean_valleys),
        format=format_3d,
        size=size_3d,
        errors='ignore'
        )

    # 3D render mean regressed forms
    gscript.write_command('r.colors',
        map=mean_forms_regression,
        rules='-',
        stdin=forms_colors_3d)
    gscript.run_command('m.nviz.image',
        elevation_map=mean_dem_regression,
        color_map=mean_forms_regression,
        resolution_fine=res_3d,
        height=height_3d,
        perspective=perspective,
        light_position=light_position,
        fringe=fringe,
        fringe_color=color_3d,
        fringe_elevation=fringe_elevation,
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
        output=os.path.join(render_3d, mean_forms_regression),
        format=format_3d,
        size=size_3d,
        errors='ignore'
        )

    # 3D render mean regressed depth
    gscript.write_command('r.colors',
        map=mean_depth_regression,
        rules='-',
        stdin=depth_colors_3d)
    gscript.run_command('m.nviz.image',
        elevation_map=mean_dem_regression,
        color_map=mean_depth_regression,
        resolution_fine=res_3d,
        height=height_3d,
        perspective=perspective,
        light_position=light_position,
        fringe=fringe,
        fringe_color=color_3d,
        fringe_elevation=fringe_elevation,
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
        output=os.path.join(render_3d, mean_depth_regression),
        format=format_3d,
        size=size_3d,
        errors='ignore'
        )

    # 3D render stdev elevation
    gscript.run_command('r.cpt2grass',
        map=stdev_dem,
        url=url,
        flags="s")
    # gscript.run_command('r.colors.matplotlib',
    #                     map=stdev_dem,
    #                     color="viridis")

    gscript.run_command('m.nviz.image',
        elevation_map=dem,
        color_map=stdev_dem,
        resolution_fine=res_3d,
        height=height_3d,
        perspective=perspective,
        light_position=light_position,
        fringe=fringe,
        fringe_color=color_3d,
        fringe_elevation=fringe_elevation,
        #arrow_position=arrow_position,
        #arrow_size=arrow_size,
        output=os.path.join(render_3d, stdev_dem),
        format=format_3d,
        size=size_3d,
        errors='ignore'
        )

    # # 3D render stdev slope
    # gscript.write_command('r.colors',
    #     map=stdev_slope,
    #     rules='-',
    #     stdin=slope_colors_3d)
    # gscript.run_command('m.nviz.image',
    #     elevation_map=stdev_dem,
    #     color_map=stdev_slope,
    #     resolution_fine=res_3d,
    #     height=height_3d,
    #     perspective=perspective,
    #     light_position=light_position,
    #     fringe=fringe,
    #     fringe_color=color_3d,
    #     fringe_elevation=stdev_fringe,
    #     #arrow_position=arrow_position,
    #     #arrow_size=arrow_size,
    #     output=os.path.join(render_3d, stdev_slope),
    #     format=format_3d,
    #     size=size_3d,
    #     errors='ignore'
    #     )
    #
    # # 3D render stdev forms
    # gscript.write_command('r.colors',
    #     map=stdev_forms,
    #     rules='-',
    #     stdin=forms_colors_3d)
    # gscript.run_command('m.nviz.image',
    #     elevation_map=stdev_dem,
    #     color_map=stdev_forms,
    #     resolution_fine=res_3d,
    #     height=height_3d,
    #     perspective=perspective,
    #     light_position=light_position,
    #     fringe=fringe,
    #     fringe_color=color_3d,
    #     fringe_elevation=stdev_fringe,
    #     #arrow_position=arrow_position,
    #     #arrow_size=arrow_size,
    #     output=os.path.join(render_3d, stdev_forms),
    #     format=format_3d,
    #     size=size_3d,
    #     errors='ignore'
    #     )
    #
    # # 3D render stdev depth
    # gscript.write_command('r.colors',
    #     map=stdev_depth,
    #     rules='-',
    #     stdin=depth_colors_3d)
    # gscript.run_command('m.nviz.image',
    #     elevation_map=stdev_dem,
    #     color_map=stdev_depth,
    #     resolution_fine=res_3d,
    #     height=height_3d,
    #     perspective=perspective,
    #     light_position=light_position,
    #     fringe=fringe,
    #     fringe_color=color_3d,
    #     fringe_elevation=stdev_fringe,
    #     #arrow_position=arrow_position,
    #     #arrow_size=arrow_size,
    #     output=os.path.join(render_3d, stdev_depth),
    #     format=format_3d,
    #     size=size_3d,
    #     errors='ignore'
    #     )
    #
    # # 3D render stdev dem difference
    # gscript.write_command('r.colors',
    #     map=stdev_dem_difference,
    #     rules='-',
    #     stdin=stdev_dem_difference_colors_3d)
    # gscript.run_command('m.nviz.image',
    #     elevation_map=stdev_dem,
    #     color_map=stdev_dem_difference,
    #     resolution_fine=res_3d,
    #     height=height_3d,
    #     perspective=perspective,
    #     light_position=light_position,
    #     fringe=fringe,
    #     fringe_color=color_3d,
    #     fringe_elevation=stdev_fringe,
    #     #arrow_position=arrow_position,
    #     #arrow_size=arrow_size,
    #     output=os.path.join(render_3d, stdev_dem_difference),
    #     format=format_3d,
    #     size=size_3d,
    #     errors='ignore'
    #     )
    #
    # # 3D render stdev dem regression
    # gscript.write_command('r.colors',
    #     map=stdev_dem_regression,
    #     rules='-',
    #     stdin=dem_colors_3d)
    # gscript.run_command('m.nviz.image',
    #     elevation_map=stdev_dem_regression,
    #     color_map=stdev_dem_regression,
    #     resolution_fine=res_3d,
    #     height=height_3d,
    #     perspective=perspective,
    #     light_position=light_position,
    #     fringe=fringe,
    #     fringe_color=color_3d,
    #     fringe_elevation=stdev_fringe,
    #     #arrow_position=arrow_position,
    #     #arrow_size=arrow_size,
    #     output=os.path.join(render_3d, stdev_dem_regression),
    #     format=format_3d,
    #     size=size_3d,
    #     errors='ignore'
    #     )
    #
    # # 3D render stdev dem regression difference
    # gscript.write_command('r.colors',
    #     map=stdev_dem_regression_difference,
    #     rules='-',
    #     stdin=stdev_dem_regression_difference_colors_3d)
    # gscript.run_command('m.nviz.image',
    #     elevation_map=stdev_dem_regression,
    #     color_map=stdev_dem_regression_difference,
    #     resolution_fine=res_3d,
    #     height=height_3d,
    #     perspective=perspective,
    #     light_position=light_position,
    #     fringe=fringe,
    #     fringe_color=color_3d,
    #     fringe_elevation=stdev_fringe,
    #     #arrow_position=arrow_position,
    #     #arrow_size=arrow_size,
    #     output=os.path.join(render_3d, stdev_dem_regression_difference),
    #     format=format_3d,
    #     size=size_3d,
    #     errors='ignore'
    #     )
    #
    # # 3D render stdev slope difference
    # gscript.write_command('r.colors',
    #     map=stdev_slope_difference,
    #     rules='-',
    #     stdin=stdev_slope_difference_colors_3d )
    # gscript.run_command('m.nviz.image',
    #     elevation_map=stdev_dem,
    #     color_map=stdev_slope_difference,
    #     resolution_fine=res_3d,
    #     height=height_3d,
    #     perspective=perspective,
    #     light_position=light_position,
    #     fringe=fringe,
    #     fringe_color=color_3d,
    #     fringe_elevation=stdev_fringe,
    #     #arrow_position=arrow_position,
    #     #arrow_size=arrow_size,
    #     output=os.path.join(render_3d, stdev_slope_difference),
    #     format=format_3d,
    #     size=size_3d,
    #     errors='ignore'
    #     )
    #
    # # 3D render stdev slope regression difference
    # gscript.write_command('r.colors',
    #     map=stdev_slope_regression_difference,
    #     rules='-',
    #     stdin=stdev_slope_difference_colors_3d )
    # gscript.run_command('m.nviz.image',
    #     elevation_map=stdev_dem_regression,
    #     color_map=stdev_slope_regression_difference,
    #     resolution_fine=res_3d,
    #     height=height_3d,
    #     perspective=perspective,
    #     light_position=light_position,
    #     fringe=fringe,
    #     fringe_color=color_3d,
    #     fringe_elevation=stdev_fringe,
    #     #arrow_position=arrow_position,
    #     #arrow_size=arrow_size,
    #     output=os.path.join(render_3d, stdev_slope_regression_difference),
    #     format=format_3d,
    #     size=size_3d,
    #     errors='ignore'
    #     )
    #
    # # 3D render stdev depth difference
    # gscript.write_command('r.colors',
    #     map=stdev_depth_difference,
    #     rules='-',
    #     stdin=flow_difference_colors_3d)
    # gscript.run_command('m.nviz.image',
    #     elevation_map=stdev_dem,
    #     color_map=stdev_depth_difference,
    #     resolution_fine=res_3d,
    #     height=height_3d,
    #     perspective=perspective,
    #     light_position=light_position,
    #     fringe=fringe,
    #     fringe_color=color_3d,
    #     fringe_elevation=stdev_fringe,
    #     #arrow_position=arrow_position,
    #     #arrow_size=arrow_size,
    #     output=os.path.join(render_3d, stdev_depth_difference),
    #     format=format_3d,
    #     size=size_3d,
    #     errors='ignore'
    #     )
    #
    # # 3D render stdev forms difference
    # gscript.write_command('r.colors',
    #     map=stdev_forms_difference,
    #     rules='-',
    #     stdin=forms_difference_colors_3d)
    # gscript.run_command('m.nviz.image',
    #     elevation_map=stdev_dem,
    #     color_map=stdev_forms_difference,
    #     resolution_fine=res_3d,
    #     height=height_3d,
    #     perspective=perspective,
    #     light_position=light_position,
    #     fringe=fringe,
    #     fringe_color=color_3d,
    #     fringe_elevation=stdev_fringe,
    #     #arrow_position=arrow_position,
    #     #arrow_size=arrow_size,
    #     output=os.path.join(render_3d, stdev_forms_difference),
    #     format=format_3d,
    #     size=size_3d,
    #     errors='ignore'
    #     )
