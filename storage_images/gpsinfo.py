from __future__ import annotations

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

from PIL.TiffImagePlugin import IFDRational


RTAGS = {v: k for (k, v) in TAGS.items()}
RGPSTAGS = {v: k for (k, v) in GPSTAGS.items()}

GPS_INFO = RTAGS["GPSInfo"]
GPS_LAT = RGPSTAGS["GPSLatitude"]
GPS_LAT_REF = RGPSTAGS["GPSLatitudeRef"]
GPS_LNG = RGPSTAGS["GPSLongitude"]
GPS_LNG_REF = RGPSTAGS["GPSLongitudeRef"]


def coord_to_deg(values: list[IFDRational], reference: str) -> float:
    # every coordinate is a list of 3 rational numbers
    # the 3 numbers are °, ' and " (degree, minute and second)
    deg = 0.0
    for index, part in enumerate(values):
        if isinstance(part, tuple):
            # Pillow < 7.0.0: the values are returned as tuples instead of rational numbers
            if part[1] != 0:
                deg += (part[0] / part[1]) / (60.0**index)
        else:
            if part.denominator != 0:
                deg += part / (60.0**index)

    if reference in ("S", "W"):
        return -deg
    else:
        return deg


def extract_location(image: Image) -> dict[str, float]:
    if not hasattr(image, "_getexif"):
        return {}
    exif = image._getexif()
    if not exif or GPS_INFO not in exif:
        return {}

    gps_info = exif[GPS_INFO]
    if (
        GPS_LAT not in gps_info
        or GPS_LAT_REF not in gps_info
        or GPS_LNG not in gps_info
        or GPS_LNG_REF not in gps_info
    ):
        return {}

    return {
        "lat": coord_to_deg(gps_info[GPS_LAT], gps_info[GPS_LAT_REF]),
        "lng": coord_to_deg(gps_info[GPS_LNG], gps_info[GPS_LNG_REF]),
    }
