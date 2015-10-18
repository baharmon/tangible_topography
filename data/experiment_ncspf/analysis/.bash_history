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
H:\tangible_landscape\experiment\code\reinterpolation.py
H:\tangible_landscape\experiment\code\analyses.py
H:\tangible_landscape\experiment\code\covar.py
H:\tangible_landscape\experiment\code\histogram.py
H:\tangible_landscape\experiment\code\series.py
H:\tangible_landscape\experiment\code\univar.py
