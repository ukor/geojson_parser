from os import getenv
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def setPolygonDestination(env: str) -> str:
    if env == "dev":
        return f"{str(Path.home())}geojson_parse/raw"
    return getenv("POLYGON_DESTINATION")

ENV = getenv("ENV")
POLYGON_DESTINATION = setPolygonDestination(ENV)
ES_ENDPOINT = getenv("AWS_ES_ENDPOINT")
ES_INDEX_NAME = getenv("ES_INDEX_NAME")

AWS_USER = getenv("AWS_USER")
AWS_ACCESS_KEY_ID = getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = getenv("AWS_REGION")
