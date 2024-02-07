import os
import logging
from botocore.exceptions import ClientError
import boto3

from apps.content.models import Post
from core.settings import env
from io import BytesIO
from PIL import Image as PilImg
from django.core.files.base import ContentFile
from rest_framework import serializers
from shutil import rmtree


AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = env.str("AWS_DEFAULT_REGION")


def upload_file_to_s3(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client("s3")
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def moderate_image(photo, bucket):
    session = boto3.Session()
    client = session.client("rekognition")

    response = client.detect_moderation_labels(Image={"S3Object": {"Bucket": bucket, "Name": photo}})
    return response


def moderation_image_with_aws(path_to_file):
    file_name = path_to_file.split("/")[-1]
    is_uploaded = upload_file_to_s3(path_to_file, "uhelp-bucket")
    if is_uploaded:
        response = moderate_image(file_name, "uhelp-bucket")
        return response
    else:
        raise serializers.ValidationError(
            "We are sorry. The image cannot be loaded at this time. Moderation service is unavailable."
        )


def image_handle(image_data):
    max_size_bytes = 5 * 1024 * 1024
    min_size_bytes = 3 * 1024
    if image_data.size > max_size_bytes or image_data.size < min_size_bytes:
        raise serializers.ValidationError("Photo size ranges from 3 kb to 5 mb. Be kind, take another photo.")

    image = PilImg.open(image_data)
    if image.format.lower() not in ["jpeg", "png"]:
        raise serializers.ValidationError("Invalid image format. Supported formats: JPEG, JPG, PNG.")

    max_size = (320, 240)
    if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
        image.thumbnail(max_size)

    compressed_image_buffer = BytesIO()
    image.save(compressed_image_buffer, format=image.format.upper())

    return ContentFile(compressed_image_buffer.getvalue(), name=image_data.name)


def remove_img_from_disk(path):
    folder_path = path[: path.rfind("/")]
    try:
        rmtree(folder_path)
    except Exception as e:
        print(f"Error while deleting file: {e}")


def moderate_img(model, response, path, serializer, prev_image, prev_image_path, attr: str, old_post_data=None):
    if response.get("ModerationLabels"):
        obj = model.objects.get(id=serializer.data.get("id"))
        if model == Post:
            if old_post_data:
                obj.title = old_post_data.get("title")
                obj.content = old_post_data.get("content")
                obj.category.set(old_post_data.get("category"))
                obj.country.set(old_post_data.get("country"))
                if prev_image is not None:
                    obj.postimage.post_image = prev_image.post_image
                    prev_image.save()
                obj.save()
            else:
                obj.delete()
        else:
            if prev_image is None:
                print("delete")
                obj.delete()
            else:
                setattr(obj, attr, prev_image)
                obj.save()

        remove_img_from_disk(path)
        raise serializers.ValidationError("Your image violates our content moderation policy.")
    if prev_image_path:
        print(prev_image_path)
        remove_img_from_disk(prev_image_path)
