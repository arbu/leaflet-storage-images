from django.conf.urls import url
from .views import handle_image

urlpatterns = [
    url(r'^image/add', handle_image, name="handle_image"),
]
