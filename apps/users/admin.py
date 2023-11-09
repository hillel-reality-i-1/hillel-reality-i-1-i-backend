from django.contrib import admin

from .models import User, UserProfile, UserProfileExtended

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(UserProfileExtended)
