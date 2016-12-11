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
render_3d = os.path.join(gisdbase, location, "render_3d", mapset)

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
-42 blue
0 192:192:192
42 red
nv 192:192:192
default 192:192:192
"""

dem_regression_difference_colors_3d = """\
-36 blue
0 192:192:192
36 red
nv 192:192:192
default 192:192:192
"""

flow_difference_colors_3d = """\
-0.5 blue
0 192:192:192
0.5 red
nv 192:192:192
default 192:192:192
"""

slope_difference_colors_3d = """\
-30 blue
0 192:192:192
30 red
nv 192:192:192
default 192:192:192
"""

forms_difference_colors_3d = """\
-10 blue
0 192:192:192
10 red
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
