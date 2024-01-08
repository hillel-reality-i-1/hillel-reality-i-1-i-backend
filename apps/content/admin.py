from django.contrib import admin

from .forms.post_validate_admin_form import PostValidateAdminForm
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    form = PostValidateAdminForm


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
