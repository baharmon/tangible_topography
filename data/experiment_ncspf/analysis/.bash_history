g.region raster=dem@PERMANENT
H:\tangible_landscape\experiment\code\preprocessing\copy.py
C:\Users\Brendan\Documents\grassdata\copy.py
g.copy
g.copy
C:\Users\Brendan\Documents\grassdata\copy.py
g.copy raster=anderson_dem_1@anderson,anderson_dem_1
g.copy raster=anderson_dem_2@anderson,anderson_dem_2
C:\Users\Brendan\Documents\grassdata\copy.py
C:\Users\Brendan\Documents\grassdata\map_copy.py
g.copy raster=anderson_dem_3@anderson,anderson_dem_3
g.copy raster=anderson_dem_4@anderson,anderson_dem_4
g.copy raster=anderson_dem_5@anderson,anderson_dem_5
C:\Users\Brendan\Documents\grassdata\map_copy.py
C:\Users\Brendan\Documents\grassdata\analyses.py
C:\Users\Brendan\Documents\grassdata\map_copy.py
g.copy
g.copy raster=scan_exp1@connie,connie_dem_1
g.copy raster=scan_exp2@connie,connie_dem_2
g.copy raster=scan_exp3@connie,connie_dem_3
g.copy raster=scan_exp4@connie,connie_dem_4
g.copy raster=scan_exp5@connie,connie_dem_5
C:\Users\Brendan\Documents\grassdata\map_copy.py
C:\Users\Brendan\Documents\grassdata\map_copy.py
g.copy raster=mccoy_01@mccoy,mccoy_dem_1
g.copy raster=mccoy_02@mccoy,mccoy_dem_2
g.copy raster=mccoy_03@mccoy,mccoy_dem_3
g.copy raster=mccoy_04@mccoy,mccoy_dem_4
g.copy raster=mccoy_05@mccoy,mccoy_dem_5
g.copy
g.copy raster=scan_saved1@art,art_dem_1
g.copy raster=scan_saved2@art,art_dem_2
g.copy raster=scan_saved3@art,art_dem_3
g.copy raster=scan_saved4@art,art_dem_4
g.copy raster=scan_saved5@art,art_dem_5
g.copy
g.copy
g.copy
g.region raster=dem@PERMANENT
C:\Users\Brendan\Documents\grassdata\map_copy.py
C:\Users\Brendan\Documents\grassdata\map_copy.py
C:\Users\Brendan\Documents\grassdata\map_copy.py
C:\Users\Brendan\Documents\grassdata\map_copy.py
C:\Users\Brendan\Documents\grassdata\map_copy.py
C:\Users\Brendan\Documents\grassdata\map_copy.py
C:\Users\Brendan\Documents\grassdata\map_copy.py
C:\Users\Brendan\Documents\grassdata\map_copy.py
C:\Users\Brendan\Documents\grassdata\map_copy.py
r.in.gdal input=H:\tangible_landscape\experiment\vue\vue_dems\anderson.tif output=anderson --overwrite -o
r.in.gdal input=H:\tangible_landscape\experiment\vue\vue_dems\connie.tif output=connie --overwrite -o
r.in.gdal input=H:\tangible_landscape\experiment\vue\vue_dems\magallanes.tif output=magallanes --overwrite -o
r.in.gdal input=H:\tangible_landscape\experiment\vue\vue_dems\mccoy.tif output=mccoy --overwrite -o
g.remove
C:\Users\Brendan\Documents\grassdata\map_copy.py
C:\Users\Brendan\Documents\grassdata\map_copy.py
C:\Users\Brendan\Documents\grassdata\map_copy.py
C:\Users\Brendan\Documents\grassdata\reinterpolation.py
g.copy
g.copy raster=scan_saved5@art,art_dem_1
g.copy --overwrite raster=scan_saved5@art,art_dem_1
g.copy --overwrite raster=scan_saved1@art,art_dem_2
g.copy --overwrite raster=scan_saved2@art,art_dem_3
g.copy --overwrite raster=scan_saved3@art,art_dem_4
g.copy --overwrite raster=scan_saved4@art,art_dem_5
g.remove
g.remove type=raster pattern=*depth
g.remove type=raster pattern=*depth*
g.copy
g.copy raster=scan_exp1@kofi,kofi_dem_1
g.copy raster=scan_exp2@kofi,kofi_dem_2
g.copy raster=scan_exp3@kofi,kofi_dem_3
g.copy raster=scan_exp4@kofi,kofi_dem_4
g.copy raster=scan_exp5@kofi,kofi_dem_5
r.in.gdal input=C:\Users\Brendan\Desktop\rhino_experiments\rhino_dems\kofi.tif output=kofi_dem_6 -o
r.colors map=kofi_dem_6@raw color=elevation
r.in.gdal input=C:\Users\Brendan\Desktop\rhino_experiments\rhino_dems\schoenthaler.tif output=schoenthaler_dem_6 -o
r.colors map=schoenthaler_dem_6@raw color=elevation
r.in.gdal input=C:\Users\Brendan\Desktop\vue_experiments\vue_dems\schoenthaler.tif output=schoenthaler_dem_7 -o
r.colors map=schoenthaler_dem_7@raw color=elevation
r.in.gdal input=C:\Users\Brendan\Desktop\vue_experiments\vue_dems\kofi.tif output=kofi_dem_7 -o
r.colors map=kofi_dem_7@raw color=elevation
i.rotate
g.extension
g.extension extension=i.rotate operation=add
i.rotate
i.rotate --ui
i.rotate input=schoenthaler_dem_7@raw output=schoenthaler_dem_7_rotate angle=-90
i.rotate --overwrite --verbose input=schoenthaler_dem_7@raw output=schoenthaler_dem_7_rotate angle=-90
i.rotate --overwrite --verbose input=schoenthaler_dem_7@raw output=schoenthaler_dem_7_rotate angle=-90
i.rotate --overwrite --verbose input=schoenthaler_dem_7@raw output=schoenthaler_dem_7_rotate angle=-90
i.rotate --overwrite --verbose input=schoenthaler_dem_7@raw output=schoenthaler_dem_7_rotate angle=-90
i.rotate --overwrite --verbose input=schoenthaler_dem_7@raw output=schoenthaler_dem_7_rotate angle=90
r.info map=schoenthaler_dem_7_rotate@raw
g.remove
g.remove type=raster name=schoenthaler_dem_7_rotate@raw
g.remove -f type=raster name=schoenthaler_dem_7_rotate@raw
g.remove
g.remove type=raster name=schoenthaler_dem_7
g.remove -f type=raster name=schoenthaler_dem_7
g.region raster=dem_4@PERMANENT
v.in.ascii -z -n -t -r input=C:\Users\Brendan\Desktop\vue_experiments\vue_dems\schoenthaler_points_7.txt output=schoenthaler_points_7 separator=comma z=3
v.in.ascii -z -n -t -r input=C:\Users\Brendan\Desktop\vue_experiments\vue_dems\schoenthaler_points_7.txt output=schoenthaler_points_7 separator=comma z=3
r.in.ascii --quiet input=C:\Users\Brendan\Desktop\vue_experiments\vue_dems\schoenthaler_points_7.txt output=schoenthaler_bin_7 type=DCELL
C:\Users\Brendan\tangible_topography\code\preprocessing\reinterpolation_vue.py
g.remove
g.remove type=vector name=schoenthaler_points_7
g.remove -f type=vector name=schoenthaler_points_7
g.rename
g.copy
g.copy
C:\Users\Brendan\Documents\grassdata\copy.py
C:\Users\Brendan\Documents\grassdata\copy.py
C:\Users\Brendan\Documents\grassdata\copy.py
C:\Users\Brendan\Documents\grassdata\mapset_copy.py
C:\Users\Brendan\Documents\grassdata\mapset_copy.py
C:\Users\Brendan\Documents\grassdata\mapset_copy.py
C:\Users\Brendan\Documents\grassdata\map_copy.py
C:\Users\Brendan\Documents\grassdata\map_copy.py
C:\Users\Brendan\Documents\grassdata\hello_world.py
C:\Users\Brendan\Documents\grassdata\hellow_world.py
C:\Users\Brendan\Documents\grassdata\hello_world.py
C:\Users\Brendan\Documents\grassdata\hello_world.py
C:\Users\Brendan\Documents\grassdata\hello_world.py
C:\Users\Brendan\Documents\grassdata\mapset_copy.py
C:\Users\Brendan\Documents\grassdata\mapset_copy.py
r.region map=leab_dem_1 raster=dem_1@PERMANENT
C:\Users\Brendan\tangible_topography\code\preprocessing\reinterpolation.py
C:\Users\Brendan\tangible_topography\code\preprocessing\reinterpolation.py
C:\Users\Brendan\tangible_topography\code\analyses.py
C:\Users\Brendan\tangible_topography\code\analyses.py
C:\Users\Brendan\tangible_topography\code\analyses.py
C:\Users\Brendan\tangible_topography\code\analyses.py
C:\Users\Brendan\tangible_topography\code\set_colors.py
C:\Users\Brendan\tangible_topography\code\covar.py
C:\Users\Brendan\tangible_topography\code\series.py
C:\Users\Brendan\tangible_topography\code\univar.py
C:\Users\Brendan\tangible_topography\code\histogram.py
