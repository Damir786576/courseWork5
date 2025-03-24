from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.serilazers import UserRegistrationSerializer, UserSerializer
from .models import CustomUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email пользователя'),
                'telegram_id': openapi.Schema(type=openapi.TYPE_STRING, description='Telegram ID (опционально)'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Пароль'),
                'password_confirm': openapi.Schema(type=openapi.TYPE_STRING, description='Подтверждение пароля'),
            },
            required=['email', 'password', 'password_confirm']
        ),
        responses={201: 'Пользователь создан', 400: 'Ошибка в данных'}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, permissions.IsAdminUser]
    queryset = CustomUser.objects.all()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
