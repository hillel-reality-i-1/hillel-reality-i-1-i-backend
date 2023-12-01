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
ROOT = env.str("ROOT", "/")


def create_simple_image_file(image_path):
    with open(image_path, "rb") as image_file:
        image = PilImg.open(image_file)
        image = image.convert("RGB")

        byte_io = BytesIO()
        image.save(byte_io, format="PNG")
        return ContentFile(
            byte_io.getvalue(),
            "image.png",
        )


def create_wrong_ext_image_file(image_path):
    with open(image_path, "rb") as image_file:
        image = PilImg.open(image_file)
        image = image.convert("RGB")

        byte_io = BytesIO()
        image.save(byte_io, format="WEBP")
        return ContentFile(
            byte_io.getvalue(),
            "image.webp",
        )


def _simple_image_path():
    from_root_path = Path("hillel-reality-i-1-i-backend/tests/fixtures/files/storage/test_image.png")
    return join(ROOT, from_root_path)


def _compress_image_path():
    from_root_path = Path("hillel-reality-i-1-i-backend/tests/fixtures/files/storage/test_image_751x849.png")
    return join(ROOT, from_root_path)


def _big_image_path():
    from_root_path = Path("hillel-reality-i-1-i-backend/tests/fixtures/files/storage/test_image_7mb.jpg")
    return join(ROOT, from_root_path)


def _wrong_ext_image_path():
    from_root_path = Path("hillel-reality-i-1-i-backend/tests/fixtures/files/storage/test_image_wrong_ext.webp")
    return join(ROOT, from_root_path)


@pytest.fixture()
def simple_image_file():
    return create_simple_image_file(_simple_image_path())


@pytest.fixture()
def compress_image_file():
    return create_simple_image_file(_compress_image_path())


@pytest.fixture()
def big_image_file():
    return create_simple_image_file(_big_image_path())


@pytest.fixture()
def wrong_ext_image_file():
    return create_wrong_ext_image_file(_wrong_ext_image_path())
