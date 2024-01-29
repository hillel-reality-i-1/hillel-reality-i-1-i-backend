from django.contrib import admin
from .models import File, Image
from .models.post_image import PostImage

admin.site.register(PostImage)
admin.site.register(File)
admin.site.register(Image)
