# Parse geoJSON
The script contained in this respository are use for downloading and parsing geoJSON, KML and shape files.
Python3.6 above is required.

# Note to the next developer

In the case where new dataset need to be parse, write a new python script.
### `Do not modify any script.`

It was dauting adapting scripts to each dataset, making it default to create reusable codes because all the geoJSON, KML and shape files where inconsitent with naming and casing of atributes and values.

Yes, there a lot of improvement that can be done here. I find it pointless since this code won't be use often. I promise to revisit when I have more time or better still, `do it yourself`.

## Before running the script
This script depend on:
- `gdal`
- `curl` or `wget`
Install tools before procceding.

### Dowload Dataset
- UK Parish
```sh
curl -o raw/parish.json https://opendata.arcgis.com/datasets/b48d99f080c34352a095df3e00cf6e8c_0.geojson
```
- London Postcode Sector
```sh
curl -o raw/london_postcode_sectors.kml https://www.doogal.co.uk/CountiesKML.ashx?county=E11000009
```
- Convert `kml` to `geojson`
```sh
ogr2ogr -f GeoJSON ./raw/london_postcode_sectors.geojson ./raw/london_postcode_sectors.kml
```

All this can done at a go by running
```sh
./scripts/set_up.sh
```

## HOW TO RUN THE SCRIPT
Checkout the `scripts` folder. It contains bash script that execute the python code.

Individual python script can be ran. The shell script where just for convince and grouping.

- The `set_up.sh` donwloads geoJSON, KML and shape files from the internet. `Always run this first`. You can code for downloading files here.
```sh
./scripts/set_up.sh
```

- The `parse.sh` execute python scripts that takes less then 30 minutes
```sh
./scripts/parse.sh
```

- The `postcode.sh` executes python scripts for parsing postcodes areas and postcode district
```sh
./scripts/postcode.sh
```

- The `postcode_sector.sh` executes python scripts for parsing postcode sectors. - This takes a lot of time. I recommend you run this script with `screen` or `nohup`
