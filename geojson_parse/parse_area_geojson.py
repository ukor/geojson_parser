import time
import simplejson as json
from os import listdir, rename
from os.path import isfile, join
import ijson
from .es import es_client


class Area:

    def __init__(self, es_client, source_path, dest_path):
        # initiate elastic search
        self.es = Elasticsearch()
        self.write_count = 0
        self._file_path = source_path
        self.destination_dir = dest_path or "./mapTestBackend/area"
        self._index = "homeknock_places"


    def parse(self) -> int:
        _file_path = self._file_path
        new_name = _file_path.strip().replace(" ", "_")
        self._read_file(new_name)
        return self.write_count


    def _read_file(self, file_path):
        with open(file_path, "rb") as _file:
            obj = ijson.items(_file, "features.item")
            features = (o for o in obj if o["type"] == "Feature")
            for feature in features:
                _props = feature['properties']
                # write to a new file
                file_name = _props['Name'].lower()
                _props["name"] = _props["Name"]
                del _props["Name"]

                es_client(es_instance=self.es).add_doc(
                    id=_props["name"].lower(),
                    name=_props["name"],
                    official_name=f'{_props["name"]} - Postcode Area',
                    polygon_file_name=file_name,
                    scope="postcode_area")

                _geoJson = {
                    "type": "FeatureCollection",
                    "features": [feature]
                }
                self._write_file(file_name, _geoJson)
                print(
                    f"Wrote geoJSON from {file_path} to {file_name}.json")
                time.sleep(0.25)


    def _write_file(self, file_name, obj):
        _f_name = file_name.lower().replace("/", "_").replace(" ", "_")
        print(f"Writing geoJSON to => {_f_name}")
        _file_path = join(self.destination_dir, _f_name)+".json"
        with open(_file_path, "w") as json_file:
            json.dump(obj, json_file, use_decimal=True, indent=2,
                    separators=(",", ":"), encoding='utf-8')
        self.write_count += 1


j = [{"postcode_area":"AB","post_town":"Aberdeen"},{"postcode_area":"AL","post_town":"St. Albans"},{"postcode_area":"B","post_town":"Birmingham"},{"postcode_area":"BA","post_town":"Bath"},{"postcode_area":"BB","post_town":"Blackburn"},{"postcode_area":"BD","post_town":"Bradford"},{"postcode_area":"BH","post_town":"Bournemouth"},{"postcode_area":"BL","post_town":"Bolton"},{"postcode_area":"BN","post_town":"Brighton"},{"postcode_area":"BR","post_town":"Bromley"},{"postcode_area":"BS","post_town":"Bristol"},{"postcode_area":"BT","post_town":"Belfast"},{"postcode_area":"CA","post_town":"Carlisle"},{"postcode_area":"CB","post_town":"Cambridge"},{"postcode_area":"CF","post_town":"Cardiff"},{"postcode_area":"CH","post_town":"Chester"},{"postcode_area":"CM","post_town":"Chelmsford"},{"postcode_area":"CO","post_town":"Colchester"},{"postcode_area":"CR","post_town":"Croydon"},{"postcode_area":"CT","post_town":"Canterbury"},{"postcode_area":"CV","post_town":"Coventry"},{"postcode_area":"CW","post_town":"Crewe"},{"postcode_area":"DA","post_town":"Dartford"},{"postcode_area":"DD","post_town":"Dundee"},{"postcode_area":"DE","post_town":"Derby"},{"postcode_area":"DG","post_town":"Dumfries"},{"postcode_area":"DH","post_town":"Durham"},{"postcode_area":"DL","post_town":"Darlington"},{"postcode_area":"DN","post_town":"Doncaster"},{"postcode_area":"DT","post_town":"Dorchester"},{"postcode_area":"DY","post_town":"Dudley"},{"postcode_area":"E","post_town":"London E"},{"postcode_area":"EC","post_town":"London EC"},{"postcode_area":"EH","post_town":"Edinburgh"},{"postcode_area":"EN","post_town":"Enfield"},{"postcode_area":"EX","post_town":"Exeter"},{"postcode_area":"FK","post_town":"Falkirk"},{"postcode_area":"FY","post_town":"Blackpool"},{"postcode_area":"G","post_town":"Glasgow"},{"postcode_area":"GL","post_town":"Gloucester"},{"postcode_area":"GU","post_town":"Guildford"},{"postcode_area":"GY","post_town":"Guernsey"},{"postcode_area":"HA","post_town":"Harrow"},{"postcode_area":"HD","post_town":"Huddersfield"},{"postcode_area":"HG","post_town":"Harrogate"},{"postcode_area":"HP","post_town":"Hemel Hempstead"},{"postcode_area":"HR","post_town":"Hereford"},{"postcode_area":"HS","post_town":"Western Isles"},{"postcode_area":"HU","post_town":"Hull"},{"postcode_area":"HX","post_town":"Halifax"},{"postcode_area":"IG","post_town":"Ilford"},{"postcode_area":"IM","post_town":"Isle Of Man"},{"postcode_area":"IP","post_town":"Ipswich"},{"postcode_area":"IV","post_town":"Inverness"},{"postcode_area":"JE","post_town":"Jersey"},{"postcode_area":"KA","post_town":"Kilmarnock"},{"postcode_area":"KT","post_town":"Kingston Upon Thames"},{"postcode_area":"KW","post_town":"Kirkwall"},{"postcode_area":"KY","post_town":"Kirkcaldy"},{"postcode_area":"L","post_town":"Liverpool"},{"postcode_area":"LA","post_town":"Lancaster"},{"postcode_area":"LD","post_town":"Llandrindod Wells"},{"postcode_area":"LE","post_town":"Leicester"},{"postcode_area":"LL","post_town":"Llandudno"},{"postcode_area":"LN","post_town":"Lincoln"},{"postcode_area":"LS","post_town":"Leeds"},{"postcode_area":"LU","post_town":"Luton"},{"postcode_area":"M","post_town":"Manchester"},{"postcode_area":"ME","post_town":"Medway"},{"postcode_area":"MK","post_town":"Milton Keynes"},{"postcode_area":"ML","post_town":"Motherwell"},{"postcode_area":"N","post_town":"London N"},{"postcode_area":"NE","post_town":"Newcastle Upon Tyne"},{"postcode_area":"NG","post_town":"Nottingham"},{"postcode_area":"NN","post_town":"Northampton"},{"postcode_area":"NP","post_town":"Newport"},{"postcode_area":"NR","post_town":"Norwich"},{"postcode_area":"NW","post_town":"London Nw"},{"postcode_area":"OL","post_town":"Oldham"},{"postcode_area":"OX","post_town":"Oxford"},{"postcode_area":"PA","post_town":"Paisley"},{"postcode_area":"PE","post_town":"Peterborough"},{"postcode_area":"PH","post_town":"Perth"},{"postcode_area":"PL","post_town":"Plymouth"},{"postcode_area":"PO","post_town":"Portsmouth"},{"postcode_area":"PR","post_town":"Preston"},{"postcode_area":"RG","post_town":"Reading"},{"postcode_area":"RH","post_town":"Redhill"},{"postcode_area":"RM","post_town":"Romford"},{"postcode_area":"S","post_town":"Sheffield"},{"postcode_area":"SA","post_town":"Swansea"},{"postcode_area":"SE","post_town":"London SE"},{"postcode_area":"SG","post_town":"Stevenage"},{"postcode_area":"SK","post_town":"Stockport"},{"postcode_area":"SL","post_town":"Slough"},{"postcode_area":"SM","post_town":"Sutton"},{"postcode_area":"SN","post_town":"Swindon"},{"postcode_area":"SO","post_town":"Southampton"},{"postcode_area":"SP","post_town":"Salisbury"},{"postcode_area":"SR","post_town":"Sunderland"},{"postcode_area":"SS","post_town":"Southend-On-Sea"},{"postcode_area":"ST","post_town":"Stoke-On-Trent"},{"postcode_area":"SW","post_town":"London SW"},{"postcode_area":"SY","post_town":"Shrewsbury"},{"postcode_area":"TA","post_town":"Taunton"},{"postcode_area":"TD","post_town":"Galashiels"},{"postcode_area":"TF","post_town":"Telford"},{"postcode_area":"TN","post_town":"Tonbridge"},{"postcode_area":"TQ","post_town":"Torquay"},{"postcode_area":"TR","post_town":"Truro"},{"postcode_area":"TS","post_town":"Cleveland"},{"postcode_area":"TW","post_town":"Twickenham"},{"postcode_area":"UB","post_town":"Southall"},{"postcode_area":"W","post_town":"London W"},{"postcode_area":"WA","post_town":"Warrington"},{"postcode_area":"WC","post_town":"London WC"},{"postcode_area":"WD","post_town":"Watford"},{"postcode_area":"WF","post_town":"Wakefield"},{"postcode_area":"WN","post_town":"Wigan"},{"postcode_area":"WR","post_town":"Worcester"},{"postcode_area":"WS","post_town":"Walsall"},{"postcode_area":"WV","post_town":"Wolverhampton"},{"postcode_area":"YO","post_town":"York"},{"postcode_area":"ZE","post_town":"Lerwick"}]
