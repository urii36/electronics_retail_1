from typing import List

from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, serializers
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView

from trade_network.models import Node
from trade_network.serializers import NodeCreateSerializer, NodeListSerializer, NodeSerializer


class NodeCreateView(CreateAPIView):
    """
    Класс NodeCreateView наследуется от класса CreateAPIView из модуля rest_framework.generics
    и представляет собой представление на основе класса для обработки запросов методами POST по адресу '/trade_network/node'.
    """
    model: models.Model = Node
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: serializers.ModelSerializer = NodeCreateSerializer


class NodeListView(ListAPIView):
    """
    Класс NodeListView наследуется от класса ListAPIView из модуля rest_framework.generics
    и представляет собой представление на основе класса для обработки запросов с помощью методов GET по адресу '/trade_network/node/list'.
    """
    model: models.Model = Node
    queryset: List[Node] = Node.objects.all()
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: serializers.ModelSerializer = NodeListSerializer
    filter_backends: list = [DjangoFilterBackend, ]
    filterset_fields: List[str] = ["contact__country", ]


class NodeView(RetrieveUpdateDestroyAPIView):
    """
    Класс NodeView наследуется от класса RetrieveUpdateDestroyAPIView из модуля rest_framework.generics
    и представляет собой представление на основе класса для обработки запросов с помощью методов GET, PUT, PATCH и DELETE по адресу
    /trade_network/node/<pk>'.
    """
    model: models.Model = Node
    queryset: List[Node] = Node.objects.all()
    serializer_class: serializers.ModelSerializer = NodeSerializer
    permission_classes: list = [permissions.IsAuthenticated, ]
