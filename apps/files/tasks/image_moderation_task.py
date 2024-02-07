from celery import shared_task


@shared_task
def image_moderation_task(temporary_path):
    from apps.content.utils.aws_utils import moderation_image_with_aws

    # with NamedTemporaryFile(delete=True, suffix=".jpg", dir="temp_images") as temp_file:
    #     temp_file.write(processed_image_data.read())
    #     temporary_path = temp_file.name
    moderation_image_with_aws(temporary_path)
