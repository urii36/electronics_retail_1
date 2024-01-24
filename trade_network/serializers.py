from typing import Tuple, List, Dict
from django.db import models
from rest_framework import serializers

from trade_network.models import Node, Contact


class ContactSerializer(serializers.ModelSerializer):
    """
    Класс ContactSerializer наследуется от класса ModelSerializer из rest_framework.serializers.
    Это класс для удобной сериализации и десериализации объектов класса Contact при
    обработке создания нового экземпляра класса Contact.
    """

    class Meta:
        """
        Метакласс - это внутренний служебный класс сериализатора,
        определяет необходимые параметры для функционирования сериализатора.
        """
        model: models.Model = Contact
        fields: List[str] = ["email", "country", "city", "street", "house_number"]


class NodeCreateSerializer(serializers.ModelSerializer):
    """
    Класс NodeCreateSerializer наследуется от класса ModelSerializer из rest_framework.serializers.
    Это класс для удобной сериализации и десериализации объектов класса Node при
    обработке создания нового экземпляра класса Node.
    """
    supplier = serializers.SlugRelatedField(required=False, queryset=Node.objects.all(), slug_field="name")
    contact = ContactSerializer(required=False)

    class Meta:
        """
        Метакласс - это внутренний служебный класс сериализатора,
        определяет необходимые параметры для функционирования сериализатора.
        """
        model: models.Model = Node
        read_only_fields: Tuple[str, ...] = ("id", "debt_to_the_supplier", "date_of_creation")
        fields: str = "__all__"

    def is_valid(self, *, raise_exception=False):
        """
        Функция is_valid переопределяет метод базового класса. Она принимает в качестве аргументов экземпляр своего собственного класса
        и любые другие позиционные аргументы. Удаляет ключ "contact" со значением из полученных данных
        и сохраняет его как защищенный атрибут. Производит добавление ключа "level" со значением, полученным
        из функции.Затем он вызывает метод базового класса.
        """
        self._contact: Dict[str, str] = self.initial_data.pop("contact", {})
        self.initial_data["level"] = level_detection(self.initial_data)
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data: dict) -> Node:
        """
        Функция create переопределяет метод базового класса. Она принимает в качестве аргументов экземпляр своего собственного класса
        и полученные проверенные данные для создания нового экземпляра класса. Создает и сохраняет новый экземпляр
        класса Node. Создает и сохраняет экземпляр связанного класса Contact.
        Возвращает созданный экземпляр класса Node.
        """
        node: Node = Node.objects.create(**validated_data)
        node.save()

        contact: Contact = Contact.objects.create(
            memder=node,
            email=self._contact.get("email", None),
            country=self._contact.get("country", None),
            city=self._contact.get("city", None),
            street=self._contact.get("street", None),
            house_number=self._contact.get("house_number", None)
        )
        contact.save()

        return node


class NodeListSerializer(serializers.ModelSerializer):
    """
    Класс сериализатора NodeList наследуется от класса ModelSerializer из rest_framework.serializers.
    Это класс для удобной сериализации и десериализации объектов класса Node при
    обработке экземпляра использования класса Node.
    """
    supplier = serializers.SlugRelatedField(queryset=Node.objects.all(), slug_field="name")
    contact = ContactSerializer()

    class Meta:
        """
        Метакласс - это внутренний служебный класс сериализатора,
        определяет необходимые параметры для функционирования сериализатора.
        """
        model: models.Model = Node
        fields: List[str] = ["id", "name", "level", "supplier", "debt_to_the_supplier", "contact"]


class NodeSerializer(serializers.ModelSerializer):
    """
    Класс NodeSerializer наследуется от класса ModelSerializer из rest_framework.serializers.
    Это класс для удобной сериализации и десериализации объектов класса Node при
    обработке экземпляра использования класса Node.
    """
    supplier = serializers.SlugRelatedField(required=False, queryset=Node.objects.all(), slug_field="name")
    contact = ContactSerializer(required=False)

    class Meta:
        """
        Метакласс - это внутренний служебный класс сериализатора,
        определяет необходимые параметры для функционирования сериализатора.
        """
        model: models.Model = Node
        fields: str = "__all__"
        read_only_fields: Tuple[str, ...] = ("id", "debt_to_the_supplier", "date_of_creation", "level")

    def is_valid(self, *, raise_exception=False):
        """
        Функция is_valid переопределяет метод базового класса. Она принимает в качестве аргументов экземпляр своего собственного класса
        и любые другие позиционные аргументы. Удаляет ключ "contact" со значением из полученных данных
        и сохраняет его как защищенный атрибут. Производит добавление ключа "level" со значением, полученным
        из функции.Затем он вызывает метод базового класса.
        """
        self._contact = self.initial_data.pop("contact", {})
        if "supplier" in self.initial_data:
            self.initial_data["level"] = level_detection(self.initial_data)
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        """
        Функция сохранения переопределяет метод базового класса. Она принимает экземпляр своего собственного класса в качестве аргумента.
        Вызывает метод базового класса. Затем она проверяет наличие данных для изменения связанного экземпляра класса Contact.
        Обновляет и сохраняет экземпляр связанного класса Contact. Возвращает обновленный экземпляр класса Node.
        """
        super().save()

        if self._contact != {}:
            self.instance.contact = self.update(self.instance.contact, self._contact)

        return self.instance


def level_detection(kwargs: dict) -> int:
    """
    The level_detection function is a utility function. It takes as an argument data to create or update
    an instance of the Node class. Specifies the hierarchical level of the location of an instance of the Node class.
    Returns the level as an integer.
    """
    level: int = 0
    if kwargs["supplier"] is None:
        return level

    supplier: Node = Node.objects.get(name=kwargs["supplier"])

    for i in range(2):
        level += 1
        if supplier.supplier is None:
            return level
        supplier = supplier.supplier

    raise Exception("Incorrect links in the hierarchical system")
