import sys
import os
import django
from django.conf import settings
from django.core.management import call_command

if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    settings.configure()
    settings.INSTALLED_APPS = ["storage_images"]
    django.setup()
    call_command("test")
