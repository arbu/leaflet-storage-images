from io import BytesIO
from random import randint

from PIL import Image
from django.conf import settings
from django.core.files.storage import get_storage_class
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import ImageForm
from .gpsinfo import extract_location
from .thumbnail import create_thumbnail

IMAGES = "images/"
THUMBNAILS = "thumbnails/"
THUMBNAIL_SIZE = (300, 300)


storage_class = (
    settings.IMAGE_FILE_STORAGE if hasattr(settings, "IMAGE_FILE_STORAGE") else None
)
storage = get_storage_class(storage_class)()


def generate_name() -> str:
    name = hex(randint(0, 2**32))[2:]
    for i in range(10):  # don't infinit-loop, djangos storage will handle this too
        if not storage.exists(IMAGES + name):
            break
        name = hex(randint(0, 2**32))[2:]
    return name


def save_thumbnail(image: Image, name: str) -> str:
    thumbnail = create_thumbnail(image, THUMBNAIL_SIZE)

    buffer = BytesIO()
    thumbnail.save(buffer, format="JPEG")
    djangofile = InMemoryUploadedFile(
        buffer, None, name, "JPEG", len(buffer.getvalue()), None
    )
    buffer.seek(0)

    return storage.save(THUMBNAILS + name, djangofile)


@require_POST
@csrf_exempt
def handle_image(request: HttpRequest) -> JsonResponse:
    form = ImageForm(request.POST, request.FILES)
    if not form.is_valid():
        return JsonResponse(form.errors.get_json_data(), status=415)

    name = generate_name()
    path = storage.save(IMAGES + name, form.cleaned_data["image"].file)
    image = Image.open(storage.path(path))

    location = extract_location(image)
    thumbnail = save_thumbnail(image, name + ".jpg")

    data = {
        "path": storage.url(path) + "." + image.format.lower(),
        "thumbnail": storage.url(thumbnail),
    }
    if location:
        data["location"] = location

    return JsonResponse(data)
