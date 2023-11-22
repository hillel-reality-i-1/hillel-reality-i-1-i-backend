from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth import get_user_model
import secrets

User = get_user_model()
# Here must be path to images from settings
# PATH_TO_UPLOAD = 'images/'


def universal_file_path_builder(instance, filename) -> str:
    content_type = ContentType.objects.get_for_model(instance)
    random_part_size = 64
    random_string_value = secrets.token_urlsafe(nbytes=random_part_size)[:random_part_size]

    _, extension = filename.rsplit(sep=".", maxsplit=1)

    default_file_name = "file"
    custom_filename = f"{default_file_name}.{extension}"

    return f"{content_type.app_label}/{content_type.model}/{random_string_value}/{custom_filename}"


class Image(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=universal_file_path_builder)
    creation_date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.image_name
