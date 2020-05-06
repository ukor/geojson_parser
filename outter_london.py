from os.path import join
import kml2geojson
import requests
from parse_postcode import PostCode

from config.config import (ENV, POLYGON_DESTINATION)

from es.es import es_client
from es.es_config import ConfigElasticSearch
from es_instance import es_instance

postcode = [
    # outter london
    {"name": "BR", "area": 8, "kml_url": "https://en.wikipedia.org/w/index.php?title=Template:Attached_KML/BR_postcode_area&action=raw"},
    {"name": "CR", "area": 8, "kml_url": "https://en.wikipedia.org/w/index.php?title=Template:Attached_KML/CR_postcode_area&action=raw"},
    {"name": "DA", "area": 18, "kml_url": "https://en.wikipedia.org/w/index.php?title=Template:Attached_KML/DA_postcode_area&action=raw"},
    {"name": "EN", "area": 11, "kml_url": "https://en.wikipedia.org/w/index.php?title=Template:Attached_KML/EN_postcode_area&action=raw"},
    {"name": "HA", "area": 9, "kml_url": "https://en.wikipedia.org/w/index.php?title=Template:Attached_KML/HA_postcode_area&action=raw"},
    {"name": "IG", "area": 9, "kml_url": "https://en.wikipedia.org/w/index.php?title=Template:Attached_KML/IG_postcode_area&action=raw"},
    {"name": "SL", "area": 10, "kml_url": "https://en.wikipedia.org/w/index.php?title=Template:Attached_KML/SL_postcode_area&action=raw"},
    {"name": "TN", "area": 40, "kml_url": "https://en.wikipedia.org/w/index.php?title=Template:Attached_KML/TN_postcode_area&action=raw"},
    {"name": "KT", "area": 24, "kml_url": "https://en.wikipedia.org/w/index.php?title=Template:Attached_KML/KT_postcode_area&action=raw"},
    {"name": "RM", "area": 20, "kml_url": "https://en.wikipedia.org/w/index.php?title=Template:Attached_KML/RM_postcode_area&action=raw"},
    {"name": "SM", "area": 7, "kml_url": "https://en.wikipedia.org/w/index.php?title=Template:Attached_KML/SM_postcode_area&action=raw"},
    {"name": "TW", "area": 20, "kml_url": "https://en.wikipedia.org/w/index.php?title=Template:Attached_KML/TW_postcode_area&action=raw"},
    {"name": "WD", "area": 11, "kml_url": "https://en.wikipedia.org/w/index.php?title=Template:Attached_KML/WD_postcode_area&action=raw"},
    # missing - central London
    {"name": "SE", "area": 20, "kml_url": "https://en.wikipedia.org/w/index.php?title=Template:Attached_KML/SE_postcode_area&action=raw"},
    {"name": "EC50", "area": 1, "kml_url": "https://www.doogal.co.uk/GetAreaKml.ashx?postcodes=EC50&topLevel=true"},
    {"name": "EC88", "area": 1, "kml_url": "https://www.doogal.co.uk/GetAreaKml.ashx?postcodes=EC88&topLevel=true"},
    {"name": "W", "area": 1, "kml_url": "https://www.doogal.co.uk/GetAreaKml.ashx?postcodes=EC88&topLevel=true"},
]

# wikipedia = "https://en.wikipedia.org/w/index.php?title=Template:Attached_KML/BR_postcode_area&action=raw"
# doogal = "https://www.doogal.co.uk/GetAreaKml.ashx?postcodes=EC1&topLevel=true"

for p in postcode:
    file_name = p.get("name").lower()
    file_path = join("./raw", file_name) + ".kml"
    # download kml files
    r = requests.get(p.get("kml_url"))

    with open(file_path, "wb") as file:
        file.write(r.content)
        # convert kml to geojson
        kml2geojson.main.convert(file_path, "./raw")
        geojson_file = join("./raw", f"{file_name}.geojson")

        # parse and index this geojson
        _es_client = es_client(es_instance=es_instance())
        _es_client.create_index()
        postcode_area = PostCode(src_path=geojson_file, dest_path=POLYGON_DESTINATION, es_instance=es_instance())
        area_count = postcode_area.parse()
        print(f"Created and Indexed {area_count} postcode areas")
        _es_client.refresh_index()
