from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Класс User является наследником класса AbstractUser из библиотеки django.contrib.auth.models.
    Это модель данных, содержащаяся в таблице базы данных user.
    """
    pass
