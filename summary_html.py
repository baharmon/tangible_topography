#!/usr/bin/env python

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
<li><a href="summary.html">Summary Statistics</a></li>
<!--<li><a href="findings.html">Findings</a></li>-->
</ul>
</nav>
</header>
<main>
<h2>Summary statistics</h2>
"""

# HTML template for a heading
heading_template="""
<h3>Analytic: {analytic}</h3>
"""

# HTML template for starting a figure
start_figure_template="""
<h5>Statistic: {stat}</h5>
<p>Exercise 1 - 7</p>
<figure>
"""

# HTML template for ending a figure
end_figure_template="""
</figure>
"""

# HTML template for adding a raster to a report
raster_template = """
<img src="{name}.png" width="210px">
"""

# HTML template for adding univariate statistics to a report
univar_template = """
<h1>Univariate statistics</h1>
<h3>Mean difference</h3>
<figure>
<img src="{mean}.png" width="500px">
</figure>
<p style="text-align:center;">y = mean difference</p>
<p style="text-align:center;">x = exercises 1 - 7</p>
<h3>Absolute value of the mean difference</h3>
<figure>
<img src="{absvalmean}.png" width="500px">
</figure>
<p style="text-align:center;">y = absolute value of the mean difference</p>
<p style="text-align:center;">x = exercises 1 - 7</p>
<h3>Covariance of DEMs by exercise</h3>
<figure>
<img src="{covar_1}.png" width="500px">
<img src="{covar_2}.png" width="500px">
<img src="{covar_3}.png" width="500px">
<img src="{covar_4}.png" width="500px">
<img src="{covar_5}.png" width="500px">
<img src="{covar_6}.png" width="500px">
<img src="{covar_7}.png" width="500px">
</figure>
<p style="text-align:center;">y = covariance of DEM</p>
<p style="text-align:center;">x = exercises 1 - 7</p>
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

    # set build directory
    directory = os.path.normpath("C:\\Users\\Brendan\\tangible_topography\\build")

    # set image directory
    series = "results/series"

    # set histogram directory
    univar = "results/univar"

    # html file
    html_file = "summary.html"
    fullpath_html = os.path.join(directory,html_file)

    # initialize a list of analyses
    analytics = ["dem","diff","form"]

    # initialize a list of statistics
    statistics = ["coeff","stddev","variance"]

    # set number of experiments
    max_experiments=7

    # template variables
    title = "Summary Statistics"

    # write to an html file using templates
    with open(fullpath_html, 'w') as output:

            # write html header
            output.write(start_template.format(title=title))

            # loop through analytics            
            for analytic in analytics:

                # write html heading
                output.write(heading_template.format(analytic=analytic))

                # loop through statistics
                for stat in statistics:

                    # start figure
                    output.write(start_figure_template.format(stat=stat))

                    # loop through experiments
                    for n in range(max_experiments):
                        num=str(n+1)

                        #set path
                        raster_name = analytic + "_" + stat + "_" + num
                        fullpath_name = "/".join([series,raster_name])

                        # write raster to html
                        output.write(raster_template.format(
                        raster_title=fullpath_name, name=fullpath_name)) 

                    # end figure      
                    output.write(end_figure_template)

            # write univariate statistics to html
            mean = os.path.join(univar,"mean")
            absvalmean = os.path.join(univar,"absvalmean")
            covar_1 = "/".join([univar,"covar_1"])
            covar_2 = "/".join([univar,"covar_2"])
            covar_3 = "/".join([univar,"covar_3"])
            covar_4 = "/".join([univar,"covar_4"])
            covar_5 = "/".join([univar,"covar_5"])
            covar_6 = "/".join([univar,"covar_6"])
            covar_7 = "/".join([univar,"covar_7"])
            output.write(univar_template.format(mean=mean, absvalmean=absvalmean, covar_1=covar_1, covar_2=covar_2, covar_3=covar_3, covar_4=covar_4, covar_5=covar_5, covar_6=covar_6, covar_7=covar_7))

            # write html footer
            output.write(end_template)

if __name__ == "__main__":
    main()