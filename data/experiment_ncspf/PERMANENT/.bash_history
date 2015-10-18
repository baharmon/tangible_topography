g.list rast
g.list vect
g.region -p
ls
v.in.ogr help
ls
v.in.shape Zipcodes.shp out=wzipcodes
v.in.ogr -e Zipcodes.shp out=wzipcodes
vi zipimport
g.region -p
g.list vect
v.info wzipcodes
ls
v.in.ogr majorroads.shp out=roads_major
g.region vect=roads_major -p
g.region res=30 -p
d.mon x0
d.vect roads_major
g.list vect
d.vect wzipcodes type=boundary co=red
g.rename vect=roads_major,wroads_major
ls
v.in.ogr soils.shp out=wsoils
g.list vect
d.vect wsoils type=boundary co=green
ls
g.region -p
ls
ls *.shp
v.in.ogr schoolsJuly06.shp out=wschools
v.in.ogr -o schoolsJuly06.shp out=wschools
d.vect wschools co=red
ls
ls *.shp
v.in.ogr wakecounty_hl.shp out=wakecounty_hl
d.vect wakecounty_hl co=blue
d.erase
d.vect wakecounty_hl
g.rename vect=wakecounty_hl,whydrolines
ls *.shp
ls
unzip Hydro_poly.zip
v.in.ogr wakecounty_hp.shp out=whydroareas
ls
vi wakecounty_hp.dbf
v.in.ogr wakecounty_hp.shp out=whydroareas
v.in.ogr wakecounty_hp.shp out=whydroareas --o
g.list vect
d.vect whydroareas co=blue
ls
unzip ctracts2000.zip
v.in.ogr -o ctracts2000.shp out=wcensus2000
d.vect census2000 co=red
g.list vect
d.vect wcensus2000 type=boundar co=red
d.vect wcensus2000 type=boundary co=red
ls
unzip cozone.zip
v.in.ogr cozoning.shp out=wzoning
ls
v.in.dxf help
ls
unzip FootprintsP079220.ZIP
v.in.dxf -l P079220.DXF
v.in.dxf P079220.DXF out=wfootprints layers=BLDG_COMMER_BL,BLDG_UC_BL,BLDG_UC_LAB
d.vect wfootprints co=red
d.vect wfootprints co=green
ls
unzip propertysw.zip
v.in.ogr propertysw.shp out=wswproperty
ls
v.in.ogr Streets.shp out=wstreets
d.vect wstreets co=green
d.erase
g.list vect
d.vect wroads_major
d.zoom
g.list vect
d.vect whydrolines co=blue
d.vect whydroareas
d.vect wstreets co=grey
g.region -p
v.info -c wsoils
v.to.rast wsoils out=wsoilscat_30m
v.to.rast help
v.to.rast wsoils out=wsoilscat_30m use=cat
d.rast wsoilscat_30m
r.colors help
r.colors wsoilscat_30m co=random
d.rast wsoilscat_30m
v.to.rast wsoils out=wsoilsID_30m col=SOILS_ID
d.rast wsoilsID_30m
r.colors wsoilsID_30m co=random
r.colors wsoilsID_30m co=rules
r.colors wsoilsID_30m co=rainbow
d.rast wsoilsID_30m
exit
g.list rast
g.list vect
d.mon x0
d.vect wstreets
d.zoom
ls
locate BE3720078300WC20020828
cd /bigdata/lindata/lindata0304/indata/lncosgeo/ncstpft/NC_flood/10K_DEM_Export/Delivery/PntsBlin/Neuse/
ls
v.in.ascii -ztb BE3720079200WC20020829.txt out=lid79200_pts z=3
vi BE3720079200WC20020829.txt
v.in.ascii -ztb BE3720079200WC20020829.txt out=lid79200_pts z=3 fs=,
d.vect lid79200_pts siz=1
ls
g.region -p
g.region res=10 -p
d.zoom
d.zoom
g.region -p
g.region res=6 -p
v.surf.rst lid79200_pts elev=elevlid_6ft lay=0 segmax=30 npmin=120
d.rast elevlid_6ft
d.vect lid79200_pts siz=1
g.region -p
nviz elevlid_6ft 
g.region res=3 -p
history
v.surf.rst lid79200_pts elev=elevlid_3ft lay=0 segmax=30 npmin=120
d.erase
nviz elevlid_3ft
cd /bigdata/lindata/lindata0304/indata/lncosgeo/
ls
history
ls
cp IMG3720079200P20040216.tfw IMG3720079200P20040216.tfwm
cp IMG3720079200P20040216.tfw.orig MG3720079200P20040216.tfw
r.in.gdal IMG3720079200P20040216.tif out=IMGNCFlood792
r.in.gdal -o IMG3720079200P20040216.tif out=IMGNCFlood792
d.rast IMGNCFlood792
r.info IMGNCFlood792
g.region -p
g.remove rast=IMGNCFlood792
ls
vi IMG3720079200P20040216.tfw.orig
g.region -p
vi IMG3720079200P20040216.tfw
cp IMG3720079200P20040216.tfw.orig IMG3720079200P20040216.tfw
r.in.gdal -o IMG3720079200P20040216.tif out=IMGNCFlood792
d.rast IMGNCFlood792
ls
cd ncstpft
ls
exit
g.list rast
g.list vect
d.mon x0
d.rast elevlid_3ft
d.vect whydrolines
d.vect wstreets
ls
v.in.ogr -o channel.shp out=lwchannel
d.vect lwchannel
d.vect lwchannel co=red
v.in.ogr -o culvert.shp out=lwculvert
d.vect lwculvert co=red
ls
v.in.ogr -o dams.shp out=lwdams
v.in.ogr -o samplers.shp out=lwsamplers
ls
v.in.oger -o hill_outline.shp out=hilloutline
v.in.ogr -o hill_outline.shp out=hilloutline
ls
v.in.ogr -o hill_breakline.shp out=hillbreakli
history
ls
v.in.ogr contours.shp out=conttest
v.in.ogr -o contours.shp out=conttest
g.list vect
d.vect lwdams co=red
d.vect lwsamplers co=blue
d.vect hillbreakli co=grey
d.vect hilloutline co=grey
d.vect conttest
g.remove vect=conttest
g.list vec
g.list vect
d.vect whydroareas
d.vect wswproperty
g.remove vect=wswproperty
g.list vect
d.zoom
d.erase
d.rast elevlid_3ft
d.vect wstreets
d.zoom
g.region -p
g.list vect
d.vect lwdams co=red
d.measure
d.zoom
d.measure
d.grid size=6
d.zoom
d.erase
d.vect lwdams co=red
d.vect wstreets
d.zoom
g.list rast
r.flow elevlid_3ft dsout=dsd_3ft
g.region rast=elevlid_3ft
r.flow elevlid_3ft dsout=dsd_3ft
d.rast dsd_3ft
d.vect wstreets
d.vect lwdams co=red
d.erase
d.rast dsd_3ft
d.vect wstreets
d.vect lwdams co=red
g.list vect
d.vect lwsamplers co=violet
d.vect lwculvert co=red
d.zoom
d.zoom
g.region save=secref_3ft
d.zoom
g.list rast
d.what.rast elevlid_3ft
r.digit
r.mapcalc dam_monitor_z="if(dam_monitor >0, 375, null())"
d.rast -o dam_monitor_z
d.what.rast
g.region secfref_3ft
g.list region
g.region secref_3ft
d.erase
cd
cd lrun
g.region -p
history
history>runwakeimport
vi runwakeimport
ls
vi runlw
vi runlw
v.surf.rst -t lid79200_pts elev=elevlidt100s1_3ft lay=0 segmax=30 npmin=120 ten=100 smo=1 slo=slplidt100s1_3ft asp=asplidt100s1_3ft
d.rast elevlidt100s1_3ft
d.rast slplidt100s1_3ft
vi runlw
v.surf.rst -t lid79200_pts elev=elevlidt150s05_3ft lay=0 segmax=30 npmin=120 ten=150 smo=0.5 slo=slplidt150s05_3ft
d.rast slplidt150s05_3ft
g.list vect
d.vect lid79200_pts siz=2
d.grid siz=12
vi runlw
v.surf.rst -dt lid79200_pts elev=elevlidt140s06_3ft lay=0 segmax=30 npmin=120 ten=140 smo=0.6 slo=dx_lidt140s06_3ft asp=dy_lidt140s06_3ft
d.erase
d.rast dx_lidt140s06_3ft
d.rast dy_lidt140s06_3ft
g.list rast
d.rast -o dam_monitor_z
r.null help
r.null dam_monitor_z null=0
r.mapcalc elevliddam="if(dam_monitor_z>0,dam_monitor_z,elevlidt140s06_3ft)"
d.rast elevliddam
r.mapcalc dam_monitor_zf=dam_monitor_z*1.
r.null dam_monitor_zf null=0
r.mapcalc elevliddam="if(dam_monitor_zf>0,dam_monitor_zf,elevlidt140s06_3ft)"
d.rast elevliddam
r.colors elevliddam rast=elevlidt140s06_3ft
d.rast elevliddam
r.mapcalc test=elevliddam-elevlidt140s06_3ft
r.describe test
d.rast -o test
r.slope.aspect elevliddam dx=dx_elevliddam dy=dy_elevliddam 
r.slope.aspect elevliddam dx=dx_elevliddam dy=dy_elevliddam zfactor=0.304801 --o
d.rast dx_elevliddam
history
vi runlw
g.list rast
d.what.rast dx_elevliddam,dx_lidt140s06_3ft
g.list rast
d.what.rast dy_elevliddam,dy_lidt140s06_3ft
r.sim.water help
vi runlw
r.mapcalc rain01=0.00001
r.mapcalc man05=0.05
r.mapcalc infil=0.000000
vi runlw
g.list rast
d.rast dsd_3ft
g.list vect
d.vect wstreets
d.zoom
g.region -p
vi runlw
r.sim.water elevin=elevlidt140s06_3ft dxin=dx_lidt140s06_3ft dyin=dy_lidt140s06_3ft rain=rain01 infil=infil0 manin=man05 depth=hhtest_3ft disch=qtest_3ft
g.list rast
g.rename rast=infil,infil0
r.sim.water elevin=elevlidt140s06_3ft dxin=dx_lidt140s06_3ft dyin=dy_lidt140s06_3ft rain=rain01 infil=infil0 manin=man05 depth=hhtest_3ft disch=qtest_3ft
vi runlw
r.sim.water -t elevin=elevlidt140s06_3ft dxin=dx_lidt140s06_3ft dyin=dy_lidt140s06_3ft rain=rain01 infil=infil0 manin=man05 depth=hhtest_3ft disch=qtest_3ft nwalk=300000 niter=500 outiter=100
bg
d.rast hhtest_3ft
g.list rast
d.rast hhtest_3ft.0099
d.rast hhtest_3ft.0499
d.what.rast
g.list rast
d.rast hhtest_3ft.0299
d.what.rast hhtest_3ft.0199,hhtest_3ft.0299,hhtest_3ft.0399,hhtest_3ft.0499
d.zoom
g.region rast=hhtest_3ft.0499 -p
vi runlw
d.erase
g.list rast
d.rast qtest_3ft.0499
r.sim.water -t elevin=elevliddam dxin=dx_elevliddam dyin=dy_elevliddam rain=rain01 infil=infil0 manin=man05 depth=hhtestd_3ft disch=qtestd_3ft nwalk=300000 niter=500 outiter=100
bg
g.list rast
d.rast hhtestd_3ft.0499
g.list vect
d.vect lwdams co=red
d.what.rast hhtestd_3ft.0199,hhtestd_3ft.0499,hhtest_3ft.0199,hhtest_3ft.0499
vi runlw
r.mapcalc tranin=0.001
vi runlw
r.mapcalc detin=0.001
r.mapcalc tauin=0.01
vi runlw
r.sim.sediment  elevin=elevlidt140s06_3ft dxin=dx_lidt140s06_3ft dyin=dy_lidt140s06_3ft wdepth=hhtest_3ft.0499 detin=detin tranin=tranin tauin=tauin manin=man05 tc=tc.test et=et.test flux=flux.test erdep=erdep.test
bg
g.list rast
d.rast et.test
d.rast tc.test
r.colors tc.test co=rules
d.rast tc.test
ps
ps
fg
d.rast hhtest_3ft.0499
d.what.rast
r.mapcalc hhtest.cut="if(hhtest_3ft.0499>0.4,0.4,hhtest_3ft.0499)"
r.sim.sediment  elevin=elevlidt140s06_3ft dxin=dx_lidt140s06_3ft dyin=dy_lidt140s06_3ft wdepth=hhtest.cut detin=detin tranin=tranin tauin=tauin manin=man05 tc=tc.test et=et.test flux=flux.test erdep=erdep.test
r.sim.sediment  elevin=elevlidt140s06_3ft dxin=dx_lidt140s06_3ft dyin=dy_lidt140s06_3ft wdepth=hhtest.cut detin=detin tranin=tranin tauin=tauin manin=man05 tc=tc.test et=et.test flux=flux.test erdep=erdep.test --o
bg
fg
vi runlw
r.sim.sediment  elevin=elevlidt140s06_3ft dxin=dx_lidt140s06_3ft dyin=dy_lidt140s06_3ft wdepth=hhtest.cut detin=detin tranin=tranin tauin=tauin manin=man05 tc=tc.test et=et.test flux=flux.test erdep=erdep.test nwalk=500000 niter=600 --o
bg
cd
cd /bigdata
ls
cd lindata
ls
cd lindata0304
ls
cd indata
ls
cd coastlid04
ls
cd ..
ls
cd lidisabel
ls
vi range
d.rast et.test
d.rast erdep.test
d.rast flux.test
d.what.rast
exit
g.proj help
g.proj -p
ls
cd elevation150
ls
cd elevation
ls
more prj.adf
r.in.gdal w001001.adf out=elev_state_150m
d.mon x0
g.region rast=elev_state_150m
d.rast elev_state_150m
r.info elev_state_150m
g.region res=500 -p
d.erase
g.region -a res=500
g.region res=1000 -ap
d.erase
d.rast elev_state_150m
g.region res=1640 -ap
d.erase
d.rast elev_state_150m
g.rename rast=elev_state_150m,elev_state_150ft
r.mapcalc elev_state_1640=elev_state_150ft*1.
exit
g.copy
g.copy rast=dem@experiment,dem
g.copy rast=dem_01@experiment,dem_01
g.copy rast=dem_02@experiment,dem_02
g.copy rast=dem_03@experiment,dem_03
g.copy rast=dem_04@experiment,dem_04
g.copy rast=dem_02@experiment,dem_02 vect=dem_contours_5@experiment,dem_contours_5
g.copy vect=dem_contours_3@experiment,dem_contours_3
g.copy
g.copy rast=aspect@experiment,aspect
g.copy rast=slope@experiment,slope
g.copy rast=dx@experiment,dx
g.copy rast=dy@experiment,dy
g.copy rast=depth@experiment,depth
g.copy rast=depth_04@experiment,depth_04
r.contour
g.region raster=dem_01@PERMANENT
r.contour --overwrite input=dem_01 output=dem_01 step=5
r.geomorphon
r.geomorphon --overwrite dem=dem_01 forms=geomorphon_01 search=9 skip=6 flat=1 dist=0
r.info map=dem_01@PERMANENT
r.geomorphon --overwrite dem=dem_01 forms=geomorphon_01 search=18 skip=12 flat=1 dist=0
r.geomorphon --overwrite dem=dem_01 forms=geomorphon_01 search=9 skip=6 flat=1 dist=0
r.slope
r.slope.aspect
r.slope.aspect --overwrite elevation=dem_01@PERMANENT slope=slope_01 format=percent
g.region raster=dem_02@PERMANENT
r.contour --overwrite input=dem_02 output=dem_02 step=5
r.geomorphon --overwrite dem=dem_02 forms=geomorphon_02 search=9 skip=6 flat=1 dist=0
r.slope.aspect --overwrite elevation=dem_02@PERMANENT slope=slope_02 format=percent
r.geomorphon --overwrite dem=dem_02 forms=geomorphon_02 search=9 skip=6 flat=1 dist=1
r.geomorphon --overwrite dem=dem_02 forms=geomorphon_02 search=9 skip=6 dist=7
r.geomorphon --overwrite dem=dem_02 forms=geomorphon_02 search=9 skip=6 flat=2 dist=7
r.geomorphon --overwrite dem=dem_02 forms=geomorphon_02 search=9 skip=6 flat=3 dist=7
r.geomorphon --overwrite dem=dem_02 forms=geomorphon_02 search=9 skip=6 dist=7
r.geomorphon --overwrite dem=dem_02 forms=geomorphon_02 search=9 skip=6 flat=3 dist=7
r.contour --overwrite input=dem_03 output=dem_03 step=5
g.region raster=dem_03@PERMANENT
r.contour --overwrite input=dem_03 output=dem_03 step=5
r.geomorphon --overwrite dem=dem_03 forms=geomorphon_03 search=9 skip=6 flat=3 dist=7
r.geomorphon --overwrite dem=dem_03 forms=geomorphon_03 search=9 skip=6 dist=7
r.geomorphon --overwrite dem=dem_03 forms=geomorphon_03 search=9 skip=6
r.slope.aspect --overwrite elevation=dem_03@PERMANENT slope=slope_03 format=percent
g.region raster=dem_04@PERMANENT
r.contour --overwrite input=dem_04 output=dem_04 step=5
r.geomorphon --overwrite dem=dem_04 forms=geomorphon_04 search=9 skip=6
r.slope.aspect --overwrite elevation=dem_04@PERMANENT slope=slope_04 format=percent
r.slope.aspect
r.slope.aspect --overwrite elevation=dem_01 slope=slope_01
g.reigon
g.region
g.region raster=dem_01
r.slope.aspect --overwrite elevation=dem_01 slope=slope_01
g.region raster=dem_02
r.slope.aspect --overwrite elevation=dem_02 slope=slope_02
g.region raster=dem_03
r.slope.aspect --overwrite elevation=dem_03 slope=slope_03
g.region raster=dem_04
r.slope.aspect --overwrite elevation=dem_04 slope=slope_04
g.copy
g.copy raster=dem_01,dem_exp3
g.copy raster=slope_01,slope_exp3
g.copy raster=geomorphon_01,geomorphon_exp3
g.copy raster=dem_02,dem_exp1
g.copy raster=slope_02,slope_exp1
g.copy raster=geomorphon_02,geomorphon_exp1
g.copy raster=dem_03,dem_exp2
g.copy raster=slope_03,slope_exp2
g.copy raster=geomorphon_03,geomorphon_exp2
g.copy raster=dem_04,dem_exp4
g.copy raster=slope_04,slope_exp4
g.copy raster=geomorphon_04,geomorphon_exp4
g.copy vector=dem_01,contour_exp3
g.copy vector=dem_02,contour_exp1
g.copy vector=dem_03,contour_exp2
g.copy vector=dem_04,contour_exp4
g.mapset
g.mapset -l
g.mapset
g.mapset mapset=analysis
g.mapset -c mapset=analysis
g.rename raster=dem_03,dem_2
g.rename raster=dem_04,dem_4
g.rename raster=dem_exp1,dem_1
g.rename raster=dem_exp2,dem_2
g.rename --overwrite raster=dem_exp2,dem_2
g.rename --overwrite raster=dem_exp3,dem_3
g.rename --overwrite raster=dem_exp4,dem_4
g.mapset mapset=analysis
g.remove
g.remove type=raster name=IMG_airBW_79200WC_3ft@PERMANENT
g.remove -f type=raster name=IMG_airBW_79200WC_3ft@PERMANENT
g.remove -f type=raster name=IMG_airBW_79200WC_3ft@PERMANENT,aspect@PERMANENT
g.remove -f type=raster name=dem_01@PERMANENT
g.remove -f type=raster name=dem_02@PERMANENT
g.remove -f type=raster name=depth@PERMANENT
g.remove -f type=raster name=depth@PERMANENT,depth_04@PERMANENT
g.remove -f type=raster name=dx@PERMANENT
g.remove -f type=raster name=dx@PERMANENT,dy@PERMANENT
g.remove -f type=raster name=geomorphon_01@PERMANENT
g.remove -f type=raster name=geomorphon_02@PERMANENT
g.remove -f type=raster name=geomorphon_03@PERMANENT
g.remove -f type=raster name=geomorphon_04@PERMANENT
g.remove -f type=raster name=geomorphon_exp1@PERMANENT
g.remove -f type=raster name=geomorphon_exp2@PERMANENT
g.remove -f type=raster name=geomorphon_exp3@PERMANENT
g.remove -f type=raster name=geomorphon_exp4@PERMANENT
g.remove -f type=raster name=slope@PERMANENT
g.remove -f type=raster name=slope_01@PERMANENT
g.remove -f type=raster name=slope_02@PERMANENT
g.remove -f type=raster name=slope_03@PERMANENT
g.remove -f type=raster name=slope_04@PERMANENT
g.remove -f type=raster name=slope_04@PERMANENT,slope_exp1@PERMANENT
g.remove -f type=raster name=slope_exp1@PERMANENT
g.remove -f type=raster name=slope_exp2@PERMANENT
g.remove -f type=raster name=slope_exp3@PERMANENT
g.remove -f type=raster name=slope_exp4@PERMANENT
r.contour
g.remove
g.remove type=vector pattern=*
g.remove -f type=vector pattern=*
r.contour input=dem_1@PERMANENT output=contour_1 step=5
r.contour input=dem_2@PERMANENT output=contour_2 step=5
r.contour input=dem_3@PERMANENT output=contour_3 step=5
r.contour input=dem_4@PERMANENT output=contour_4 step=5
g.region
g.region raster=dem_1
r.contour --overwrite input=dem_1@PERMANENT output=contour_1 step=5
g.region raster=dem_2
r.contour --overwrite input=dem_2@PERMANENT output=contour_2 step=5
g.region raster=dem_3
r.contour --overwrite input=dem_3@PERMANENT output=contour_3 step=5
g.region raster=dem_4
r.contour --overwrite input=dem_4@PERMANENT output=contour_4 step=5
r.relief
g.region raster=dem_1
r.relief input=dem_1@PERMANENT output=relief_1
g.region raster=dem_2
r.relief input=dem_2@PERMANENT output=relief_2
g.region raster=dem_3
g.region raster=dem_3
r.relief input=dem_3@PERMANENT output=relief_3
g.region raster=dem_4
r.relief input=dem_4@PERMANENT output=relief_4
