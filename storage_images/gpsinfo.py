# coding: utf-8
from PIL.ExifTags import TAGS, GPSTAGS

RTAGS = {v: k for (k, v) in TAGS.items()}
RGPSTAGS = {v: k for (k, v) in GPSTAGS.items()}

GPSINFO = RTAGS["GPSInfo"]

def coord_to_deg(values):
    # every coordinate is a list of 3 pairs
    # every pair is a fraction ( (n, d) -> n/d )
    # the 3 values are °, ' and " (degree, minute and second)
    deg = 0
    for i in range(3):
        (n, d) = values[i]
        if d != 0:
            deg += n/(d * (60.**i))
    return deg

def extract_location(image):
    if not hasattr(image, "_getexif"):
        return {}
    exif = image._getexif()
    if not exif:
        return {}
    try:
        gpsinfo = exif[GPSINFO]
        lat = coord_to_deg(gpsinfo[RGPSTAGS["GPSLatitude"]])
        if gpsinfo[RGPSTAGS["GPSLatitudeRef"]] == "S":
            lat = -lat
        lng = coord_to_deg(gpsinfo[RGPSTAGS["GPSLongitude"]])
        if gpsinfo[RGPSTAGS["GPSLongitudeRef"]] == "S":
            lng = -lng
        return {"lat":lat, "lng":lng}
    except (KeyError, IndexError):
        return {}
