from rest_framework import generics, status
from rest_framework.response import Response
from apps.users.token_generators import DeleteAllContentTokenGenerator
from ..permissions import IsVerifiedUser
from ..serializers.delete_all_content_confirm_serializer import DeleteAllContentConfirmSerializer
from ...content.models import Post, Comment, Contribution


class DeleteAllContentConfirmView(generics.DestroyAPIView):
    permission_classes = [IsVerifiedUser]

    def get_queryset(self):
        user = self.request.user
        return {
            'posts': Post.objects.filter(author=user),
            'comments': Comment.objects.filter(author=user),
            'contributions': Contribution.objects.filter(author=user),
        }

    def perform_destroy(self, instance):
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        serializer = DeleteAllContentConfirmSerializer(data=request.data)

        if serializer.is_valid():
            token = serializer.validated_data['token']
            password = serializer.validated_data['password']

            # Перевірити токен та пароль
            token_status = DeleteAllContentTokenGenerator().check_token(user, token)
            password_valid = user.check_password(password)

            if token_status['status'] and password_valid:
                # Якщо токен та пароль вірні, видалити контент
                queryset = self.get_queryset()

                for _, obj_list in queryset.items():
                    for obj in obj_list:
                        self.perform_destroy(obj)

                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                # Якщо токен або пароль невірні, повернути відповідні помилки
                error_details = {
                    'token_status': token_status['details'],
                    'password_status': 'Невірний пароль' if not password_valid else 'OK',
                }
                return Response(error_details, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Якщо дані не є валідними, повернути помилки валідації
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
