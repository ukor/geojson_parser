#!/usr/bin/env bash

# download parish boundaries
curl -o raw/parish.json https://opendata.arcgis.com/datasets/b48d99f080c34352a095df3e00cf6e8c_0.geojson
curl -o raw/london_postcode_sectors.kml https://www.doogal.co.uk/CountiesKML.ashx?county=E11000009

python3 london.py
python3 london_areas.py
python3 london_postcode_sector.py
python3 outter_london.py
python3 parish.py
python3 london_boroughs.py
python3 london_ward.py
python3 london_constituncy.py
python3 london_postcode.py
# python3 parse_postcode.py
