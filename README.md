# Mustang Map

Mustang Map visualizes government data on Mustangs and presents a user-friendly view onto otherwise inaccessible data. The source data has been imported from heterogenous government data into a PostgreSQL database, which is then served via a Python application using Flask, SQLAlchemy, and flask-RESTful to make the data available both to the Mustang Map website and third party applications. Mustang Map uses Google Maps to present relevant geographic data converted into geojson format from the original GDB format supplied by the government. Non-geographical data is visualized via the Highcharts library. In addition to the static government data, the site allows users to log in and upload pictures of mustangs and associate those pictures with specific herd areas.

Learn more about the developer [here](https://oliviaknott.com).

![](http://g.recordit.co/Lk5fj3QNeR.gif)

## Contents
- [Technologies Used](#technologiesused)
- [Features](#features)
- [API](#api)
- [Maps](#maps)
- [Data Visualizations](#datavisualizations)
- [Account Creation and Login](#login)
- [Data](#data)

## <a name="technologiesused"></a>Technologies Used
- [Python](https://www.python.org/)
- [Javascript](https://developer.mozilla.org/en-US/docs/Web?Javascript/)
- [PostGreSQL](https://www.postgresql.org/)
- [Flask](http://flask.pocoo.org/)
- [SQLAlchemy](http://www.sqlalchemy.org/)
- [jQuery](https://jquery.com/)
- [Google Maps API](https://developers.google.com/maps/)
- [Bootstrap](http://getbootstrap.com/)
- [Highcharts](http://www.highcharts.com/)
- [flask-RESTful](https://flask-restful.readthedocs.io/)
- [Flask-Images](https://mikeboers.github.io/Flask-Images/)
- [bcrypt](https://www.npmjs.com/package/bcrypt/)

## <a name="features"></a>Features

*Current*

- [X] Google Map displays states and herd areas managed by the Bureau of Land Management's Mustang Program
- [X] Highcharts renders charts depicting data
- [X] Flask app renders HTML and handles AJAX requests to the database
- [X] Flask-RESTful returns a RESTful api of database information as jsons
- [X] Bcrypt is used to ensure the security of user accounts
- [X] Flask-Images handles image upload to the database and serves images to the site
- [X] Javascript functions handle search and AJAX calls

*Future*

- [ ] Allow users to manage their photos
- [ ] Incorporate additional geographic data


## <a name="maps"></a>Maps

The states and herd areas shown on google maps are rendered from geojson files. The herd area geojsons were converted from the Bureau of Land Management's original provided GDB format. States and herd areas can be clicked on to pan to the center of the area and initialize an AJAX call to create the charts for that state or area.


## <a name="datavisualizations"></a>Data Visualizations

The data visualizations generated on Mustang Map use the graphing library Highcharts.  An area-spline chart is used to visualize adoption and removal information for horses and burros from 2005 to 2015 for national and state data. A dual-axis chart is used to display population data over acreage for 2005 to 2016 for nation, state, and individual herd areas. All charts are responsive and users can hide specific types of information in order to change better visualize other data.


## <a name="login"></a>Account Creation, Login, and Image Display

Users can create an account and log in in order to upload images which are used in the herd area information display. Password encryption is handled by bcrypt. Users can also chose to login with Facebook's login API. Backend functions ensure that the files uploaded are picture files. For herd areas with multiple images, a random choice algorithm serves one picture per herd area on a given AJAX call.


## <a name="data"></a>Data

Mustang Map's data comes from the Bureau of Land Management's Mustang Program, and can be found [here](https://www.blm.gov/wo/st/en/prog/whbprogram/herd_management/Data.html). This data is provided as PDF and in some case scans of PDFS making conversion to a databse difficult. Due to this potential for conversion error, small errors may be present. This site is intended for visualization of data and should not be considered 100% accurate. Geospacial Data was sourced from a variety of individual BLM agency websites. Some state agencies do not provide GIS data for herd areas and others provide inaccrute data (New Mexico's herd areas, for exmaple, show up in the ocean off the coast of Africa) so all maps shown in Mustang Map should be used only for general visualization and not for research or navigational purposes.


## <a name="api"></a>API

Mustang Map provides an API which is available to third-party applications. For more information on using the Mustang Map API, please see the api [documentation](https://github.com/cholestria/MustangMap/tree/master/api_documentation).
