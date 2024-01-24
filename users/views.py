from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.models import User
from users.serializers import UserCreateSerializer, LoginSerializer, UserSerializer, UpdatePasswordSerializer


class UserCreateView(CreateAPIView):
    """
    Класс User Create View наследуется от класса CreateAPIView из модуля rest_framework.generics и представляет
    собой представление на основе класса для обработки запросов методами POST по адресу "/core/signup".
    """
    model = User
    serializer_class = UserCreateSerializer
    permission_classes: list = [AllowAny]


class LoginView(CreateAPIView):
    """
    Класс LoginView наследуется от класса CreateAPIView из модуля rest_framework.generics и представляет
    собой представление на основе класса для обработки запросов методами POST по адресу "/core/login".
    """
    serializer_class = LoginSerializer
    permission_classes: list = [AllowAny]

    def post(self, request, *args, **kwargs) -> Response:
        """
        Функция post переопределяет метод родительского класса. Принимает объект запроса и любые позиционные
        и именованные аргументы в качестве параметров. Если метод вызывается, он проверяет и сериализует полученные данные
        и вызывает метод входа в систему для объекта пользовательского класса. Возвращает сериализованные объектные данные в формате JSON.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request=request, user=user)
        return Response(serializer.data)


class ProfileView(RetrieveUpdateDestroyAPIView):
    """
    The ProfileView class inherits from the RetrieveUpdateDestroyAPIView class from the rest_framework.generics module
    and is a class-based view for processing requests with POST, PUT, PATCH and DELETE methods at the address
     '/core/profile'.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self) -> User:
        """
        Функция get_object переопределяет метод родительского класса. Она не принимает аргументы в качестве параметров,
        за исключением самого экземпляра. Если метод вызывается, он возвращает экземпляр класса User, соответствующий
        пользователю, который сделал запрос.
        """
        return self.request.user

    def delete(self, request, *args, **kwargs) -> Response:
        """
        Функция delete переопределяет метод родительского класса. Принимает объект запроса и все другие
        позиционные и именованные аргументы в качестве параметров. Если метод вызывается, он вызывает метод выхода из системы для
        экземпляра класса User, соответствующего пользователю, который сделал запрос.
        """
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdatePasswordView(UpdateAPIView):
    """
    Класс представления пароля обновления наследуется от класса UpdateAPIView из модуля rest_framework.generics
    и представляет собой представление на основе класса для обработки запросов методами PUT и PATCH по адресу
     '/core/update_password'.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UpdatePasswordSerializer

    def get_object(self):
        """
        Функция get_object переопределяет метод родительского класса. Она не принимает аргументы в качестве параметров,
        за исключением самого экземпляра. Если метод вызывается, он возвращает экземпляр класса User, соответствующий
        пользователю, который сделал запрос.
        """
        return self.request.user
