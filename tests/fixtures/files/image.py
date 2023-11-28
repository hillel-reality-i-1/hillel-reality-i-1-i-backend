from pathlib import Path
import environ
import pytest
from django.conf import settings
from os.path import join
from PIL import Image as PilImg
from io import BytesIO
from django.core.files.base import ContentFile


env = environ.FileAwareEnv()
env.read_env(settings.BASE_DIR.joinpath(".env"))
ROOT = env.str("ROOT", '/')


def create_image_file(image_path):
    with open(image_path, 'rb') as image_file:
        image = PilImg.open(image_file)
        image = image.convert('RGB')

        byte_io = BytesIO()
        image.save(byte_io, format='PNG')
        return ContentFile(
            byte_io.getvalue(),
            'image.png',
        )


def _image_path():
    from_root_path = Path("hillel-reality-i-1-i-backend/tests/fixtures/files/storage/test_image.png")
    return join(ROOT, from_root_path)


@pytest.fixture()
def image_file():
    return create_image_file(_image_path())
