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
light_position = (0.68, -0.68 ,0.95)
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
dem_colors_3d = '0% 0:191:191\n20% 0:255:0\n40% 255:255:0\n60% 255:127:0\n80% 191:127:63\n100% 200:200:200\nnv 192:192:192\ndefault 192:192:192'
slope_colors_3d = '0 192:192:192\n2 255:255:0\n5 0:255:0\n10 0:255:255\n15 0:0:255\n30 255:0:255\n50 255:0:0\n90 0:0:0\nnv 192:192:192\ndefault 192:192:192'
depressions_colors_3d = '0% aqua\n100% blue\nnv 192:192:192\ndefault 192:192:192'
depth_colors_3d = '0 192:192:192\n0.001 255:255:0\n0.05 0:255:255\n0.1 0:127:255\n0.5 0:0:255\n100% 0:0:0\nnv 192:192:192\ndefault 192:192:192'
forms_colors_3d = '0 192:192:192\n1 220:220:220\n2 56:0:0\n3 200:0:0\n4 255:80:20\n5 250:210:60\n6 255:255:60\n7 180:230:20\n8 60:250:150\n9 0:0:255\n10 0:0:56\n11 255:0:255\nnv 192:192:192\ndefault 192:192:192'
dem_difference_colors_3d = '-40 blue\n0 192:192:192\n40 red\nnv 192:192:192\ndefault 192:192:192'
flow_difference_colors_3d = '-0.5 blue\n0 192:192:192\n0.5 red\nnv 192:192:192\ndefault 192:192:192'
slope_difference_colors_3d = '-30 blue\n0 192:192:192\n30 red\nnv 192:192:192\ndefault 192:192:192'
forms_difference_colors_3d = '-10 blue\n0 192:192:192\n10 red\nnv 192:192:192\ndefault 192:192:192'

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
    flow_lines = dem.replace("dem","flow_lines")
    mean_peaks = dem.replace("dem","mean_peaks")
    mean_peak_points = dem.replace("dem","mean_peak_points")
    peak_lines= dem.replace("dem","peak_lines")
    mean_pits = dem.replace("dem","mean_pits")
    mean_pit_points = dem.replace("dem","mean_pit_points")
    pit_lines = dem.replace("dem","pit_lines")
    mean_ridges = dem.replace("dem","mean_ridges")
    mean_ridge_points = dem.replace("dem","mean_ridge_points")
    ridge_lines = dem.replace("dem","ridge_lines")
    mean_valleys = dem.replace("dem","mean_valleys")
    mean_valley_points = dem.replace("dem","mean_valley_points")
    valley_lines = dem.replace("dem","valley_lines")

    # set region
    gscript.run_command('g.region',
                        rast=region,
                        res=res)

    # 3D render elevation
    try:
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
                        )
    except:
        pass

    # 3D render slope
    try:
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
                        )
    except:
        pass

    # 3D render landforms
    try:
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
                        )
    except:
        pass

    # 3D render water flow
    try:
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
                        )
    except:
        pass

    # 3D render depressions
    try:
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
                        )
    except:
        pass

    # 3D render difference
    try:
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
                        )
    except:
        pass

    # 3D render concentrated flow
    try:
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
                        )
    except:
        pass

    # 3D render peaks
    try:
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
                        )
    except:
        pass

    # 3D render pits
    try:
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
                        )
    except:
        pass

    # 3D render ridges
    try:
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
                        )
    except:
        pass

    # 3D render valleys
    try:
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
                        )
    except:
        pass

    # 3D render mean elevation
    try:
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
                        )
    except:
        pass

    # 3D render mean slope
    try:
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
                        )
    except:
        pass

    # 3D render mean landforms
    try:
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
                        )
    except:
        pass

    # 3D render mean water flow
    try:
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
                        )
    except:
        pass

    # 3D render mean depressions
    try:
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
                        )
    except:
        pass

    # 3D render mean elevation difference
    try:
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
                        )
    except:
        pass

    # 3D render mean regressed elevation difference
    try:
        gscript.write_command('r.colors',
                            map=mean_dem_regression_difference,
                            rules='-',
                            stdin=dem_difference_colors_3d)
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
                        #arrow_position=arrow_position,
                        #arrow_size=arrow_size,
                        output=os.path.join(render_3d, mean_dem_regression_difference),
                        format=format_3d,
                        size=size_3d,
                        )
    except:
        pass

    # 3D render mean slope difference
    try:
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
                        )
    except:
        pass

    # 3D render mean regressed slope difference
    try:
        gscript.write_command('r.colors',
                            map=mean_slope_regression_difference,
                            rules='-',
                            stdin=slope_difference_colors_3d)
        gscript.run_command('m.nviz.image',
                        elevation_map=mean_dem,
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
                        )
    except:
        pass

    # 3D render mean flow difference
    try:
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
                        )
    except:
        pass

    # 3D render mean flow distance
    try:
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
                        )
    except:
        pass

    # 3D render mean peak distance
    try:
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
                        )
    except:
        pass

    # 3D render mean pit distance
    try:
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
                        )
    except:
        pass

    # 3D render mean ridge distance
    try:
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
                        )
    except:
        pass

    # 3D render mean valley distance
    try:
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
                        )
    except:
        pass
