from pathlib import Path
import environ
import pytest
from django.conf import settings
from os.path import join


env = environ.FileAwareEnv()
env.read_env(settings.BASE_DIR.joinpath(".env"))
ROOT = env.str("ROOT", '/')


@pytest.fixture
def image_path():
    from_root_path = Path("hillel-reality-i-1-i-backend/tests/fixtures/files/storage/test_image.png")
    return join(ROOT, from_root_path)
