# download parish boundaries
curl -o raw/parish.json https://opendata.arcgis.com/datasets/b48d99f080c34352a095df3e00cf6e8c_0.geojson
curl -o raw/london_postcode_sectors.kml https://www.doogal.co.uk/CountiesKML.ashx?county=E11000009
# install gdal-bin - [see README.md]
# sudo apt-get install gdal-bin -y
# convert kml to geojson
ogr2ogr -f GeoJSON ./raw/london_postcode_sectors.geojson ./raw/london_postcode_sectors.kml
