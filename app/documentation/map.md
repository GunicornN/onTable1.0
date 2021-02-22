# Base de données spatiales

Documentation : https://docs.djangoproject.com/fr/3.1/ref/contrib/gis/tutorial/
Inspired by : https://realpython.com/location-based-app-with-geodjango-tutorial/

## Installing GeoDjango Dependencies

You will need :
- GEOS is an open-source geometry engine and a C++ port of the JTS (Java Topology Suite). It’s required by GeoDjango for performing geometric operations.

- PROJ.4 is an open-source GIS library for easily working with spatial reference systems and projections. You need it because you’ll be using PostGIS as the spatial database.

- GDAL is an open-source geospatial data abstraction library for working with raster and vector data formats. It’s needed for many utilities used by GeoDjango


Linux/Ubuntu :
` sudo aptitude install gdal-bin libgdal-dev `

` sudo aptitude install python3-gdal `

` sudo aptitude install binutils libproj-dev `

Mac : w/ Homebrew :
<code>
brew install postgresql
brew install postgis
brew install gdal
brew install libgeoip
</code>
