# -*- coding: utf-8 -*-

"""
@brief: spatial analysis for the tangible topography experiment

This program is free software under the GNU General Public License
(>=v2). Read the file COPYING that comes with GRASS for details.

@author: Brendan Harmon (brendanharmon@gmail.com)
"""

import os
import sys
import atexit
import grass.script as gscript
from grass.exceptions import CalledModuleError
import matplotlib.pyplot as plt

# set graphics driver
driver = "cairo"

# temporary region
gscript.use_temp_region()

# set environment
env = grass.gisenv()

    env['GRASS_OVERWRITE'] = True
    env['GRASS_VERBOSE'] = False
    env['GRASS_MESSAGE_FORMAT'] = 'standard'
    gisdbase = env['GISDBASE']
    location = env['LOCATION_NAME']
    mapset = env['MAPSET']

    # set rendering directory
    render = os.path.join(gisdbase, location, 'results')

# set paramters
#overwrite = True

# set variables
experiments = 7
iterator = experiments+1

# set color rules
depressions_colors = '0% aqua\n100% blue'
depth_colors = '0 255:255:255\n0.001 255:255:0\n0.05 0:255:255\n0.1 0:127:255\n0.5 0:0:255\n100% 0:0:0'
difference_colors = '-0.5 blue\n0 white\n0.5 red'

# set region
region = "dem@PERMANENT"
gscript.run_command('g.region', rast=region, res=3)

# driver settings
info = gscript.parse_command('r.info', map=region, flags='g')
width = int(info.cols)+int(info.cols)/2
height = int(info.rows)

def main():
    reference()
    analysis()
    #cells, distance = analysis()
    #plot(cells, distance)
    atexit.register(cleanup)
    sys.exit(0)

def cleanup():
    try:
        # remove temporary maps
        gscript.run_command('g.remove', type='raster', name=['depressionless_dem', 'flow_dir', 'dx', 'dy'], flags='f')

    except CalledModuleError:
        pass

def reference():
    """Spatial analyses of the reference maps"""

    # list scanned DEMs
    dems = gscript.list_grouped('rast', pattern='dem*')['PERMANENT']

    # iterate through scanned DEMs
    for dem in dems:

        # variables
        region = dem
        relief = dem.replace("dem","relief")
        contour = dem.replace("dem","contour")
        slope = dem.replace("dem","slope")
        forms = dem.replace("dem","forms")
        depth = dem.replace("dem","depth")
        dem_before = dem
        dem_after = dem
        dem_difference = dem.replace("dem","dem_difference")
        slope_before = slope
        slope_after = slope
        slope_difference = dem.replace("dem","slope_difference")
        forms_before = forms
        forms_after = forms
        forms_difference = dem.replace("dem","forms_difference")
        depth_before = depth
        depth_after = depth
        depth_difference = dem.replace("dem","depth_difference")
        depressions = dem.replace("dem","depressions")
        concentrated_flow = dem.replace("dem","concentrated_flow")
        concentrated_points = dem.replace("dem","concentrated_points")
        peaks = dem.replace("dem","peaks")
        peak_points = dem.replace("dem","peak_points")
        pits = dem.replace("dem","pits")
        pit_points = dem.replace("dem","pit_points")
        ridges = dem.replace("dem","ridges")
        ridge_points = dem.replace("dem","ridge_points")
        valleys = dem.replace("dem","valleys")
        valley_points = dem.replace("dem","valley_points")
        npoints = "100%"

        # set region
        gscript.run_command('g.region', rast=region, res=3)

        # render DEM
        info = gscript.parse_command('r.info', map=dem, flags='g')
        width=int(info.cols)+int(info.cols)/2
        height=int(info.rows)
        gscript.run_command('d.mon', start=driver, width=width, height=height,  output=os.path.join(render,dem+".png"), env=env)
        gscript.run_command('r.colors', map=dem, color="elevation")
        gscript.run_command('r.relief', input=dem, output=relief, altitude=90, azimuth=45, zscale=1, units="intl", env=env)
        gscript.run_command('r.contour', input=dem, output=contour, step=5, env=env)
        gscript.run_command('d.shade', shade=relief, color=dem, brighten=75)
        gscript.run_command('d.vect', map=contour, display="shape")
        gscript.run_command('d.legend', raster=dem, fontsize=9, at=(10,70,1,4))
        gscript.run_command('d.mon', stop=driver)

        # compute slope
        gscript.run_command('d.mon', start=driver, width=width, height=height,  output=os.path.join(render,slope+".png"), env=env)
        gscript.run_command('r.param.scale', input=dem, output=slope, size=9, method="slope", env=env)
        gscript.run_command('r.colors', map=slope, color="slope")
        gscript.run_command('d.shade', shade=relief, color=slope, brighten=75)
        gscript.run_command('d.vect', map=contour, display='shape')
        gscript.run_command('d.legend', raster=slope, fontsize=9, at=(10,90,1,4))
        gscript.run_command('d.mon', stop=driver)

        #compute geomorphon
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,forms+".png"), env=env)
        gscript.run_command('r.geomorphon', dem=dem, forms=forms, search=9, skip=6, env=env)
        gscript.run_command('d.shade', shade=relief, color=forms, brighten=75)
        gscript.run_command('d.vect', map=contour, display='shape')
        gscript.run_command('d.legend', raster=forms, fontsize=9, at=(10,90,1,4))
        gscript.run_command('d.mon', stop=driver)

        # simulate water flow
        gscript.run_command('d.mon', start=driver, width=width, height=height,  output=os.path.join(render,depth+".png"), env=env)
        gscript.run_command('r.slope.aspect', elevation=dem, dx='dx', dy='dy', env=env)
        gscript.run_command('r.sim.water', elevation=dem, dx='dx', dy='dy', rain_value=300, depth=depth, nwalkers=5000, niterations=4, env=env)
        gscript.run_command('g.remove', flags='f', type='raster', name=['dx', 'dy'])
        gscript.run_command('d.shade', shade=relief, color=depth, brighten=75)
        gscript.run_command('d.vect', map=contour, display='shape')
        gscript.run_command('d.legend', raster=depth, fontsize=9, at=(10,90,1,4))
        gscript.run_command('d.mon', stop=driver)

        # identify depressions
        gscript.run_command('r.fill.dir', input=dem, output='depressionless_dem', direction='flow_dir',env=env)
        gscript.run_command('r.mapcalc', expression='{depressions} = if({depressionless_dem} - {dem} > {depth}, {depressionless_dem} - {dem}, null())'.format(depressions=depressions, depressionless_dem='depressionless_dem', dem=dem, depth=0), env=env)
        gscript.write_command('r.colors', map=depressions, rules='-', stdin=depressions_colors)
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,depressions+".png"), env=env)
        gscript.run_command('d.shade', shade=relief, color=depressions, brighten=75)
        gscript.run_command('d.vect', map=contour, display='shape')
        gscript.run_command('d.legend', raster=depressions, fontsize=9, at=(10,90,1,4))
        gscript.run_command('d.mon', stop=driver)

        # compute the difference between the modeled and reference elevation
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,dem_difference+".png"), env=env)
        gscript.run_command('r.mapcalc', expression='{difference} = {before} - {after}'.format(before=dem_before,after=dem_after,difference=dem_difference), env=env)
        gscript.write_command('r.colors', map=dem_difference, rules='-', stdin=difference_colors)
        gscript.run_command('d.shade', shade=relief, color=dem_difference, brighten=75)
        gscript.run_command('d.vect', map=contour, display='shape')
        gscript.run_command('d.legend', raster=dem_difference, fontsize=9, at=(10,90,1,4))
        gscript.run_command('d.mon', stop=driver)

        # compute the difference between the modeled and reference slope
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,slope_difference+".png"), env=env)
        gscript.run_command('r.mapcalc', expression='{difference} = {before} - {after}'.format(before=slope_before,after=slope_after,difference=slope_difference), env=env)
        gscript.write_command('r.colors', map=slope_difference, rules='-', stdin=difference_colors)
        gscript.run_command('d.shade', shade=relief, color=slope_difference, brighten=75)
        gscript.run_command('d.vect', map=contour, display='shape')
        gscript.run_command('d.legend', raster=slope_difference, fontsize=9, at=(10,90,1,4))
        gscript.run_command('d.mon', stop=driver)

        # compute the difference between the modeled and reference landorms
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,forms_difference+".png"), env=env)
        gscript.run_command('r.mapcalc', expression='{difference} = {before} - {after}'.format(before=forms_before,after=forms_after,difference=forms_difference), env=env)
        gscript.write_command('r.colors', map=forms_difference, rules='-', stdin=difference_colors)
        gscript.run_command('d.shade', shade=relief, color=forms_difference, brighten=75)
        gscript.run_command('d.vect', map=contour, display='shape')
        gscript.run_command('d.legend', raster=forms_difference, fontsize=9, at=(10,90,1,4))
        gscript.run_command('d.mon', stop=driver)

        # compute the difference between the modeled and reference flow depth
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,depth_difference+".png"), env=env)
        gscript.run_command('r.mapcalc', expression='{difference} = {before} - {after}'.format(before=depth_before,after=depth_after,difference=depth_difference), env=env)
        gscript.write_command('r.colors', map=depth_difference, rules='-', stdin=difference_colors)
        gscript.run_command('d.shade', shade=relief, color=depth_difference, brighten=75)
        gscript.run_command('d.vect', map=contour, display='shape')
        gscript.run_command('d.legend', raster=depth_difference, fontsize=9, at=(10,90,1,4))
        gscript.run_command('d.mon', stop=driver)

        # extract peaks
        gscript.run_command('r.mapcalc', expression='{peaks} = if({forms}==2,2,null())'.format(peaks=peaks,forms=forms), env=env)
        gscript.run_command('r.colors', map=peaks, raster=forms)
        gscript.run_command('r.random', input=peaks, npoints=npoints, vector=peak_points, env=env)
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,peaks+".png"), env=env)
        gscript.run_command('d.shade', shade=relief, color=peaks, brighten=75)
        gscript.run_command('d.vect', map=peak_points, display='shape')
        gscript.run_command('d.legend', raster=peaks, fontsize=9, at=(10,90,1,4))
        gscript.run_command('d.mon', stop=driver)

        # extract pits
        gscript.run_command('r.mapcalc', expression='{pits} = if({forms}==10,10,null())'.format(pits=pits,forms=forms), env=env)
        gscript.run_command('r.colors', map=pits, raster=forms)
        gscript.run_command('r.random', input=pits, npoints=npoints, vector=pit_points, env=env)
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,pits+".png"), env=env)
        gscript.run_command('d.shade', shade=relief, color=pits, brighten=75)
        gscript.run_command('d.vect', map=pit_points, display='shape')
        gscript.run_command('d.legend', raster=pits, fontsize=9, at=(10,90,1,4))
        gscript.run_command('d.mon', stop=driver)

        # extract ridges
        gscript.run_command('r.mapcalc', expression='{ridges} = if({forms}==3,3,null())'.format(ridges=ridges,forms=forms), env=env)
        gscript.run_command('r.colors', map=ridges, raster=forms)
        gscript.run_command('r.random', input=ridges, npoints=npoints, vector=ridge_points, env=env)
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,ridges+".png"), env=env)
        gscript.run_command('d.shade', shade=relief, color=ridges, brighten=75)
        gscript.run_command('d.vect', map=ridge_points, display='shape')
        gscript.run_command('d.legend', raster=ridges, fontsize=9, at=(10,90,1,4))
        gscript.run_command('d.mon', stop=driver)

        # extract valleys
        gscript.run_command('r.mapcalc', expression='{valleys} = if({forms}==9,9,null())'.format(valleys=valleys,forms=forms), env=env)
        gscript.run_command('r.colors', map=valleys, raster=forms)
        gscript.run_command('r.random', input=valleys, npoints=npoints, vector=valley_points, env=env)
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,valleys+".png"), env=env)
        gscript.run_command('d.shade', shade=relief, color=valleys, brighten=75)
        gscript.run_command('d.vect', map=valley_points, display='shape')
        gscript.run_command('d.legend', raster=valleys, fontsize=9, at=(10,90,1,4))
        gscript.run_command('d.mon', stop=driver)

        # extract concentrated flow
        gscript.run_command('r.mapcalc', expression='{concentrated_flow} = if({depth}>=0.05,{depth},null())'.format(depth=depth,concentrated_flow=concentrated_flow), env=env)
        gscript.write_command('r.colors', map=concentrated_flow, rules='-', stdin=depth_colors)
        gscript.run_command('r.random', input=concentrated_flow, npoints=npoints, vector=concentrated_points, env=env)
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(render,concentrated_flow+".png"), env=env)
        gscript.run_command('d.shade', shade=relief, color=concentrated_flow, brighten=75)
        gscript.run_command('d.vect', map=concentrated_points, display='shape')
        gscript.run_command('d.legend', raster=concentrated_flow, fontsize=9, at=(10,90,1,4))
        gscript.run_command('d.mon', stop=driver)

        # compute number of cells with depressions
        univar = gscript.parse_command('r.univar', map=depressions, separator='newline', flags='g')
        depression_cells =  float(univar['sum'])
        print 'cells in ' + dem + ' with depressions: ' + str(depression_cells)

        # compute number of cells with peaks
        univar = gscript.parse_command('r.univar', map=peaks, separator='newline', flags='g')
        peak_cells =  float(univar['sum'])
        print 'cells in ' + dem + ' with peaks: ' + str(peak_cells)

        # compute number of cells with pits
        univar = gscript.parse_command('r.univar', map=pits, separator='newline', flags='g')
        pit_cells =  float(univar['sum'])
        print 'cells in ' + dem + ' with pits: ' + str(pit_cells)

        # compute number of cells with ridges
        univar = gscript.parse_command('r.univar', map=ridges, separator='newline', flags='g')
        ridge_cells =  float(univar['sum'])
        print 'cells in ' + dem + ' with ridges: ' + str(ridge_cells)

        # compute number of cells with valleys
        univar = gscript.parse_command('r.univar', map=valleys, separator='newline', flags='g')
        valley_cells =  float(univar['sum'])
        print 'cells in ' + dem + ' valleys: ' + str(valley_cells)

def analysis():
    """compute the difference, water flow, depressions, and concentrated flow for each series of models"""

    # list reference DEMs
    dems = gscript.list_grouped('rast', pattern='dem*')['PERMANENT']

    # iterate through reference DEMs
    for dem in dems:

        # list scanned DEMs
        dem_list = gscript.list_grouped('rast', pattern='*'+dem)['analysis']

        # variables
        region = dem
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
        flow_distance = dem.replace("dem","flow_distance")
        mean_peaks = dem.replace("dem","mean_peaks")
        mean_peak_points = dem.replace("dem","mean_peak_points")
        peak_points = dem.replace("dem","peak_points")
        copied_peak_points = dem.replace("dem","copied_peak_points")
        peak_distance = dem.replace("dem","peak_distance")
        mean_pits = dem.replace("dem","mean_pits")
        mean_pit_points = dem.replace("dem","mean_pit_points")
        pit_points = dem.replace("dem","pit_points")
        copied_pit_points = dem.replace("dem","copied_pit_points")
        pit_distance = dem.replace("dem","pit_distance")
        mean_ridges = dem.replace("dem","mean_ridges")
        mean_ridge_points = dem.replace("dem","mean_ridge_points")
        ridge_points = dem.replace("dem","ridge_points")
        copied_ridge_points = dem.replace("dem","copied_ridge_points")
        ridge_distance = dem.replace("dem","ridge_distance")
        mean_valleys = dem.replace("dem","mean_valleys")
        mean_valley_points = dem.replace("dem","mean_valley_points")
        valley_points = dem.replace("dem","valley_points")
        copied_valley_points = dem.replace("dem","copied_valley_points")
        valley_distance = dem.replace("dem","valley_distance")
        npoints = "100%"

        # initialize arrays
        cells = []
        distance = []

        # set region
        gscript.run_command('g.region', rast=region, res=3)

        # compute mean DEM
        gscript.run_command('r.series', input=dem_list, output=mean_dem, method="average", env=env)
        gscript.run_command('r.colors', map=mean_dem, color="elevation")
        gscript.run_command('r.relief', input=mean_dem, output=mean_relief, altitude=90, azimuth=45, zscale=1, units="intl", env=env)
        gscript.run_command('r.contour', input=mean_dem, output=mean_contour, step=5, env=env)
        info = gscript.parse_command('r.info', map=dem, flags='g')
        width=int(info.cols)+int(info.cols)/2
        height=int(info.rows)
        gscript.run_command('d.mon', start=driver, width=width, height=height,  output=os.path.join(render,mean_dem+".png"), env=env)
        gscript.run_command('d.shade', shade=mean_relief, color=mean_dem, brighten=75)
        gscript.run_command('d.vect', map=mean_contour, display="shape")
        gscript.run_command('d.legend', raster=mean_dem, fontsize=9, at=(10,70,1,4))
        gscript.run_command('d.mon', stop=driver)

        # compute mean slope










# ADAPT CODE FROM REFERENCE FUNCTION


# EDITING HERE

        # compute the mean of depths
        gscript.run_command('r.series', input=depth_list, output=mean_depth, method="average", env=env)
        gscript.write_command('r.colors', map=mean_depth, rules='-', stdin=depth_colors)
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(series, mean_depth+".png"), env=env)
        gscript.run_command('d.shade', shade=reference_relief, color=mean_depth, brighten=75)
        gscript.run_command('d.vect', map=reference_contour, display='shape')
        gscript.run_command('d.legend', raster=mean_depth, fontsize=9, at=(10, 90, 1, 4))
        gscript.run_command('d.mon', stop=driver)

        # compute mean of differences of depths
        gscript.run_command('r.series', input=diff_list, output=mean_diff, method="average", env=env)
        gscript.run_command('r.colors', map=mean_diff, color='differences')
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(series, mean_diff+".png"), env=env)
        gscript.run_command('d.shade', shade=reference_relief, color=mean_diff, brighten=75)
        gscript.run_command('d.vect', map=reference_contour, display='shape')
        gscript.run_command('d.legend', raster=mean_diff, fontsize=9, at=(10, 90 ,1 ,4))
        gscript.run_command('d.mon', stop=driver)

        # compute maximum flow depth
        gscript.run_command('r.series', input=depth_list, output=max_depth, method="maximum", env=env)
        gscript.write_command('r.colors', map=max_depth, rules='-', stdin=depth_colors)
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(series, max_depth+".png"), env=env)
        gscript.run_command('d.shade', shade=reference_relief, color=max_depth, brighten=75)
        gscript.run_command('d.vect', map=reference_contour, display='shape')
        gscript.run_command('d.legend', raster=max_depth, fontsize=9, at=(10, 90, 1, 4))
        gscript.run_command('d.mon', stop=driver)

        # compute sum of flow depth
        gscript.run_command('r.series', input=depth_list, output=sum_depth, method="sum", env=env)
        gscript.write_command('r.colors', map=sum_depth, rules='-', stdin=depth_colors)
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(series, sum_depth+".png"), env=env)
        gscript.run_command('d.shade', shade=reference_relief, color=sum_depth, brighten=75)
        gscript.run_command('d.vect', map=reference_contour, display='shape')
        gscript.run_command('d.legend', raster=sum_depth, fontsize=9, at=(10, 90, 1, 4))
        gscript.run_command('d.mon', stop=driver)

        # compute mean depressions
        gscript.run_command('r.series', input=depressions_list, output=mean_depressions, method="average", env=env)
        gscript.write_command('r.colors', map=mean_depressions, rules='-', stdin=depressions_colors)
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(series, mean_depressions+".png"), env=env)
        gscript.run_command('d.shade', shade=reference_relief, color=mean_depressions, brighten=75)
        gscript.run_command('d.vect', map=reference_contour, display='shape')
        gscript.run_command('d.legend', raster=mean_depressions, fontsize=9, at=(10, 90, 1, 4))
        gscript.run_command('d.mon', stop=driver)

        # compute maximum depressions
        gscript.run_command('r.series', input=depressions_list,
                            output=max_depressions, method="maximum", env=env)
        gscript.write_command('r.colors', map=max_depressions, rules='-', stdin=depressions_colors)
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(series,max_depressions+".png"), env=env)
        gscript.run_command('d.shade', shade=reference_relief, color=max_depressions, brighten=75)
        gscript.run_command('d.vect', map=reference_contour, display='shape')
        gscript.run_command('d.legend', raster=max_depressions, fontsize=9, at=(10, 90, 1, 4))
        gscript.run_command('d.mon', stop=driver)

        # compute sum of depressions
        gscript.run_command('r.series', input=depressions_list, output=sum_depressions, method="sum", env=env)
        gscript.write_command('r.colors', map=sum_depressions, rules='-', stdin=depressions_colors)
        gscript.run_command('d.mon', start=driver, width=width, height=height, output=os.path.join(series, sum_depressions+".png"), env=env)
        gscript.run_command('d.shade', shade=reference_relief, color=sum_depressions, brighten=75)
        gscript.run_command('d.vect', map=reference_contour, display='shape')
        gscript.run_command('d.legend', raster=sum_depressions, fontsize=9, at=(10, 90, 1, 4))
        gscript.run_command('d.mon', stop=driver)

        # extract concentrated flow
        gscript.run_command('r.mapcalc', expression='{concentrated_flow} = if({mean_depth}>=0.05,{mean_depth},null())'.format(mean_depth=mean_depth, concentrated_flow=concentrated_flow), env=env)
        gscript.write_command('r.colors', map=concentrated_flow, rules='-', stdin=depth_colors)
        gscript.run_command('r.random', input=concentrated_flow, npoints='100%', vector=concentrated_points, env=env)

        # compute distance from reference
        gscript.run_command('g.copy', vector=[reference_points+'@PERMANENT', copied_points], env=env)
        gscript.run_command('v.db.addcolumn', map=copied_points, columns='distance INTEGER', env=env)
        gscript.run_command('v.distance', from_=copied_points, to=concentrated_points, upload='dist', column='distance', output=flow_distance, separator='newline', env=env)
        univar_distance = gscript.parse_command('v.db.univar', map=copied_points, column='distance', flags='g', env=env)
        dist = float(univar_distance['sum'])
        distance.append(dist)
        print 'sum of min distance in experiment '+str(i)+': ' + str(dist)
        mean_dist = float(univar_distance['mean'])
        print 'mean of min distance in experiment '+str(i)+': ' + str(mean_dist)

        # render
        gscript.run_command('d.mon', start=driver, width=width*2, height=height*2, output=os.path.join(series,concentrated_flow+".png"), env=env)
        gscript.run_command('d.shade', shade=reference_relief, color=mean_diff, brighten=75)
        gscript.run_command('d.vect', map=reference_contour, display='shape')
        gscript.run_command('d.vect', map=reference_points, display='shape', color='blue')
        gscript.run_command('d.vect', map=concentrated_points, display='shape', color='red')
        gscript.run_command('d.vect', map=flow_distance, display='shape')
        gscript.run_command('d.mon', stop=driver)

        # compute number of cells with depressions
        univar = gscript.parse_command('r.univar', map=sum_depressions, separator='newline', flags='g')
        nulls = float(univar['null_cells'])
        depression_cells = total_count - nulls
        depression_percent = depression_cells/total_count*100
        cells.append(depression_percent)
        print 'percent of cells with depressions in experiment '+str(i)+': ' + str(depression_percent)


    #
    # # compute percentage of cells with depressions in the reference
    # univar_ref_cells = gscript.parse_command('r.univar', map="depressions@PERMANENT", separator='newline', flags='g')
    # total_count = float(univar_ref_cells['cells'])
    # null_count = float(univar_ref_cells['null_cells'])
    # depression_count = total_count - null_count
    # reference_percent = depression_count/total_count*100
    # cells.append(reference_percent)
    # print 'percentage cells with depressions in reference: ' + str(reference_percent)


    # return cells, distance

if __name__ == "__main__":
    atexit.register(cleanup)
    sys.exit(main())
