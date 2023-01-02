from __future__ import annotations

import json
from io import BytesIO
from tempfile import TemporaryDirectory
from typing import Optional

from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.test import TestCase, RequestFactory

from storage_images.views import handle_image

EXIF_NO_LOCATION = b"Exif\x00\x00MM\x00*\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00"
EXIF_LOCATION_N_E = (
    b"Exif\x00\x00MM\x00*\x00\x00\x00\x08\x00\x01\x88%\x00\x04\x00\x00\x00\x01\x00\x00\x00\x1a\x00"
    b"\x00\x00\x00\x00\x05\x00\x00\x00\x01\x00\x00\x00\x04\x02\x02\x00\x00\x00\x01\x00\x02\x00\x00"
    b"\x00\x02N\x00\x00\x00\x00\x02\x00\x05\x00\x00\x00\x03\x00\x00\x00X\x00\x03\x00\x02\x00\x00\x00"
    b"\x02E\x00\x00\x00\x00\x04\x00\x05\x00\x00\x00\x03\x00\x00\x00p\x00\x00\x004\x00\x00\x00\x01\x00"
    b"\x00\x00\x1f\x00\x00\x00\x01\x00\x00\x00\x07\x00\x00\x00\x01\x00\x00\x00\r\x00\x00\x00\x01\x00"
    b"\x00\x00\x18\x00\x00\x00\x01\x00\x00\x00\x1e\x00\x00\x00\x01 "
)
EXIF_LOCATION_S_W = (
    b"Exif\x00\x00MM\x00*\x00\x00\x00\x08\x00\x01\x88%\x00\x04\x00\x00\x00\x01\x00\x00\x00\x1a\x00"
    b"\x00\x00\x00\x00\x05\x00\x00\x00\x01\x00\x00\x00\x04\x02\x02\x00\x00\x00\x01\x00\x02\x00\x00"
    b"\x00\x02S\x00\x00\x00\x00\x02\x00\x05\x00\x00\x00\x03\x00\x00\x00X\x00\x03\x00\x02\x00\x00\x00"
    b"\x02W\x00\x00\x00\x00\x04\x00\x05\x00\x00\x00\x03\x00\x00\x00p\x00\x00\x00\x16\x00\x00\x00\x01"
    b"\x00\x00\x006\x00\x00\x00\x01\x00\x00\x00\x1e\x00\x00\x00\x01\x00\x00\x00+\x00\x00\x00\x01\x00"
    b"\x00\x00\x0b\x00\x00\x00\x01\x00\x00\x00/\x00\x00\x00\x01 "
)


def generage_image_file(image_format: str, exif: Optional[bytes] = None) -> bytes:
    im = Image.new("1", (8, 8))
    im_bytes = BytesIO()
    if exif is not None:
        im.save(im_bytes, image_format.upper(), exif=exif)
    else:
        im.save(im_bytes, image_format.upper())
    im_bytes.seek(0)
    return im_bytes.read()


class RegularImageUpload(TestCase):
    databases = {}

    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_upload(self) -> None:
        with TemporaryDirectory() as media_dir, self.settings(
            MEDIA_ROOT=media_dir, MEDIA_URL=""
        ):
            for image_format in ["jpeg", "png", "gif", "bmp", "ppm"]:
                self.assert_can_upload(image_format, generage_image_file(image_format))

            self.assert_can_upload(
                "jpeg", generage_image_file("jpeg", EXIF_NO_LOCATION)
            )
            self.assert_can_upload(
                "jpeg",
                generage_image_file("jpeg", EXIF_LOCATION_N_E),
                dict(lat=52.51861111111111, lng=13.408333333333333),
            )
            self.assert_can_upload(
                "jpeg",
                generage_image_file("jpeg", EXIF_LOCATION_S_W),
                dict(lat=-22.90833333333333, lng=-43.19638888888888),
            )

    def assert_can_upload(
        self,
        image_format: str,
        image_content: bytes,
        location: Optional[dict[str, float]] = None,
    ):
        image_file = ContentFile(image_content, name="myimage." + image_format)

        request = self.factory.post("/image/add", {"image": image_file})
        response = handle_image(request)

        self.assertEqual(response.status_code, 200)

        values = json.loads(response.content)

        if location is None:
            self.assertFalse("location" in values)
        else:
            self.assertEqual(values["location"], location)

        image_path = values["path"].lstrip("/")
        self.assertTrue(default_storage.exists(image_path.split(".")[0]))

        thumbnail = values["thumbnail"].lstrip("/")
        self.assertTrue(default_storage.exists(thumbnail))
