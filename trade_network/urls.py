from django.urls import path

from trade_network import views

urlpatterns = [
    path("node", views.NodeCreateView.as_view()),
    path("node/list", views.NodeListView.as_view()),
    path("node/<pk>", views.NodeView.as_view()),
]
