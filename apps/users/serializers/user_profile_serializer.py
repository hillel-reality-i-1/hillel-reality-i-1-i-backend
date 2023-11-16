from io import BytesIO
from PIL import Image as PilImg
from rest_framework import serializers
from apps.files.api.serializers import ImageSerializer
from apps.users.models import UserProfile
from django.core.files.base import ContentFile


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    profile_picture = ImageSerializer()

    class Meta:
        model = UserProfile
        fields = "__all__"

    def get_email(self, obj):
        return obj.user.email

    def create(self, validated_data):
        # Извлечь данные для вложенного поля profile_picture
        profile_picture_data = validated_data.pop("profile_picture", None)

        # Создать объект UserProfile
        user_profile = UserProfile.objects.create(**validated_data)

        # Если есть данные для profile_picture, создать связанный объект Image
        if profile_picture_data:
            # Извлечь данные для создания Image
            img = self.image_handle(profile_picture_data.get("image"))
            image_data = {
                "author": user_profile.user.pk,
                "image_name": profile_picture_data.get("image_name"),
                "image": img,
            }

            # Обработать ImageSerializer для создания Image
            image_serializer = ImageSerializer(data=image_data)
            if image_serializer.is_valid():
                image = image_serializer.save()

                # Присвоить ID изображения в поле profile_picture объекта UserProfile
                user_profile.profile_picture = image
                user_profile.save()
            else:
                # Вернуть ошибки валидации, если что-то пошло не так
                raise serializers.ValidationError(image_serializer.errors)

        return user_profile

    def image_handle(self, image_data):
        image = PilImg.open(image_data)
        if image.format.lower() not in ["jpeg", "png"]:
            raise serializers.ValidationError("Invalid image format. Supported formats: JPEG, PNG.")

        max_size = (320, 240)
        if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
            image.thumbnail(max_size)
            compressed_image_buffer = BytesIO()
            image.save(compressed_image_buffer, format=image.format.upper())

            return ContentFile(compressed_image_buffer.getvalue(), name=image_data.name)

        return image_data
