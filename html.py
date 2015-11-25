#!/usr/bin/env python

import grass.script as gscript
from collections import defaultdict
import os

# set global variables

# HTML template for the header of a report
start_template = """
<!doctype html>
<html>
<head>
<title>Tangible Topography</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<link href="layout.css" rel="stylesheet" type="text/css" media="screen">
<link href="style.css" rel="stylesheet" type="text/css" media="screen">
</head>
<body>
<div id="outercontainer">
<div id="container">
<header>
<div id="header-image"><p>Tangible Topography</p></div>
<nav>
<ul class="nav">
<li><a href="index.html">Introduction</a></li>
<li><a href="methods.html">Methodology</a></li>
<li><a href="analyses.html">Analyses</a></li>
<!--<li><a href="findings.html">Findings</a></li>-->
</ul>
</nav>
</header>
<main>
<h2>Analyses</h2>
"""

# HTML template for a heading
heading_template="""
<h3>Experiment {n}</h3>
"""

# HTML template for reference images
reference_template="""
<p>Reference</p>
<figure>
<img src="{fullpath_dem}.png" width="300px">
<img src="{fullpath_slope}.png" width="300px">
<img src="{fullpath_diff}.png" width="300px">
<img src="{fullpath_depth}.png" width="300px">
<img src="{fullpath_form}.png" width="300px">
</figure>
<br/>
"""

# HTML template for starting a figure
start_figure_template="""
<p>Participant {participant}</p>
<figure>
"""

# HTML template for ending a figure
end_figure_template="""
</figure>
"""

# HTML template for adding a raster to a report
raster_template = """
<img src="{name}.png" width="300px">
"""

# HTML template for adding statistics to a report
stats_template = """
<details>
<summary style="font-size:12px"><i>Statistics</i></summary>
<img src="{name}_dem_hist_{n}.png" width="300px">
<img src="{name}_diff_hist_{n}.png" width="300px">
</details>
<br/>

"""

# HTML template for ending a report
end_template = """
<br/>
</main>
<footer>
<nav>
<ul>
<li>
<a href="https://github.com/baharmon/tangible_topography" title="Fork on GitHub">
<img src="images/style/github_logo.png" alt="GitHub Octocat logo">
</a>
</li>
<li title="Copyright and license (not applicable to linked materials)">
&copy; 2015
<a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA</a>
<a href="http://geospatial.ncsu.edu/osgeorel/">NCSU OSGeoREL</a>
</li>
</ul>
</nav>
</footer>
</body>
</html>
"""

def main():

    # temporary region
    gscript.use_temp_region()

    # set image directory
    images = "results\\render"

    # set histogram directory
    histogram = "results\\anonymous"

    # set reference image directory
    reference_dir = "results\\reference"

    # html file
    html = "analyses.html"

    # initialize a dictionary for each name
    d = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))

    # initialize a list for participants' names
    name_list = []

    # initialize a list of categories
    categories = ["dem","slope","diff","depth","form"]

    # get list of rasters
    rasters = gscript.list_strings('raster', pattern="a*")

    for raster in rasters:

        raster_name, separator, mapset = raster.partition('@')

        name, separator, cat_number = raster_name.partition('_')

        cat, separator, number = cat_number.partition('_')

        name_list.append(name)    

        # add values to dictionary
        d[name][number][cat] = raster 

    # remove duplicates
    name_list = set(name_list)

    # anonymize list of participants
    participants = {v: k for k,v in enumerate(name_list)}
    # participants = dict((v,k) for k,v in enumerate(name_list))

    # template variables
    title = "Analyses"

    # write to an html file using templates
    with open(html, 'w') as output:

            # write html header
            output.write(start_template.format(title=title))

            # loop through experiments
            max_experiments=7
            for n in range(max_experiments):

                # write html heading
                output.write(heading_template.format(n=str(n+1)))

                # write reference images to html
                ref_dem = "dem_"+str(n+1)
                ref_slope = "slope_"+str(n+1)
                ref_diff = "diff_"+str(n+1)
                ref_depth = "depth_"+str(n+1)
                ref_form = "form_"+str(n+1)
                fullpath_dem = os.path.join(reference_dir,ref_dem)
                fullpath_slope = os.path.join(reference_dir,ref_slope)
                fullpath_diff = os.path.join(reference_dir,ref_diff)
                fullpath_depth = os.path.join(reference_dir,ref_depth)
                fullpath_form = os.path.join(reference_dir,ref_form)
                output.write(reference_template.format(n=str(n+1), fullpath_dem=fullpath_dem, fullpath_slope=fullpath_slope, fullpath_diff=fullpath_diff, fullpath_depth=fullpath_depth, fullpath_form=fullpath_form))

                # loop through participants
                for name in name_list:

                    # start figure
                    participant = str(int(participants[name])+1)
                    output.write(start_figure_template.format(participant=participant))

                    # loop through categories
                    for cat in categories:

                        raster = d[name][str(n+1)][cat]
                        if not raster:
                            continue

                        # set region
                        gscript.run_command('g.region', rast=raster)

                        # compute univariate statistics                    
                        #stat = gscript.parse_command('r.univar', map=raster, flags='g')

                        #set path
                        raster_name = name + "_" + cat + "_" + str(n+1)
                        fullpath_name = os.path.join(images,raster_name)

                        # write raster to html
                        output.write(raster_template.format(
                        raster_title=raster, name=fullpath_name)) 

                    # end figure      
                    output.write(end_figure_template)

                    # write stats to html
                    histogram_path = os.path.join(histogram,participant)
                    output.write(stats_template.format(
                    n=str(n+1),raster_title=raster, name=histogram_path))
                    #min=stat['min'], max=stat['max'], mean=stat['mean'], var=stat['variance']

            # write html footer
            output.write(end_template)

if __name__ == "__main__":
    main()