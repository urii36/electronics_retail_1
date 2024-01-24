from datetime import datetime
from typing import List
from django.db import models


class Node(models.Model):
    """
    Класс Node наследуется от базового класса Model из модуля django.db.models.
    Определяет поля таблицы базы данных, их свойства и ограничения.
    """
    name = models.CharField(max_length=300, unique=True)
    supplier = models.ForeignKey('self', null=True, blank=True, default=None, on_delete=models.SET_DEFAULT)
    level = models.IntegerField(choices=[(0, 0), (1, 1), (2, 2)])
    debt_to_the_supplier = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_of_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """
        Функция __str__ переопределяет метод родительского класса Model и создает
        выходной формат для экземпляров этого класса.
        """
        return self.name

    class Meta:
        """
        Метакласс содержит общее имя экземпляра модели в единственном и множественном числе, используемое
        в панели администрирования.
        """
        verbose_name: str = 'trading network member'
        verbose_name_plural: str = 'trading network members'
        ordering: List[str] = ['level']

    def save(self, *args, **kwargs):
        """
        Функция сохранения добавляет дополнительную функциональность методу родительского класса. Автоматически заполняет
        поля при создании экземпляров класса. После этого она вызывает метод родительского класса.
        """
        if not self.id:
            self.date_of_creation = datetime.now()
        return super().save(*args, **kwargs)


class Contact(models.Model):
    """
    Класс Contact наследуется от базового класса Model из модуля django.db.models.
    Определяет поля таблицы базы данных, их свойства и ограничения.
    """
    member = models.OneToOneField(Node, on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=50, blank=True, null=True)
    house_number = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        """
        Метакласс содержит общее имя экземпляра модели в единственном и множественном числе, используемое
        в панели администрирования.
        """
        verbose_name: str = 'contact'
        verbose_name_plural: str = 'contacts'


class Product(models.Model):
    """
    Класс Product наследуется от базового класса Model из модуля django.db.models.
    Определяет поля таблицы базы данных, их свойства и ограничения.
    """
    name = models.CharField(max_length=150)
    model = models.CharField(max_length=100)
    release_date = models.DateField()
    owner = models.ForeignKey(Node, on_delete=models.CASCADE)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self) -> str:
        """
        Функция __str__ переопределяет метод родительского класса Model и создает
        выходной формат для экземпляров этого класса.
        """
        return self.name

    class Meta:
        """
        Метакласс содержит общее имя экземпляра модели в единственном и множественном числе, используемое
        в панели администрирования.
        """
        verbose_name: str = 'product'
        verbose_name_plural: str = 'products'
        ordering: List[str] = ['name', 'model']
