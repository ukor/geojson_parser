from hashlib import sha256
import string

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

def hashFileName(fileName: str) -> str:
    return sha256(fileName.encode('utf-8')).hexdigest()


def removePuntautions(word: str) -> str:
    # [see stackoverflow question] https://stackoverflow.com/q/53664775/3501729
    table = str.maketrans("", "", string.punctuation)
    seprator = ""
    # remove all punctuation
    s = [w.translate(table) for w in word]
    return seprator.join(s)

def getPoints(geometry: dict):
    fp = geometry.get("coordinates")[0][0]
    _first_point = fp[0] if isinstance(fp[0], list) else fp
    return Point(_first_point[0], _first_point[1])
