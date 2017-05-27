from setuptools import setup

import storage_images

setup(
    name="leaflet-storage-images",
    version=storage_images.__version__,
    author=storage_images.__author__,
    author_email=storage_images.__contact__,
    description=storage_images.__doc__,
    keywords="django leaflet geodjango",
    url=storage_images.__homepage__,
    download_url=storage_images.__homepage__,
    packages=["storage_images"],
    include_package_data=True,
    platforms=["any"],
    zip_safe=False,
    install_requires=["pillow"],
    long_description=storage_images.__doc__,

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
    ],
)
