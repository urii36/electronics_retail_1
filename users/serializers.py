from typing import List

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated

from users.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Класс UserCreateSerializer наследуется от класса ModelSerializer из rest_framework.serializers.
    Это класс для удобной сериализации и десериализации объектов класса User при обработке
    создайте новый экземпляр класса User.
    """
    id = serializers.IntegerField(required=False)
    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        """
        Метакласс - это внутренний служебный класс сериализатора,
        определяет необходимые параметры для функционирования сериализатора.
        """
        model = User
        fields: List[str] = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_repeat']

    def validate(self, attrs) -> dict:
        """
        Функция validate переопределяет метод родительского класса. Принимает значения экземпляра класса
        атрибуты в качестве параметров. Вызывает родительский метод и добавляет проверки сложности пароля в соответствии с
        указанные валидаторы и совпадение полученных значений 'password' и 'password_repeat',
        вызывает исключение ValidationError, если есть различия. После сравнения удаляет ключ и значение
        из 'password_repeat'. Возвращает объект данных.
        """
        data: dict = super().validate(attrs)
        validate_password(data['password'])
        if data['password'] != data['password_repeat']:
            raise serializers.ValidationError('The entered passwords must match')
        del data['password_repeat']
        return data

    def create(self, validated_data) -> User:
        """
        Функция create переопределяет метод родительского класса. Принимает значения validated_data в качестве параметров.
        Создает экземпляр класса User, добавляет значение хэшированного пароля и сохраняет объект
        в базе данных. Возвращает созданный объект.
        """
        user: User = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    """
    Класс LoginSerializer наследуется от класса ModelSerializer из rest_framework.serializers.
    Это класс для удобной сериализации и десериализации объектов класса User при обработке
    экземпляра login класса User.
    """
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        """
        Метакласс - это внутренний служебный класс сериализатора,
        определяет необходимые параметры для функционирования сериализатора.
        """
        model = User
        fields: str = '__all__'

    def create(self, validated_data) -> User:
        """
        Функция create переопределяет метод родительского класса. Принимает значения validated_data в качестве параметров.
        Проверяет подлинность экземпляра класса User в соответствии с полученными значениями, вызывает ошибку проверки подлинности
        исключение, если в базе данных отсутствует информация о пользователе или неверные данные. Возвращает найденный объект.
        """
        user = authenticate(username=validated_data['username'], password=validated_data['password'])
        if user is None:
            raise AuthenticationFailed
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Класс UserSerializer наследуется от класса ModelSerializer из rest_framework.serializers.
    Это класс для удобной сериализации и десериализации объектов класса User.
    """

    class Meta:
        """
        Метакласс - это внутренний служебный класс сериализатора,
        определяет необходимые параметры для функционирования сериализатора.
        """
        model = User
        fields: List[str] = ['id', 'username', 'first_name', 'last_name', 'email']


class UpdatePasswordSerializer(serializers.Serializer):
    """
    Класс сериализатора обновлений паролей наследуется от класса ModelSerializer из rest_framework.serializers.
    Это класс для удобной сериализации и десериализации объектов класса User при обработке
    обновите пароль экземпляра класса User.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs: dict) -> dict:
        """
        Функция validate переопределяет метод родительского класса. Принимает объект attrs в качестве параметров.
        Проверяет наличие аутентификации пользователя и корректность введенного значения 'old_password' в случае, если
        неверных данных вызывает исключение ValidationError. Возвращает объект, полученный в качестве параметра.
        """
        user: User = attrs['user']
        if not user:
            raise NotAuthenticated
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError({'old_password': 'uncorrect password'})
        return attrs

    def create(self, validated_data) -> None:
        """
        Функция create переопределяет метод родительского класса. Принимает объект validated_data в качестве параметров.
        При вызове метода возникает исключение NotImplementedError. Метод не используется в этом сериализаторе.
        """
        raise NotImplementedError

    def update(self, instance: User, validated_data) -> User:
        """
        Функция обновления переопределяет метод родительского класса. Принимает объекты экземпляра в качестве параметров
        экземпляр класса User и validated_data. Если метод вызывается, он обновляет значение
        поля 'пароль' и сохраняет обновленный экземпляр в базе данных. Возвращает обновленный экземпляр
        класса User.
        """
        instance.password = make_password(validated_data['new_password'])
        instance.save(update_fields=('password',))
        return instance
