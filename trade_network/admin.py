from typing import Tuple, List, Union
from django.contrib import admin
from django.db import models
from django.db.models import QuerySet
from django.utils.html import format_html

from trade_network.models import Node, Contact, Product


class ContactInline(admin.TabularInline):
    """
    Класс ContactInLine наследуется от базового класса TabularInLine из модуля django.contrib.admin.
    Предназначен для отображения и редактирования объектов связанных моделей на той же странице сайта Django.admin
    что и объект базовой модели.
    """
    model: models.Model = Contact


class ProductInline(admin.TabularInline):
    """
    Класс ProductInLine наследуется от базового класса TabularInLine из модуля django.contrib.admin.
    Предназначен для отображения и редактирования объектов связанных моделей на той же странице сайта Django.admin
    что и объект базовой модели.
    """
    model: models.Model = Product
    extra = 0


class NodeAdmin(admin.ModelAdmin):
    """
    Класс NodeAdmin наследуется от класса ModelAdmin. Определяет вывод полей экземпляра
    на панель администрирования и возможность их редактирования.
    """
    inlines: List[admin.TabularInline] = [ContactInline, ProductInline, ]
    list_display: Tuple[str, ...] = ("id", "name", "level", "to_supplier", "debt_to_the_supplier")
    list_display_links: Tuple[str, ...] = ('name', 'to_supplier')
    list_filter: Tuple[str, ...] = ('contact__city',)
    fields: List[Union[Tuple[str, ...], str]] = [("id", "name"),
                                                 ("level", "supplier"),
                                                 "debt_to_the_supplier",
                                                 "date_of_creation"]
    readonly_fields: Tuple[str, ...] = ("id", "date_of_creation",)
    search_fields: Tuple[str, ...] = ("name",)
    save_on_top: bool = True
    actions: List[str] = ['clear_dept']

    def to_supplier(self, obj: Node):
        """
        Функция to_supplier определяет метод класса NodeAdmin. Она принимает в качестве аргументов экземпляр
        своего собственного класса и экземпляр класса Node. Переопределяет создание ссылки в списке
        экземпляров на панели администратора на поставщика. Возвращает ссылку в формате html.
        """
        if obj.supplier is not None:
            return format_html(
                '<a href="/admin/trade_network/node/{id}">{name}</a>',
                id=obj.supplier.id,
                name=obj.supplier
            )

    @admin.action(description='clear debt_to_the_supplier')
    def clear_dept(self, request, queryset: QuerySet) -> None:
        """
        Функция clear_depth(self, request, queryset: QuerySet определяет метод класса NodeAdmin.
        Она принимает экземпляр своего собственного класса, объект request и объект queryset в качестве аргументов.
        Определяет действия, когда соответствующие действия выбраны в панели администратора.
        """
        queryset.update(debt_to_the_supplier=0)


class ProductAdmin(admin.ModelAdmin):
    """
    Класс ProductAdmin наследуется от класса ModelAdmin. Определяет вывод полей экземпляра
    на панель администрирования и возможность их редактирования.
    """
    list_display: Tuple[str, ...] = ("name", "model", "release_date", "owner")
    list_display_links = ('name', 'owner')
    search_fields: Tuple[str, ...] = ("name", "model", "release_date")
    save_on_top = True


admin.site.register(Node, NodeAdmin)
admin.site.register(Product, ProductAdmin)
