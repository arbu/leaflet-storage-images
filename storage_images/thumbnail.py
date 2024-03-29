from __future__ import annotations

from PIL import Image
from PIL.ExifTags import TAGS

for tag, name in TAGS.items():
    if name == "Orientation":
        ORIENTATION = tag
        break


def orientate(image: Image, value: int) -> Image:
    if value in (2, 5):
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
    if value in (4, 7):
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
    if value in (5, 7, 8):
        image = image.transpose(Image.ROTATE_90)
    if value == 3:
        image = image.transpose(Image.ROTATE_180)
    if value == 6:
        image = image.transpose(Image.ROTATE_270)
    return image


def create_thumbnail(image: Image, size: tuple[int, int]) -> Image:
    thumbnail = Image.new("RGB", image.size, (255, 255, 255))
    if len(image.split()) > 3:
        thumbnail.paste(image, mask=image.split()[3])
    else:
        thumbnail.paste(image)

    if hasattr(image, "_getexif"):
        exif = image._getexif()
        if exif and ORIENTATION in exif:
            thumbnail = orientate(thumbnail, exif[ORIENTATION])

    thumbnail.thumbnail(size, Image.ANTIALIAS)
    return thumbnail
