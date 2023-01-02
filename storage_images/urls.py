from django.urls import path
from .views import handle_image

urlpatterns = [
    path("image/add", handle_image, name="handle_image"),
]
