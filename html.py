#!/usr/bin/env python

import grass.script as gscript
from collections import defaultdict
import os

# set global variables

# HTML template for the header of a report
start_template = """
<html>
<head>
<title>{title}</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<link href="layout.css" rel="stylesheet" type="text/css" media="screen">
<link href="style.css" rel="stylesheet" type="text/css" media="screen">
</head>
<div id="outercontainer">
<div id="container">
<body>
<header>
<div id="header-image"><p>{title}</p></div>
<!--
<nav>
<ul class="nav">
<li><a href="index.html">About</a></li>
<li><a href="research.html">Research</a></li>
<li><a href="publications.html">Publications</a></li>
<li><a href="teaching.html">Teaching</a></li>
</ul>
</nav
-->
</header> 
<main>
"""

# HTML template for adding a raster to a report
raster_template = """
<h2>{raster_title}</h2>
<h3>Statistics</h3>
<table>
<tr><td>Min</td><td>{min}</td>
<tr><td>Max</td><td>{max}</td>
<tr><td>Mean</td><td>{mean}</td>
<tr><td>Variance</td><td>{var}</td>
</table>
<h3>Map</h3>
<p style="text-align:center;">
<img src="{name}.png">
</p>
"""

# HTML template for ending a report
end_template = """
</main>
</body>
</html>
"""

def main():

    # set rendering directory
    directory = os.path.normpath("C:\Users\Brendan\tangible_topography")
    
    # files
    html_file = "analysis.html"
    style = "style.css"
    layout = "layout.css"
    fullpath_html = os.path.join(directory,html_file)
    fullpath_style = os.path.join(directory,style)
    fullpath_layout = os.path.join(directory,layout)

    # initialize a dictionary for each category of raster
    cats = defaultdict(list)

    # loop through the elevation, slope, aspect, pca, depth, stddev, variance, and coeff maps
    categories = ["elevation","slope","aspect","pca","depth","stddev","variance","coeff"]
    for category in categories:
        
        # variables
        pattern = category+"*"

        # get list of rasters
        rasters = gscript.list_strings('raster', pattern=pattern)
    
        # iterate through the list of rasters
        for raster in rasters:

            # add values to dictionary
            cats[category].append(raster)

    # template variables
    title = "Analysis"

    # write to a css file using the style template
    with open(fullpath_style, 'w') as output:
        output.write(style_template.replace("background_image",background_image))
        
    # write to a css file using the layout template
    with open(fullpath_layout, 'w') as output:
        output.write(layout_template)

    # write to an html file using templates
    with open(fullpath_html, 'w') as output:

            output.write(start_template.format(title=title))
        
            for category in categories:
                for raster in cats[category]:
                    
                    # compute univariate statistics                    
                    stat = gscript.parse_command('r.univar', map=raster, flags='g')
                    
                    # partition raster name
                    name, separator, mapset = raster.partition('@')

                    # write html
                    output.write(raster_template.format(
                        raster_title=raster, name=name, min=stat['min'], max=stat['max'], mean=stat['mean'], var=stat['variance']))
                        
            output.write(end_template)

if __name__ == "__main__":
    main()