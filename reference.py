
def reference():
    """Spatial analyses of the reference maps"""

    # list scanned DEMs
    dems = gscript.list_grouped('rast', pattern='*dem*')['PERMANENT']

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
        gscript.run_command('g.region', rast="dem")
        gscript.run_command('r.relief', input=dem, output=relief, altitude=90, azimuth=45, zscale=1, units="intl", env=env)
        gscript.run_command('g.region', rast=region)
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
        print 'cells with depressions: ' + str(depression_cells)

        # compute number of cells with peaks
        univar = gscript.parse_command('r.univar', map=peaks, separator='newline', flags='g')
        peak_cells =  float(univar['sum'])
        print 'cells with peaks: ' + str(peak_cells)

        # compute number of cells with pits
        univar = gscript.parse_command('r.univar', map=pits, separator='newline', flags='g')
        pit_cells =  float(univar['sum'])
        print 'cells with pits: ' + str(pit_cells)

        # compute number of cells with ridges
        univar = gscript.parse_command('r.univar', map=ridges, separator='newline', flags='g')
        ridge_cells =  float(univar['sum'])
        print 'cells with ridges: ' + str(ridge_cells)

        # compute number of cells with valleys
        univar = gscript.parse_command('r.univar', map=valleys, separator='newline', flags='g')
        valley_cells =  float(univar['sum'])
        print 'cells with valleys: ' + str(valley_cells)
