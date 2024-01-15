from rest_framework import serializers


class ContactVisibilitySerializer(serializers.Serializer):
    contact_type = serializers.ChoiceField(
        choices=[
            'telegram', 'instagram', 'email', 'phone', 'linkedin', 'facebook'
        ]
    )
