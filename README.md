# leaflet-storage-images

A module for [django-leaflet-storage](https://github.com/umap-project/django-leaflet-storage) and [Leaflet.Storage](https://github.com/yohanboniface/Leaflet.Storage) (a.k.a. [uMap](https://github.com/umap-project/umap)) which adds support for adding images to Markers. If the image contains GPS-informations, the Marker position can be updated.

## Installation

    git clone https://github.com/arbu/leaflet-storage-images
    cd leaflet-storage-images
    python setup.py install

Add `storage_images` to you apps:

    INSTALLED_APPS = (
        ...
        "storage_images",
    )

Include `storage_images` urls:

    (r'', include('storage_images.urls')),

Add `Leaflet.Storage.Images` scripts to your base.html:

    <script src="{{ STATIC_URL }}images/js/leaflet.storage.images.js"></script>
    {% if locale %}
    <script src="{{ STATIC_URL }}images/locale/{{ locale }}.js"></script>
    {% endif %}

Depending on your setup you may need to run:

    python manage.py collectstatic

Also make sure you have configured `MEDIA_URL` and `MEDIA_PATH`.

If you want to limit the maximum filesize to upload, I recommend to configure the webserver (apache, nginx etc.) accordingly. 

## Dependencies

The only dependency is [pillow](https://github.com/python-pillow/Pillow), while [django-leaflet-storage](https://github.com/umap-project/django-leaflet-storage) or [uMap](https://github.com/umap-project/umap) is recommended :)

The current version of django-leaflet-storage depends on pillow 3.0.0, which contains a bug that prevents reading GPS-informations from an image. If you want/need this feature, install any other version of pillow, e.g.:

    pip install pillow==3.1.1 --force-reinstall

This won't brake django-leaflet-storage, only your dependency tree.

## Basic usage

When adding a new or editing an existing Marker, you can choose an image to upload under "Add image". The image is automatically uploaded. If the image contains GPS-informations, you are asked if you want to update the Marker.
