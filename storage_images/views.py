from random import randint
from PIL import Image
from io import BytesIO

from django.core.files.storage import default_storage, get_storage_class
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .forms import ImageForm
from .gpsinfo import extract_location
from .thumbnail import create_thumbnail

IMAGES = "images/"
THUMBNAILS = "thumbnails/"
THUMBNAIL_SIZE = (300, 300)

try:
    storage = get_storage_class(settings.IMAGE_FILE_STORAGE)()
except AttributeError:
    storage = default_storage

def generate_name():
    for i in range(10): # don't infinit-loop, djangos storage will handle this too
        name = hex(randint(0,2**32))[2:]
        if not storage.exists(IMAGES + name):
            break
    return name

def save_thumbnail(image, name):
    thumbnail = create_thumbnail(image, THUMBNAIL_SIZE)

    buffer = BytesIO()
    thumbnail.save(buffer, format="JPEG")
    djangofile = InMemoryUploadedFile(buffer, None, name, "JPEG", len(buffer.getvalue()), None)
    buffer.seek(0)

    return storage.save(THUMBNAILS + name, djangofile)
    
@require_POST
@csrf_exempt
def handle_image(request):
    form = ImageForm(request.POST, request.FILES)
    if not form.is_valid():
        return HttpResponse(form.errors.as_json(), content_type='application/json', status=415)
    
    name = generate_name()
    path = storage.save(IMAGES + name, form.cleaned_data['image'].file)
    image = Image.open(storage.path(path))
    
    location = extract_location(image)
    thumbnail = save_thumbnail(image, name + ".jpg")
    
    data = {"path": storage.url(path) + "." + image.format.lower(), "thumbnail": storage.url(thumbnail)}
    if location:
        data["location"] = location
    
    return JsonResponse(data)
